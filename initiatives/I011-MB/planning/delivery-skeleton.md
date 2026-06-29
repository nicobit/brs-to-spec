# Delivery Skeleton (Light)

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant Portal, Underwriter Dashboard, Admin Dashboard | React apps; Applicant Portal uses ARN-only lookup (no accounts) |
| Backend API | Yes | Intake API, Scoring Service, Compliance Worker, Disbursement Orchestrator | REST services; explainability artifacts stored in ExplainabilityStore |
| Infrastructure | Yes | AKS, Container Apps, CI/CD pipelines (nb-repo) | UK data centres for PII; observability via App Insights |
| Integrations | Yes | Experian, HMRC, DocuSign, Temenos T24 | Adapters for external systems; T24 is REST-based |

---

## Epic Summary

| Metric | Value |
|---|---|
| Total epics | 8 |
| Must | 6 |
| Should | 2 |
| Could | 0 |

---

## Epic and Feature Hierarchy

### E-001 — Intake & Submission

*Provide reliable, performant applicant intake and submission flows.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | None |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-001 | Intake Form & Submission | FR-001, FR-002, FR-003, FR-004, NFR-001 | Must |
| F-002 | Status Retrieval (ARN) | FR-005 | Must |
| F-003 | Submission Orchestration | FR-006, FR-030 | Must |

### E-002 — Scoring & Explainability

*Run AI pre-screening and produce auditable scores and explainability artifacts.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-004 | Scoring Pipeline & Explainability | FR-007, FR-008, NFR-002, C-004, OBJ-001 | Must |
| F-005 | Experian Integration & Credit Checks | FR-009, NFR-007 | Must |
| F-006 | Explainability Store & APIs | FR-007, FR-030 | Should |

### E-003 — Compliance & KYC

*Perform AML/KYC checks and enforce compliance holds.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-002 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-007 | AML & KYC Checks | FR-012, FR-013, FR-014, C-001 | Must |

### E-004 — Underwriter Decisioning

*Provide queue, detail view, actions, and immutable audit trail for underwriters.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | E-002, E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-008 | Underwriter Queue & Dashboard | FR-015, FR-016, FR-019, OBJ-002 | Must |
| F-009 | Underwriter Actions & Audit | FR-017, FR-018, FR-028, NFR-005 | Must |

### E-005 — Offer & Acceptance

*Generate offers, present to applicants, and capture e-signature acceptance.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | E-003, E-004 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-010 | Offer Generation & Presentation | FR-020, FR-021, FR-011 | Must |
| F-011 | E-signature & Cooling-off | FR-022, FR-023 | Must |

### E-006 — Disbursement & Payments

*Execute disbursement instructions reliably via T24 adapter.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | High |
| Dependencies | E-005 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-012 | Disbursement Orchestration & T24 Adapter | FR-024, FR-025, FR-026, FR-027, OBJ-005 | Should |

### E-007 — Operations, Admin & Observability

*Provide admin metrics, monitoring, and alerts.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | Low |
| Dependencies | E-001..E-006 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-013 | Admin Metrics & Observability | FR-029, FR-030, NFR-006 | Should |

### E-008 — Platform, Security & Audit

*Ensure data residency, encryption, immutable audit logs, and platform readiness.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001..E-006 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-014 | Platform, Security & Audit Controls | NFR-004, NFR-005, NFR-007, C-002, OBJ-003, OBJ-004 | Must |

---

## Epic Dependency Summary

| Epic | Depends On | Depended On By | Risk |
|---|---|---|---|
| E-001 | None | E-002 | Medium |
| E-002 | E-001 | E-003, E-004 | High |
| E-003 | E-002 | E-004 | High |
| E-004 | E-002, E-003 | E-005 | Medium |
| E-005 | E-003, E-004 | E-006 | Medium |
| E-006 | E-005 | None | High |
| E-007 | E-001..E-006 | None | Low |
| E-008 | E-001..E-006 | None | High |

---

## Requirement Coverage

| REQ / FR | Feature | Epic | Status |
|---|---|---|---|
| OBJ-001 | F-004 | E-002 | Covered |
| OBJ-002 | F-008 | E-004 | Covered |
| OBJ-003 | F-014 | E-008 | Covered |
| OBJ-004 | F-007 | E-003 | Covered |
| OBJ-005 | F-012 | E-006 | Covered |
| FR-001 | F-001 | E-001 | Covered |
| FR-002 | F-001 | E-001 | Covered |
| FR-003 | F-001 | E-001 | Covered |
| FR-004 | F-001 | E-001 | Covered |
| FR-005 | F-002 | E-001 | Covered |
| FR-006 | F-003 | E-001 | Covered |
| FR-007 | F-004 | E-002 | Covered |
| FR-008 | F-004 | E-002 | Covered |
| FR-009 | F-005 | E-002 | Covered |
| FR-010 | F-004 | E-002 | Covered |
| FR-011 | F-010 | E-005 | Covered |
| FR-012 | F-007 | E-003 | Covered |
| FR-013 | F-007 | E-003 | Covered |
| FR-014 | F-007 | E-003 | Covered |
| FR-015 | F-008 | E-004 | Covered |
| FR-016 | F-008 | E-004 | Covered |
| FR-017 | F-009 | E-004 | Covered |
| FR-018 | F-009 | E-004 | Covered |
| FR-019 | F-008 | E-004 | Covered |
| FR-020 | F-010 | E-005 | Covered |
| FR-021 | F-010 | E-005 | Covered |
| FR-022 | F-011 | E-005 | Covered |
| FR-023 | F-011 | E-005 | Covered |
| FR-024 | F-012 | E-006 | Covered |
| FR-025 | F-012 | E-006 | Covered |
| FR-026 | F-012 | E-006 | Covered |
| FR-027 | F-012 | E-006 | Covered |
| FR-028 | F-009 | E-004 | Covered |
| FR-029 | F-013 | E-007 | Covered |
| FR-030 | F-013 | E-007 | Covered |
| NFR-001 | F-001 | E-001 | Covered |
| NFR-002 | F-004 | E-002 | Covered |
| NFR-003 | F-003 | E-001 | Covered |
| NFR-004 | F-014 | E-008 | Covered |
| NFR-005 | F-009 | E-004 | Covered |
| NFR-006 | F-013 | E-007 | Covered |
| NFR-007 | F-005 | E-002 | Covered |
| C-001 | F-007 | E-003 | Covered |
| C-002 | F-014 | E-008 | Covered |
| C-003 | F-005 | E-002 | Covered |
| C-004 | F-004 | E-002 | Covered |

---

Contact: Delivery Lead
