from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_BLOCK = """```text
00a-extract-brs-from-word.md
00b-extract-architecture-from-word.md
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
07-create-business-test-expectations.md
```"""

CORE_BLOCK = """```text
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
```"""

CENTRAL_DOCS = [
    ROOT / "README.md",
    ROOT / "HOW_TO_USE.md",
    ROOT / "docs" / "business-intake-prompt-sequence.md",
    ROOT / "docs" / "workflow.md",
    ROOT / "docs" / "architecture-alignment-usage.md",
]

OLD_NAME = "03-review-brs-against-architecture.md"

def main() -> int:
    failed = False

    for path in CENTRAL_DOCS:
        if not path.exists():
            print(f"Missing central doc: {path.relative_to(ROOT)}")
            failed = True
            continue

        text = path.read_text(encoding="utf-8")

        if CANONICAL_BLOCK not in text:
            print(f"Canonical sequence block missing in {path.relative_to(ROOT)}")
            failed = True

        if CORE_BLOCK not in text:
            print(f"Core 02 -> 03 -> 04 -> 05 block missing in {path.relative_to(ROOT)}")
            failed = True

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".yml", ".yaml", ".json", ".txt"}:
            continue
        if path.name == "check_prompt_sequence.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if OLD_NAME in text:
            print(f"Outdated prompt filename found in {path.relative_to(ROOT)}")
            failed = True

    if failed:
        return 1

    print("Prompt sequence validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
