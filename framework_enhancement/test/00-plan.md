# Framework Enhancement Plan — Testing Lifecycle Redesign

## Objective

Restructure the brs-to-spec testing lifecycle to align with Agile delivery:
- Move testing activities to the right phase (three-amigos / refinement)
- Add a per-story test plan with risk-based criticality
- Make test stubs automatic, not manual
- Eliminate duplicate BDD content across artifacts
- Give developers a complete, self-contained test contract in every story folder

---

## Changes overview

| # | Change | Files affected | Prompt |
|---|---|---|---|
| 1 | Move BDD to stage 9b (three-amigos, right after delivery structure confirmed) | `brs-to-spec-run-workflow.md` | `01-move-bdd-to-stage-9b.md` |
| 2 | Move test strategy to stage 10 (after BDD, references SCN-NNN) | `brs-to-spec-run-workflow.md`, `create-test-strategy.md` | `02-move-test-strategy-to-stage-10.md` |
| 3 | New skill: `qa.create_test_plan_per_story` — risk-based test plan per story | NEW `skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md`, NEW `templates/openspec-handoff/test-plan.md`, `module-index.md` | `03-create-test-plan-skill.md` |
| 4 | Update `story.md` — BDD section becomes pointer, not copy | `templates/openspec-handoff/story.md` | `04-update-story-template.md` |
| 5 | Update `tasks.md` — validation tasks reference TC-NNN from test-plan.md | `templates/openspec-handoff/tasks.md` | `05-update-tasks-template.md` |
| 6 | Update `coding-prompt.md` — "tests to make pass" uses TC-NNN C1+C2 from test-plan.md | `templates/openspec-handoff/coding-prompt.md` | `06-update-coding-prompt-template.md` |
| 7 | Make test stub generation automatic at stage 13a (after handoff) | `brs-to-spec-run-workflow.md`, `03-generate-test-stubs-from-bdd.md` | `07-make-test-stubs-automatic.md` |
| 8 | Update `module-index.md` — add new skill, update stage table, update BDD trigger | `module-index.md` | `08-update-module-index.md` |
| 9 | Update `workflow-state.json` template — add new artifact entries | `templates/state/workflow-state.json` | `09-update-workflow-state-template.md` |

---

## Execution order

Changes must be executed in this order — each builds on the previous:

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09
```

Changes 04, 05, 06 are independent of each other and can run in parallel after 03.
Changes 08 and 09 must run last (they reference all prior changes).

---

## New stage table (after all changes applied)

| # | Stage | Artifact | Phase |
|---|---|---|---|
| ... | (unchanged through stage 9) | | |
| 9 | Delivery structure confirmed | `planning/delivery-structure/` | Refinement |
| **9b** | **BDD scenarios (three amigos)** | `quality-gates/bdd/` | **Three amigos — MOVED from 12** |
| 9c | Process flows confirmed | `business-analysis/process-flows.md` | Refinement |
| 9d | Use cases confirmed | `business-analysis/use-case-spec.md` | Refinement |
| 9e | Story enrichment check | `planning/delivery-structure/` (enriched) | Orchestrator inline |
| **9f** | **Test plans per story** | `quality-gates/test-plans/F-XXX.X-test-plan.md` (one per story) | **Three amigos — NEW** |
| **10** | **Test strategy** | `quality-gates/test-strategy.md` | **After BDD + test plans — MOVED from 12** |
| 11 | Initiative context | `engineering-readiness/initiative-context.md` | Sprint 0 |
| 12 | Quality gates (security, API, data, observability) | `quality-gates/<gate>.md` | Quality gates |
| 12b | Entity model | `business-analysis/entity-model.md` | After data-contract |
| 13 | Handoff | `specs/` | Sprint ready |
| **13a** | **Test stub generation (automatic)** | Target application repo | **Auto-triggered after handoff — NEW** |
| 14 | Review package | `review-package/status.md` | On-demand |

---

## Key design decisions

### BDD at stage 9b — the three-amigos principle
BDD scenarios ARE the acceptance criteria in executable form. They must be written during
backlog refinement (three amigos: PO + dev + QA), not after engineering readiness. Moving BDD
to 9b means the engineering readiness check (stage 8) can reference concrete scenario IDs,
and the test strategy (stage 10) can map FR-NNN → SCN-NNN with real traceability.

### Test plan per story — risk-based approach
A `test-plan.md` per story is the test contract for that story. It answers:
- What test types apply (unit, integration, API, UI, security, performance)?
- What are the specific test cases (TC-NNN IDs)?
- What is the criticality (C1–C4) of each test case, and why?
- What is the minimum passing bar before the story is done?

Risk tiers:
- **C1 Critical**: high business impact + low existing confidence → blocks merge
- **C2 High**: high impact + partial coverage → blocks sprint done
- **C3 Medium**: moderate impact → should pass; deferral requires documented risk
- **C4 Low**: cosmetic / negligible impact → advisory only

### Single source of truth for BDD
`quality-gates/bdd/F-NNN.md` is the canonical source. `story.md` references it — does not
copy it. This eliminates silent divergence when scenarios are updated after handoff.

### Test stubs automatic at 13a
Test stub generation is not optional and not manual. When the handoff is generated, stubs are
automatically written to the target application repository. Developers start every story with
red tests. The "CI fails until implemented" promise is kept structurally, not by convention.

### Test plan as input to stubs (not just BDD)
The stub generator reads `test-plan.md` TC-NNN rows to generate unit test stubs (type=Unit),
not just BDD stubs. This closes the unit test gap — unit tests now have a defined scope before
implementation starts.
