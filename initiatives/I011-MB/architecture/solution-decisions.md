# Solution Decisions

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

---

## Decision Summary

| Metric | Value |
|---|---|
| Total decisions | 16 |
| Create new | 6 |
| Modify existing | 5 |
| Extend existing | 3 |
| Reuse as-is | 2 |
| New repositories | needs-clarification |
| Flagged conflicts | 0 |

---

## Service Decisions

| ID | Component | Decision | Target Repository | Technology | Rationale | AR Constraints |
|---|---|---|---|---|---|---|
| SD-001 | Intake API | create-new | needs-clarification | .NET 8 (inferred) | Accept applicant data, validation, enqueue scoring | AR-NNN |
| SD-002 | Scoring Service | create-new | needs-clarification | Python / ML runtime | Model scoring and explainability export | AR-NNN |
| SD-003 | Compliance / KYC Worker | create-new | needs-clarification | Node.js (inferred) | HMRC & sanctions checks, circuit-breaker | AR-NNN |
| SD-004 | Disbursement Orchestrator | modify-existing | needs-clarification | Java (existing) | Extend with payment adapter for T24 | AR-NNN |
| SD-005 | Offer Generator | modify-existing | needs-clarification | needs-clarification | Extend to emit offers and DocuSign flow | AR-NNN |
| SD-006 | Payment orchestration adapter | create-new | needs-clarification | service | Adapter to handle T24 variations and retries | AR-NNN |

---

## API Decisions

| ID | API / Endpoint | Decision | Target Service | Protocol | Versioning | Rationale |
|---|---|---|---|---|---|---|
| AP-001 | /applications | create-new | Intake API | REST | v1 | Intake endpoint for applicant submissions |
| AP-002 | /scores/{id} | create-new | Scoring Service | REST | v1 | Return score + explainability payload for audit and UI display |
| AP-003 | underwriter action APIs | modify-existing | Underwriter UI / Intake API | REST | v1 | Expose review and audit endpoints for manual decisions |

---

## UI Decisions

| ID | Page / Module | Decision | Target Application | Routing | Rationale |
|---|---|---|---|---|---|
| UI-001 | Applicant Portal — Application Form | create-new | Applicant Portal | /applications | New public submission flow as per FR-001 |
| UI-002 | Underwriter — Application Detail | modify-existing | Underwriter UI | /underwriter/application/:arn | Add panels for score explainability and audit trail |
| UI-003 | Admin — Metrics Dashboard | modify-existing | Admin Dashboard | /admin/metrics | Extend monitoring views for operations |

---

## Data Decisions

| ID | Schema / Table | Decision | Target Data Store | Migration Strategy | Rationale |
|---|---|---|---|---|---|
| D-001 | application payload schema | create-new | ApplicantDB | additive | New fields for intake and consent; PII handling |
| D-002 | scoring + explainability schema | create-new | ExplainabilityStore / FeatureStore | additive | Persist explainability traces and results |
| D-003 | audit entry schema | extend-existing | AuditStore | additive | Capture underwriter and scoring events for compliance |

---

## Integration Decisions

| ID | Integration | Decision | Contract Approach | Test Strategy | Rationale |
|---|---|---|---|---|---|
| I-001 | Experian CreditExpert | reuse-as-is | existing-contract | contract tests | Use existing vendor contract; map errors to underwriter fallback |
| I-002 | HMRC KYC API | create-new (adapter) | new-contract / adapter | contract tests + adapter mocks | Build adapter in Compliance Worker boundary; negotiate contract |
| I-003 | Temenos T24 Disbursement | create-new (adapter) | adapter | adapter integration tests | Use payment orchestration adapter to isolate T24 specifics |
| I-004 | DocuSign | reuse-as-is | existing-contract | contract tests | Use existing e-signature provider for offer acceptance |

---

## Infrastructure Decisions

| ID | Component | Decision | Target | CI/CD | Rationale |
|---|---|---|---|---|---|
| INF-001 | Scoring Service infra | create-new | AKS | new-pipeline (needs-clarification) | Containerized ML runtime for model scoring |
| INF-002 | Intake API infra | create-new | Azure Container Apps | new-pipeline | Lightweight API hosting with autoscale |
| INF-003 | ExplainabilityStore | create-new | Azure Blob (immutable) | existing-pipeline (storage) | Tamper-evident explainability storage |

---

## Repository Summary

| Repository | Status | Technology | Deployment Target | Decisions |
|---|---|---|---|---|
| needs-clarification | existing / new | various | various | SD-001, SD-002, SD-003, SD-004, SD-005, SD-006 |

---

## Architecture Rule Compliance

| Decision | AR Rule | Status | Notes |
|---|---|---|---|
| SD-001 | AR-NNN | compliant | Intake API must comply with data residency AR-NNN |
| SD-002 | AR-NNN | compliant | Scoring explainability storage must satisfy audit AR-NNN |

---

## Open Solution Design Questions

| ID | Question | Affects Decision(s) | Blocking? | Required Before | Status |
|---|---|---|---|---|---|
| SDQ-001 | Provide repository mapping and CI pipeline names for all target components | SD-001, SD-002, SD-004, SD-005, SD-006 | Yes | delivery-planning / repository inventory | open |
| SDQ-002 | Confirm contract schema for `/scores/{id}` explainability payload | SD-002, D-002, UI-002 | Yes | API contract finalization | open |
| SDQ-003 | Confirm Temenos T24 contract and whether SOAP or REST connector is required | SD-006, SD-004 | Yes | integration negotiation | open |

---

## Carried-Forward Open Questions

| ID | Question | From | Impact | Owner |
|---|---|---|---|---|
| Q-001 | Repository mapping for service artifacts | impacted-systems.md | Blocks CI and delivery planning | Delivery Lead |

---

*Set Status: Draft — decisions recorded; repository mapping and API contracts required before delivery planning.*
