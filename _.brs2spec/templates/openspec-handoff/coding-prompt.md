---
Story: {{F-XXX.X}} — {{story name}}
Generated: {{YYYY-MM-DD}}
---

# Coding Prompt — {{F-XXX.X}} {{story name}}

## Repository execution guard

> **Run this check BEFORE modifying any file.**
> This package was generated from architecture and design artifacts — it has not seen the actual repository.
> The file paths, module names, and commands below are candidates. Verify before implementing.

Before touching any code:

1. **Inspect repository structure** — confirm the actual folder layout matches the module map in `specs/by-repository/{{alias}}/repo-context.md` if it exists, or in `input/repositories/{{alias}}.md` directly.
2. **Confirm candidate files** — check that each file listed in "Candidate files to touch" exists (for modify/delete) or that its parent folder exists (for create).
3. **Run build command** — confirm the unmodified codebase builds cleanly before making any change.
4. **Run test command** — confirm existing tests pass before making any change.
5. **Verify exclusions** — confirm that paths listed in "What you must NOT do" are still present and still excluded.
6. **Check open questions** — if this story has open questions in `story.md`, confirm all blocking questions are resolved before implementing.
7. **Check test plan** — read `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md`. Note all C1 test cases (blocks merge) — you must make these pass before the PR is submitted. Note C2 test cases (blocks sprint done) — make these pass before sprint review.

**Stop and report to the human if:**
- The actual folder structure does not match the module map — implement against wrong structure produces wrong results.
- The build fails on the unmodified codebase — there may be a pre-existing issue that must be resolved first.
- A file listed for modification does not exist — the design assumption may be wrong.
- A validation command cannot be run — note why and ask for the correct command before proceeding.
- An open question in this story is still unresolved and blocking.
- The test plan file `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md` does not exist — a test plan is required before implementation starts.

After completing the guard: proceed with implementation in the order specified in "Tasks".

## Goal

{{One sentence from the "so that" clause of the user story. This is the agent's objective.}}

## Business rules that constrain this story

<!-- Source: business-intake/business-rules.md — list only rules whose "impacted features/stories" includes this story's F-XXX.X -->
<!-- If no rules apply: write "Business rules: none apply — [reason]" and delete the table -->

| Rule | Text | How to enforce |
|---|---|---|
| BR-NNN | {{rule text}} | {{enforcement instruction — e.g. "reject request with 422 if condition fails"}} |

## Architecture rules that constrain this story

<!-- Source: architecture/architecture-rules.md — list only rules relevant to this story's scope -->

| Rule | Text | Applies to |
|---|---|---|
| AR-NNN | {{rule text}} | {{scope within this story}} |

## Acceptance criteria (testable)

<!-- Source: story.md AC table — copy verbatim; restate vague AC as an observable, verifiable outcome -->

| AC | Verifiable statement |
|---|---|
| AC-NNN | {{testable outcome — e.g. "POST /endpoint returns 201 with { id } when all required fields are valid"}} |

## Tests to make pass

<!-- Source: quality-gates/test-plans/{{F-XXX.X}}-test-plan.md (C1 and C2 rows) -->
<!-- Full test plan: quality-gates/test-plans/{{F-XXX.X}}-test-plan.md -->
<!-- Full BDD scenarios: quality-gates/bdd/F-NNN.md -->

### C1 — Must pass before merge

<!-- Copy C1 rows from test-plan.md. These block the PR from being merged. -->

| TC-ID | Test type | Condition | How to run |
|---|---|---|---|
| TC-NNN | {{Unit / Integration / Security}} | {{condition}} | {{e.g. pytest tests/test_loan.py::test_null_income}} |

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

## Tasks

<!-- Copy from tasks.md verbatim — do not summarize or change task scope -->

{{tasks copied verbatim from tasks.md}}

## Candidate files to touch

<!-- Source: design.md "What this story touches" + repo descriptor module map (if available) -->
<!-- These are CANDIDATES derived from architecture and design — not confirmed facts. -->
<!-- Before editing: verify the file exists and the path is correct in the actual repository. -->
<!-- If actual structure differs: revise this list and note the change before proceeding. -->
<!-- Change type: create | modify | delete -->

| File path | Change type | Reason |
|---|---|---|
| {{src/path/to/file}} | create / modify / delete | {{one-line reason — e.g. "new endpoint for this story"}} |

## Validation commands

<!-- Source: input/codebase-context.md validation-commands section if it exists -->
<!-- If codebase-context.md does not exist: derive from initiative technology stack in initiative-context.md -->
<!-- Run these commands after implementation. If they fail, fix before declaring done. -->

```bash
{{command 1 — e.g. dotnet build}}
{{command 2 — e.g. dotnet test --filter Category=Unit}}
{{command 3 — e.g. npm run lint}}
```

If a command cannot be run in the current environment, note why and report to the human.

## What you must NOT do

<!-- Derive from AR-NNN forbidden patterns and security-review constraints for this story — at least one item required -->

- {{forbidden pattern}} ({{AR-NNN or SEC-NNN}})

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
