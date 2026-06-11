"""
check_registry.py — Persona Skill Registry validator for brs-to-spec.

Validates:
  - .brs2spec/module-index.md exists and contains required keywords
  - .brs2spec/module-full.md exists
  - .brs2spec/module-registry.yaml is valid YAML (if present)
  - All prompt: paths referenced in module-registry.yaml exist on disk
  - All personas have at least one skill
  - All skills have a prompt and outputs field
  - Skill IDs in module-registry.yaml match skill IDs in module-index.md Skill Index table

Usage:
  python .brs2spec/tools/scripts/check_registry.py
"""

import re
from pathlib import Path

# Script lives at .brs2spec/tools/scripts/check_registry.py
# parents[0] = scripts/, parents[1] = tools/, parents[2] = .brs2spec/, parents[3] = repo root
ROOT = Path(__file__).resolve().parents[3]
BRS2SPEC = ROOT / ".brs2spec"

MODULE_INDEX = BRS2SPEC / "module-index.md"
MODULE_FULL = BRS2SPEC / "module-full.md"
MODULE_REGISTRY_YAML = BRS2SPEC / "module-registry.yaml"

REQUIRED_KEYWORDS_IN_MODULE_INDEX = [
    "persona",
    "skill",
    "orchestrator",
    "product-owner",
    "architect",
    "delivery-lead",
    "qa-analyst",
    "security-reviewer",
    "engineering-lead",
    "reviewer",
]

# Matches skill ID in backticks in the Skill Index table, e.g. `orchestrator.run_workflow`
_SKILL_ID_IN_MODULE_MD = re.compile(r"^\| [^\|]+ \| `([a-z_]+\.[a-z_]+)` \|", re.MULTILINE)


def check_module_md(failures: list) -> None:
    if not MODULE_INDEX.exists():
        failures.append(f"FAIL: {MODULE_INDEX} does not exist")
        return
    if not MODULE_FULL.exists():
        failures.append(f"FAIL: {MODULE_FULL} does not exist")
    text = MODULE_INDEX.read_text(encoding="utf-8", errors="ignore")
    for keyword in REQUIRED_KEYWORDS_IN_MODULE_INDEX:
        if keyword not in text:
            failures.append(f"FAIL: module-index.md missing required keyword: {keyword!r}")
    full_size = MODULE_FULL.stat().st_size if MODULE_FULL.exists() else 0
    print(f"  module-index.md found ({len(text)} chars), module-full.md ({full_size} chars)")


def check_yaml_valid(failures: list) -> dict | None:
    if not MODULE_REGISTRY_YAML.exists():
        print(f"  module-registry.yaml not found — skipping YAML checks")
        return None

    try:
        import yaml  # type: ignore
    except ImportError:
        print("  PyYAML not installed — skipping YAML validation (pip install pyyaml)")
        return None

    try:
        with open(MODULE_REGISTRY_YAML, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print(f"  module-registry.yaml is valid YAML")
        return data
    except Exception as e:
        failures.append(f"FAIL: module-registry.yaml is not valid YAML — {e}")
        return None


def check_personas_and_skills(data: dict, failures: list) -> None:
    personas = data.get("personas", {})
    if not personas:
        failures.append("FAIL: module-registry.yaml has no 'personas' key or it is empty")
        return

    for persona_id, persona_data in personas.items():
        skills = persona_data.get("skills", {})
        if not skills:
            failures.append(f"FAIL: persona '{persona_id}' has no skills")
            continue

        for skill_id, skill_data in skills.items():
            # Check prompt field
            prompt = skill_data.get("prompt", "")
            if not prompt:
                failures.append(
                    f"FAIL: persona '{persona_id}' skill '{skill_id}' has no 'prompt' field"
                )
            elif str(prompt).startswith("TBD"):
                # TBD prompts are explicitly not-yet-implemented; skip path check
                print(
                    f"  WARN: persona '{persona_id}' skill '{skill_id}' has TBD prompt — skipping path check"
                )
            else:
                # Resolve prompt path relative to .brs2spec/
                prompt_path = BRS2SPEC / prompt
                if not prompt_path.exists():
                    failures.append(
                        f"FAIL: prompt not found on disk: .brs2spec/{prompt} "
                        f"(referenced by {persona_id}.{skill_id})"
                    )

            # Check outputs field
            outputs = skill_data.get("outputs", None)
            if outputs is None:
                failures.append(
                    f"FAIL: persona '{persona_id}' skill '{skill_id}' has no 'outputs' field"
                )
            elif not isinstance(outputs, list) or len(outputs) == 0:
                failures.append(
                    f"FAIL: persona '{persona_id}' skill '{skill_id}' has empty 'outputs' list"
                )

    print(f"  Checked {len(personas)} personas and their skills")



# module.md uses abbreviated skill ID prefixes for some personas.
# Map YAML persona key → the prefix used in module.md skill IDs.
_PERSONA_PREFIX: dict[str, str] = {
    "qa-analyst": "qa",
    "security-reviewer": "security",
}


def _yaml_skill_ids(data: dict) -> set[str]:
    """Return full skill IDs from YAML in module.md prefix form (e.g. qa.create_bdd_scenarios)."""
    ids: set[str] = set()
    for persona_id, persona_data in data.get("personas", {}).items():
        prefix = _PERSONA_PREFIX.get(persona_id, persona_id.replace("-", "_"))
        for skill_id in (persona_data.get("skills") or {}):
            ids.add(f"{prefix}.{skill_id}")
    return ids


def _module_md_skill_ids() -> set[str]:
    """Return skill IDs from the Skill Index table in module-index.md."""
    if not MODULE_INDEX.exists():
        return set()
    text = MODULE_INDEX.read_text(encoding="utf-8", errors="ignore")
    return set(_SKILL_ID_IN_MODULE_MD.findall(text))


def check_skill_id_alignment(data: dict, failures: list) -> None:
    yaml_ids = _yaml_skill_ids(data)
    md_ids = _module_md_skill_ids()

    only_in_yaml = yaml_ids - md_ids
    only_in_md = md_ids - yaml_ids

    for skill_id in sorted(only_in_yaml):
        failures.append(
            f"FAIL: skill '{skill_id}' is in module-registry.yaml but missing from module-index.md Skill Index"
        )
    for skill_id in sorted(only_in_md):
        failures.append(
            f"FAIL: skill '{skill_id}' is in module-index.md Skill Index but missing from module-registry.yaml"
        )

    if not only_in_yaml and not only_in_md:
        print(f"  Skill IDs aligned — {len(yaml_ids)} skills match between both files")
    else:
        print(f"  Skill ID alignment: {len(only_in_yaml)} only in YAML, {len(only_in_md)} only in module.md")


def main() -> None:
    print("=" * 60)
    print("brs-to-spec Persona Skill Registry Validator")
    print("=" * 60)

    failures: list[str] = []

    print("\n[1] Checking module.md ...")
    check_module_md(failures)

    print("\n[2] Checking module-registry.yaml ...")
    data = check_yaml_valid(failures)

    if data is not None:
        print("\n[3] Checking personas and skills ...")
        check_personas_and_skills(data, failures)

        print("\n[4] Checking skill ID alignment between module-index.md and module-registry.yaml ...")
        check_skill_id_alignment(data, failures)
    else:
        print("\n[3] Skipping persona/skill checks (YAML not loaded)")
        print("\n[4] Skipping skill ID alignment check (YAML not loaded)")

    print("\n" + "=" * 60)
    if failures:
        print(f"FAILED — {len(failures)} issue(s) found:\n")
        for f in failures:
            print(f"  {f}")
        print()
        raise SystemExit(1)
    else:
        print("PASSED — registry is valid.")
    print("=" * 60)


if __name__ == "__main__":
    main()
