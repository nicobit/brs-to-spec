# Enhancement Prompt 05 — Update tasks.md Template

## What this prompt does

Edits `.brs2spec/templates/openspec-handoff/tasks.md` to:
1. Add a "Unit test targets" section (derived from test plan TC-NNN rows of type Unit)
2. Update validation tasks to reference TC-NNN from test-plan.md (not just raw SCN-NNN)
3. Update done criteria to reference test plan C1/C2 gating tiers
4. Keep implementation tasks section unchanged

## File to edit

```
.brs2spec/templates/openspec-handoff/tasks.md
```

## Change 1 — Add "Unit test targets" section before Validation tasks

After the `## Implementation tasks` section and before `## Validation tasks`, insert:

```markdown
## Unit test targets

<!-- Derived from quality-gates/test-plans/{{F-XXX.X}}-test-plan.md — rows where Test type = Unit -->
<!-- This is a commitment made during refinement. The developer implements these before marking the story done. -->
<!-- Do not add new unit test targets here during implementation — update the test plan instead. -->

| TC-ID | Class / function to test | Condition to cover | Expected outcome | Criticality |
|---|---|---|---|---|
| TC-NNN | {{e.g. LoanEligibilityService.evaluate()}} | {{e.g. null income input}} | {{e.g. throws ArgumentNullException}} | C1 |
| TC-NNN | {{class / function}} | {{e.g. DTI ratio at boundary (0.43)}} | {{e.g. returns eligible = true}} | C2 |
| TC-NNN | {{class / function}} | {{e.g. DTI ratio above boundary (0.44)}} | {{e.g. returns eligible = false}} | C2 |

<!-- Fill from test-plan.md Unit rows. -->
<!-- If no unit test targets apply: write "Unit tests: none required for this story — [reason]" and delete the table. -->
```

## Change 2 — Update Validation tasks section

Find:
```markdown
## Validation tasks

<!-- One entry per AC that requires an explicit test or verification step. -->
<!-- Link each validation task to the BDD scenario(s) it executes — use SCN-NNN IDs from story.md. -->

- [ ] OS-{{F-XXX.X}}-V01: Verify {{criterion}} — {{SCN-NNN}}
  - Acceptance source: AC-NNN
  - BDD scenario: SCN-NNN (see `quality-gates/bdd/<F-NNN.md>` for this story's feature)
  - How to validate:
  - Evidence expected:
```

Replace with:

```markdown
## Validation tasks

<!-- One entry per test case (TC-NNN) in the test plan that requires explicit execution evidence. -->
<!-- Derived from quality-gates/test-plans/{{F-XXX.X}}-test-plan.md -->
<!-- C1 tasks must be executed before merge. C2 tasks must be executed before sprint review. -->

- [ ] OS-{{F-XXX.X}}-V01: Verify {{criterion}} — {{TC-NNN}} ({{C1 / C2}})
  - Test case: TC-NNN (see `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md`)
  - Test type: {{Unit / Integration / API / Security / Performance}}
  - BDD scenario: {{SCN-NNN or "— (unit test, no BDD scenario)"}}
  - Acceptance source: AC-NNN
  - How to validate: {{e.g. run `pytest tests/test_loan_eligibility.py::test_null_income`}}
  - Evidence expected: {{e.g. test passes in CI; attach CI run link}}
  - Gating: {{Blocks merge / Blocks sprint done / Advisory}}
```

## Change 3 — Update Done criteria section

Find:
```markdown
## Done criteria

<!-- This story is done when ALL of the following are true. -->
<!-- Keep this short — these are the conditions, not implementation steps. -->

- [ ] All implementation tasks merged and passing CI
- [ ] All BDD scenarios referenced in story.md pass (SCN-NNN … SCN-NNN)
- [ ] All validation tasks executed with evidence attached
- [ ] Any telemetry signals from this story visible in staging
- [ ] Dependent stories unblocked — notify team when done (see dependency-graph.md)
```

Replace with:

```markdown
## Done criteria

<!-- This story is done when ALL of the following are true. -->
<!-- Keep this short — these are the conditions, not implementation steps. -->

- [ ] All implementation tasks merged and passing CI
- [ ] All C1 test cases pass in CI before merge (see test-plan.md — Blocks merge list)
- [ ] All C2 test cases pass in staging before sprint review (see test-plan.md — Blocks sprint done list)
- [ ] All unit test targets (TC-NNN rows above) implemented and passing
- [ ] All BDD scenarios referenced in story.md pass (SCN-NNN … SCN-NNN — see quality-gates/bdd/F-NNN.md)
- [ ] All validation tasks executed with evidence attached
- [ ] Any telemetry signals from this story visible in staging
- [ ] Dependent stories unblocked — notify team when done (see dependency-graph.md)
```

## Self-review after applying

Verify:
- [ ] `## Unit test targets` section exists between Implementation tasks and Validation tasks
- [ ] Unit test targets table has TC-NNN, class/function, condition, expected outcome, criticality columns
- [ ] Validation tasks reference TC-NNN not just SCN-NNN
- [ ] Validation tasks include test type and gating tier
- [ ] Done criteria references C1 (blocks merge) and C2 (blocks sprint done) test cases
- [ ] Done criteria references both TC-NNN (test plan) and SCN-NNN (BDD)
