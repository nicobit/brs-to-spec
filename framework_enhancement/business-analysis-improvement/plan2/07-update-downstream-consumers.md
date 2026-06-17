# Step 7 — Update Downstream Consumers

## Purpose

Update all event templates and skill prompts outside the business-analysis phase so they consume the new canonical artifacts. This step handles the `use-case-spec.md` → `use-cases/UC-*.md` transition for every downstream consumer identified in Step 4.

## Prerequisite

Steps 1–6 must be complete. All new artifacts must be in place before downstream consumers are changed to read from them.

## Run this prompt

```text
Update downstream .brs2spec2 event templates and prompts so they consume the new business-analysis
artifacts from Steps 1–6.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md
  Focus on "Downstream Consumption Model".

Before making any changes, search across .brs2spec2/ for all files that reference:
- business-analysis/use-case-spec.md
- business-analysis/actors-and-personas.md (check if it is read via old assumption that actors precede UCs)
- business-analysis/process-flows.md (check if it is a required input anywhere it should now be optional)

List all found references with the file path and the context.

Note on the two use-case diagram files:
- use-cases.puml is the PlantUML source for tooling and CI rendering.
- use-cases.md is the Mermaid-in-markdown version for GitLab Pages and IDE preview.
- Downstream consumers that produce human-readable output (review-package, handoff, readiness)
  should reference use-cases.md as the readable input.
- Downstream consumers that need the raw diagram structure for tooling may reference use-cases.puml.
- Where both are relevant, list use-cases.md as optional input alongside use-cases.puml.

Then make the following changes:

--- Planning event templates ---

Inspect:
- EVT-TPL-011-create-delivery-structure.yaml
- EVT-TPL-013-identify-software-modules.yaml
- EVT-TPL-014-define-delivery-increments.yaml
- EVT-TPL-012-create-traceability-matrix.yaml
- EVT-TPL-029-create-agile-planning-view.yaml

For each:
- Replace any input reference to business-analysis/use-case-spec.md
  with business-analysis/use-cases/UC-*.md or business-analysis/use-cases/ (folder).
- Add business-analysis/requirements.md as a required input where it is currently absent.
- Add business-analysis/use-cases.puml as an optional input where relevant.

--- Quality gate event templates ---

Inspect:
- EVT-TPL-017-create-bdd-scenarios.yaml
- EVT-TPL-018-create-test-strategy.yaml
- EVT-TPL-019-create-security-review.yaml
- EVT-TPL-020-create-api-contract.yaml
- EVT-TPL-021-create-data-contract.yaml
- EVT-TPL-031-create-business-test-expectations.yaml
- EVT-TPL-036-create-test-plan-per-story.yaml

For each:
- Replace any reference to business-analysis/use-case-spec.md with business-analysis/use-cases/UC-*.md.
- For data-contract: confirm entity-model.md is listed as a required input.
- For BDD: confirm use-cases/UC-*.md and business-rules.md are required inputs.

--- Handoff event templates ---

Inspect:
- EVT-TPL-024-create-openspec-handoff.yaml
- EVT-TPL-025-create-standalone-handoff.yaml
- EVT-TPL-026-create-compact-handoff.yaml

For each:
- Replace any reference to business-analysis/use-case-spec.md with business-analysis/use-cases/UC-*.md.
- Confirm requirements.md is listed as an input.

--- Review package ---

Inspect:
- EVT-TPL-028-create-review-package.yaml

- Replace reference to use-case-spec.md with use-cases/UC-*.md.
- Confirm requirements.md is included.

--- Engineering readiness ---

Inspect:
- EVT-TPL-015-check-engineering-readiness.yaml
- EVT-TPL-016-generate-initiative-context.yaml

- Replace any reference to use-case-spec.md.
- Confirm requirements.md and use-cases/UC-*.md are readable inputs.

--- Rules for all changes ---

- Do not change skill prompt content in this step — only event template input lists.
- Do not change blocked_by dependencies — the workflow structure was set in Steps 1–3.
- If a file has no reference to use-case-spec.md, note it as confirmed clean and move on.
- After all changes, produce a list of every file modified in this step.
```

## Done when

- No downstream event template still references `business-analysis/use-case-spec.md` as an input
- Planning event templates read `requirements.md` and `use-cases/UC-*.md`
- Quality gate templates read `use-cases/UC-*.md` and `entity-model.md` where appropriate
- Handoff and review-package templates read `use-cases/UC-*.md`
- A list of all modified files exists (either in this step's output or as a note in this folder)
