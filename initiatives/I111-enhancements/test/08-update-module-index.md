# Enhancement Prompt 08 — Update module-index.md

## What this prompt does

Edits `.brs2spec/module-index.md` to:
1. Add `qa.create_test_plan_per_story` to the Skill Index table
2. Add the trigger entry for the new skill
3. Add the artifact-to-skill lookup entry for `quality-gates/test-plans/`
4. Update the `@qa` persona quick-reference entry
5. Update the stage references for BDD (now stage 9b) and test strategy (now stage 10)

## File to edit

```
.brs2spec/module-index.md
```

## Change 1 — Add to the Skill Index table

Find the qa-analyst rows in the Skill Index table. After the existing `qa.create_test_strategy` row, insert:

```
| qa-analyst | `qa.create_test_plan_per_story` | `skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md` | Create one test-plan.md per confirmed user story — risk classification (C1–C4), TC-NNN test cases by type, minimum passing bar |
```

## Change 2 — Add to the Trigger-to-skill lookup table

Find the trigger table. After the row:
```
| BDD gate triggered by readiness check | `qa.create_bdd_scenarios` | Mandatory gate |
```

Insert:
```
| BDD gate triggered — stage 9b (three amigos) | `qa.create_bdd_scenarios` | Runs immediately after delivery structure confirmed (stage 9); does NOT require engineering readiness |
| Test plans missing / "create test plans" / "test plan per story" | `qa.create_test_plan_per_story` | Runs after BDD accepted (stage 9b); produces one F-XXX.X-test-plan.md per story |
| `quality-gates/test-strategy.md` missing or not Accepted — stage 10 | `qa.create_test_strategy` | Runs after BDD and test plans complete; references SCN-NNN and TC-NNN IDs |
```

Replace the existing test-strategy trigger row:
```
| `quality-gates/test-strategy.md` missing or not Accepted | `qa.create_test_strategy` | Always required — not conditional |
```
With:
```
| `quality-gates/test-strategy.md` missing or not Accepted — stage 10 | `qa.create_test_strategy` | Always required; runs after BDD (9b) and test plans (9f) — not conditional on engineering readiness |
```

## Change 3 — Add to the Artifact-to-skill lookup table

Find the qa-analyst rows. After the `quality-gates/test-strategy.md` row, insert:

```
| `quality-gates/test-plans/` (folder — one F-XXX.X-test-plan.md per story) | `qa.create_test_plan_per_story` | `module-personas/qa-analyst.md` |
```

## Change 4 — Update the @qa persona quick-reference

Find:
```
| `@qa` / "create BDD scenarios" / "write acceptance tests" | QA Analyst | `qa.create_bdd_scenarios` | `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
```

Replace with:
```
| `@qa` / "create BDD scenarios" / "write acceptance tests" | QA Analyst | `qa.create_bdd_scenarios` | `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@qa` / "create test plans" / "test plan per story" / "risk-based testing" | QA Analyst | `qa.create_test_plan_per_story` | `skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md` |
```

## Change 5 — Update stage references in the BDD trigger note

Find any note in the trigger table that says BDD requires readiness check or engineering readiness. Update to clarify:

Old note on BDD row: `Mandatory gate`
New note: `Stage 9b — runs after delivery structure confirmed; does NOT require engineering readiness or test strategy`

## Change 6 — Update the workflow path in the Persona quick-reference header note

Find the quick-reference section header text that describes stages. If any text references "BDD at stage 12" or "test strategy at stage 12", update:

- BDD scenarios → stage 9b (three amigos, after delivery structure confirmed)
- Test plans per story → stage 9f (three amigos, after BDD)
- Test strategy → stage 10 (after BDD and test plans)
- Security/API/data/observability gates → stage 12 (unchanged)

## Self-review after applying

Verify:
- [ ] `qa.create_test_plan_per_story` appears in Skill Index with correct prompt path
- [ ] Trigger table has an entry for "test plans missing / create test plans / test plan per story"
- [ ] BDD trigger note says stage 9b, not stage 12
- [ ] Test strategy trigger note says stage 10 and references BDD + test plans as prerequisites
- [ ] Artifact-to-skill table has `quality-gates/test-plans/` pointing to `qa.create_test_plan_per_story`
- [ ] `@qa` persona quick-reference has two rows (BDD and test plans)
- [ ] No trigger entry says BDD or test strategy require engineering readiness as a hard gate
