# Requirements Catalog

> Status: Draft
> Initiative: I111-NEXT11

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Source | input/brs.md; business-intake/business-intake-summary.md |
| Created at | 2026-06-18 |

## Functional Requirements

| ID | Title | Requirement | Priority | Status | Source |
|---|---|---|---|---|---|
| FR-001 | Online application intake | Applicants can submit a personal loan application with required fields (name, DOB, NI, employment, income, amount, purpose, term). | High | Open | input/brs.md |
| FR-002 | Field validation | System validates mandatory fields and prevents submission of incomplete applications. | High | Open | input/brs.md |
| FR-003 | Application reference number | System assigns a unique ARN to every application and displays it to the applicant. | High | Open | input/brs.md |
| FR-004 | Email confirmation | Send confirmation email with ARN within 2 minutes of submission. | Medium | Open | input/brs.md |
| FR-005 | Status lookup | Applicant can retrieve application status via ARN + DOB without registration. | Medium | Open | input/brs.md |
| FR-006 | AI pre-screening trigger | Trigger AI pre-screening within 60 seconds of submission. | High | Open | input/brs.md |
| FR-007 | Risk scoring output | AI produces a 0–1000 risk score and recommendation (AUTO_APPROVE / REFER_TO_UNDERWRITER / AUTO_DECLINE). | High | Open | input/brs.md |
| FR-009 | Experian integration | Integrate Experian CreditExpert API; complete within 30s; fallback route to refer if unavailable. | High | Open | input/brs.md |
| FR-010 | Auto-approve threshold | AUTO_APPROVE with amount ≤£10,000 proceeds to offer generation (subject to AML/KYC). | Medium | Open | input/brs.md |
| FR-011 | Auto-decline handling | AUTO_DECLINE notifications within 5 minutes and 30-day cooling-off. | Medium | Open | input/brs.md |
| FR-012 | AML screening | Perform AML screening against sanctions and PEP lists within 60s. | High | Open | input/brs.md |
| FR-013 | KYC verification | Perform KYC by verifying NI, name, DOB against HMRC API. | High | Open | input/brs.md |
| FR-014 | Compliance hold routing | Flag and route applications failing AML/KYC as COMPLIANCE_HOLD; notify applicant. | High | Open | input/brs.md |
| FR-015 | Underwriter queue | Present REFER_TO_UNDERWRITER and large approvals to underwriter queue within 2 minutes. | High | Open | input/brs.md |
| FR-016 | Underwriter dashboard | Dashboard shows applicant summary, score, credit summary, ratios, employment, AML/KYC. | High | Open | input/brs.md |
| FR-017 | Underwriter actions | Underwriter can approve, decline, or request info; actions recorded immutably. | High | Open | input/brs.md |
| FR-018 | Underwriter audit trail | Record underwriter actions with ID, timestamp, reason, and AI recommendation. | High | Open | input/brs.md |
| FR-019 | Escalation | Unactioned applications escalate after 4 business hours. | Medium | Open | input/brs.md |
| FR-020 | Offer generation | Generate loan offer document with terms for every approved application. | High | Open | input/brs.md |
| FR-021 | Offer delivery | Present offer via portal and email; valid 14 days. | Medium | Open | input/brs.md |
| FR-022 | E-signature acceptance | Accept offers via DocuSign with timestamp and IP logging. | High | Open | input/brs.md |
| FR-023 | Cooling-off reminders | Send reminders at day 7 and day 13 of cooling-off period. | Low | Open | input/brs.md |
| FR-024 | Disbursement trigger | Trigger disbursement to core banking (Temenos T24) after acceptance and cooling-off. | High | Open | input/brs.md |
| FR-025 | Disbursement details | Include account, sort code, amount, reference, value date in disbursement. | High | Open | input/brs.md |
| FR-026 | Disbursement confirmation | Update status to DISBURSED upon confirmation; retry once if not received within 2 minutes. | High | Open | input/brs.md |
| FR-027 | Post-disbursement notification | Notify applicant via email and portal of disbursement and value date. | Medium | Open | input/brs.md |
| FR-028 | Immutable audit log | Maintain immutable audit log of every state transition with snapshots. | High | Open | input/brs.md |
| FR-029 | Admin dashboards | Admin dashboard with volumes, averages, distributions, and rates refreshed every 5 minutes. | Medium | Open | input/brs.md |
| FR-030 | Observability events | Emit structured events for key lifecycle events including ARN and actor. | High | Open | input/brs.md |

## Non-Functional Requirements

| ID | Requirement | Target | Priority | Status | Source |
|---|---|---|---|---|---|
| NFR-001 | Form load time | ≤2s | High | Open | input/brs.md |
| NFR-002 | AI scoring latency | ≤90s end-to-end | High | Open | input/brs.md |
| NFR-003 | Concurrency | 500 concurrent submissions | Medium | Open | input/brs.md |
| NFR-004 | Encryption | AES-256 at rest; TLS1.3 in transit | High | Open | input/brs.md |
| NFR-005 | Audit log tamper-evidence | Write-once, tamper-evident store | High | Open | input/brs.md |
| NFR-006 | Availability | 99.9% business-hours uptime | High | Open | input/brs.md |
| NFR-007 | Circuit breakers | All external API integrations implement circuit breakers | High | Open | input/brs.md |

## Constraints

| ID | Constraint | Source | Impact |
|---|---|---|---|
| C-001 | Regulatory compliance (FCA Consumer Duty, GDPR) | input/brs.md | Must design for auditability and UK data residency |
| C-002 | Use Experian, DocuSign, Temenos T24 | input/brs.md | Requires contract and connector work before implementation |

## Notes

- This file was generated from `input/brs.md` and `business-intake/business-intake-summary.md`. Verify numbering continuity if additional FRs are added.
