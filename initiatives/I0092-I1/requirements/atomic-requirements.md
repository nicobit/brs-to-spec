# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I0092-I1 |
| Created at | 2026-06-22 |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | 18 |
| Functional | 13 |
| Non-functional | 3 |
| Data | 1 |
| Integration | 5 |
| Security | 3 |
| Operational | 2 |
| Reporting | 1 |
| Blocking questions | 3 |

---

## Requirement Catalogue

### REQ-001 — Application submission and ARN assignment

| Field | Value |
|---|---|
| ID | REQ-001 |
| Type | Functional |
| Source Section | Epic 1 — FR-001, FR-003 |
| Actor | Applicant, Applicant Portal |
| Business Object | Application, ARN |
| Trigger / Event | Applicant submits application form |
| Expected Outcome | Application stored and ARN returned to applicant |
| Dependencies | None |
| Ambiguities | None |
| Assumptions | Applicant provides required identity fields |
| Blocking Questions | None |

#### Requirement Text

The system shall accept an online personal loan application with mandatory fields (name, DOB, NI, employment status, income, amount, purpose, term), validate mandatory fields, persist the application, and immediately assign and display a unique Application Reference Number (ARN).

#### Notes

Derived from FR-001 and FR-003.

---

### REQ-002 — Inline validation before submission

| Field | Value |
|---|---|
| ID | REQ-002 |
| Type | Functional |
| Source Section | FR-002 |
| Actor | Applicant Portal |
| Business Object | Application form |
| Trigger / Event | Form completion / submit attempt |
| Expected Outcome | Inline validation prevents incomplete submission |
| Dependencies | REQ-001 |
| Ambiguities | Validation rules per field must be defined in acceptance criteria |
| Assumptions | Standard field validation rules apply |
| Blocking Questions | None |

#### Requirement Text

The system shall validate mandatory fields client-side and server-side and prevent submission of incomplete applications; validation errors shall be shown inline.

---

### REQ-003 — Submission confirmation email

| Field | Value |
|---|---|
| ID | REQ-003 |
| Type | Functional |
| Source Section | FR-004 |
| Actor | Notification Service |
| Business Object | Applicant email |
| Trigger / Event | Successful submission and ARN assigned |
| Expected Outcome | Email with ARN and estimated timeline sent within 2 minutes |
| Dependencies | REQ-001, Notification Service availability |
| Ambiguities | Email template approvals |
| Assumptions | SMTP/email provider operational |
| Blocking Questions | None |

#### Requirement Text

The system shall send an email confirmation to the applicant within 2 minutes of submission containing the ARN and estimated decision timeline.

---

### REQ-004 — Retrieve status by ARN

| Field | Value |
|---|---|
| ID | REQ-004 |
| Type | Functional |
| Source Section | FR-005 |
| Actor | Applicant |
| Business Object | Application status |
| Trigger / Event | Applicant requests status with ARN + DOB |
| Expected Outcome | System returns current status without requiring registration |
| Dependencies | REQ-001, identity lookup |
| Ambiguities | Rate-limiting and abuse prevention |
| Assumptions | ARN + DOB are sufficient for lookup |
| Blocking Questions | None |

#### Requirement Text

The system shall allow an applicant to retrieve application status using ARN and date of birth without account registration.

---

### REQ-005 — AI pre-screening and risk scoring

| Field | Value |
|---|---|
| ID | REQ-005 |
| Type | Functional |
| Source Section | Epic 2 — FR-006, FR-007 |
| Actor | AI Scoring Service |
| Business Object | Risk score, recommendation |
| Trigger / Event | Application submission (or within 60s) |
| Expected Outcome | Produce risk score (0–1000) and recommendation AUTO_APPROVE/REFER_TO_UNDERWRITER/AUTO_DECLINE |
| Dependencies | Experian integration (REQ-006) |
| Ambiguities | Model vendor and explainability artifacts (OQ-001) |
| Assumptions | Scoring completes within 60s under normal conditions |
| Blocking Questions | OQ-001 |

#### Requirement Text

The system shall trigger an AI pre-screening assessment within 60 seconds producing a risk score (0–1000) and categorical recommendation (AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE). The scoring service must retain explainability evidence for each score.

---

### REQ-006 — Experian credit bureau integration

| Field | Value |
|---|---|
| ID | REQ-006 |
| Type | Integration |
| Source Section | FR-009 |
| Actor | Loan Origination API, Experian API |
| Business Object | Credit report |
| Trigger / Event | Scoring pipeline requests credit data |
| Expected Outcome | Credit report returned within 30 seconds or fall back to REFER_TO_UNDERWRITER |
| Dependencies | External Experian availability |
| Ambiguities | Experian SLA details; caching policy |
| Assumptions | Existing enterprise contract in place |
| Blocking Questions | None |

#### Requirement Text

Integrate with Experian CreditExpert API to retrieve a credit report within 30 seconds; if unavailable, route the application to REFER_TO_UNDERWRITER.

---

### REQ-007 — Auto-approve rule for small loans

| Field | Value |
|---|---|
| ID | REQ-007 |
| Type | Functional |
| Source Section | FR-010 |
| Actor | Loan Origination API |
| Business Object | Offer generation |
| Trigger / Event | AI recommendation AUTO_APPROVE and amount ≤ £10,000 and AML/KYC cleared |
| Expected Outcome | Proceed to offer generation without underwriter review |
| Dependencies | REQ-005, REQ-012 (AML/KYC) |
| Ambiguities | Exact thresholds and condition list |
| Assumptions | AML/KYC clear in parallel |
| Blocking Questions | None |

#### Requirement Text

Applications recommended AUTO_APPROVE and loan amount ≤ £10,000 shall proceed to offer generation without underwriter review, provided AML/KYC checks pass.

---

### REQ-008 — Auto-decline and notification

| Field | Value |
|---|---|
| ID | REQ-008 |
| Type | Functional |
| Source Section | FR-011 |
| Actor | Notification Service |
| Business Object | Applicant notification |
| Trigger / Event | AI recommendation AUTO_DECLINE |
| Expected Outcome | Applicant notified within 5 minutes with decline category; 30-day cooling-off enforced |
| Dependencies | Notification Service |
| Ambiguities | Decline reason categories |
| Assumptions | Legal-approved message templates exist |
| Blocking Questions | None |

#### Requirement Text

The system shall notify applicants of AUTO_DECLINE decisions within 5 minutes with a decline reason category and enforce a 30-day cooling-off period before reapplication.

---

### REQ-009 — AML / KYC screening

| Field | Value |
|---|---|
| ID | REQ-009 |
| Type | Security/Functional |
| Source Section | Epic 3 — FR-012, FR-013, FR-014 |
| Actor | Compliance Service |
| Business Object | AML/KYC status |
| Trigger / Event | Before offer generation |
| Expected Outcome | AML/KYC checks completed within 60s; failures flagged COMPLIANCE_HOLD and routed to compliance team |
| Dependencies | HM Treasury / HMRC integrations |
| Ambiguities | Fallback behaviour when HMRC unavailable (OQ-003) |
| Assumptions | Sanctions provider is HM Treasury only (per OQ-004) |
| Blocking Questions | OQ-003, OQ-004 |

#### Requirement Text

Perform AML screening against HM Treasury sanctions and KYC verification via HMRC before any offer generation; if either fails, mark application COMPLIANCE_HOLD and route to compliance team.

---

### REQ-010 — Underwriter queue and actions

| Field | Value |
|---|---|
| ID | REQ-010 |
| Type | Functional |
| Source Section | Epic 4 — FR-015..FR-019 |
| Actor | Underwriter, Underwriter Dashboard |
| Business Object | Underwriter actions, audit record |
| Trigger / Event | Application routed to underwriter (REF or manual) |
| Expected Outcome | Underwriter can approve/decline/request info; action recorded immutably with metadata |
| Dependencies | Audit log (REQ-013) |
| Ambiguities | Escalation timing policies |
| Assumptions | Underwriters authenticated via Azure AD |
| Blocking Questions | None |

#### Requirement Text

Present REFER_TO_UNDERWRITER and manual review cases to an underwriter queue within 2 minutes; allow approve/decline/request info actions and record each action immutably with underwriter ID, timestamp, reason, and presented AI recommendation.

---

### REQ-011 — Offer generation and digital acceptance

| Field | Value |
|---|---|
| ID | REQ-011 |
| Type | Functional |
| Source Section | Epic 5 — FR-020..FR-023 |
| Actor | Loan Origination API, Notification Service, Applicant Portal |
| Business Object | Loan offer, e-signature record |
| Trigger / Event | Application approved |
| Expected Outcome | Offer generated, presented to applicant, accepted via DocuSign, logged with timestamp and IP |
| Dependencies | DocuSign integration, AML/KYC clearance |
| Ambiguities | Cooling-off waiver policy (OQ-002) |
| Assumptions | DocuSign contract available |
| Blocking Questions | OQ-002 |

#### Requirement Text

Generate loan offer documents for approved applications, present via portal and email, and enable digital acceptance via DocuSign; acceptance must be logged with timestamp and IP address.

---

### REQ-012 — Disbursement trigger and confirmation

| Field | Value |
|---|---|
| ID | REQ-012 |
| Type | Functional/Integration |
| Source Section | Epic 6 — FR-024..FR-027 |
| Actor | Payment Gateway Adapter, Core Banking (T24) |
| Business Object | Disbursement instruction |
| Trigger / Event | Post-acceptance and cooling-off expiry |
| Expected Outcome | Send disbursement instruction to T24; mark DISBURSED on confirmation; retry once on timeout and alert operations if still failing |
| Dependencies | T24 integration (OQ-005) |
| Ambiguities | T24 API contract specifics |
| Assumptions | Internal payment gateway available |
| Blocking Questions | OQ-005 |

#### Requirement Text

Upon acceptance and cooling-off expiry, trigger disbursement to Temenos T24 via internal payment gateway and update application status to DISBURSED upon confirmation; retry once on timeout then alert operations.

---

### REQ-013 — Immutable audit log

| Field | Value |
|---|---|
| ID | REQ-013 |
| Type | Operational |
| Source Section | Epic 7 — FR-028 |
| Actor | All services, Audit Log Store |
| Business Object | Audit events |
| Trigger / Event | Every state transition and important action |
| Expected Outcome | Immutable, append-only audit records for every state change within 24h |
| Dependencies | Cosmos DB append-only container |
| Ambiguities | Retention and access controls |
| Assumptions | Cosmos DB configured as append-only |
| Blocking Questions | None |

#### Requirement Text

Maintain an immutable audit log of every state transition for each application including previous/new state, triggering actor, timestamp, and relevant data snapshot; ensure write-once, tamper-evident storage.

---

### REQ-014 — Observability and metrics

| Field | Value |
|---|---|
| ID | REQ-014 |
| Type | Reporting/Operational |
| Source Section | FR-029, FR-030 |
| Actor | Admin Dashboard, Telemetry pipeline |
| Business Object | Metrics, events |
| Trigger / Event | Operational events (submission, scoring, underwriter action, offer acceptance, disbursement) |
| Expected Outcome | Emit structured events with ARN and metrics; dashboards refresh every 5 minutes |
| Dependencies | Telemetry pipeline and dashboards |
| Ambiguities | Exact metrics SLAs |
| Assumptions | Monitoring systems available |
| Blocking Questions | None |

#### Requirement Text

Emit structured observability events for key lifecycle events (submission, scoring, AML/KYC, underwriter decision, offer acceptance, disbursement) including ARN and timestamp; provide dashboard metrics refreshed every 5 minutes.

---

### REQ-015 — Performance and scalability NFRs

| Field | Value |
|---|---|
| ID | REQ-015 |
| Type | Non-functional |
| Source Section | NFR-001..NFR-003 |
| Actor | Platform architects |
| Business Object | Response times, concurrency |
| Trigger / Event | Normal and peak load |
| Expected Outcome | Intake form loads ≤2s; scoring pipeline completes ≤90s; support 500 concurrent submissions |
| Dependencies | Infrastructure sizing |
| Ambiguities | Load profile details |
| Assumptions | Azure resources sized appropriately |
| Blocking Questions | None |

#### Requirement Text

Meet non-functional targets: application form loads ≤2s on standard broadband, scoring pipeline end-to-end ≤90s, and support for 500 concurrent application submissions.

---

## Open Questions

| OQ-NNN | Question | Source REQ | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach (in-house vs. Experian PowerCurve)? | REQ-005 | Yes | Head of AI | Open |
| OQ-002 | Does the cooling-off period waiver require a separate legal sign-off flow? | REQ-011 | Yes | Legal | Open |
| OQ-003 | What is the fallback for HMRC KYC API when unavailable — manual verification or auto-refer? | REQ-009 | Yes | Compliance | Open |

---

## Assumptions

| ASM-NNN | Assumption | Source REQ | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Experian enterprise contract is available and performant | REQ-006 | High | Confirm contract and run smoke tests | Open |
| ASM-002 | DocuSign integration contract exists | REQ-011 | High | Confirm contract and integration tests | Open |
| ASM-003 | T24 payment gateway contract is available or can be defined | REQ-012 | High | Confirm with IT Architecture | Open |

---

## Traceability Notes

All functional requirements are traceable to specific BRS sections (Epic headings and FR IDs). Blocking open questions OQ-001..OQ-003 must be resolved before implementation of impacted requirements.

---
### Requirement ID mappings (sample)

| Source ID | Mapped REQ |
|---|---|
| FR-001 | REQ-001 |
| FR-002 | REQ-002 |
| FR-003 | REQ-001 |
| FR-004 | REQ-003 |
| FR-005 | REQ-004 |
| FR-006 | REQ-005 |
| FR-007 | REQ-005 |
| FR-008 | REQ-005 |
| FR-009 | REQ-006 |
| FR-010 | REQ-007 |
| FR-011 | REQ-008 |
| FR-012 | REQ-009 |
| FR-013 | REQ-009 |
| FR-014 | REQ-009 |
| FR-015 | REQ-010 |
| FR-016 | REQ-010 |
| FR-017 | REQ-010 |
| FR-018 | REQ-010 |
| FR-019 | REQ-010 |
| FR-020 | REQ-011 |
| FR-021 | REQ-011 |
| FR-022 | REQ-011 |
| FR-023 | REQ-011 |
| FR-024 | REQ-012 |
| FR-025 | REQ-012 |
| FR-026 | REQ-012 |
| FR-027 | REQ-012 |
| FR-028 | REQ-013 |
| FR-029 | REQ-014 |
| FR-030 | REQ-014 |
| NFR-001 | REQ-015 |
| NFR-002 | REQ-015 |
| NFR-003 | REQ-015 |
| C-001 | REQ-013 |

---
*Set Status: Accepted only after human review. Never self-accept.*
