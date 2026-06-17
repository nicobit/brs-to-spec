# Implementation Prompt — Phase 2: Skills and Artifact Templates

**Target:** `.brs2spec2/skills/` (~35 files) and `.brs2spec2/artifact-templates/` (~20 files)  
**Prerequisites:** Persona files complete; engine complete  
**Produces:** One skill file per v1 skill prompt; one artifact template per major output artifact

---

## Context

You are porting skill prompts and artifact templates from v1 to v2. The content of these files does not fundamentally change — the domain logic is preserved. What changes is the structure and the fact that skill files are now referenced by `skill_ref` in event files, not loaded monolithically by the orchestrator.

Read before writing:
- `.flow-engine/instructions/event-execution-rules.md` — understand how skill files are loaded and used
- `.brs2spec2/personas/<persona>.md` for the persona you are porting skills for
- The corresponding v1 skill prompt from `.brs2spec/skills/<path>.md`
- The corresponding v1 template from `.brs2spec/templates/<path>.md`

**Port in this order — do not jump ahead:**
1. Slice 1 skills only (orchestrator route skill + product-owner business intake skill)
2. Validate Slice 1 end-to-end on a real initiative
3. Then port remaining skills per the slice plan

---

## Skill file structure

Every skill file in `.brs2spec2/skills/<persona>/<skill-name>.md` must follow this structure:

```markdown
# Skill — <Title>

## Identity

skill_id: <persona>.<skill_name>
persona: <persona-id>
event_types: [list of event types this skill handles — usually just one]
produces: <artifact path(s)>

## When this skill is used

One sentence. What condition triggers this skill to be referenced in an event.

## Role for this task

How the persona should frame themselves specifically for this task. More specific than the 
persona's general role definition. 1–3 sentences.

## Prerequisites check

Before doing any work, verify:
- [list of things to check in required_inputs before starting]
- If any check fails: stop, do not write partial output, note in result file

## Instructions

The full task instructions. This is the core content ported from v1 skill prompts.
Keep all domain logic, formatting rules, ID conventions, and quality requirements.
Remove references to v1 workflow state management (the engine handles that now).

## Output requirements

Explicit requirements for the write_to artifact(s):
- Structure requirements (sections that must exist)
- ID format requirements (BR-NNN, FR-NNN, etc.)
- Completeness requirements (no empty rows, no placeholder text)
- Cross-reference requirements (every X must link to Y)

## Done criteria

Testable assertions that must all be true for this skill's output to pass validation.
These are the natural_language validation rules the dispatcher will evaluate.
Write them as a checklist — each item is a yes/no check on the artifact.

## Stop conditions

Conditions under which this skill must stop and write a fail result rather than producing output:
- [condition] → failure_reason text to use in result file
```

---

## Skills to port — Slice 1 (do these first)

### `.brs2spec2/skills/orchestrator/route-initiative.md`
- Port from: `.brs2spec/skills/1-routing/01-select-delivery-and-execution-mode.md`
- event_type: ROUTE_INITIATIVE
- produces: `state/routing-decision.md`
- Key content to preserve: delivery mode selection rules (OpenSpec / Standalone / FastPath / BusinessCopilot), scoring criteria, hard constraints
- Remove: v1 workflow-state.json update instructions (engine handles this)

### `.brs2spec2/skills/product-owner/create-business-intake-summary.md`
- Port from: `.brs2spec/skills/2-business-intake/01-create-business-intake-summary.md`
- event_type: CREATE_ARTIFACT
- produces: `business-intake/business-intake-summary.md`
- artifact_template_ref: `.brs2spec2/artifact-templates/business-intake-summary.md`
- Key content to preserve: all domain logic, template reference, consolidation rules, source-document inventory instructions

---

## Skills to port — Slice 2 and beyond

Port these after Slice 1 validates end-to-end. Group by persona for efficiency.

### product-owner skills
- `create-business-rules.md` ← `.brs2spec/skills/2-business-intake/02-extract-business-rules.md`
- `create-actors-and-personas.md` ← `.brs2spec/skills/2-business-intake/03-extract-actors-and-personas.md`
- `create-process-flows.md` ← `.brs2spec/skills/2-business-intake/04-create-process-flows.md`
- `create-use-case-specs.md` ← `.brs2spec/skills/2-business-intake/05-create-use-case-specs.md`
- `create-brs.md` ← `.brs2spec/skills/0-intake/00-create-brs.md`
- `convert-brs-to-markdown.md` ← `.brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md`
- `find-gaps-and-questions.md` ← `.brs2spec/skills/2-business-intake/advanced/03-find-gaps-and-questions.md`
- `create-business-test-expectations.md` ← `.brs2spec/skills/2-business-intake/advanced/04-create-business-test-expectations.md`

### architect skills
- `draft-architecture-from-brs.md` ← `.brs2spec/skills/0-input-preparation/04-draft-architecture-from-brs.md`
- `convert-architecture-to-markdown.md` ← `.brs2spec/skills/0-input-preparation/02-convert-architecture-word-to-markdown.md`
- `create-entity-model.md` ← `.brs2spec/skills/2-business-intake/06-create-entity-model.md`
- `review-initial-architecture.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md`
- `create-architecture-rules.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/02-create-global-architecture-rules.md`
- `review-existing-system-impact.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/08-review-existing-system-impact.md`

### delivery-lead skills
- `create-delivery-structure.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/03-create-delivery-structure.md`
- `identify-software-modules.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/04-identify-software-modules.md`
- `map-capabilities-to-modules.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md`
- `define-delivery-increments.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/06-define-delivery-increments.md`
- `create-traceability-matrix.md` ← `.brs2spec/skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md`
- `create-review-package.md` ← `.brs2spec/skills/6-review-package/01-create-review-package.md`
- `create-agile-planning-view.md` ← `.brs2spec/skills/7-perspectives/agile-planning/01-create-gitlab-planning-view.md`

### qa-analyst skills
- `create-bdd-scenarios.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md`
- `create-test-plan-per-story.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md`
- `create-test-strategy.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-test-strategy.md`
- `generate-test-stubs-from-bdd.md` ← `.brs2spec/skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md`
- `qa-review.md` ← `.brs2spec/skills/9-reviewers/02-qa-review.md`

### security-reviewer skills
- `create-security-review.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-security-review.md`
- `create-threat-model.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-threat-model.md`
- `create-data-contract.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-data-contract.md`
- `security-review-of-implementation.md` ← `.brs2spec/skills/9-reviewers/04-security-review.md`

### engineering-lead skills
- `check-engineering-readiness.md` ← `.brs2spec/skills/4-engineering-readiness/01-check-engineering-readiness.md`
- `generate-initiative-context.md` ← `.brs2spec/skills/4-engineering-readiness/02-generate-initiative-context.md`
- `create-api-contract.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-api-contract.md`
- `create-event-contract.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-event-contract.md`
- `create-observability-plan.md` ← `.brs2spec/skills/4-engineering-readiness/quality-gates/create-observability-plan.md`
- `create-openspec-handoff.md` ← `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`
- `create-standalone-handoff.md` ← `.brs2spec/skills/5-handoff/02-create-standalone-delivery-package.md`
- `create-compact-handoff.md` ← `.brs2spec/skills/5-handoff/03-create-compact-handoff-package.md`
- `implement-one-task.md` ← `.brs2spec/skills/8-copilot-implementation/01-implement-one-task.md`
- `fix-review-comments.md` ← `.brs2spec/skills/8-copilot-implementation/02-fix-review-comments.md`

### reviewer skills
- `senior-code-review.md` ← `.brs2spec/skills/9-reviewers/01-senior-code-review.md`
- `architecture-review.md` ← `.brs2spec/skills/9-reviewers/03-architecture-review.md`
- `spec-correction.md` ← `.brs2spec/skills/9-reviewers/05-spec-correction.md`

---

## Artifact template porting

Artifact templates define the expected output shape. They are referenced by `artifact_template_ref` in event files. The persona uses them as the structural contract for what to produce.

Port from `.brs2spec/templates/`. Keep all headings and structural guidance. Remove any "how to fill in" instruction text that belongs in the skill file.

### Templates to create in `.brs2spec2/artifact-templates/`

| Template file | Port from |
|---|---|
| `routing-decision.md` | New — create from scratch (v1 had no explicit template for this) |
| `business-intake-summary.md` | `.brs2spec/templates/business-intake/business-intake-summary.md` |
| `business-rules.md` | `.brs2spec/templates/business-intake/business-rules.md` |
| `actors-and-personas.md` | `.brs2spec/templates/review-package/01-business-analysis/actors-and-personas.md` |
| `process-flows.md` | `.brs2spec/templates/review-package/01-business-analysis/process-flows.md` |
| `use-case-spec.md` | `.brs2spec/templates/review-package/03-delivery-structure/use-case-spec.md` |
| `entity-model.md` | `.brs2spec/templates/review-package/02-solution-analysis/entity-model.md` |
| `architecture-review.md` | `.brs2spec/templates/planning-and-modular-delivery/architecture-review.md` |
| `architecture-rules.md` | `.brs2spec/templates/planning-and-modular-delivery/architecture-rules.md` |
| `delivery-structure.md` | `.brs2spec/templates/planning-and-modular-delivery/delivery-structure.md` (+ epic/feature/overview variants) |
| `traceability-matrix.md` | `.brs2spec/templates/planning-and-modular-delivery/traceability-matrix.md` |
| `readiness-check.md` | `.brs2spec/templates/engineering-readiness/readiness-check.md` |
| `initiative-context.md` | `.brs2spec/templates/engineering-readiness/initiative-context.md` |
| `bdd-scenarios.md` | `.brs2spec/templates/quality-gates/bdd-scenarios.md` + `bdd-feature.md` + `bdd-acceptance-checklist.md` |
| `test-strategy.md` | `.brs2spec/templates/quality-gates/test-strategy.md` |
| `security-review.md` | `.brs2spec/templates/quality-gates/security-review.md` |
| `threat-model.md` | `.brs2spec/templates/quality-gates/threat-model.md` |
| `data-contract.md` | `.brs2spec/templates/quality-gates/data-contract.md` |
| `api-contract.md` | `.brs2spec/templates/quality-gates/api-contract.md` |
| `open-decisions.md` | `.brs2spec/templates/state/open-decisions.md` |

### `routing-decision.md` — create from scratch

Since v1 had no explicit template for routing-decision.md, create one with:
- Metadata section: initiative_id, created_at, created_by
- Delivery mode: OpenSpec | Standalone | FastPath | BusinessCopilot (with rationale)
- Execution mode: Enterprise | Enterprise+Modular | Standard (with rationale)
- Evidence: the criteria scored for each decision
- Constraints: any routing constraints that apply (e.g. "team does not use OpenSpec tooling")

---

## Quality bar

- Every Slice 1 skill file must be complete enough to run a real event end-to-end without needing to consult v1 files
- Skill files must not contain workflow state management instructions — the engine handles that
- Artifact templates must contain structural headings and placeholder guidance only — not "how to write content" instructions (those belong in skill files)
- Done criteria in each skill file must exactly match the natural_language validation_rules in the corresponding event template (written in Phase 3)
