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

<!-- Remove rows for test types that do not apply to this story. -->
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
