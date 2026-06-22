# Enhancement Prompt 02 — Move Test Strategy to Stage 10

## What this prompt does

1. Edits `.brs2spec/brs-to-spec-run-workflow.md` to move test strategy from stage 12 to stage 10
2. Edits `.brs2spec/skills/4-engineering-readiness/quality-gates/create-test-strategy.md` to:
   - Add BDD scenarios (`quality-gates/bdd/`) as a primary input
   - Add test plans (`quality-gates/test-plans/`) as a primary input
   - Update the FR→test mapping section to reference SCN-NNN and TC-NNN IDs
   - Update the prerequisite: test strategy requires BDD (stage 9b) and test plans (stage 9f)

## File 1: `brs-to-spec-run-workflow.md`

### Update stage table

After stage 9e (story enrichment check), insert stage 10 as test strategy:

```
| 10 | Test strategy | `quality-gates/test-strategy.md` | Scope note present; Technology Stack table populated from initiative-context.md; Test Levels table filled with test types, automation targets, and frameworks; Requirement-to-Test Mapping references FR-NNN → SCN-NNN and TC-NNN IDs (not generic test types only); Risks section has owners; `Status: Accepted` in Metadata table | `skills/4-engineering-readiness/quality-gates/create-test-strategy.md` | (9b) BDD accepted; (9f) test plans complete |
```

Remove test strategy from the stage 12 group. Stage 12 now covers only: security-review, api-contract, data-contract, observability-plan.

Update the stage 11 row (initiative context) — it is unchanged, remains at 11.

### Update hard gate table

Add:
```
| Test strategy (10) | `quality-gates/bdd/` with Status: Accepted in acceptance-checklist.md; at least one test plan in `quality-gates/test-plans/` |
```

Update:
```
| Handoff (13) | All triggered gates with `Status: Accepted` — including BDD (9b), test strategy (10), and all stage-12 gates; `state/open-decisions.md` with zero blocking decisions |
```

### Update pre-generation gate check

Add a new check block for test strategy:

```
**For `quality-gates/test-strategy.md` (stage 10 — after BDD and test plans):**
- [ ] `quality-gates/bdd/acceptance-checklist.md` exists and has `Status: Accepted` — BDD must be complete before test strategy is written
- [ ] At least one `quality-gates/test-plans/F-XXX.X-test-plan.md` exists — test plans provide the TC-NNN inventory and risk classification that feeds the Requirement-to-Test Mapping section
- [ ] `engineering-readiness/initiative-context.md` exists — provides Technology Stack source for the test strategy Technology Stack table
- If BDD or test plans are missing: execute those stages first. Do not write test strategy without them.
```

## File 2: `skills/4-engineering-readiness/quality-gates/create-test-strategy.md`

### Update the Inputs section

Add to the top of the inputs list (before readiness-check.md):

```
- `quality-gates/bdd/` — **primary input**: read all F-NNN.md files and acceptance-checklist.md; use SCN-NNN IDs and story coverage to populate the Requirement-to-Test Mapping section; the acceptance test coverage is now known — do not estimate it
- `quality-gates/test-plans/` — **primary input**: read all F-XXX.X-test-plan.md files; use TC-NNN rows, test types, and risk classifications (C1–C4) to populate the Test Levels table with initiative-specific evidence and the Risks section with story-level risk signals
```

### Update the Generation steps section

Replace step 3 ("Write quality-gates/test-strategy.md...") with:

```
3. Write `quality-gates/test-strategy.md` starting with `## Metadata` table as in the template
4. **Requirement-to-Test Mapping**: for each FR-NNN in `business-intake/business-intake-summary.md`, find the corresponding SCN-NNN scenarios in `quality-gates/bdd/` and the TC-NNN test cases in `quality-gates/test-plans/`. Map FR-NNN → SCN-NNN list → TC-NNN list → test levels covered. This is now a concrete mapping, not a generic estimate.
5. **Test Levels**: for each test level (Unit, Integration, API, UI, Security, Performance, Audit/Compliance), aggregate evidence from test plans: count of C1/C2/C3/C4 test cases per level; automation target from initiative-context.md technology stack; framework from test plans.
6. **Risks**: derive from test plans — any story with overall risk C1 and no automation candidate is a testing risk. Any test type with zero TC-NNN rows is a coverage gap.
7. Complete all remaining sections.
```

### Update the Quality bar section

Add:
```
- The Requirement-to-Test Mapping table must reference specific SCN-NNN and TC-NNN IDs, not just test types. A mapping row that says "FR-001 → Integration test" without citing scenarios is incomplete.
- The Test Levels table must include a "C1 count / C2 count" column derived from test plans — not estimated.
- Risks must include any story where overall risk is C1 but automation coverage is None.
```

### Update the Self-review checklist

Add:
```
- [ ] Requirement-to-Test Mapping cites specific SCN-NNN and TC-NNN IDs — not generic test types only
- [ ] Test Levels table includes C1/C2 counts derived from test plans
- [ ] At least one Risk row exists per story with overall risk = C1 and automation = None
- [ ] BDD acceptance-checklist.md was read before writing — test strategy does not re-estimate BDD coverage
- [ ] Test plans were read before writing — test strategy does not re-estimate unit test coverage
```

## Self-review after applying

Verify:
- [ ] Stage 10 in workflow runner stage table is test-strategy with prerequisite (9b) and (9f)
- [ ] Stage 12 does not mention test-strategy
- [ ] Hard gate table has a row for test strategy (10) with BDD and test plans as prerequisites
- [ ] `create-test-strategy.md` inputs list BDD and test-plans as primary inputs
- [ ] `create-test-strategy.md` generation steps reference SCN-NNN and TC-NNN mapping
- [ ] `create-test-strategy.md` quality bar requires specific ID references in mapping table
