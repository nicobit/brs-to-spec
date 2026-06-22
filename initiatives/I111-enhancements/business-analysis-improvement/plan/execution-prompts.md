# Prompt List To Execute The Improvements

## How to use this file

These prompts are intended for carrying out the actual `.brs2spec2` improvement work in the repository.

They assume the improvement package in `framework_enhancement/business-analysis-improvement/` is the design reference.

Each prompt is written so it can be run as a focused implementation task.

## Prompt 1 — Review and lock the target design

Use this prompt first.

```text
Review the business-analysis improvement package in `framework_enhancement/business-analysis-improvement/` and lock the target design decisions before editing `.brs2spec2`.

Read at minimum:
- `artifact-map.md`
- `proposed-stage-design.md`
- `prompt-adoption-strategy.md`
- `prompts/README.md`

Then inspect the current `.brs2spec2` files:
- `.brs2spec2/workflow/workflow-definition.yaml`
- `.brs2spec2/workflow/artifact-ownership.md`
- `.brs2spec2/workflow/event-templates/EVT-TPL-003-create-business-rules.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-004-create-actors-and-personas.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-005-find-gaps-and-questions.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-006-create-process-flows.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-030-create-entity-model.yaml`

Produce a concise implementation decision note under `framework_enhancement/business-analysis-improvement/plan/` that confirms:
- target artifact names and paths
- compatibility decisions for old artifacts
- whether underscore or hyphen naming will be standardized
- whether migration is cutover or transitional
```

## Prompt 2 — Add the requirements artifact to `.brs2spec2`

```text
Implement support for `business-analysis/requirements.md` in `.brs2spec2`.

Use these design references:
- `framework_enhancement/business-analysis-improvement/artifact-map.md`
- `framework_enhancement/business-analysis-improvement/prompts/01-create-requirements.md`
- `framework_enhancement/business-analysis-improvement/proposed-stage-design.md`

Update the framework as needed:
- add a new skill prompt under `.brs2spec2/skills/`
- add a matching artifact template if needed
- add a new event template under `.brs2spec2/workflow/event-templates/`
- update `.brs2spec2/workflow/workflow-definition.yaml`
- update `.brs2spec2/workflow/artifact-ownership.md`

Requirements:
- `requirements.md` must become the canonical business-analysis catalog
- it must be generated after `business-intake/business-intake-summary.md`
- later business-analysis artifacts must be able to depend on it

Also document any compatibility implications in the improvement plan folder.
```

## Prompt 3 — Add the use-case diagram artifact

```text
Implement support for `business-analysis/use_cases.puml` in `.brs2spec2`.

Use these design references:
- `framework_enhancement/business-analysis-improvement/artifact-map.md`
- `framework_enhancement/business-analysis-improvement/prompts/03-create-use-case-diagram.md`
- `framework_enhancement/business-analysis-improvement/proposed-stage-design.md`

Update the framework as needed:
- add a new skill prompt
- add a new event template
- update workflow dependencies
- update artifact ownership

Requirements:
- `use_cases.puml` must be generated from `requirements.md`
- it must assign stable `UC-NNN` IDs
- it must become the prerequisite for detailed use-case specs
```

## Prompt 4 — Replace monolithic use-case spec with one-file-per-UC

```text
Refactor `.brs2spec2` so detailed use-case specs are written to `business-analysis/use_cases/UC-*.md` instead of `business-analysis/use-case-spec.md`.

Use these design references:
- `framework_enhancement/business-analysis-improvement/artifact-map.md`
- `framework_enhancement/business-analysis-improvement/prompts/04-create-use-case-spec.md`
- `framework_enhancement/business-analysis-improvement/proposed-stage-design.md`

Inspect and update at minimum:
- `.brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml`
- any current artifact templates for use-case specs
- `.brs2spec2/workflow/artifact-ownership.md`
- downstream references in `.brs2spec2/workflow/event-templates/`

Requirements:
- one file per use case
- no multiple UCs in one file
- downstream references to `business-analysis/use-case-spec.md` must be identified and updated or given a compatibility strategy
```

## Prompt 5 — Rework entity model as a first-class artifact

```text
Rework `.brs2spec2` entity-model support so `business-analysis/entity_model.md` is aligned with the AIUP-style business-analysis spine.

Use these design references:
- `framework_enhancement/business-analysis-improvement/artifact-map.md`
- `framework_enhancement/business-analysis-improvement/prompts/02-create-entity-model.md`
- `framework_enhancement/business-analysis-improvement/proposed-stage-design.md`

Inspect and update at minimum:
- `.brs2spec2/workflow/event-templates/EVT-TPL-030-create-entity-model.yaml`
- any existing entity-model prompt and template
- workflow-definition stage logic
- downstream data-contract dependencies

Requirements:
- entity model should derive primarily from `requirements.md`
- it should not remain only a side-path artifact for optional analysis
- naming consistency must be addressed: `entity_model.md` vs `entity-model.md`
```

## Prompt 6 — Refactor support artifacts around the new spine

```text
Refactor the framework-native business-analysis artifacts so they consume the new canonical analysis spine.

Use these design references:
- `framework_enhancement/business-analysis-improvement/artifact-map.md`
- `framework_enhancement/business-analysis-improvement/prompts/05-create-business-rules.md`
- `framework_enhancement/business-analysis-improvement/prompts/06-create-actors-and-personas.md`
- `framework_enhancement/business-analysis-improvement/prompts/07-create-process-flows.md`
- `framework_enhancement/business-analysis-improvement/prompts/08-find-gaps-and-questions.md`

Update as needed:
- business-rules prompt/template/event
- actors-and-personas prompt/template/event
- process-flows prompt/template/event
- gaps-and-questions prompt/template/event

Requirements:
- business rules should derive from `requirements.md`
- actors should align with `use_cases.puml`
- process flows should synthesize from `use_cases/UC-*.md` plus actors
- gaps should absorb findings from requirements, entity model, UCs, rules, and architecture findings
```

## Prompt 7 — Redesign the workflow overlap with architecture

```text
Update `.brs2spec2/workflow/workflow-definition.yaml` to support the intended overlap between business analysis and architecture.

Use these design references:
- `framework_enhancement/business-analysis-improvement/proposed-stage-design.md`
- especially:
  - "What Must Exist Before Architecture Starts"
  - "Recommended Overlap Model"
  - "Architecture Entry Point"

Requirements:
- architecture must not wait for all business-analysis artifacts to finish
- architecture should start after a minimum baseline:
  - business-intake summary
  - requirements
  - initial gaps/questions
- business-analysis artifacts should continue refining after architecture starts
- planning should depend on both business-analysis maturity and architecture maturity

Produce the workflow-definition changes and summarize the new dependency model.
```

## Prompt 8 — Update downstream consumers

```text
Update downstream `.brs2spec2` event templates and prompts so they consume the new business-analysis artifacts correctly.

Use these design references:
- `framework_enhancement/business-analysis-improvement/artifact-map.md`
- `framework_enhancement/business-analysis-improvement/proposed-stage-design.md`

Inspect and update at minimum:
- planning event templates
- traceability event templates
- readiness event templates
- quality-gate event templates
- handoff event templates
- review-package event template

Requirements:
- planning should read `requirements.md` and `use_cases/UC-*.md` first
- review-package and handoff must not depend on the old monolithic `use-case-spec.md`
- quality gates should use the new canonical artifacts wherever appropriate
```

## Prompt 9 — Add migration and compatibility handling

```text
Design and implement a compatibility strategy for the business-analysis artifact transition in `.brs2spec2`.

Use these design references:
- `framework_enhancement/business-analysis-improvement/plan/implementation-plan.md`
- the parent-folder artifact map and stage design

Requirements:
- identify all references to `business-analysis/use-case-spec.md`
- decide how old initiatives continue to work
- address filename compatibility for `entity-model.md` vs `entity_model.md`
- document the migration strategy in the improvement plan folder

If code changes are needed, implement the least risky transition path and document tradeoffs.
```

## Prompt 10 — Validate the redesigned business-analysis flow

```text
Validate the redesigned `.brs2spec2` business-analysis flow end to end on a representative initiative.

Use these design references:
- `framework_enhancement/business-analysis-improvement/plan/implementation-plan.md`
- all prompt drafts under `framework_enhancement/business-analysis-improvement/prompts/`

Validate at least:
- business-intake summary
- requirements
- use-case diagram
- use-case spec folder output
- entity model
- business rules
- actors and personas
- process flows
- gaps and questions
- architecture overlap behavior
- planning consumption

Document the findings, issues, and remaining follow-up work in the improvement plan folder.
```

## Recommended execution order

Use the prompts in this order:

1. Prompt 1
2. Prompt 2
3. Prompt 3
4. Prompt 4
5. Prompt 5
6. Prompt 6
7. Prompt 7
8. Prompt 8
9. Prompt 9
10. Prompt 10
