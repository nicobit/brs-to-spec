"""Workspace resolution — locates and validates the initiative workspace root."""

from pathlib import Path


class WorkspaceError(Exception):
    pass


def resolve_workspace(workspace_arg: str | None = None, repo_root: Path | None = None) -> Path:
    """
    Resolve the active initiative workspace root.

    Priority:
    1. Explicit --workspace argument (absolute or relative to cwd)
    2. Auto-detect: scan initiatives/ under repo_root for the most recently
       modified workspace that contains .flow/events/pending/

    Returns the absolute Path to the initiative workspace root.
    Raises WorkspaceError if no valid workspace can be found.
    """
    if workspace_arg:
        path = Path(workspace_arg).resolve()
        _assert_valid_workspace(path)
        return path

    root = repo_root or _find_repo_root()
    initiatives_dir = root / "initiatives"
    if not initiatives_dir.is_dir():
        raise WorkspaceError(f"initiatives/ directory not found under {root}")

    candidates = [
        d for d in initiatives_dir.iterdir()
        if d.is_dir() and (d / ".flow" / "events" / "pending").is_dir()
    ]
    if not candidates:
        raise WorkspaceError(
            "No v2 initiative workspace found. "
            "A valid workspace must contain .flow/events/pending/"
        )

    # most recently modified first
    candidates.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return candidates[0]


def _assert_valid_workspace(path: Path) -> None:
    if not path.is_dir():
        raise WorkspaceError(f"Workspace path does not exist: {path}")
    if not (path / ".flow" / "events" / "pending").is_dir():
        raise WorkspaceError(
            f"Path is not a valid v2 initiative workspace "
            f"(missing .flow/events/pending/): {path}"
        )


def _find_repo_root() -> Path:
    """Walk up from cwd looking for the repo root (contains initiatives/ and .flow-engine/)."""
    current = Path.cwd()
    for candidate in [current, *current.parents]:
        if (candidate / "initiatives").is_dir() and (candidate / ".flow-engine").is_dir():
            return candidate
    raise WorkspaceError(
        "Could not locate repo root. "
        "Run from inside the brs-to-spec repository, or pass --workspace explicitly."
    )


def resolve_path(workspace: Path, relative: str) -> Path:
    """
    Resolve a path from an event's read_from or write_to relative to the workspace root.
    Rejects paths that escape the workspace boundary.
    """
    resolved = (workspace / relative).resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError:
        raise WorkspaceError(
            f"Path '{relative}' resolves outside the workspace boundary: {resolved}"
        )
    return resolved


def flow_dir(workspace: Path) -> Path:
    return workspace / ".flow"


def pending_dir(workspace: Path) -> Path:
    return workspace / ".flow" / "events" / "pending"


def processing_dir(workspace: Path) -> Path:
    return workspace / ".flow" / "events" / "processing"


def done_dir(workspace: Path) -> Path:
    return workspace / ".flow" / "events" / "done"


def failed_dir(workspace: Path) -> Path:
    return workspace / ".flow" / "events" / "failed"


def state_dir(workspace: Path) -> Path:
    return workspace / ".flow" / "state"


def workflow_state_path(workspace: Path) -> Path:
    return state_dir(workspace) / "workflow-state.json"


def event_log_path(workspace: Path) -> Path:
    return state_dir(workspace) / "event-log.jsonl"


def integrity_check_path(workspace: Path) -> Path:
    return state_dir(workspace) / "integrity-check.yaml"
