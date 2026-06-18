# Requirements Catalog

> Produced by: product-owner
> Primary consumer: Product Owner, Business Analyst, Delivery Lead, Engineers
> Purpose: canonical, traceable functional and non-functional requirements derived from the BRS

## Metadata

| Field | Value |
|---|---|
| Initiative | AI-Powered Loan Origination Platform (I012-NEXT12) |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Functional Requirements

| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
|---|---|---|---|---|
| FR-001 | Applicant can submit online application with mandatory fields | Enables digital intake and reduces manual processing | `input/brs.md` | Form validation and ARN issuance |
| FR-002 | Inline validation prevents submission of incomplete applications | Improves data quality and reduces rework | `input/brs.md` | Client-side and server-side validation tests |
| FR-003 | Assign unique Application Reference Number (ARN) on submission | Enables traceability and lookup | `input/brs.md` | ARN displayed post-submission |
| FR-004 | Send email confirmation within 2 minutes containing ARN | Improves user communication and SLA | `input/brs.md` | Email delivery within SLA during tests |
| FR-005 | Allow status retrieval by ARN + DOB without registration | Lowers friction for applicants | `input/brs.md` | Status lookup tests |
| FR-006 | Trigger AI pre-screening within 60s of submission | Enables rapid decisioning | `input/brs.md` | Scoring completes within 60s under normal load |
| FR-007 | AI produces risk score (0–1000) and recommendation | Standardizes automated recommendations | `input/brs.md` | Score and recommendation logged per application |
| FR-008 | AI model uses applicant, credit bureau, DTI, LTI, employment stability, credit history length | Ensures consistent inputs for scoring | `input/brs.md` | Input mapping and model input tests |
| FR-009 | Integrate with Experian CreditExpert API; fallback to refer | Provides credit report input or safe fallback | `input/brs.md` | Experian integration test and fallback behavior |
| FR-010 | AUTO_APPROVE for ≤£10,000 proceeds to offer generation (subject to AML/KYC) | Speeds decisions for low-risk loans | `input/brs.md` | Offer generation flow tests for eligible cases |
| FR-011 | AUTO_DECLINE notifications within 5 minutes with category reason | Provides timely applicant feedback and compliance | `input/brs.md` | Notification delivery tests |
| FR-012 | Perform AML screening against HM Treasury and PEP DB within 60s | Regulatory compliance | `input/brs.md` | AML screening SLA tests and routing to compliance team |
| FR-013 | Perform KYC identity verification via HMRC API | Identity assurance for applicants | `input/brs.md` | KYC verification integration tests |
| FR-014 | Applications failing AML/KYC flagged `COMPLIANCE_HOLD` and routed to compliance team | Ensures no offers for non-compliant cases | `input/brs.md` | Compliance routing tests |
| FR-015 | Present REFER_TO_UNDERWRITER or >£10,000 AUTO_APPROVE to underwriter queue within 2 minutes | Ensures timely human review where required | `input/brs.md` | Underwriter queue latency tests |
| FR-016 | Underwriter dashboard displays summary, AI score, credit bureau summary, ratios, AML/KYC status | Supports informed human decisions | `input/brs.md` | UI acceptance criteria and data availability tests |
| FR-017 | Underwriter actions: approve (optional conditions), decline (reason mandatory), request info | Captures manual decisions and rationale | `input/brs.md` | Audit logs and UI action tests |
| FR-018 | Record every underwriter action with metadata immutably | Auditability and traceability | `input/brs.md` | Immutable audit log verification |
| FR-019 | Escalation notification after 4 business hours for unactioned underwriter items | Operational SLA enforcement | `input/brs.md` | Escalation simulation tests |
| FR-020 | Generate loan offer document with terms and digital acceptance via DocuSign | Enables digital acceptance and downstream disbursement | `input/brs.md` | DocuSign integration and offer generation tests |
| FR-021 | Present offer via portal and email; offer valid 14 days | Applicant visibility and legal constraints | `input/brs.md` | Offer visibility and expiry tests |
| FR-022 | Digital acceptance logged with timestamp and IP address | Legal traceability | `input/brs.md` | Acceptance logging tests |
| FR-023 | Enforce 14-day cooling-off period with reminders at day 7 and 13 | Consumer protection and compliance | `input/brs.md` | Reminder scheduling and cooling-off enforcement tests |
| FR-024 | Trigger disbursement to Temenos T24 via payment gateway after acceptance | Completes the loan lifecycle | `input/brs.md` | Disbursement integration and retry tests |
| FR-025 | Include account details and reference in disbursement instruction | Accurate settlement | `input/brs.md` | Disbursement payload tests |
| FR-026 | Receive disbursement confirmation and update status; retry once if no confirmation within 2 minutes | Reliability of funds movement | `input/brs.md` | Confirmation and retry tests |
| FR-027 | Notify applicant on disbursement with expected value date | Applicant communications | `input/brs.md` | Notification tests |
| FR-028 | Maintain immutable audit log of every state transition with snapshot data | Compliance and forensic needs | `input/brs.md` | Audit log immutability tests |
| FR-029 | Admin dashboard: volumes, average decision time, AI distribution, underwriter rates, AML/KYC hold rates | Operational visibility | `input/brs.md` | Dashboard data refresh and accuracy tests |
| FR-030 | Emit structured observability events for key lifecycle events | Monitoring and tracing | `input/brs.md` | Event stream and telemetry tests |

## Non-Functional Requirements

| Requirement ID | Description | Source reference |
|---|---|---|
| NFR-001 | Application intake form shall load within 2s on standard broadband | `input/brs.md` |
| NFR-002 | AI scoring pipeline shall complete end-to-end within 90s under normal load | `input/brs.md` |
| NFR-003 | Support 500 concurrent submissions | `input/brs.md` |
| NFR-004 | PII encrypted at rest (AES-256) and in transit (TLS 1.3) | `input/brs.md` |
| NFR-005 | Audit log shall be write-once and tamper-evident | `input/brs.md` |
| NFR-006 | Achieve 99.9% uptime during business hours (08:00–20:00 GMT) | `input/brs.md` |
| NFR-007 | API integrations must implement circuit breakers with defined fallback behaviour | `input/brs.md` |

## Constraints

| Constraint | Source | Impact |
|---|---|---|
| Data residency: UK-only | `input/brs.md` / `input/architecture.md` | Limits cloud region choices and storage locations |
| Must use Experian CreditExpert | `input/brs.md` | Integration contract and latency constraints; fallback required |
| E-signature must use DocuSign | `input/brs.md` | Vendor integration required |
| Core banking integration: Temenos T24 | `input/brs.md` | Payment gateway adapter and contract negotiation may be required |
| AI decisions must be explainable | `input/brs.md` | Affects model selection and testing |
