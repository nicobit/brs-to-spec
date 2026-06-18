"""Queue mechanics — real file moves between pending/processing/done/failed."""

from __future__ import annotations

import shutil
from pathlib import Path

from .workspace import pending_dir, processing_dir, done_dir, failed_dir, WorkspaceError

VALID_BUCKETS = ("pending", "processing", "done", "failed")

_BUCKET_DIR = {
    "pending": pending_dir,
    "processing": processing_dir,
    "done": done_dir,
    "failed": failed_dir,
}


class QueueError(Exception):
    pass


def move_event(
    workspace: Path,
    event_id: str,
    from_bucket: str,
    to_bucket: str,
    move_result: bool = True,
) -> dict:
    """
    Move an event file (and optionally its result file) between queue buckets.
    Uses real move semantics — the file exists in exactly one bucket afterwards.

    Returns a dict describing what was moved.
    Raises QueueError on any violation.
    """
    _validate_buckets(from_bucket, to_bucket)

    src_dir = _BUCKET_DIR[from_bucket](workspace)
    dst_dir = _BUCKET_DIR[to_bucket](workspace)
    dst_dir.mkdir(parents=True, exist_ok=True)

    event_file = _find_event_file(src_dir, event_id)
    result_file = _find_result_file(src_dir, event_id)

    # reject if event already exists in destination
    if any(dst_dir.glob(f"{event_id}-*.yaml")):
        existing = next(dst_dir.glob(f"{event_id}-*.yaml"))
        raise QueueError(
            f"Event {event_id} already exists in {to_bucket}/: {existing.name}. "
            f"Cannot move from {from_bucket}/."
        )

    moved: list[str] = []

    # move event file
    dst_event = dst_dir / event_file.name
    shutil.move(str(event_file), str(dst_event))
    moved.append(f"{from_bucket}/{event_file.name} → {to_bucket}/{event_file.name}")

    # move result file if present and requested
    if move_result and result_file:
        dst_result = dst_dir / result_file.name
        shutil.move(str(result_file), str(dst_result))
        moved.append(f"{from_bucket}/{result_file.name} → {to_bucket}/{result_file.name}")

    return {
        "event_id": event_id,
        "from": from_bucket,
        "to": to_bucket,
        "moved": moved,
    }


def find_event_in_any_bucket(workspace: Path, event_id: str) -> dict[str, Path]:
    """
    Returns a dict of bucket_name → Path for every bucket where this event_id appears.
    Used to detect duplicate presence.
    """
    found: dict[str, Path] = {}
    for bucket, dir_fn in _BUCKET_DIR.items():
        d = dir_fn(workspace)
        if not d.is_dir():
            continue
        matches = list(d.glob(f"{event_id}-*.yaml"))
        # exclude result files
        event_matches = [m for m in matches if "-result" not in m.stem]
        if event_matches:
            found[bucket] = event_matches[0]
    return found


def _find_event_file(bucket_dir: Path, event_id: str) -> Path:
    if not bucket_dir.is_dir():
        raise QueueError(f"Bucket directory does not exist: {bucket_dir}")
    matches = [
        f for f in bucket_dir.glob(f"{event_id}-*.yaml")
        if "-result" not in f.stem
    ]
    if not matches:
        raise QueueError(f"Event file for {event_id} not found in {bucket_dir}")
    return matches[0]


def _find_result_file(bucket_dir: Path, event_id: str) -> Path | None:
    matches = list(bucket_dir.glob(f"{event_id}-result.yaml"))
    return matches[0] if matches else None


def _validate_buckets(from_bucket: str, to_bucket: str) -> None:
    for b in (from_bucket, to_bucket):
        if b not in VALID_BUCKETS:
            raise QueueError(f"Invalid bucket '{b}'. Must be one of: {VALID_BUCKETS}")
    if from_bucket == to_bucket:
        raise QueueError(f"Source and destination bucket are the same: '{from_bucket}'")

    # reject nonsensical transitions
    invalid = {("done", "pending"), ("done", "processing"), ("failed", "processing")}
    if (from_bucket, to_bucket) in invalid:
        raise QueueError(
            f"Transition {from_bucket} → {to_bucket} is not permitted."
        )


def list_bucket(workspace: Path, bucket: str) -> list[Path]:
    """Return all event files (not result files) in the given bucket."""
    _validate_buckets(bucket, "pending")  # just validates bucket name; reuse
    d = _BUCKET_DIR[bucket](workspace)
    if not d.is_dir():
        return []
    return sorted(
        f for f in d.glob("*.yaml") if "-result" not in f.stem
    )
