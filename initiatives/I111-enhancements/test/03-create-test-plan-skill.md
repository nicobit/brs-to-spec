# Enhancement Prompt 03 — Create Test Plan Per Story Skill

## What this prompt does

Creates two new files:
1. **New skill**: `.brs2spec/skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md`
2. **New template**: `.brs2spec/templates/openspec-handoff/test-plan.md`

And adds the skill entry to `.brs2spec/module-index.md` (handled in prompt 08).

---

## File 1 — New skill: `create-test-plan-per-story.md`

Create the file at:
```
.brs2spec/skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md
```

### Full content to write

```markdown
# Prompt — Create Test Plan Per Story

## Role

You are a senior QA analyst conducting a three-amigos session to define the test contract
for each confirmed user story. You work alongside the product owner and developer to specify
what will be tested, at what level, and with what priority — before implementation starts.

## Context

This skill runs at stage 9f, immediately after BDD scenarios are authored (stage 9b).
Together with BDD, it completes the three-amigos output: BDD defines the *what* (observable
behaviors); the test plan defines the *how* (test types, test cases, risk classification).

A test plan is not code and not a test script. It is a structured commitment about:
- Which test types apply to this story (unit, integration, API, UI, security, performance)
- What specific test cases (TC-NNN) must be written and what each one verifies
- The criticality (C1–C4) of each test case, derived from business risk
- The minimum passing bar for the story to be marked Done

**One test plan per user story.** Output is a folder of test plan files — one per F-XXX.X story.

## Inputs

Read all of the following before writing a single test plan:

- `planning/delivery-structure/` — full list of confirmed stories with F-XXX.X IDs, AC-NNN, FR-NNN, BR-NNN links
- `quality-gates/bdd/` — all F-NNN.md files and acceptance-checklist.md; derive which SCN-NNN scenarios cover each story
- `input/brs.md` or `input/brs/*.md` — functional requirements (FR-NNN), NFRs (NFR-NNN), and acceptance criteria (AC-NNN); read NFRs for performance, security, and compliance test cases
- `business-intake/business-rules.md` — BR-NNN rules; rules with financial, compliance, or data integrity implications are C1 risk signals
- `architecture/architecture-rules.md` — AR-NNN constraints; rules about auth, encryption, data residency, or forbidden patterns generate security test cases
- `quality-gates/security-review.md` — if exists: security findings that produce C1 test cases
- `engineering-readiness/initiative-context.md` — technology stack; determines which test frameworks and levels are available
- `quality-gates/api-contract.md` — if exists: endpoint contracts that generate API test cases

## Output path

```text
quality-gates/test-plans/
  F-XXX.X-test-plan.md    ← one file per confirmed story (e.g. F-001.1-test-plan.md)
```

**Overwrite completely if a test plan already exists for a story — do not append.**

## TC-NNN ID sequencing

TC-NNN IDs are sequential across the entire initiative, not per story.
Before writing the first test plan:
1. List all F-XXX.X stories from `planning/delivery-structure/` in order
2. Assign a TC range to each story (e.g. F-001.1 gets TC-001–TC-010, F-001.2 gets TC-011–TC-020)
3. Record the ranges in `quality-gates/test-plans/test-plan-index.md` (create this file last)
4. Use only the assigned range when writing that story's test plan

## Risk classification model

Assign an overall story risk tier (C1–C4) and a per-test-case criticality using the two-axis model:

### Two axes

| Axis | What it measures | Signals |
|---|---|---|
| **Business impact** | Consequence if this story fails in production | Data loss, financial error, compliance breach, user-visible failure, regulatory audit trigger |
| **Test confidence gap** | How well existing automated coverage already catches failures in this area | None = new module / no existing tests; Partial = some related tests exist; Good = well-covered module with regression suite |

### Four tiers

| Tier | Label | Business impact | Confidence gap | Gate implication |
|---|---|---|---|---|
| C1 | Critical | High | None or Partial | **Blocks merge** — must pass in CI before PR is approved |
| C2 | High | High | Good — OR — Medium impact + None | **Blocks sprint done** — must pass in staging before sprint review |
| C3 | Medium | Moderate | Any | Should pass — deferral requires documented accepted risk |
| C4 | Low | Low / cosmetic | Any | Advisory — tracked but not gating |

### Risk signals that always trigger C1

Regardless of confidence gap, assign C1 if any of the following apply:
- Story processes financial transactions, loan amounts, or payment data (linked to FR-NNN of this type)
- Story writes to an immutable audit log required by a BR-NNN compliance rule
- Story enforces authentication or authorization boundaries (AR-NNN or SEC-NNN)
- Story includes data that must be encrypted at rest or in transit (AR-NNN encryption rule)
- Story exports or migrates PII data
- Story is on the critical path — blocking 3 or more downstream stories

## Test types

For each story, assess which test types apply and why. Do not include a test type with zero
test cases — only include types where at least one TC-NNN case exists.

| Test type | When it applies | What it verifies |
|---|---|---|
| **Unit** | Every story that introduces a new class, function, or business rule evaluation | Individual function correctness: null inputs, boundary values, business rule branches (BR-NNN conditions), error paths |
| **Integration** | Stories with database writes, service calls, event publishing, or multi-step flows | End-to-end story flow, data persistence, event emission, error propagation across layers |
| **API** | Stories that create or modify API endpoints | HTTP contract: status codes, request/response schema, auth enforcement, error codes from api-contract.md |
| **UI** | Stories with user-facing forms, lists, or interactions | Form validation messages, empty states, loading states, error display, accessibility |
| **Security** | Stories with auth, RBAC, PII, encryption, or SEC-NNN findings | Unauthorized access rejection, boundary enforcement, PII not leaked in responses |
| **Performance** | Stories with NFR-NNN performance thresholds | Response time at stated load, throughput, degradation behavior |
| **Audit/Compliance** | Stories that write to audit logs or trigger compliance rules | Log completeness, immutability, required fields (actor, timestamp, action, resource, outcome) |

## Authoring rules

### What a test case IS

A test case (TC-NNN) is:
- A name (descriptive, one line)
- A test type (from the table above)
- The specific condition being tested (the "what if" — one condition per TC)
- The expected outcome (observable, verifiable)
- The AC-NNN or NFR-NNN it validates
- The SCN-NNN BDD scenario it maps to (or "—" if it is a unit test with no corresponding Gherkin)
- A criticality tier (C1–C4) with a one-line rationale

### What a test case is NOT

- A test case is not an implementation step ("call the service method")
- A test case is not a copy of the BDD Gherkin — it is a definition of what to test, not the test script
- A test case is not vague ("test the happy path") — it must name the specific condition

### Unit test cases — how to derive them

Unit tests are not derived from BDD (which operates at integration/acceptance level).
Derive unit test cases from:
1. **Business rule branches**: for each BR-NNN rule that applies to this story, there must be at least one unit test for the "rule passes" branch and one for the "rule fails" branch
2. **Boundary values**: for each numeric input with a constraint (min/max, threshold), test the boundary value and one above/below
3. **Null and missing inputs**: for each required field, test what happens when it is missing or null
4. **Error propagation**: for each dependency call (DB, service, queue), test what happens when it throws
5. **State transitions**: for each state a domain entity can be in, test the valid and invalid transition

Minimum: 2 unit test cases per story (one business rule happy path + one boundary/null/error). Stories with multiple BR-NNN rules: one pair per rule.

### Integration test cases

Integration test cases align with BDD scenarios at the story flow level. For each happy-path SCN-NNN:
- One integration test case that drives the full flow from API entry to data persistence
For each failure SCN-NNN:
- One integration test case that validates the error response and the absence of side effects (no partial write, no orphan record)

### Security test cases

Security test cases are required whenever:
- AR-NNN contains an auth or access control rule
- SEC-NNN findings exist in security-review.md
- The story handles PII (from data-contract.md)

Minimum: one "unauthorized attempt" test case per auth boundary in the story.

## Test data requirements

For each test plan, include a test data section listing:
- What input data is needed (fixture, generated, seeded)
- Boundary values that must exist in test fixtures
- PII-safe substitutes for real data

## Output format — test-plan.md template

See `.brs2spec/templates/openspec-handoff/test-plan.md` for the required output structure.
Read that template before writing any test plan.

## Quality bar

A good test plan must:

- Have at least one TC-NNN per AC-NNN in the story — every acceptance criterion has at least one test case
- Have at least one unit test case per BR-NNN rule that applies to this story
- Have security test cases whenever AR-NNN or SEC-NNN rules apply
- Have API test cases for every endpoint the story creates or modifies
- Assign C1 to every test case that, if failing, would allow corrupted data, unauthorized access, or compliance breach
- Include a Minimum passing bar section that states which TC-NNN are C1 (blocks merge) and C2 (blocks sprint done)

## Anti-patterns to avoid

- Do not include test types with zero test cases — omit sections that do not apply
- Do not write vague test case descriptions ("test the form") — name the specific condition
- Do not assign all test cases the same criticality — read the business and architecture rules to differentiate
- Do not copy BDD Gherkin into the test plan — reference SCN-NNN, do not duplicate
- Do not invent AC-NNN or FR-NNN not present in the delivery structure or BRS
- Do not skip unit tests because "they will be written during implementation" — the test plan commits to their scope before implementation
- Do not write a test plan without reading BR-NNN rules — business rule branches are the primary source of unit test cases
- Do not assign C4 to a test case that covers an auth boundary or financial calculation — those are always C1

## Stop conditions

- If `planning/delivery-structure/` has no confirmed stories (F-XXX.X IDs), stop — test plans require confirmed stories
- If `quality-gates/bdd/` does not exist or has no Gherkin blocks, run stage 9b first — test plans depend on SCN-NNN IDs for integration test mapping
- If a story has no BR-NNN links and no AC-NNN, flag it as requiring story enrichment before a test plan can be written

## Self-review checklist

Before finalizing each test plan, verify:

- [ ] Every AC-NNN in the delivery structure for this story has at least one TC-NNN
- [ ] Every BR-NNN rule linked to this story has at least one unit test case (happy branch + fail branch)
- [ ] Overall story risk tier is stated with rationale
- [ ] Every TC-NNN has: name, test type, condition, expected outcome, AC/NFR reference, SCN reference or "—", criticality tier with rationale
- [ ] C1 test cases exist wherever the story touches financial data, auth boundaries, audit logs, or PII
- [ ] Security test cases exist wherever AR-NNN or SEC-NNN rules apply
- [ ] API test cases exist for every endpoint the story creates or modifies
- [ ] Minimum passing bar states which specific TC-NNN are C1 (blocks merge) and C2 (blocks sprint done)
- [ ] Test data requirements section is complete
- [ ] No test case has a vague description — each names a specific condition
- [ ] TC-NNN IDs are within the assigned range for this story (no overlap with other stories)
- [ ] test-plan-index.md has been updated with this story's TC range
```

---

## File 2 — New template: `test-plan.md`

Create the file at:
```
.brs2spec/templates/openspec-handoff/test-plan.md
```

### Full content to write

```markdown
# Test Plan — {{F-XXX.X}}: {{User Story Name}}

> Defines what will be tested for this story, at what level, and with what priority.
> Produced during the three-amigos session (stage 9f) — before implementation starts.
> Single source of truth for test case definitions. Referenced by tasks.md and coding-prompt.md.
>
> **Repository scope (omit this line if flat handoff structure):** This test plan covers the `{{repo-name}}` repository slice of story {{F-XXX.X}}.

## Risk classification

| Risk factor | Assessment | Rationale |
|---|---|---|
| Business impact | High / Medium / Low | {{e.g. processes loan application — financial data integrity}} |
| Failure visibility | High / Medium / Low | {{e.g. user-facing rejection screen vs internal audit log}} |
| Existing coverage | None / Partial / Good | {{e.g. no test suite in this module yet}} |
| Regulatory / compliance | Yes / No | {{e.g. BR-007 requires audit trail for all decisions}} |
| Auth / security boundary | Yes / No | {{e.g. AR-003 enforces role separation}} |
| **Overall story risk** | **C1 / C2 / C3 / C4** | {{one sentence — the dominant risk driver}} |

**Risk tiers:**
- **C1 Critical** — blocks merge: must pass in CI before PR is approved
- **C2 High** — blocks sprint done: must pass in staging before sprint review
- **C3 Medium** — should pass: deferral requires documented accepted risk
- **C4 Low** — advisory: tracked but not gating

---

## Test cases

<!-- TC-NNN IDs are sequential across the initiative. See quality-gates/test-plans/test-plan-index.md for assigned range. -->

| TC-ID | Test type | Condition | Expected outcome | AC / NFR | BDD scenario | Criticality | Gating |
|---|---|---|---|---|---|---|---|
| TC-NNN | Unit | {{specific condition — e.g. "LoanEligibilityService.evaluate() receives null income"}} | {{expected outcome — e.g. "throws ArgumentNullException"}} | AC-NNN | — | C1 | Blocks merge |
| TC-NNN | Unit | {{condition}} | {{outcome}} | AC-NNN | — | C2 | Blocks sprint done |
| TC-NNN | Integration | {{condition — e.g. "valid application submitted by authenticated ACT-001"}} | {{outcome — e.g. "application record created, event published, 201 returned"}} | AC-NNN | SCN-NNN | C1 | Blocks merge |
| TC-NNN | Integration | {{condition}} | {{outcome}} | AC-NNN | SCN-NNN | C1 | Blocks merge |
| TC-NNN | API | {{condition — e.g. "POST /submissions with missing required field"}} | {{outcome — e.g. "returns 400 with field-level error details"}} | AC-NNN | SCN-NNN | C2 | Blocks sprint done |
| TC-NNN | Security | {{condition — e.g. "unauthenticated request to POST /submissions"}} | {{outcome — e.g. "returns 401, no application record created"}} | AR-NNN | SCN-NNN | C1 | Blocks merge |
| TC-NNN | Performance | {{condition — e.g. "100 concurrent submissions"}} | {{outcome — e.g. "P95 response ≤ 500ms"}} | NFR-NNN | SCN-NNN | C2 | Blocks sprint done |

<!-- Remove test type sections (rows) that do not apply to this story. -->
<!-- Do not include a test type with zero rows. -->

---

## Minimum passing bar

To mark story {{F-XXX.X}} **Done**:

### Blocks merge (C1 — must pass in CI)
<!-- List all C1 TC-NNN IDs -->
- TC-NNN: {{name}}
- TC-NNN: {{name}}

### Blocks sprint done (C2 — must pass in staging)
<!-- List all C2 TC-NNN IDs -->
- TC-NNN: {{name}}
- TC-NNN: {{name}}

### Advisory (C3/C4 — tracked but not gating)
<!-- List C3/C4 TC-NNN IDs with one-line accepted-risk note if deferred -->
- TC-NNN: {{name}} — {{accepted risk note if deferred}}

---

## Test data requirements

| Data needed | Source | Notes |
|---|---|---|
| {{e.g. valid applicant profile}} | {{fixture / generated / seeded}} | {{e.g. income > 0, DTI < 0.43}} |
| {{e.g. boundary DTI value (0.43)}} | {{generated}} | {{pass threshold}} |
| {{e.g. boundary DTI value (0.44)}} | {{generated}} | {{fail threshold}} |
| {{e.g. PII-safe applicant}} | {{fixture}} | {{use anonymised data — no real names/SSN}} |

---

## Coverage traceability

| AC-NNN | Test cases covering it | BDD scenarios covering it |
|---|---|---|
| AC-NNN | TC-NNN, TC-NNN | SCN-NNN, SCN-NNN |
| AC-NNN | TC-NNN | SCN-NNN |

---

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| BDD scenarios | `quality-gates/bdd/F-NNN.md` | Full Gherkin for SCN-NNN referenced above |
| Business rules | `business-intake/business-rules.md` | BR-NNN rules that drive unit test branches |
| Architecture rules | `architecture/architecture-rules.md` | AR-NNN constraints that drive security test cases |
| API contract | `quality-gates/api-contract.md` | Endpoint schemas for API test cases |
| Security review | `quality-gates/security-review.md` | SEC-NNN findings that produce C1 test cases |
```

---

## Self-review after applying

Verify:
- [ ] `create-test-plan-per-story.md` exists in `skills/4-engineering-readiness/quality-gates/`
- [ ] `test-plan.md` template exists in `templates/openspec-handoff/`
- [ ] Risk classification model (C1–C4) is clearly defined with gate implications
- [ ] Unit test derivation rules cover BR-NNN branches, boundary values, null inputs, error propagation
- [ ] Self-review checklist in skill has ≥10 items
- [ ] Template has TC-NNN ID, test type, condition, expected outcome, AC/NFR ref, SCN ref, criticality, gating columns
