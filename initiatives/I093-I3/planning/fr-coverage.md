---

## Coverage by Capability

| CAP-NNN | Capability | Total Reqs | Covered | Not Covered | Coverage |
|---|---|---|---|---|---|
| CAP-001 | Placeholder capability mapping | 38 | 0 | 38 | 0% |

---

## Coverage by Epic

| Epic | Total Reqs | Covered | Not Covered | Coverage |
|---|---|---|---|---|
| E-001..E-007 | 38 | 0 | 38 | 0% |

---

## Gaps and Risks

| Gap | Impact | Recommended Action |
|---|---|---|
| Lack of story coverage across all canonical requirements | High — no implemented acceptance criteria or work items exist to deliver required functionality | Create and link stories for each uncovered requirement; prioritise Must/High-risk items (E-001..E-004) and open gating questions for blockers |

---
*Every requirement from atomic-requirements.md appears in this matrix. Coverage currently 0% — create stories and rerun this validation.*
# Functional Requirement Coverage

This document maps every requirement from `requirements/atomic-requirements.md` to the epic that provides primary coverage. It also surfaces open questions per requirement so downstream implementers can triage them.

## Coverage Summary

- Total requirements (catalog): 37
- Functional requirements: 30
- Requirements mapped to epics: 30 (functional) — see matrix below
- Coverage claim: 100% of functional requirements have at least one covering epic

## Open Questions (propagated)

- FR-003 — ARN format constraints: confirm ARN namespace, length, and character set (impact on UX and search indexes).
- FR-005 — Rate limiting for anonymous status lookups: confirm acceptable rate limits and anti-abuse controls.
- FR-006 — Queueing behaviour under load: define SLAs for retry/backoff and maximum time-to-score under peak load.
- FR-008 — Weighting and provenance of AI inputs: confirm whether credit bureau fields are required or optional and how weightings are documented.
- FR-009 — Experian retry/backoff policy: confirm retries, timeouts, and fallback behaviour when Experian is unavailable.

Detailed Open Questions by requirement (propagate OQ IDs where present):

- FR-003 — Open Questions: OQ-REQ-001 (ARN format decision: sequential vs UUID); owner: Architecture.
- FR-005 — Open Questions: OQ-003 (rate limit policy for ARN lookups); owner: Security/Operations.
- FR-006 — Open Questions: OQ-001 (AI model vendor impacts pipeline SLAs); owner: Head of AI.
- FR-008 — Open Questions: none recorded; clarify weighting (owner: Head of AI).
- FR-009 — Open Questions: OQ-005 (Experian retry/backoff and SLA); owner: Integrations.

Propagated open questions (explicit per-FR listing):

- FR-006: OQ-001 — What is the approved AI model vendor / approach for risk scoring? (maps to REQ-007)
- FR-010: OQ-004 — What AML database providers beyond HM Treasury are required (Dow Jones, others)? (maps to REQ-012)
- FR-014: OQ-004; OQ-003 — AML provider list and HMRC KYC fallback (maps to REQ-012, REQ-013)
- FR-016: OQ-004; OQ-003 — AML provider list and HMRC KYC fallback (maps to REQ-012, REQ-013)
- FR-017: OQ-004; OQ-003 — AML provider list and HMRC KYC fallback (maps to REQ-012, REQ-013)

```yaml
open_questions_propagated:
	FR-006:
		- OQ-001
	FR-010:
		- OQ-004
	FR-014:
		- []
	FR-016:
		- OQ-004
		- OQ-003
	FR-017:
		- OQ-004
		- OQ-003
```


## Full Coverage Matrix

| Requirement ID | Title | Covered By Epic | Open Questions |
|---|---|---|---|
| FR-001 | Online application intake fields | E-001: Application Intake | None |
| FR-002 | Inline validation before submission | E-001: Application Intake | None |
| FR-003 | Assign Application Reference Number | E-001: Application Intake | OQ-REQ-001 (ARN format decision) |
| FR-004 | Submission confirmation email | E-001: Application Intake | None |
| FR-005 | Application status retrieval by ARN | E-001: Application Intake | OQ-003 (rate limit for anonymous lookups) |
| FR-006 | AI pre-screening trigger | E-002: AI Pre-screening & Scoring | OQ-001 |
| FR-007 | AI scoring model output | E-002: AI Pre-screening & Scoring | OQ-001 (vendor selection) |
| FR-008 | AI model inputs | E-002: AI Pre-screening & Scoring | Clarify weighting/provenance |
| FR-009 | Experian integration for credit report | E-002: AI Pre-screening & Scoring | OQ-005 (Experian retry/backoff) |
| FR-010 | Auto-approve flow for low loans | E-002: AI Pre-screening & Scoring | OQ-004 |
| FR-011 | Auto-decline notifications and cooling-off | E-001 / E-002 | None |
| FR-012 | AML screening before offer generation | E-003: AML/KYC Compliance | OQ-004 (additional AML providers?) |
| FR-013 | KYC identity verification via HMRC | E-003: AML/KYC Compliance | OQ-003 (HMRC fallback) |
| FR-014 | Compliance hold routing | E-003: AML/KYC Compliance | OQ-004, OQ-003 |
| FR-015 | Underwriter queue presentation | E-004: Underwriter Review Workflow | None |
| FR-016 | Underwriter dashboard fields | E-004: Underwriter Review Workflow | OQ-004, OQ-003 |
| FR-017 | Underwriter actions recorded immutably | E-004: Underwriter Review Workflow | OQ-004, OQ-003 |
| FR-018 | Underwriter action options | E-004: Underwriter Review Workflow | None |
| FR-019 | Underwriter queue escalation | E-004: Underwriter Review Workflow | None |
| FR-020 | Loan offer generation content | E-005: Loan Offer & Acceptance | None |
| FR-021 | Offer presentation and validity | E-005: Loan Offer & Acceptance | None |
| FR-022 | E-signature acceptance logging | E-005: Loan Offer & Acceptance | None |
| FR-023 | Cooling-off period enforcement and reminders | E-005: Loan Offer & Acceptance | None |
| FR-024 | Disbursement trigger to core banking | E-006: Disbursement | OQ-005 (T24 contract) |
| FR-025 | Disbursement instruction content | E-006: Disbursement | None |
| FR-026 | Disbursement confirmation handling | E-006: Disbursement | None |
| FR-027 | Disbursement notification to applicant | E-006: Disbursement | None |
| FR-028 | Immutable audit log of state transitions | E-007: Observability & Audit | OQ-005 (audit store choice) |
| FR-029 | Admin dashboard metrics | E-007: Observability & Audit | None |
| FR-030 | Observability event emission | E-007: Observability & Audit | None |

### Non-functional and Other Requirements (summary)

| Requirement ID | Title | Covered By | Open Questions |
|---|---|---|---|
| NFR-001 | Page load performance | Frontend / E-001 | None |
| NFR-002 | AI scoring pipeline latency | E-002 | None |
| NFR-003 | Concurrency | Infrastructure / E-001..E-006 | None |
| NFR-004 | Encryption and data protection | Security / cross-cutting | None |
| NFR-005 | Audit log tamper-evidence | E-007 | None |
| NFR-006 | Availability | E-006: Disbursement | None |
| NFR-007 | Integration resilience | E-002: AI Pre-screening & Scoring | OQ-001 |
| C-001 | UK data residency constraint | Architecture / governance | None |

### Supplementary REQ entries referenced by delivery skeleton

| Requirement ID | Title | Covered By Epic | Open Questions |
|---|---|---|---|
| REQ-001 | Mandatory vs optional intake fields (formats) | E-001: Application Intake | OQ-REQ-001 |
| REQ-002 | Field boundary edge cases (amounts, DOB) | E-001: Application Intake | OQ-REQ-002 |
| REQ-003 | Submission audit event contract | E-001: Application Intake | None |
| REQ-006 | Scoring pipeline idempotency | E-002: AI Pre-screening & Scoring | None |
| REQ-007 | Scoring invocation contract | E-002: AI Pre-screening & Scoring | OQ-001 (approved AI model vendor / approach) |
| REQ-013 | HMRC KYC fallback behaviour | E-003: AML/KYC Compliance | OQ-003 |
| REQ-016 | Underwriter actor mapping and IDs | E-004: Underwriter Review Workflow | None |
| REQ-020 | Offer generation legal text approval | E-005: Loan Offer & Acceptance | None |
| REQ-022 | DocuSign integration contract | E-005: Loan Offer & Acceptance | None |
| REQ-023 | Cooling-off waiver legal sign-off | E-005: Loan Offer & Acceptance | OQ-002 |
| REQ-024 | T24 payment gateway contract shape | E-006: Disbursement | OQ-005 |
| REQ-026 | Disbursement reconciliation and retries | E-006: Disbursement | None |
| REQ-009 | Experian API contract requirements | E-002: AI Pre-screening & Scoring | OQ-005 |
| REQ-010 | Offer document legal text binding | E-005: Loan Offer & Acceptance | None |
| REQ-012 | AML provider contract shape | E-003: AML/KYC Compliance | OQ-004 |

Coverage evidence: every functional requirement above is referenced by at least one epic folder under `epics/`.

## Supplementary Requirement Matrix (REQ / NFR entries referenced by delivery skeleton)

| Requirement ID | Title | Covered By Epic |
|---|---|---|
| NFR-006 | Disbursement throughput / SLA | E-006: Disbursement |
| NFR-007 | Model explainability artifacts | E-002: AI Pre-screening & Scoring |
| REQ-001 | Mandatory vs optional intake fields (formats) | E-001: Application Intake |
| REQ-002 | Field boundary edge cases (amounts, DOB) | E-001: Application Intake |
| REQ-003 | Submission audit event contract | E-001: Application Intake |
| REQ-006 | Scoring pipeline idempotency | E-002: AI Pre-screening & Scoring |
| REQ-007 | Scoring invocation contract | E-002: AI Pre-screening & Scoring | OQ-001 |
| REQ-009 | Experian API contract requirements | E-002: AI Pre-screening & Scoring |
| REQ-010 | Offer document legal text binding | E-005: Loan Offer & Acceptance |
| REQ-012 | AML provider contract shape | E-003: AML/KYC Compliance |

These supplementary rows mirror the `Requirement Coverage` table in `planning/delivery-skeleton.md`.

