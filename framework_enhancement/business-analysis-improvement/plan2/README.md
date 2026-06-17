# Business Analysis Improvement — Revised Execution Plan

This folder contains the revised, per-prompt execution plan for improving `.brs2spec2` business analysis.

## What changed from `plan/`

- Prompt 7 (workflow overlap with architecture) moved **earlier** — before use-case specs and entity model — because the dependency encoding must be in place before new artifacts are wired up. Doing it last would require unwinding linearity already introduced.
- Naming convention locked to framework standard: **hyphen-separated** throughout (`entity-model.md`, `use-cases.puml`, `use-cases/UC-*.md`). The `entity_model.md` / `use_cases.puml` underscore forms from the AIUP reference design are **not used**.
- Use-case per-file output folder uses `use-cases/` (hyphen), matching `.brs2spec2` artifact naming.
- Design-lock prompt includes an explicit naming decision section so there is no ambiguity before any framework file is edited.

## Execution order

| Step | File | What it does |
|---|---|---|
| 0 | [00-lock-design-decisions.md](00-lock-design-decisions.md) | Lock target artifact names, paths, naming convention, and compatibility strategy before editing any framework file |
| 1 | [01-add-requirements-artifact.md](01-add-requirements-artifact.md) | Add `business-analysis/requirements.md` as the canonical analysis entry point |
| 2 | [02-add-use-case-diagram.md](02-add-use-case-diagram.md) | Add `business-analysis/use-cases.puml` with stable `UC-NNN` IDs |
| 3 | [03-update-workflow-overlap.md](03-update-workflow-overlap.md) | Encode architecture overlap in `workflow-definition.yaml` — do this before wiring UC specs and entity model |
| 4 | [04-replace-use-case-spec-with-per-uc-files.md](04-replace-use-case-spec-with-per-uc-files.md) | Replace `use-case-spec.md` with `use-cases/UC-*.md` one-file-per-UC output |
| 5 | [05-rework-entity-model.md](05-rework-entity-model.md) | Make `entity-model.md` a first-class artifact derived from `requirements.md` |
| 6 | [06-refactor-support-artifacts.md](06-refactor-support-artifacts.md) | Refactor business-rules, actors, process-flows, and gaps to consume the new spine |
| 7 | [07-update-downstream-consumers.md](07-update-downstream-consumers.md) | Update planning, quality gates, handoff, and review-package to use new artifacts |
| 8 | [08-migration-and-compatibility.md](08-migration-and-compatibility.md) | Define and implement compatibility strategy for existing initiatives |
| 9 | [09-validate-end-to-end.md](09-validate-end-to-end.md) | Validate the redesigned flow on a representative initiative |

## Naming conventions locked for this plan

| Artifact | Path in initiative workspace |
|---|---|
| Requirements catalog | `business-analysis/requirements.md` |
| Entity model | `business-analysis/entity-model.md` |
| Use-case diagram (PlantUML, tooling) | `business-analysis/use-cases.puml` |
| Use-case diagram (Mermaid, GitLab Pages / IDE) | `business-analysis/use-cases.md` |
| Use-case specs (per-file) | `business-analysis/use-cases/UC-NNN.md` |
| Business rules | `business-analysis/business-rules.md` |
| Actors and personas | `business-analysis/actors-and-personas.md` |
| Process flows | `business-analysis/process-flows.md` |
| Gaps and questions | `business-analysis/gaps-and-questions.md` |

All names use hyphens. No underscores. This matches the existing `.brs2spec2` artifact naming pattern confirmed in `artifact-ownership.md` and `artifact-templates/`.
