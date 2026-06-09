# Prompt — Create BDD Scenarios

## Role

You are a senior QA analyst creating the executable acceptance specification for this initiative.

## Context

This gate is only run when `engineering-readiness/readiness-check.md` marks it as Triggered = Yes and Required = Yes.

BDD scenarios are the bridge between business acceptance criteria and implementation verification. They are authored at **user story level** — one group of scenarios per story — and referenced by story ID in the OpenSpec handoff so developers know exactly which scenarios their implementation must make pass.

## Purpose

Produce business-readable Gherkin scenarios covering happy path, failure/negative, boundary, and authorization flows for every in-scope user story. The output must be complete enough for a developer or coding agent to implement against without needing to re-read the BRS.

## Inputs

Read all of the following before writing a single scenario:

- `planning/delivery-structure.md` — the list of user stories in scope; derive one scenario group per story
- `input/brs.md` or `input/brs/*.md` — acceptance criteria (AC-NNN IDs) and functional requirements (FR-NNN)
- `engineering-readiness/readiness-check.md` — which stories triggered this gate and why
- `business-intake/business-intake-summary.md` — business rules and personas
- `architecture/architecture-rules.md` — constraints that affect testable behavior (e.g. auth model, data residency)
- `input/architecture.md` — integration points and system boundaries that affect scenario setup

## Output path

```text
quality-gates/bdd-scenarios.md
```

## Template

Use:

```text
templates/quality-gates/bdd-scenarios.md
```

Preserve the template structure. Group all scenarios under a `### F-XXX.X — Story name` heading. Do not mix scenarios from different stories in the same block.

## Authoring rules

**Coverage minimum per story:**
- At least one happy-path scenario (the primary success flow)
- At least one failure/negative scenario (invalid input, system error, or rejection)
- Authorization scenario where the story has role-based access control
- Boundary scenario where the AC implies a limit (character count, date range, amount threshold, etc.)

**Scenario ID format:** `SCN-NNN` — sequential across the whole artifact, not per story.

**Each scenario must reference:**
- `Story ID` — the F-XXX.X it belongs to
- `Requirement ID` — the FR-NNN from the BRS
- `AC ID` — the specific acceptance criterion it validates (AC-NNN)

**Gherkin rules:**
- Use `Given` for pre-conditions (system state, user role, existing data)
- Use `When` for the single action the user or system takes
- Use `Then` for the observable outcome (what the user sees or what the system records)
- Use `And` to extend any of the above — not to chain multiple actions
- Keep each scenario atomic — one behavior per block
- Do not embed implementation detail (SQL queries, class names, endpoint paths)

**Coverage summary table:** fill in one row per scenario before writing the scenario blocks. This gives reviewers a map before reading the full Gherkin.

## Quality bar

A good output must:

- cover every user story that is listed as in-scope in `planning/delivery-structure.md`
- have at least a happy-path and a failure scenario per story — a story with only a happy-path scenario is incomplete
- reference AC-NNN IDs so scenarios are traceable to the BRS
- reference Story IDs so the OpenSpec handoff can link directly to relevant scenarios
- use plain business language in `Given/When/Then` — not technical implementation steps
- make authorization boundaries explicit where the architecture rules define role separation
- record open questions where the BRS is ambiguous — do not invent AC

## Anti-patterns to avoid

Do not produce outputs that:

- group scenarios by requirement ID instead of by user story — story grouping is mandatory
- write only happy-path scenarios and skip failure paths
- write `Then` clauses that describe implementation ("the database saves a record") instead of observable behavior ("the user sees a confirmation message")
- leave Story ID or AC ID blank in the coverage summary
- chain multiple user actions in a single `When` step
- invent AC not present in the BRS or intake — record as an open question instead
- create scenarios for stories that are explicitly out of scope in this deliverable

## Stop conditions

- If this gate was not triggered in the readiness check, stop immediately and state that it must not be run.
- If `planning/delivery-structure.md` does not exist or has no user stories, stop — scenarios cannot be authored without a story list.
- If AC-NNN IDs are missing from the BRS for a story, create the scenario with a placeholder and add a row to the open questions table.
- Do not invent evidence or acceptance criteria.

## Self-review checklist

Before finalizing, verify:

- [ ] Gate was triggered in the readiness check.
- [ ] Every in-scope user story from `planning/delivery-structure.md` appears in the coverage summary.
- [ ] Every story has at least one happy-path and one failure/negative scenario.
- [ ] Every scenario has Story ID, Requirement ID, and AC ID filled in.
- [ ] Gherkin uses observable outcomes in `Then`, not implementation steps.
- [ ] Authorization and boundary scenarios are present where the AC implies them.
- [ ] Open questions table is complete — no ambiguous AC was silently assumed.
- [ ] Coverage summary table matches the scenario blocks below it.
