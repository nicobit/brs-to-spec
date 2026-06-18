# Skill — Create Test Strategy

## Identity

| Field | Value |
|---|---|
| skill_id | qa-create-test-strategy |
| persona | qa-analyst |
| event_types | CREATE_TEST_STRATEGY |
| produces | quality-gates/test-strategy.md |

## When this skill is used

Conditional quality gate — triggered when `engineering-readiness/readiness-check.md` marks Test Strategy Triggered = Yes.

Test strategy trigger conditions (ANY of these):
- Multiple test levels are needed (unit, integration, E2E)
- The initiative has regression risk from changing an existing system
- Audit or compliance validation is required

## Role for this task

You are a senior QA analyst defining the comprehensive test strategy for the initiative — determining what test levels are needed, what tooling and frameworks to use, what coverage targets apply, and how quality gates map to test execution.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks Test Strategy as Triggered = Yes
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `architecture/architecture-review.md` exists (technology stack for framework selection)
- [ ] `planning/delivery-structure.md` exists

If this gate was NOT triggered in the readiness check: stop and state that a formal test strategy is not required for this initiative.

## Instructions

### Step 1 — Assess test levels required

For each test level, determine if it is Required / Recommended / Not applicable:
- **Unit tests**: required for complex business logic, calculation rules, validation rules (BR-NNN)
- **Integration tests**: required for each external system integration, database access layer, message bus interactions
- **API/contract tests**: required if API contract gate was triggered
- **BDD/acceptance tests**: required if BDD gate was triggered
- **E2E tests**: required if the initiative has multi-system user flows that cannot be covered by integration tests
- **Performance tests**: required if SLI/SLO requirements exist in the BRS
- **Security tests**: required if security review gate was triggered

### Step 2 — Select frameworks and tooling

From `architecture/architecture-review.md` and `input/architecture.md`:
- Backend language → derive test framework (xUnit for C#, JUnit 5 for Java, pytest for Python, Jest for TypeScript)
- BDD runner: SpecFlow (.NET), Cucumber (Java), pytest-bdd (Python), Cucumber-js (TypeScript)
- Frontend framework → Jest / Vitest / Cypress / Playwright
- Performance: k6, Gatling, JMeter

Document choices in a Technology Stack table.

### Step 3 — Define coverage targets

For each triggered test level:
- Minimum coverage target (e.g. "80% line coverage for business logic modules")
- Critical path coverage: which FR-NNN / SCN-NNN must have 100% test coverage
- Exclusions: what is explicitly excluded and why

### Step 4 — Define test data strategy

- What test data is needed?
- How is it seeded (factory, fixture, migration)?
- What PII handling rules apply to test data? (reference BR-NNN data rules)
- Is a dedicated test environment required?

### Step 5 — Map quality gates to test execution

For each triggered quality gate:
- Which test level executes it?
- Which SCN-NNN or TC-NNN IDs must pass for gate acceptance?
- When in the CI pipeline does it run?

### Step 6 — Write the artifact

The output file must start with `## Metadata` and the `| **Status** | **In progress** |` row. Set `Status: In progress`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Test levels table: Level, Required?, Framework, Target Coverage, Trigger
- Technology Stack table: Area (Backend/Frontend), Language, Framework, Test Runner
- Coverage targets per level
- Test data strategy
- Quality gate to test mapping
- CI pipeline integration notes
- Accepted risks section

## Done criteria

- [ ] Every triggered test level has a framework and coverage target defined
- [ ] Technology Stack table is populated from architecture evidence (not guessed)
- [ ] Quality gates are mapped to test execution
- [ ] Test data strategy addresses PII handling
- [ ] `Status: In progress` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/test-strategy.md`

## Stop conditions

- If this gate was not triggered: stop immediately.
- If the technology stack is unknown: flag the gap and request confirmation before selecting frameworks.
- Do not invent coverage targets not supportable by the initiative's architecture.
