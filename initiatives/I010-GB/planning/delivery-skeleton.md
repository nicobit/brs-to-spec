# Delivery Skeleton

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant portal, Underwriter dashboard | Web SPA for applicants; internal dashboard for underwriters |
| Backend API | Yes | Intake API, Underwriter API, Offer API, Disbursement Orchestration | REST APIs; AR/PII constraints applied |
| Infrastructure | Yes | CI/CD, environments, monitoring | Mono-repo pipelines; staging/production environments required |
| Integrations | Yes | Experian, HMRC, DocuSign, Temenos T24 | Adapters with circuit-breakers; staging contracts TBD |

---

## Epic Summary

| Metric | Value |
|---|---|
| Total epics | 5 |
| Must | 4 |
| Should | 1 |
| Could | 0 |

---

## Epic and Feature Hierarchy

### E-001 — Intake & Submission

*Provide the public application flow, submission validation, ARN assignment, and confirmation.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | None |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-001 | Application submission & validation | FR-001, FR-002, FR-005 | Must |
| F-002 | ARN generation & registry | FR-003 | Must |
| F-003 | Confirmation email & notifications | FR-004, FR-027 | Must |

### E-002 — Decisioning & Scoring

*Run automated scoring, produce recommendations and explainability artifacts.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-004 | Scoring pipeline ingestion & model inference | FR-006, FR-007, FR-008 | Must |
| F-005 | Explainability artifact capture & storage | FR-007, AR-005 | Must |

### E-003 — Compliance & Underwriting

*Underwriter workflows, AML/KYC orchestration, compliance holds, and casework tooling.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-002 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-006 | Underwriter queue & case detail UI | FR-015, FR-016, FR-017 | Must |
| F-007 | AML/KYC orchestration & HMRC integration | FR-012, FR-013 | Must |
| F-008 | Compliance hold routing & auditing | FR-014, FR-018 | Must |

### E-004 — Offer, Acceptance & Disbursement

*Generate offers, capture digital acceptance, and orchestrate disbursement to T24.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-002, E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-009 | Offer generation & presentation | FR-020, FR-021 | Must |
| F-010 | Digital acceptance via DocuSign & audit | FR-022, FR-023 | Must |
| F-011 | Disbursement orchestration to T24 | FR-024, FR-025, FR-026 | Must |

### E-005 — Platform & Observability

*Operational features: monitoring, metrics, admin dashboards, and audit store.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | Medium |
| Dependencies | E-001..E-004 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-012 | Metrics pipeline and admin dashboards | FR-029, FR-006 | Should |
| F-013 | Immutable audit store & append API | FR-018, FR-028 | Must |

---

## Epic Dependency Summary

| Epic | Depends On | Depended On By | Risk |
|---|---|---|---|
| E-001 | None | E-002, E-004 | Medium |
| E-002 | E-001 | E-003, E-004 | High |
| E-003 | E-002 | E-004 | High |
| E-004 | E-002, E-003 | None | High |
| E-005 | E-001..E-004 | None | Medium |

---

## Requirement Coverage

| REQ / FR | Feature | Epic | Status |
|---|---|---|---|
| FR-001 | F-001 | E-001 | Covered |
| FR-002 | F-001 | E-001 | Covered |
| FR-003 | F-002 | E-001 | Covered |
| FR-004 | F-003 | E-001 | Covered |
| FR-005 | F-001 | E-001 | Covered |
| FR-006 | F-004 | E-002 | Covered |
| FR-007 | F-004 / F-005 | E-002 | Covered |
| FR-009 | F-004 / F-011 | E-002 / E-004 | Covered |
| FR-012 | F-007 | E-003 | Covered |
| FR-015 | F-006 | E-003 | Covered |
| FR-016 | F-006 | E-003 | Covered |
| FR-018 | F-013 | E-005 | Covered |
| FR-020 | F-009 | E-004 | Covered |
| FR-021 | F-009 | E-004 | Covered |
| FR-022 | F-010 | E-004 | Covered |
| FR-024 | F-011 | E-004 | Covered |
| FR-029 | F-012 | E-005 | Covered |
| FR-008 | F-004 | E-002 | Covered |
| FR-010 | F-004 | E-002 | Covered |
| FR-011 | F-004 | E-002 | Covered |
| FR-013 | F-007 | E-003 | Covered |
| FR-014 | F-008 | E-003 | Covered |
| FR-017 | F-006 | E-003 | Covered |
| FR-019 | F-006 | E-003 | Covered |
| FR-023 | F-010 | E-004 | Covered |
| FR-025 | F-011 | E-004 | Covered |
| FR-026 | F-011 | E-004 | Covered |
| FR-027 | F-003 | E-001 | Covered |
| FR-028 | F-013 | E-005 | Covered |
| FR-030 | F-012 | E-005 | Covered |
| NFR-001 | F-001 | E-001 | Covered |
| NFR-002 | F-004 | E-002 | Covered |
| NFR-003 | F-004 | E-002 | Covered |
| NFR-004 | F-001 | E-001 | Covered |
| NFR-005 | F-013 | E-005 | Covered |
| NFR-006 | F-013 | E-005 | Covered |
| NFR-007 | F-004 | E-002 | Covered |
| C-001 | F-011 | E-004 | Covered |
| C-002 | F-011 | E-004 | Covered |
| C-003 | F-010 | E-004 | Covered |
| C-004 | F-010 | E-004 | Covered |

---

*This is a lightweight delivery skeleton. Stories and estimates are produced later during epic elaboration. Set Status: Draft — review required.*
