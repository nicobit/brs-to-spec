# Prompt 8 — Golden Example

## Context

You are working on the `.b2s` framework at the root of this repository.

The framework already has a realistic in-flight initiative: `initiatives/I013-NEXT13`. This is a UK regulated lending origination platform (NEXT13) with AML/KYC compliance, Experian credit scoring, Temenos T24 integration, and underwriter workflow. It is more than sufficient as a golden example domain — do not create a synthetic one.

The current `specs/` output for I013-NEXT13 was generated before the story package upgrade. The story files are shallow (2–5 lines, no BDD, no traceability, no coding prompt). The golden example must regenerate this output at full quality.

Your task is to regenerate the `specs/` folder for I013-NEXT13 by executing `rerun-last-action` for `create-openspec-handoff`, producing story packages that pass the new validator, and then package the result as a standalone golden example under `examples/`.

## Step 1 — Verify current state

Run:
```
python .b2s/scripts/b2s_cli.py next-step --workspace-root initiatives/I013-NEXT13
```

Confirm `selected_action` is `create-openspec-handoff` or that the action has status `ai_validated`.

If it is `ai_validated`, run:
```
python .b2s/scripts/b2s_cli.py rerun-last-action --workspace-root initiatives/I013-NEXT13
```

Confirm state shows `next_action: create-openspec-handoff`.

## Step 2 — Read all available inputs for I013-NEXT13

Before generating any story content, read these files in full:

**Required:**
- `initiatives/I013-NEXT13/planning/delivery-structure.md`
- `initiatives/I013-NEXT13/engineering-readiness/initiative-context.md`
- `initiatives/I013-NEXT13/architecture/architecture-rules.md`
- `initiatives/I013-NEXT13/engineering-readiness/readiness-check.md`

**Read if present:**
- `initiatives/I013-NEXT13/business-analysis/requirements.md`
- `initiatives/I013-NEXT13/business-analysis/business-rules.md`
- `initiatives/I013-NEXT13/business-analysis/actors-and-personas.md`
- `initiatives/I013-NEXT13/business-analysis/use-cases/` (all files)
- `initiatives/I013-NEXT13/architecture/architecture-review.md`
- `initiatives/I013-NEXT13/planning/traceability-matrix.md`
- `initiatives/I013-NEXT13/quality-gates/api-contract.md`
- `initiatives/I013-NEXT13/quality-gates/data-contract.md`
- `initiatives/I013-NEXT13/quality-gates/bdd-scenarios.md`

Do not generate any story content until all available files are read.

## Step 3 — Execute create-openspec-handoff for I013-NEXT13

Follow `.b2s/skills/engineering-lead/create-openspec-handoff.md` exactly.

Regenerate all story folders under `initiatives/I013-NEXT13/specs/`. Delete the existing story folders before writing new ones, but preserve `specs/dependency-graph.md` if it exists (you will replace it).

The stories to generate (from delivery-structure.md) are:
- F-001.1, F-001.2, F-001.3 (Application Intake feature)
- F-002.1, F-002.2 (AI Scoring feature)
- F-003.1, F-003.2 (Compliance Screening feature)
- F-004.1, F-004.2 (Underwriter Workflow feature)
- Any additional stories present in delivery-structure.md

For each story, produce all four files: `story.md`, `design.md`, `tasks.md`, `coding-prompt.md`.

**Quality bar for each story.md:**
- All 12 sections populated with I013-NEXT13 specific content
- Actor named from actors-and-personas.md (not "user" or "person")
- FR-NNN links from requirements.md
- BR-NNN links from business-rules.md
- At minimum: one happy path BDD scenario + one negative scenario in valid Gherkin
- Named components from architecture-review.md (e.g. "Intake API", "Experian connector", "AML screening pipeline")
- Architecture rules from architecture-rules.md explicitly listed in Section 7
- Coding-agent prompt in Section 12 that is self-contained and includes constraints and test instructions

Do not produce generic content. I013-NEXT13 is a regulated UK lending platform. Every story must reflect that domain.

## Step 4 — Validate the generated output

Run:
```
python .b2s/scripts/b2s_cli.py validate-artifact \
  --workspace-root initiatives/I013-NEXT13 \
  --action-id create-openspec-handoff
```

If validation fails, fix the failing stories and re-validate. Do not mark the action complete until validation passes.

## Step 5 — Update workflow state

Run:
```
python .b2s/scripts/b2s_cli.py update-state \
  --workspace-root initiatives/I013-NEXT13 \
  --action-id create-openspec-handoff
```

Confirm `action_status.create-openspec-handoff` is `ai_validated`.

## Step 6 — Package as golden example

Create `examples/golden-I013-NEXT13/` with the following structure:

```text
examples/golden-I013-NEXT13/
  README.md
  input/
    brs.md          (copy from initiatives/I013-NEXT13/input/brs.md)
    architecture.md (copy from initiatives/I013-NEXT13/input/architecture.md, if present)
  specs/
    (copy the full regenerated specs/ folder)
  selected-artifacts/
    business-intake-summary.md
    requirements.md
    business-rules.md
    architecture-review.md
    delivery-structure.md
    traceability-matrix.md
    readiness-check.md
    review-package.md (if present)
```

Create `examples/golden-I013-NEXT13/README.md` with:

```markdown
# Golden Example — I013 NEXT13 Lending Origination Platform

## Initiative

NEXT13 is a UK regulated digital lending origination platform. It covers application
intake, AI credit scoring (Experian), AML/KYC compliance screening (HMRC), underwriter
workflow, and loan disbursement via Temenos T24.

## Why this is a good golden example

- regulated domain with real compliance constraints (FCA, GDPR, AML)
- brownfield integration (Temenos T24, Experian, HMRC)
- multiple actors (Applicant, Underwriter, Compliance Officer, AI scoring pipeline)
- complex state machine (Draft → Submitted → Scored → Compliance Hold → Underwriter Review → Approved/Rejected → Disbursed)
- 8+ stories across 4 features and 2 epics

## Delivery mode

OpenSpec — full story packages with BDD, implementation context, and coding-agent prompts.

## Generated artifacts

| Artifact | Path |
|---|---|
| Business Intake Summary | selected-artifacts/business-intake-summary.md |
| Requirements | selected-artifacts/requirements.md |
| Business Rules | selected-artifacts/business-rules.md |
| Architecture Review | selected-artifacts/architecture-review.md |
| Delivery Structure | selected-artifacts/delivery-structure.md |
| Traceability Matrix | selected-artifacts/traceability-matrix.md |
| Readiness Check | selected-artifacts/readiness-check.md |
| Story Packages | specs/ |

## How to evaluate output quality

For each story package, check:
1. Is the actor named and non-generic?
2. Is there a clear business outcome (so that ...)?
3. Are FR-NNN and BR-NNN links present?
4. Are there at least two BDD scenarios in valid Gherkin?
5. Are the Then clauses observable and specific (not "it works")?
6. Are architecture constraints listed in Section 7?
7. Can the coding-agent prompt in Section 12 be handed to Copilot/Codex/Claude without additional context?

## Known limitations

- BDD scenarios are AI-generated and must be reviewed by a QA analyst before use
- Architecture impact in design.md must be validated by a solution architect
- Story sizing should be verified by a delivery lead before sprint planning
```

## What not to change

- Do not change any framework files (`.b2s/`) while producing the golden example output.
- Do not change the workflow-state.json other than via CLI commands.
- Do not create initiative workspace files outside `initiatives/I013-NEXT13/specs/`.

## Done criteria

- [ ] All story folders in `initiatives/I013-NEXT13/specs/` are regenerated
- [ ] Every story.md has all 12 sections with I013-NEXT13 specific content
- [ ] Every story has FR-NNN links, at least one BR-NNN link, and two BDD scenarios
- [ ] Validation passes: `validate-artifact --action-id create-openspec-handoff`
- [ ] `update-state` sets `create-openspec-handoff` to `ai_validated`
- [ ] `examples/golden-I013-NEXT13/` exists with README, input, specs, selected-artifacts
- [ ] All existing tests still pass: `python -m pytest .b2s/tests/ -q`
