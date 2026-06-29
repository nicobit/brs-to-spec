# Impacted Systems

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

---

## Impact Summary

| Metric | Value |
|---|---|
| Requirements mapped | 29 functional FRs |
| Existing services impacted | Web frontend, Email subsystem, Temenos T24 (external) |
| New services proposed | Intake API, ARN service, Scoring pipeline, Explainability service, Experian adapter (if absent), AML/KYC orchestration, Underwriter dashboard, Disbursement orchestration, Immutable audit store |
| New APIs required | Intake API, Explainability telemetry API, Disbursement adapter API |
| New schemas required | Application submission schema, Scoring result schema, Disbursement instruction schema, Immutable-audit entry schema |
| Cross-cutting concerns | Audit logging, Observability, Security (PII encryption), Circuit breakers |

---

## Requirement Impact Map

### FR-001 — Loan application submission

| Dimension | Details |
|---|---|
| Existing services impacted | Web frontend (applicant portal), Email subsystem (confirmation) |
| New services needed | Intake API (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | Intake API (accept submission) |
| New data schemas | Application submission schema (fields list) |
| Integration changes | None beyond intake; emits events to event bus/audit store |
| Notes | ARN assignment handled by ARN service (FR-003). |

---

### FR-002 — Inline validation before submission

| Dimension | Details |
|---|---|
| Existing services impacted | Web frontend |
| New services needed | None (frontend responsibility) |
| Impacted repositories | needs-clarification |
| New APIs | None |
| New data schemas | Validation rules manifest (optional) |
| Integration changes | Client-side validation; server-side validation in Intake API |
| Notes | Ensure consistent validation logic between frontend and Intake API. |

---

### FR-003 — Assign Application Reference Number (ARN)

| Dimension | Details |
|---|---|
| Existing services impacted | Intake API (new) |
| New services needed | ARN service (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | ARN generation API |
| New data schemas | ARN registry schema |
| Integration changes | Intake API calls ARN service; ARN emitted to audit store and email subsystem |
| Notes | ARN must be unique and persisted. |

---

### FR-004 — Email confirmation within 2 minutes

| Dimension | Details |
|---|---|
| Existing services impacted | Email subsystem |
| New services needed | None (use existing email subsystem) |
| Impacted repositories | needs-clarification |
| New APIs | Intake API -> Email subsystem integration call |
| New data schemas | Confirmation email template metadata |
| Integration changes | Ensure retry and SLA for email delivery |
| Notes | SLA requirement drives monitoring. |

---

### FR-005 — Retrieve status by ARN and DOB

| Dimension | Details |
|---|---|
| Existing services impacted | Web frontend, Intake API |
| New services needed | None beyond Intake API data endpoint |
| Impacted repositories | needs-clarification |
| New APIs | Status retrieval API on Intake API |
| New data schemas | Status response schema |
| Integration changes | Authentication/lookup logic and PII handling |
| Notes | Must comply with NFR-004 (PII encryption). |

---

### FR-006 — Trigger AI pre-screening within 60s

| Dimension | Details |
|---|---|
| Existing services impacted | Intake API (triggers), Event bus/logging |
| New services needed | Scoring pipeline (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | Scoring pipeline ingestion API |
| New data schemas | Scoring job input schema |
| Integration changes | Intake API publishes scoring task to pipeline; Experian data may be required beforehand (FR-009) |
| Notes | Performance SLA drives scaling requirements. |

---

### FR-007 — Produce risk score and recommendation

| Dimension | Details |
|---|---|
| Existing services impacted | None (new scoring pipeline output consumed by Intake API/Underwriter dashboard) |
| New services needed | Scoring pipeline, Explainability service |
| Impacted repositories | needs-clarification |
| New APIs | Scoring result API; Explainability telemetry API |
| New data schemas | Scoring result schema (score, recommendation, feature contributions) |
| Integration changes | Results stored in audit store and emitted to underwriter queue if needed |
| Notes | Must retain explainability artifacts per AR-005. |

---

### FR-008 — Model inputs for scoring

| Dimension | Details |
|---|---|
| Existing services impacted | Intake API, Experian adapter |
| New services needed | None beyond scoring pipeline and explainability service |
| Impacted repositories | needs-clarification |
| New APIs | Input enrichment APIs (internal) |
| New data schemas | Model input schema |
| Integration changes | Pull Experian data via Experian adapter; compute DTI/LTI metrics |
| Notes | Data privacy rules apply (C-002, NFR-004). |

---

### FR-009 — Experian integration

| Dimension | Details |
|---|---|
| Existing services impacted | Experian adapter (existing/proposed), Scoring pipeline |
| New services needed | Experian adapter (if not present) |
| Impacted repositories | needs-clarification |
| New APIs | Experian adapter interface; circuit-breaker configuration |
| New data schemas | Experian response mapping schema |
| Integration changes | Implement timeout and fallback to refer-to-underwriter |
| Notes | Integration contract and SLA verification needed. |

---

### FR-010 — AUTO_APPROVE flow for ≤£10,000

| Dimension | Details |
|---|---|
| Existing services impacted | Scoring pipeline, Intake API, AML/KYC orchestration |
| New services needed | None (composition of existing proposed services) |
| Impacted repositories | needs-clarification |
| New APIs | Orchestration flows to generate offers and call AML/KYC services |
| New data schemas | Offer generation schema |
| Integration changes | Ensure AML/KYC checks pass before offer generation |
| Notes | Cross-check with FR-012 and FR-013. |

---

### FR-011 — AUTO_DECLINE notification and cooling-off

| Dimension | Details |
|---|---|
| Existing services impacted | Intake API, Email subsystem |
| New services needed | None |
| Impacted repositories | needs-clarification |
| New APIs | Notification API usage |
| New data schemas | Decline reason categorization schema |
| Integration changes | Cooling-off enforcement in applicant lifecycle management |
| Notes | Retain decision rationale in audit store. |

---

### FR-012 — AML screening before offer generation

| Dimension | Details |
|---|---|
| Existing services impacted | AML/KYC orchestration (proposed), Scoring pipeline |
| New services needed | AML/KYC orchestration service (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | AML screening API connectors (HMRC) |
| New data schemas | AML screening result schema |
| Integration changes | Circuit-breaker and retry semantics with HMRC integrations |
| Notes | Failure paths route to COMPLIANCE_HOLD. |

---

### FR-013 — KYC identity verification

| Dimension | Details |
|---|---|
| Existing services impacted | Identity Verification (via HMRC) |
| New services needed | HMRC connector in AML/KYC orchestration if not present |
| Impacted repositories | needs-clarification |
| New APIs | HMRC identity verification adapter |
| New data schemas | KYC verification response schema |
| Integration changes | Handle PII securely and comply with data residency |
| Notes | Failure => COMPLIANCE_HOLD. |

---

### FR-014 — COMPLIANCE_HOLD routing

| Dimension | Details |
|---|---|
| Existing services impacted | Compliance queue / casework tools |
| New services needed | None beyond orchestration and queueing |
| Impacted repositories | needs-clarification |
| New APIs | Routing API to compliance queue |
| New data schemas | Compliance case schema |
| Integration changes | Ensure visibility for compliance team tools |
| Notes | Audit entries must record hold reasons. |

---

### FR-015 — Underwriter queue rules

| Dimension | Details |
|---|---|
| Existing services impacted | Underwriter queue (existing/proposed), Scoring pipeline |
| New services needed | Underwriter queue operational rules (may be in existing queue) |
| Impacted repositories | needs-clarification |
| New APIs | Queue management API |
| New data schemas | Queue metadata schema |
| Integration changes | Ensure enqueue within 2 minutes of scoring completion |
| Notes | Monitoring and SLAs required. |

---

### FR-016 — Underwriter dashboard contents

| Dimension | Details |
|---|---|
| Existing services impacted | Underwriter dashboard (proposed), Scoring pipeline, Experian adapter, AML/KYC orchestration |
| New services needed | Underwriter dashboard service (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | Dashboard data API aggregating scoring, Experian, AML status |
| New data schemas | Dashboard view model schema |
| Integration changes | Aggregation from multiple services into dashboard API |
| Notes | Must include explainability artifacts. |

---

### FR-017 — Underwriter actions

| Dimension | Details |
|---|---|
| Existing services impacted | Underwriter dashboard, Compliance queue |
| New services needed | None beyond dashboard and queue integration |
| Impacted repositories | needs-clarification |
| New APIs | Underwriter action API (record action) |
| New data schemas | Underwriter action record schema (immutable) |
| Integration changes | Actions must write immutable entries to audit store |
| Notes | Satisfies FR-018 when immutable. |

---

### FR-018 — Immutable underwriter action record

| Dimension | Details |
|---|---|
| Existing services impacted | Immutable audit store (proposed), Underwriter dashboard |
| New services needed | Immutable audit store (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | Audit append API |
| New data schemas | Immutable audit entry schema |
| Integration changes | All action writes must append to audit store with tamper-evident guarantees |
| Notes | Aligns with NFR-005. |

---

### FR-019 — Escalation after 4 business hours

| Dimension | Details |
|---|---|
| Existing services impacted | Queue monitoring, Notification subsystem |
| New services needed | Escalation scheduler/monitor (could be part of queue infra) |
| Impacted repositories | needs-clarification |
| New APIs | Escalation notification API |
| New data schemas | Escalation rule schema |
| Integration changes | Integration with team lead notification channels |
| Notes | Business-hours calendar awareness required. |

---

### FR-020 — Loan offer content

| Dimension | Details |
|---|---|
| Existing services impacted | Offer generation service (proposed), Web frontend, Email subsystem |
| New services needed | Offer generation component (could be part of Intake API or a separate service) |
| Impacted repositories | needs-clarification |
| New APIs | Offer generation API |
| New data schemas | Offer document schema |
| Integration changes | Store offer in audit store and send to DocuSign for acceptance |
| Notes | Legal content templates required. |

---

### FR-021 — Present offer via portal and email

| Dimension | Details |
|---|---|
| Existing services impacted | Web frontend, Email subsystem |
| New services needed | None beyond offer generation and email integration |
| Impacted repositories | needs-clarification |
| New APIs | Offer retrieval API for portal |
| New data schemas | Offer presentation schema |
| Integration changes | Delivery SLA for email and portal visibility |
| Notes | Follow-up tracking for acceptance. |

---

### FR-022 — Digital acceptance via DocuSign

| Dimension | Details |
|---|---|
| Existing services impacted | DocuSign integration, Offer generation, Immutable audit store |
| New services needed | DocuSign adapter if not present |
| Impacted repositories | needs-clarification |
| New APIs | DocuSign callback handling API |
| New data schemas | Acceptance record schema (timestamp, IP) |
| Integration changes | Ensure callback writes acceptance to audit store and triggers disbursement flow |
| Notes | Contract verification for DocuSign (C-004). |

---

### FR-023 — 14-day cooling-off enforcement

| Dimension | Details |
|---|---|
| Existing services impacted | Offer lifecycle management, Notification subsystem |
| New services needed | Cooling-off scheduler (or managed by orchestration) |
| Impacted repositories | needs-clarification |
| New APIs | Cooling-off status API |
| New data schemas | Cooling-off schedule schema |
| Integration changes | Reminders at day 7 and day 13 via email subsystem |
| Notes | Ties into disbursement trigger (FR-024). |

---

### FR-024 — Trigger disbursement to T24

| Dimension | Details |
|---|---|
| Existing services impacted | Disbursement orchestration (proposed), Temenos T24 (external) |
| New services needed | Disbursement orchestration service (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | Disbursement adapter API to T24 |
| New data schemas | Disbursement instruction schema (FR-025) |
| Integration changes | Idempotency and retry semantics with T24 adapter |
| Notes | Align with C-003 (T24 integration). |

---

### FR-025 — Disbursement instruction fields

| Dimension | Details |
|---|---|
| Existing services impacted | Disbursement orchestration |
| New services needed | None beyond disbursement orchestration |
| Impacted repositories | needs-clarification |
| New APIs | Disbursement instruction API fields defined |
| New data schemas | Disbursement instruction schema |
| Integration changes | Ensure mapping to T24 fields |
| Notes | Validate formatting and bank details. |

---

### FR-026 — Disbursement confirmation handling and retries

| Dimension | Details |
|---|---|
| Existing services impacted | Disbursement orchestration, Notification subsystem |
| New services needed | None beyond orchestration and monitoring |
| Impacted repositories | needs-clarification |
| New APIs | Confirmation handling API |
| New data schemas | Disbursement confirmation schema |
| Integration changes | Retry once after 2 minutes then alert operations |
| Notes | Operational alerts integration required. |

---

### FR-027 — Applicant notification on disbursement

| Dimension | Details |
|---|---|
| Existing services impacted | Email subsystem, Web frontend |
| New services needed | None |
| Impacted repositories | needs-clarification |
| New APIs | Notification API usage |
| New data schemas | Disbursement notification schema |
| Integration changes | Delivery SLA and expected value date included |
| Notes | UX for value date display in portal. |

---

### FR-028 — Immutable audit log of state transitions

| Dimension | Details |
|---|---|
| Existing services impacted | Immutable audit store (proposed), All services that change state |
| New services needed | Immutable audit store service (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | Audit append API, Audit query API |
| New data schemas | Immutable audit entry schema |
| Integration changes | All state-changing operations must append audit entries atomically |
| Notes | Critical for regulatory audit (OBJ-003). |

---

### FR-029 — Admin dashboard metrics and refresh

| Dimension | Details |
|---|---|
| Existing services impacted | Admin dashboard (existing/proposed), Event bus, Logging |
| New services needed | Dashboard aggregation API and metrics pipelines |
| Impacted repositories | needs-clarification |
| New APIs | Metrics query API |
| New data schemas | Metrics and aggregation schema |
| Integration changes | 5-minute refresh pipeline from event stream or data store |
| Notes | Instrumentation required across services. |

---

## Impact Summary Table

| Requirement | Existing Services | New Services | Impacted Repos | New APIs | New Schemas |
|---|---|---|---|---|---|
| FR-001 | Web frontend, Email subsystem | Intake API | needs-clarification | Intake API | Application submission schema |
| FR-002 | Web frontend | None | needs-clarification | None | Validation manifest |
| FR-003 | Intake API | ARN service | needs-clarification | ARN API | ARN registry |
| FR-004 | Email subsystem | None | needs-clarification | Email integration | Email template metadata |
| FR-005 | Intake API | None | needs-clarification | Status API | Status response schema |
| FR-006 | Intake API, Event bus | Scoring pipeline | needs-clarification | Scoring ingestion API | Scoring job input |
| FR-007 | Scoring pipeline | Explainability service | needs-clarification | Scoring result API | Scoring result schema |
| FR-008 | Intake API, Experian adapter | None | needs-clarification | Enrichment APIs | Model input schema |
| FR-009 | Experian adapter, Scoring pipeline | Experian adapter (if needed) | needs-clarification | Experian adapter API | Experian mapping schema |
| FR-010 | Scoring pipeline, AML/KYC | None | needs-clarification | Orchestration APIs | Offer schema |
| FR-011 | Intake API, Email subsystem | None | needs-clarification | Notification APIs | Decline reason schema |
| FR-012 | AML/KYC orchestration | AML/KYC orchestration | needs-clarification | AML connector APIs | AML result schema |
| FR-013 | HMRC connector | HMRC connector | needs-clarification | HMRC adapter API | KYC response schema |
| FR-014 | Compliance queue | None | needs-clarification | Routing API | Compliance case schema |
| FR-015 | Underwriter queue | None | needs-clarification | Queue API | Queue metadata schema |
| FR-016 | Underwriter dashboard | Underwriter dashboard | needs-clarification | Dashboard API | Dashboard view schema |
| FR-017 | Underwriter dashboard | None | needs-clarification | Action API | Underwriter action schema |
| FR-018 | Underwriter dashboard, Audit store | Audit store | needs-clarification | Audit append API | Immutable audit schema |
| FR-019 | Queue monitoring | Escalation scheduler | needs-clarification | Escalation API | Escalation schema |
| FR-020 | Offer generation, Web frontend | Offer generation component | needs-clarification | Offer API | Offer document schema |
| FR-021 | Web frontend, Email subsystem | None | needs-clarification | Offer retrieval API | Offer presentation schema |
| FR-022 | DocuSign integration, Audit store | DocuSign adapter | needs-clarification | DocuSign callback API | Acceptance record schema |
| FR-023 | Offer lifecycle | Cooling-off scheduler | needs-clarification | Cooling-off API | Cooling-off schema |
| FR-024 | Disbursement orchestration, T24 | Disbursement orchestration | needs-clarification | Disbursement adapter API | Disbursement instruction schema |
| FR-025 | Disbursement orchestration | None | needs-clarification | Disbursement API | Disbursement instruction schema |
| FR-026 | Disbursement orchestration | None | needs-clarification | Confirmation API | Disbursement confirmation schema |
| FR-027 | Email subsystem, Web frontend | None | needs-clarification | Notification API | Disbursement notification schema |
| FR-028 | All services | Immutable audit store | needs-clarification | Audit APIs | Immutable audit schema |
| FR-029 | Admin dashboard | Metrics pipelines | needs-clarification | Metrics API | Metrics schema |

---

## Cross-Cutting Concerns

| Concern | Affected Components | Requirements | Notes |
|---|---|---|---|
| Audit logging | All services, Immutable audit store | FR-018, FR-028, OBJ-003 | Append-only audit store; retention and query SLAs required |
| Observability / metrics | Scoring pipeline, Intake API, Disbursement | FR-006, FR-029 | Emit structured events (FR-030) into metrics pipeline |
| Security / PII handling | Intake API, HMRC adapter, Experian adapter, Audit store | FR-001, NFR-004, C-002 | Ensure encryption at rest/in transit and UK-only residency |
| Integration resilience | Experian, HMRC, DocuSign, T24 adapters | FR-009, FR-012, FR-022, FR-024 | Circuit breakers, retries, and fallbacks per NFR-007 |

---

## Non-Functional Requirement Impacts

| NFR | Affected Components | Impact Type | Notes |
|---|---|---|---|
| NFR-001 | Web frontend | performance | Frontend optimization and CDN for ≤2s load |
| NFR-002 | Scoring pipeline | performance | Pipeline sizing and model latency targets |
| NFR-003 | Intake API, Scoring pipeline | scalability | Autoscaling and throughput testing for 500 concurrent submissions |
| NFR-004 | All PII-handling components | security | KMS, encryption, and data residency controls |
| NFR-005 | Audit store | security / durability | WORM or equivalent tamper-evident storage required |
| NFR-006 | All production services | availability | Multi-AZ deployment and failover design |
| NFR-007 | External adapters | resilience | Circuit breakers and fallback strategies required |

---

## New-Proposed Components

| Component | Type | Rationale | Triggered by Requirements |
|---|---|---|---|
| Intake API | api | Centralize submission handling and validation | FR-001, FR-002, FR-005 |
| ARN service | service | Guaranteed unique ARN generation and registry | FR-003 |
| Scoring pipeline | service/pipeline | Host models and generate scores | FR-006, FR-007 |
| Explainability service | service | Persist model rationale for audit and regulator review | FR-007, AR-005 |
| Immutable audit store | storage | Tamper-evident store required for regulatory audit | FR-018, FR-028, NFR-005 |
| Disbursement orchestration | service | Orchestrate T24 integration with idempotency | FR-024, FR-025, FR-026 |

---

## Open Questions

| ID | Question | Impact | Owner |
|---|---|---|---|
| Q-001 | Are the Experian and DocuSign contracts already provisioned for test environments? | Affects integration timeline and testing | Procurement / IT |
| Q-002 | Will repository-level mapping be provided (`input/repository-context.md`)? | Affects where code changes will be implemented | Engineering Lead |
| Q-003 | Which teams own the proposed new services (scoring, audit store)? | Affects delivery planning and SLAs | Delivery Lead |

---

*Set Status: Draft — derived, not yet verified with code owners.*
