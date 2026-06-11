from pathlib import Path
import argparse
import re
import shutil


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "source"


def ensure_multi_brs_mode(initiative_root: Path) -> Path:
    input_dir = initiative_root / "input"
    brs_dir = input_dir / "brs"
    single_file = input_dir / "brs.md"

    brs_dir.mkdir(parents=True, exist_ok=True)
    if single_file.exists():
        migrated = brs_dir / "main.md"
        if not migrated.exists():
            shutil.move(str(single_file), str(migrated))
    return brs_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add another normalized BRS file to an existing initiative workspace."
    )
    parser.add_argument(
        "initiative_path",
        help="Path to the initiative workspace, for example initiatives/I001-customer-onboarding.",
    )
    parser.add_argument("name", help="Short source name for the additional BRS.")
    args = parser.parse_args()

    initiative_root = Path(args.initiative_path)
    brs_dir = ensure_multi_brs_mode(initiative_root)
    target = brs_dir / f"{slugify(args.name)}.md"
    if target.exists():
        raise SystemExit(f"BRS file already exists: {target}")

    target.write_text(
        """
        # BRS

        ## Source Metadata

        | Field | Value |
        |---|---|
        | Source name |  |
        | Source version/date |  |
        | Extracted by |  |
        | Extraction date |  |

        ## Executive Summary
        """.strip()
        + "\n",
        encoding="utf-8",
    )

    print(f"Created BRS source file: {target}")


if __name__ == "__main__":
    main()
