# Step 6 — Refactor Support Artifacts Around the New Spine

## Purpose

Refactor the four framework-native support artifacts so they consume the new canonical analysis spine instead of deriving directly from raw BRS or intake summary.

Artifacts affected:
- `business-analysis/business-rules.md` — derive from `requirements.md`
- `business-analysis/actors-and-personas.md` — align to `use-cases.puml`
- `business-analysis/process-flows.md` — synthesize from `use-cases/UC-*.md` and actors
- `business-analysis/gaps-and-questions.md` — absorb findings from the full analysis set

## Prerequisite

Steps 1–4 must be complete. All canonical artifacts must be wired before the support artifacts are refactored to read from them.

## Run this prompt

```text
Refactor the framework-native business-analysis support artifacts so they consume the new canonical
analysis spine in .brs2spec2.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/prompts/05-create-business-rules.md
- framework_enhancement/business-analysis-improvement/prompts/06-create-actors-and-personas.md
- framework_enhancement/business-analysis-improvement/prompts/07-create-process-flows.md
- framework_enhancement/business-analysis-improvement/prompts/08-find-gaps-and-questions.md

Read the current framework files:
- .brs2spec2/workflow/event-templates/EVT-TPL-003-create-business-rules.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-004-create-actors-and-personas.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-005-find-gaps-and-questions.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-006-create-process-flows.yaml
- .brs2spec2/skills/product-owner/ (list and read any matching skill prompts)

Make the following changes:

--- Business Rules (EVT-TPL-003) ---

Update inputs:
  required:
    - business-analysis/requirements.md
  optional:
    - input/brs.md (fallback for rules not captured in requirements)
    - business-intake/business-intake-summary.md
    - architecture/architecture-review.md (optional: integration and boundary rules)

Update skill prompt to derive BR-NNN catalog primarily from requirements.md FR/NFR/constraints tables.
Base on framework_enhancement/business-analysis-improvement/prompts/05-create-business-rules.md.

Update blocked_by in workflow-definition.yaml:
  blocked_by: CREATE_REQUIREMENTS_CATALOG
  (remove any dependency on actors-and-personas or process-flows that no longer makes sense)

--- Actors and Personas (EVT-TPL-004) ---

Update inputs:
  required:
    - business-analysis/requirements.md
    - business-analysis/use-cases.puml
  optional:
    - business-analysis/business-rules.md
    - architecture/architecture-review.md (optional: external system actors)

Update skill prompt to derive ACT-NNN and SYS-NNN catalog from requirements and the use-case diagram.
Base on framework_enhancement/business-analysis-improvement/prompts/06-create-actors-and-personas.md.

Update blocked_by in workflow-definition.yaml:
  blocked_by: CREATE_USE_CASE_DIAGRAM
  (actors must align to the diagram, not run before it)

--- Gaps and Questions (EVT-TPL-005) ---

Update inputs:
  required:
    - business-intake/business-intake-summary.md
    - business-analysis/requirements.md
  optional:
    - business-analysis/entity-model.md
    - business-analysis/use-cases/UC-*.md (or use-cases/ folder)
    - business-analysis/business-rules.md
    - architecture/architecture-review.md (optional: architecture findings absorbed as gaps)

Update skill prompt to synthesize gap catalog from requirements, entity model, UCs, rules, and architecture.
Base on framework_enhancement/business-analysis-improvement/prompts/08-find-gaps-and-questions.md.

Update blocked_by in workflow-definition.yaml:
  blocked_by: CREATE_REQUIREMENTS_CATALOG
  (gaps can start as soon as requirements exist — early draft gaps are needed for architecture entry)

--- Process Flows (EVT-TPL-006) ---

Update inputs:
  required:
    - business-analysis/use-cases/UC-*.md (or use-cases/ folder)
    - business-analysis/actors-and-personas.md
  optional:
    - business-analysis/business-rules.md

Update skill prompt so process flows synthesize cross-UC journeys, not BRS-derived swimlanes.
Base on framework_enhancement/business-analysis-improvement/prompts/07-create-process-flows.md.

Update blocked_by in workflow-definition.yaml:
  blocked_by:
    - CREATE_USE_CASE_SPECS
    - CREATE_ACTORS_AND_PERSONAS
  (process flows are now a downstream synthesis artifact)

--- General rules for all four ---

- Do not change artifact paths or identifier schemes (BR-NNN, ACT-NNN, SYS-NNN, PF-NNN).
- Do not change the artifact templates unless the section structure is incompatible with the new inputs.
- Do not update downstream consumers (planning, handoff, quality gates) — that is Step 7.
```

## Done when

- `EVT-TPL-003` inputs include `requirements.md` as required
- `EVT-TPL-004` inputs include `use-cases.puml` as required and is blocked by `CREATE_USE_CASE_DIAGRAM`
- `EVT-TPL-005` can start as soon as `requirements.md` exists (early draft)
- `EVT-TPL-006` is blocked by `CREATE_USE_CASE_SPECS` and `CREATE_ACTORS_AND_PERSONAS`
- All four skill prompts updated to derive from the new canonical spine
- Artifact paths and ID schemes unchanged
