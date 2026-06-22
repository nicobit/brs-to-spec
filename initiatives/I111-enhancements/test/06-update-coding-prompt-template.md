# Enhancement Prompt 06 — Update coding-prompt.md Template

## What this prompt does

Edits `.brs2spec/templates/openspec-handoff/coding-prompt.md` to:
1. Replace "BDD scenarios to make pass" section with "Tests to make pass" (covers C1+C2 from test-plan.md)
2. Add test plan reference to the Repository execution guard
3. Update Definition of done to reference TC-NNN criticality tiers

## File to edit

```
.brs2spec/templates/openspec-handoff/coding-prompt.md
```

## Change 1 — Update Repository execution guard

Find the numbered list inside `## Repository execution guard`. After item 6 ("Check open questions"), add:

```markdown
7. **Check test plan** — read `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md`. Note all C1 test cases (blocks merge). You must make these pass before the PR is submitted. Note C2 test cases (blocks sprint done) — make these pass before sprint review.
```

Also add to the "Stop and report to the human if:" list:

```markdown
- The test plan file `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md` does not exist — a test plan is required before implementation starts.
```

## Change 2 — Replace "BDD scenarios to make pass" with "Tests to make pass"

Find:

```markdown
## BDD scenarios to make pass

<!-- Source: quality-gates/bdd/F-NNN.md for this feature group -->
<!-- If BDD gate not triggered: write "BDD gate not triggered for this initiative." -->

- SCN-NNN: {{scenario title}}
```

Replace with:

```markdown
## Tests to make pass

<!-- Source: quality-gates/test-plans/{{F-XXX.X}}-test-plan.md (C1 and C2 rows) -->
<!-- Full test plan: quality-gates/test-plans/{{F-XXX.X}}-test-plan.md -->
<!-- Full BDD scenarios: quality-gates/bdd/F-NNN.md -->

### C1 — Must pass before merge

<!-- Copy C1 rows from test-plan.md. These block the PR from being merged. -->

| TC-ID | Test type | Condition | How to run |
|---|---|---|---|
| TC-NNN | {{Unit / Integration / Security}} | {{condition}} | {{e.g. pytest tests/test_loan.py::test_null_income}} |
| TC-NNN | {{test type}} | {{condition}} | {{command}} |

### C2 — Must pass before sprint review

<!-- Copy C2 rows from test-plan.md. These block sprint done. -->

| TC-ID | Test type | Condition | How to run |
|---|---|---|---|
| TC-NNN | {{test type}} | {{condition}} | {{command}} |

### BDD scenarios (acceptance / integration level)

<!-- Source: quality-gates/bdd/F-NNN.md — scenarios for this story -->
<!-- If BDD gate not triggered: write "BDD gate not triggered for this initiative." -->

| SCN-ID | Scenario name | Type | TC mapping |
|---|---|---|---|
| SCN-NNN | {{scenario name}} | Happy path | TC-NNN |
| SCN-NNN | {{scenario name}} | Failure | TC-NNN |
| SCN-NNN | {{scenario name}} | Authorization | TC-NNN |
```

## Change 3 — Update Definition of done

Find the Definition of done section:

```markdown
## Definition of done

- [ ] Repository execution guard completed — repo structure confirmed, build clean, tests passing before changes
- [ ] All tasks in the Tasks section implemented
- [ ] All AC-NNN acceptance criteria pass as stated above
- [ ] All BDD scenarios listed above pass
- [ ] All AR-NNN rules respected — no forbidden patterns introduced
- [ ] All BR-NNN rules enforced in the implemented code
- [ ] Only files in "Candidate files to touch" modified (or revised list documented) — no out-of-scope changes
- [ ] All validation commands run and pass
- [ ] Tests added for each AC-NNN
```

Replace with:

```markdown
## Definition of done

- [ ] Repository execution guard completed — repo structure confirmed, build clean, tests passing before changes
- [ ] All tasks in the Tasks section implemented
- [ ] All C1 test cases (TC-NNN listed above) pass in CI — PR cannot be merged until these pass
- [ ] All C2 test cases (TC-NNN listed above) pass in staging before sprint review
- [ ] All unit test targets from tasks.md implemented and passing
- [ ] All BDD scenarios listed above pass (SCN-NNN — see quality-gates/bdd/F-NNN.md)
- [ ] All AC-NNN acceptance criteria pass as stated above
- [ ] All AR-NNN rules respected — no forbidden patterns introduced
- [ ] All BR-NNN rules enforced in the implemented code
- [ ] Only files in "Candidate files to touch" modified (or revised list documented) — no out-of-scope changes
- [ ] All validation commands run and pass
```

## Self-review after applying

Verify:
- [ ] Repository execution guard step 7 references the test plan
- [ ] "Stop and report" includes missing test plan as a stop condition
- [ ] `## BDD scenarios to make pass` is replaced by `## Tests to make pass`
- [ ] `## Tests to make pass` has C1 table, C2 table, and BDD scenarios table
- [ ] C1 and C2 tables have TC-NNN, test type, condition, how-to-run columns
- [ ] BDD table has SCN-NNN, scenario name, type, TC mapping columns
- [ ] Definition of done references C1 (blocks merge) and C2 (blocks sprint done)
- [ ] Definition of done references unit test targets from tasks.md
- [ ] No mention of "Tests added for each AC-NNN" (too vague — replaced by TC-NNN references)
