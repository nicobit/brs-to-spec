from pathlib import Path


# Script lives at .brs2spec/tools/scripts/check_program.py → parents[3] is the repo root
ROOT = Path(__file__).resolve().parents[3]

REQUIRED = [
    # Persona skill registry
    ".brs2spec/module.md",
    "README.md",
    "HOW_TO_USE.md",
    "CHANGELOG.md",
    ".github/copilot-instructions.md",
    # Workflow runner — canonical prompt
    ".brs2spec/brs-to-spec-run-workflow.md",
    # GitHub Copilot slash-command stubs (current path: .github/prompts/brs2spec/)
    ".github/prompts/brs2spec/brs-to-spec-run-workflow.prompt.md",
    ".github/prompts/brs2spec/create-engineering-readiness.prompt.md",
    ".github/prompts/brs2spec/create-openspec-handoff.prompt.md",
    ".github/prompts/brs2spec/create-standalone-handoff.prompt.md",
    ".github/prompts/brs2spec/create-gitlab-planning-view.prompt.md",
    ".vscode/settings.json",
    "docs/14-agile-planning-view.md",
    "docs/15-github-copilot-workflow.md",
    "docs/16-prompt-execution-environments.md",
    "docs/17-copilot-usage.md",
    "docs/18-entry-modes.md",
    "docs/19-brownfield-existing-system-mode.md",
    "docs/20-small-change-paths.md",
    "docs/21-artifact-quality-review.md",
    # Core prompts
    ".brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md",
    ".brs2spec/skills/0-input-preparation/03-normalize-input-package.md",
    ".brs2spec/skills/2-business-intake/01-create-business-intake-summary.md",
    ".brs2spec/skills/8-copilot-implementation/01-implement-one-task.md",
    ".brs2spec/skills/8-copilot-implementation/02-fix-review-comments.md",
    ".brs2spec/skills/9-reviewers/01-senior-code-review.md",
    ".brs2spec/skills/9-reviewers/02-qa-review.md",
    ".brs2spec/skills/9-reviewers/03-architecture-review.md",
    ".brs2spec/skills/9-reviewers/04-security-review.md",
    # Templates — current .brs2spec-relative paths
    ".brs2spec/templates/input-preparation/input-package.md",
    ".brs2spec/templates/quality-gates/ready-for-copilot-checklist.md",
    ".brs2spec/templates/perspectives/agile-planning/gitlab-planning-view.md",
    ".brs2spec/templates/planning-and-modular-delivery/existing-system-impact.md",
    # Workflow-state template — new rule
    ".brs2spec/templates/state/workflow-state.json",
    # Repository descriptor template — multi-repo handoff
    ".brs2spec/templates/repositories/_template.md",
    # OpenSpec handoff templates — story-scoped model
    ".brs2spec/templates/openspec-handoff/dependency-graph.md",
    ".brs2spec/templates/openspec-handoff/story.md",
    ".brs2spec/templates/openspec-handoff/design.md",
    ".brs2spec/templates/openspec-handoff/tasks.md",
    # Tools
    ".brs2spec/tools/scripts/new_initiative.py",
    ".brs2spec/tools/scripts/add_brs.py",
    ".brs2spec/tools/scripts/add_architecture.py",
    "examples/initiative-workspace-end-to-end/README.md",
]

PERSONA_SKILL_CHECKS = {
    # module.md must contain persona and skill sections
    ".brs2spec/module.md": [
        "persona",
        "skill",
        "orchestrator",
        "architect",
        "delivery-lead",
        "qa-analyst",
        "security-reviewer",
        "engineering-lead",
        "reviewer",
    ],
    # orchestrator prompt must reference module.md as the skill registry source
    ".brs2spec/brs-to-spec-run-workflow.md": [
        ".brs2spec/module.md",
        "Skill selection model",
        "skill_id",
    ],
}


def check_yaml(path: str) -> list[str]:
    """Return list of error strings if YAML file exists but is invalid."""
    import importlib.util

    full_path = ROOT / path
    if not full_path.exists():
        return []
    spec = importlib.util.find_spec("yaml")
    if spec is None:
        return []
    import yaml  # type: ignore

    try:
        with open(full_path, encoding="utf-8") as f:
            yaml.safe_load(f)
        return []
    except yaml.YAMLError as e:
        return [f"YAML validation failed: {path} — {e}"]


CONTENT_CHECKS = {
    # README: product positioning, example output pointer, key structural terms
    "README.md": [
        "From enterprise BRS to AI-safe engineering handoff.",
        "initiatives/I001-customer-onboarding/",
        "dependency-graph.md",
        "workflow-state.json",
        "business-intake/business-intake-summary.md",
        "planning/traceability-matrix.md",
        "initiative workspace",
        "reviewer prompts are downstream helpers",
        "single team-facing Delivery Planning View",
        "OpenSpec or standalone tasks remain the engineering implementation contract.",
        "Epic / Feature / User Story structure should be defined during delivery planning",
        "## Entry modes",
        "BRS-first",
        "existing-system enhancement",
        "## Brownfield / existing-system mode",
        "architecture/existing-system-impact.md",
        "## Small-change paths",
        "docs/20-small-change-paths.md",
        "## Artifact use model",
        "Primary consumer",
        "Do not duplicate",
        "## Planning artifact density rule",
        "delivery-structure.md = planning structure and traceability logic",
        "high-level solution architecture context",
        "## Architecture handling rule",
        "impacted components",
        "validation implications",
        "Optional visual views may be embedded inside the owning artifact",
        "prefer embedded Mermaid in markdown",
    ],
    # HOW_TO_USE: step coverage, multi-repo described as optional
    "HOW_TO_USE.md": [
        "python .brs2spec/tools/scripts/new_initiative.py onboarding-request --initiative-id I001",
        "python .brs2spec/tools/scripts/add_brs.py initiatives/I001-onboarding-request compliance",
        "python .brs2spec/tools/scripts/add_architecture.py initiatives/I001-onboarding-request security-constraints",
        "Do not implement from user stories alone.",
        "Use one approved OpenSpec or standalone task as the implementation unit.",
        "`planning/delivery-structure.md` should define the initiative's Epic / Feature / User Story structure early",
        "## Step 3 - Create early delivery shape",
        "## Step 4 - Review and refine architecture",
        "## Step 5 - Complete delivery planning",
        "## Choose an entry mode first",
        "docs/18-entry-modes.md",
        "docs/19-brownfield-existing-system-mode.md",
        "architecture/existing-system-impact.md",
        "docs/20-small-change-paths.md",
        "## Artifact use rule",
        "gitlab-planning-view.md",
        "## Planning density rule",
        "Reference instead of repeat:",
        "At this stage, architecture input is often high-level solution architecture context",
        "Readiness should consume:",
        "Do not proceed with OpenSpec handoff from vague delivery structure or weak architecture refinement.",
        "Do not proceed with standalone handoff from vague delivery structure or weak architecture refinement.",
        "input/repositories/",
        "optional",
    ],
    # Workflow runner: state machine, new rules
    ".brs2spec/brs-to-spec-run-workflow.md": [
        "state/workflow-state.json",
        "stale_artifacts",
        "next_action",
        "one well-formed story",
        "splitting justification",
        "dependency-graph.md",
        "input/repositories/",
        "Case B",
    ],
    # Docs: spot-check key terms still present
    "docs/15-github-copilot-workflow.md": [
        "every major artifact should have an obvious consumer",
        "primary consumer",
        "Readiness should consume:",
        "architecture refinement -> readiness",
    ],
    "docs/16-prompt-execution-environments.md": [
        ".brs2spec/skills/8-copilot-implementation",
        "VS Code Copilot Agent mode",
        "Work inside one initiative workspace at a time.",
    ],
    "docs/17-copilot-usage.md": [
        "Workflow-status rule",
        "current stage",
        "Implement Task 001",
    ],
    "docs/21-artifact-quality-review.md": [
        "## Quick quality review",
        "## Common failure patterns",
        "## Minimum evidence of usefulness by artifact",
        "### Business intake",
        "### Delivery structure",
        "### Readiness",
        "### Tasks",
    ],
    "docs/14-agile-planning-view.md": [
        "All of the paths above are relative to the active initiative workspace.",
        "Engineers implement from approved OpenSpec or standalone tasks",
        "The Epic / Feature / User Story structure should already exist in `planning/delivery-structure.md`.",
    ],
    "docs/18-entry-modes.md": [
        "BRS-first",
        "existing-system enhancement",
        "small change / bug fix",
        "large modular initiative",
    ],
    "docs/19-brownfield-existing-system-mode.md": [
        "architecture/existing-system-impact.md",
        "existing behavior that must remain stable",
    ],
    "docs/20-small-change-paths.md": [
        "Fast Path is acceptable when:",
        "Small changes that still need gates",
    ],
    # Core prompts
    ".brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md": [
        "input/brs.md",
        "input/brs/<short-name>.md",
    ],
    ".brs2spec/skills/0-input-preparation/03-normalize-input-package.md": [
        "input/brs.md or input/brs/*.md",
        "input/architecture.md or input/architecture/*.md",
    ],
    ".brs2spec/skills/2-business-intake/01-create-business-intake-summary.md": [
        "input/brs.md or input/brs/*.md",
        "input/architecture.md or input/architecture/*.md",
    ],
    ".brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md": [
        "architecture/existing-system-impact.md",
        "planning/delivery-structure.md",
    ],
    ".brs2spec/skills/3-planning-and-modular-delivery/02-create-global-architecture-rules.md": [
        "planning/delivery-structure.md",
    ],
    ".brs2spec/skills/4-engineering-readiness/01-check-engineering-readiness.md": [
        "architecture/existing-system-impact.md",
    ],
    ".brs2spec/skills/1-routing/01-select-delivery-and-execution-mode.md": [
        "Small-change path applicable?",
    ],
    ".brs2spec/skills/7-perspectives/agile-planning/01-create-gitlab-planning-view.md": [
        "user stories are business context, not engineering contract",
    ],
    # OpenSpec handoff: story-scoped model, dependency-graph, multi-repo
    ".brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md": [
        "one folder per user story",
        "dependency-graph.md",
        "input/repositories/",
        "Case B",
        "Case A",
    ],
    ".brs2spec/skills/5-handoff/02-create-standalone-delivery-package.md": [
        "standalone-delivery/",
    ],
    # Reviewers
    ".brs2spec/skills/9-reviewers/01-senior-code-review.md": [
        "Finding ID",
        "Required before",
    ],
    # Templates — workflow-state
    ".brs2spec/templates/state/workflow-state.json": [
        "brs2spec-workflow-state/1.0",
        "current_stage",
        "next_action",
        "stale_artifacts",
        "open_decisions",
        "quality_gates_triggered",
    ],
    # Templates — repository descriptor
    ".brs2spec/templates/repositories/_template.md": [
        "Responsibility",
    ],
    # Templates — openspec handoff dependency-graph
    ".brs2spec/templates/openspec-handoff/dependency-graph.md": [
        "dependency",
    ],
    # Existing-system impact template
    ".brs2spec/templates/planning-and-modular-delivery/existing-system-impact.md": [
        "## Compatibility and Regression Risk",
    ],
}


def check_registry_prompt_paths() -> list[str]:
    """Validate every prompt path in module-registry.yaml resolves to a real file under .brs2spec/."""
    import importlib.util

    registry_path = ROOT / ".brs2spec/module-registry.yaml"
    if not registry_path.exists():
        return ["Registry prompt path check skipped — module-registry.yaml not found"]
    spec = importlib.util.find_spec("yaml")
    if spec is None:
        return ["Registry prompt path check skipped — PyYAML not installed"]
    import yaml  # type: ignore

    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"Registry prompt path check skipped — YAML parse error: {e}"]

    errors = []
    brs2spec = ROOT / ".brs2spec"
    personas = data.get("personas", {})
    for persona_id, persona in personas.items():
        for skill_id, skill in persona.get("skills", {}).items():
            prompt = skill.get("prompt", "")
            if not prompt:
                continue
            resolved = brs2spec / prompt
            if not resolved.exists():
                errors.append(
                    f"Registry prompt path missing: {persona_id}.{skill_id} → "
                    f".brs2spec/{prompt}"
                )
    return errors


def check_persona_files_have_all_skills() -> list[str]:
    """Validate each module-personas/<persona>.md file contains all skill IDs listed in module-index.md."""
    index_path = ROOT / ".brs2spec/module-index.md"
    personas_dir = ROOT / ".brs2spec/module-personas"
    if not index_path.exists():
        return ["Persona skill coverage check skipped — module-index.md not found"]
    if not personas_dir.exists():
        return ["Persona skill coverage check skipped — module-personas/ not found"]

    import re

    index_text = index_path.read_text(encoding="utf-8")

    # Parse skill index table: | persona | skill_id | prompt | description |
    skill_by_persona: dict[str, list[str]] = {}
    for line in index_text.splitlines():
        m = re.match(r"\|\s*([\w-]+)\s*\|\s*`([\w_.]+)`\s*\|", line)
        if m:
            persona = m.group(1)
            skill_id = m.group(2)
            skill_by_persona.setdefault(persona, []).append(skill_id)

    errors = []
    for persona, skill_ids in skill_by_persona.items():
        persona_file = personas_dir / f"{persona}.md"
        if not persona_file.exists():
            errors.append(f"Persona file missing: module-personas/{persona}.md")
            continue
        text = persona_file.read_text(encoding="utf-8")
        for skill_id in skill_ids:
            if skill_id not in text:
                errors.append(
                    f"Persona file missing skill: module-personas/{persona}.md "
                    f"does not contain {skill_id!r}"
                )
    return errors


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f" - {path}")
        raise SystemExit(1)

    failures = []

    # Persona skill registry checks
    for path, terms in PERSONA_SKILL_CHECKS.items():
        full_path = ROOT / path
        if not full_path.exists():
            failures.append(f"Persona skill registry check skipped — file not found: {path}")
            continue
        text = full_path.read_text(encoding="utf-8", errors="ignore")
        for term in terms:
            if term not in text:
                failures.append(f"Persona skill registry check failed: {path} missing {term!r}")

    # YAML validation for module-registry.yaml if present
    for err in check_yaml(".brs2spec/module-registry.yaml"):
        failures.append(err)

    # Registry prompt path validation — every prompt in module-registry.yaml must exist on disk
    for err in check_registry_prompt_paths():
        failures.append(err)

    # Persona file coverage — every skill in module-index.md must appear in its persona file
    for err in check_persona_files_have_all_skills():
        failures.append(err)

    for path, terms in CONTENT_CHECKS.items():
        full_path = ROOT / path
        if not full_path.exists():
            failures.append(f"Content check skipped — file not found: {path}")
            continue
        text = full_path.read_text(encoding="utf-8", errors="ignore")
        for term in terms:
            if term not in text:
                failures.append(f"Content check failed: {path} missing {term!r}")

    if failures:
        for f in failures:
            print(f)
        raise SystemExit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
