#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FEATURE_FILES = [
    "input/brs-original.md",
    "business-intake/requirements.md",
    "business-intake/epics-and-features.md",
    "business-intake/user-stories.md",
    "business-intake/gaps-and-questions.md",
    "engineering-contracts/technical-spec.md",
    "openspec-change/proposal.md",
    "openspec-change/design.md",
    "openspec-change/tasks.md",
]

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/scripts/validate_feature.py <feature-name>")
        sys.exit(1)

    feature = sys.argv[1]
    feature_dir = ROOT / "features" / feature
    errors = []

    if not feature_dir.exists():
        print(f"Feature not found: {feature}")
        sys.exit(1)

    for rel in REQUIRED_FEATURE_FILES:
        p = feature_dir / rel
        if not p.exists():
            errors.append(f"Missing: {rel}")
        elif len(p.read_text(encoding="utf-8").strip()) < 20:
            errors.append(f"Too short / likely empty: {rel}")

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print(f"Feature validation passed: {feature}")

if __name__ == "__main__":
    main()
