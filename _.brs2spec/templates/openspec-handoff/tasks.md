# Tasks — {{F-XXX.X}}: {{User Story Name}}

> Implementation checklist for `/opsx:apply`.
> Scoped to this user story only. Tasks are ordered within this story — complete each before starting the next.
> See `specs/dependency-graph.md` for the order between stories.
>
> **Repository scope (omit this line if flat handoff structure):** These tasks cover the `{{repo-name}}` repository slice of story {{F-XXX.X}} only. Check `dependency-graph.md` § Cross-repo dependencies to see if this repo must wait for a sibling repo to deliver first.

## Implementation tasks

<!--
One task per independently reviewable unit of work (one PR boundary).
- [ ] OS-{{F-XXX.X}}-NNN: <verb> <what> — <one-line outcome>
  - Requirement: FR-NNN / NFR-NNN
  - Acceptance: <AC ID or location>
  - Architecture constraint: AR-XXX — <rule summary>  (omit if none)
  - Data: <tables created or modified>  (omit if none)
  - API: <endpoints created or modified>  (omit if none)
  - Events to emit: <signal names from design.md#observability>  (omit if none)
  - Evidence expected: <what proves this task is done>
-->

- [ ] OS-{{F-XXX.X}}-001:
  - Requirement:
  - Acceptance:
  - Architecture constraint:
  - Data:
  - API:
  - Events to emit:
  - Evidence expected:

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
