# Enhancement Prompt 09 — Update workflow-state.json Template

## What this prompt does

Edits `.brs2spec/templates/state/workflow-state.json` to add the new artifact entries for:
1. `quality-gates/test-plans/` (new folder — one test plan per story)
2. `quality-gates/test-stubs` (new — generated stubs in target repo)

Also updates the `repair-workspace-state.md` scan table to include the new stages and artifacts.

---

## File 1: `templates/state/workflow-state.json`

### Update the `artifacts` object

Find the existing quality gates block:
```json
"quality-gates/bdd/":                                   { "status": "not-triggered", "note": "" },
"quality-gates/test-strategy.md":                      { "status": "not-triggered", "note": "" },
"quality-gates/security-review.md":                    { "status": "not-triggered", "note": "" },
```

Replace with (adding test-plans and reordering to reflect new stage sequence):
```json
"quality-gates/bdd/":                                   { "status": "not-triggered", "note": "" },
"quality-gates/test-plans/":                            { "status": "not-triggered", "note": "" },
"quality-gates/test-strategy.md":                      { "status": "not-triggered", "note": "" },
"quality-gates/security-review.md":                    { "status": "not-triggered", "note": "" },
"quality-gates/api-contract.md":                       { "status": "not-triggered", "note": "" },
"quality-gates/data-contract.md":                      { "status": "not-triggered", "note": "" },
"quality-gates/observability-plan.md":                 { "status": "not-triggered", "note": "" },
"quality-gates/test-stubs":                            { "status": "not-triggered", "note": "" },
```

Note: `quality-gates/test-stubs` uses `not-triggered` as the initial status because stubs are
generated only when the handoff exists. The workflow runner sets this to `triggered-incomplete`
when stage 13 completes and to `triggered-complete` when stage 13a completes.

---

## File 2: `skills/0-repair/repair-workspace-state.md`

### Update the scan table in Step 3

Find the artifacts scan table. After the existing stage 12 row:
```
| 12 | Quality gates | Per triggered gate | `Status: Accepted` in Metadata table at top of each gate file |
```

Update to:
```
| 9b | BDD scenarios (three amigos) | `quality-gates/bdd/` | acceptance-checklist.md exists with `Status: Accepted`; at least one F-NNN.md file with complete Gherkin blocks |
| 9f | Test plans per story | `quality-gates/test-plans/` | At least one F-XXX.X-test-plan.md exists; each has TC-NNN rows with criticality and minimum passing bar |
| 10 | Test strategy | `quality-gates/test-strategy.md` | `Status: Accepted` in Metadata table; references SCN-NNN and TC-NNN in Requirement-to-Test Mapping |
| 12 | Quality gates (security, API, data, observability) | Per triggered gate | `Status: Accepted` in Metadata table at top of each gate file |
| 13a | Test stubs | Target application repository | Stub files exist in test folder; each stub has a failing assertion |
```

### Update the absolute blocking table in Step 4

After the existing rows, add:
```
| `quality-gates/bdd/acceptance-checklist.md` missing or not Accepted | next_action cannot be later than stage 9b |
| `quality-gates/test-plans/` missing or empty | next_action cannot be later than stage 9f |
| `quality-gates/test-strategy.md` missing or not Accepted | next_action cannot be later than stage 10 |
```

### Update the gate chain walk in Step 4

The current gate chain is:
```
1 → 2 → 2b → 2c → 2d → 2e → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 9b → 9c → 9d → 10 → 11 → 12 → 12b → 13 → 14
```

Update to reflect new stage assignments:
```
1 → 2 → 2b → 2c → 2d → 2e → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 9b (BDD) → 9c (process flows) → 9d (use cases) → 9e (story enrichment) → 9f (test plans) → 10 (test strategy) → 11 → 12 → 12b → 13 → 13a (test stubs) → 14
```

---

## Self-review after applying

Verify:
- [ ] `workflow-state.json` template has `quality-gates/test-plans/` with `not-triggered` status
- [ ] `workflow-state.json` template has `quality-gates/test-stubs` with `not-triggered` status
- [ ] `quality-gates/test-plans/` appears between `quality-gates/bdd/` and `quality-gates/test-strategy.md`
- [ ] `repair-workspace-state.md` scan table has rows for stages 9b, 9f, 10, 13a
- [ ] `repair-workspace-state.md` absolute blocking table has rows for BDD, test plans, test strategy
- [ ] `repair-workspace-state.md` gate chain walk includes 9b, 9f, 10, 13a in correct order
