#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]

def copy_tree(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copy_tree(item, target)
        else:
            text = item.read_text(encoding="utf-8")
            text = text.replace("<feature name>", dst.parents[0].name if dst.name != "openspec-change" else dst.parent.name)
            target.write_text(text, encoding="utf-8")

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/scripts/new_feature.py <feature-name>")
        sys.exit(1)

    feature = sys.argv[1].strip()
    if not feature:
        print("Feature name is required")
        sys.exit(1)

    feature_dir = ROOT / "features" / feature
    if feature_dir.exists():
        print(f"Feature already exists: {feature_dir}")
        sys.exit(1)

    (feature_dir / "input").mkdir(parents=True)
    brs_template = ROOT / "templates" / "input" / "brs-original.md"
    if brs_template.exists():
        (feature_dir / "input" / "brs-original.md").write_text(brs_template.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        (feature_dir / "input" / "brs-original.md").write_text("# Original BRS\n\nPaste converted Word BRS here.\n", encoding="utf-8")
    (feature_dir / "input" / "architecture-draft.md").write_text("# Architecture Draft\n\nPaste draft architecture here.\n", encoding="utf-8")

    copy_tree(ROOT / "templates" / "business-intake", feature_dir / "business-intake")
    copy_tree(ROOT / "templates" / "engineering-contracts", feature_dir / "engineering-contracts")
    copy_tree(ROOT / "templates" / "openspec-change", feature_dir / "openspec-change")
    copy_tree(ROOT / "templates" / "quality-gates", feature_dir / "quality-gates")
    copy_tree(ROOT / "templates" / "reviews", feature_dir / "reviews")

    print(f"Created feature package: {feature_dir}")

if __name__ == "__main__":
    main()
