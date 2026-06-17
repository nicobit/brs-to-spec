# Step 3 — Overlap Summary

## New dependency model (plain language)

Architecture now starts as soon as three artifacts exist: the business intake summary, the requirements catalog, and a draft gaps-and-questions. It no longer waits for use-case specs, actors, process flows, entity model, or business rules.

While architecture is running, the rest of business analysis continues in parallel: the use-case diagram, entity model, business rules, actors, use-case specs, and process flows all proceed independently. Architecture findings become available to those artifacts as optional reads — entity model, use-case specs, and business rules can absorb architecture feedback without being blocked by it.

Planning (delivery structure, traceability, modules, increments) cannot start until both use-case specs AND the architecture review are complete. This is the planning gate: it requires both analysis maturity and architecture maturity before decomposing delivery.

## Dependency changes made

| Event | Was blocked by | Now blocked by |
|---|---|---|
| `REVIEW_INITIAL_ARCHITECTURE` (EVT-TPL-008) | full stage 2b | `CREATE_REQUIREMENTS_CATALOG` + `FIND_GAPS_AND_QUESTIONS` |
| `DRAFT_ARCHITECTURE_FROM_BRS` (EVT-TPL-032) | full stage 2b | `CREATE_REQUIREMENTS_CATALOG` |
| `REVIEW_EXISTING_SYSTEM_IMPACT` (EVT-TPL-010) | full stage 2b | `CREATE_REQUIREMENTS_CATALOG` |
| `CREATE_DELIVERY_STRUCTURE` (EVT-TPL-011) | full stage 2b | `CREATE_USE_CASE_SPECS` + `REVIEW_INITIAL_ARCHITECTURE` |

## Files changed in this step

- `.brs2spec2/workflow/workflow-definition.yaml` — stage 3-planning events updated
- `.brs2spec2/workflow/event-templates/EVT-TPL-008-review-initial-architecture.yaml` — inputs updated to require `requirements.md` and `gaps-and-questions.md`; `entity-model.md` and `use-cases.puml` added as optional reads
