# Impacted Systems

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

---

## Impact Summary

| Metric | Value |
|---|---|
| Requirements mapped | 30 |
| Existing services impacted | 6 |
| New services proposed | 5 |
| New APIs required | 8 |
| New schemas required | 6 |
| Cross-cutting concerns | audit-logging, explainability, auth, observability |

---

## Requirement Impact Map

### FR-001 — Submit application

| Dimension | Details |
|---|---|
| Existing services impacted | ApplicantDB |
| New services needed | Intake API (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | /applications (proposed) |
| New data schemas | application payload schema (proposed) |
| Integration changes | none external |
| Notes | PII handling and input validation; UK datacentre requirement |

### FR-002 — Pre-screen applicants using ML

| Dimension | Details |
|---|---|
| Existing services impacted | Scoring Service (proposed), FeatureStore |
| New services needed | ExplainabilityStore (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | /scores/{id} (proposed) |
| New data schemas | scoring result + explainability schema |
| Integration changes | Experian call for credit reports |
| Notes | Ensure explainability artifacts are stored and auditable |

### FR-003 — Compliance checks

| Dimension | Details |
|---|---|
| Existing services impacted | Compliance / KYC Worker (proposed) |
| New services needed | none |
| Impacted repositories | needs-clarification |
| New APIs | HMRC KYC integration (external) |
| New data schemas | compliance flags schema |
| Integration changes | HMRC API, sanctions list lookups |
| Notes | Circuit breaker and fallback required |

### FR-004 — Underwriter decisioning

| Dimension | Details |
|---|---|
| Existing services impacted | Underwriter UI (existing), Scoring Service |
| New services needed | none |
| Impacted repositories | needs-clarification |
| New APIs | review endpoints for underwriter UI |
| New data schemas | decision audit schema |
| Integration changes | none |
| Notes | Manual override path required |

### FR-005 — Disbursement orchestration

| Dimension | Details |
|---|---|
| Existing services impacted | Disbursement Orchestrator (existing) |
| New services needed | Payment orchestration adapter (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | T24 disbursement adapter (outbound) |
| New data schemas | payment instruction schema |
| Integration changes | Temenos T24 contract integration |
| Notes | Ensure transactional safety and rollback procedures |

## Impact Summary Table

| Requirement | Existing Services | New Services | Impacted Repos | New APIs | New Schemas |
|---|---|---|---|---|---|
| FR-001 | ApplicantDB | Intake API | needs-clarification | /applications | application payload schema |
| FR-002 | Intake API | none | needs-clarification | none | validation rules schema |
| FR-003 | Intake API, ApplicantDB | none | needs-clarification | ARN API | ARN metadata schema |
| FR-004 | Notification pipeline | none | needs-clarification | email API | email template schema |
| FR-005 | Intake API, ApplicantDB | none | needs-clarification | status API | status response schema |
| FR-006 | Intake API, Scoring Service | none | needs-clarification | scoring trigger API | scoring request schema |
| FR-007 | Scoring Service, FeatureStore | ExplainabilityStore | needs-clarification | /scores/{id} | scoring + recommendation schema |
| FR-008 | Scoring Service, FeatureStore | none | needs-clarification | none | feature vector schema |
| FR-009 | Scoring Service | none | needs-clarification | Experian client | Experian mapping schema |
| FR-010 | Scoring Service, Disbursement Orchestrator | none | needs-clarification | offer API | offer schema |
| FR-011 | Scoring Service, Notification pipeline | none | needs-clarification | notification API | decline reason schema |
| FR-012 | Compliance Worker | none | needs-clarification | AML integration | AML result schema |
| FR-013 | Compliance Worker | none | needs-clarification | HMRC integration | KYC schema |
| FR-014 | Compliance Worker, Underwriter UI | none | needs-clarification | compliance hold API | compliance hold schema |
| FR-015 | Underwriter UI, Scoring Service | none | needs-clarification | underwriter queue API | queue schema |
| FR-016 | Underwriter UI | none | needs-clarification | dashboard API | dashboard schema |
| FR-017 | Underwriter UI, ApplicantDB | none | needs-clarification | underwriter action API | action audit schema |
| FR-018 | ApplicantDB, AuditStore | AuditStore | needs-clarification | audit write API | audit entry schema |
| FR-019 | Underwriter UI, Notification pipeline | none | needs-clarification | escalation API | escalation schema |
| FR-020 | Offer Generator | Offer Generator | needs-clarification | offer generation API | offer document schema |
| FR-021 | Underwriter UI, Notification pipeline | none | needs-clarification | offer presentation API | presentation schema |
| FR-022 | Offer Generator, Notification pipeline | DocuSign integration | needs-clarification | DocuSign client | signature metadata schema |
| FR-023 | Offer Generator, Notification pipeline | none | needs-clarification | cooling-off API | cooling-off schema |
| FR-024 | Disbursement Orchestrator | none | needs-clarification | T24 disbursement API | payment instruction schema |
| FR-025 | Disbursement Orchestrator | none | needs-clarification | none | payment instruction schema |
| FR-026 | Disbursement Orchestrator, Operations | none | needs-clarification | confirmation API | confirmation schema |
| FR-027 | Notification pipeline | none | needs-clarification | notification API | disbursement notification schema |
| FR-028 | AuditStore, All services | AuditStore | needs-clarification | audit API | audit log schema |
| FR-029 | Monitoring, Admin UI | none | needs-clarification | metrics API | metrics schema |
| FR-030 | Monitoring, All services | none | needs-clarification | observability emitter | event schema |

---

## Cross-Cutting Concerns

| Concern | Affected Components | Requirements | Notes |
|---|---|---|---|
| Audit Logging | All services | FR-001, FR-004, FR-005 | Centralized audit store required for compliance |
| Explainability | Scoring Service, ExplainabilityStore | FR-002 | Must be tamper-evident and queryable for audits |
| Authentication | Intake API, Underwriter UI | FR-001, FR-004 | Integrate with enterprise auth provider |

---

## Non-Functional Requirement Impacts

| NFR | Affected Components | Impact Type | Notes |
|---|---|---|---|
| NFR-001 (performance) | Scoring Service | performance | May require model optimization and caching |
| NFR-004 (security) | ApplicantDB, Integrations | security | PII encryption and secure transmission required |

---

## New-Proposed Components

| Component | Type | Rationale | Triggered by Requirements |
|---|---|---|---|
| ExplainabilityStore | blob | Persist explainability traces for auditability | FR-002 |
| Payment orchestration adapter | service | Adapter layer to handle T24 variations and retries | FR-005 |

---

## Open Questions

| ID | Question | Impact | Owner |
|---|---|---|---|
| Q-001 | Repository mapping for service artifacts | Affects where code changes are made | Delivery Lead |

---

*Set Status: Draft — impacts mapped from `atomic-requirements.md` and `technical-landscape.md`.*
