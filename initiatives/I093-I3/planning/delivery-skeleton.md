# Delivery Skeleton

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I093-I3 |
| Created at | 2026-06-22 |
| Created by | delivery-lead |
| Status | Draft |

---

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant portal, Underwriter dashboard | Web UI hosted in UK region |
| Backend API | Yes | Intake service, Scoring pipeline, Underwriter API | Microservices, containerised |
| Infrastructure | Yes | CI/CD, Staging/Prod envs, Immutable infra | AWS/Azure UK regions (TBD) |
| Integrations | Yes | Experian, HMRC, DocuSign, Temenos T24 | Circuit-breakers and retries required |

---

## Epic Summary

| Metric | Value |
|---|---|
| Total epics | 7 |
| Must | 5 |
| Should | 1 |
| Could | 1 |

---

## Epic and Feature Hierarchy

### E-001 — Application Intake

*Capture application submission and basic validation.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | None |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-001 | Online application intake | FR-001, FR-002, FR-003, FR-004, FR-005 | Must |

### E-002 — AI Pre-screening & Scoring

*Automated risk scoring and recommendation.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-002 | AI scoring pipeline | FR-006, FR-007, FR-008, FR-009 | Must |

### E-003 — AML/KYC Compliance

*Perform AML and KYC checks before offer generation.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-002 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-003 | AML/KYC checks | FR-012, FR-013, FR-014 | Must |

### E-004 — Underwriter Review Workflow

*Human-in-the-loop review and decisioning.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | E-002, E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-004 | Underwriter dashboard & actions | FR-015, FR-016, FR-017, FR-018, FR-019 | Must |

### E-005 — Loan Offer & Acceptance

*Offer generation, e-signature, and acceptance flows.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | Medium |
| Dependencies | E-004 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-005 | Offer generation & e-signature | FR-020, FR-021, FR-022, FR-023 | Should |

### E-006 — Disbursement

*Trigger disbursement to core banking after acceptance.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-005 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-006 | Disbursement integration | FR-024, FR-025, FR-026, FR-027 | Must |

### E-007 — Observability & Audit

*Eventing, monitoring, and immutable audit logs.*

| Field | Value |
|---|---|
| Priority | Could |
| Risk | Medium |
| Dependencies | E-001..E-006 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-007 | Observability and audit | FR-028, FR-029, FR-030 | Could |

---

## Epic Dependency Summary

| Epic | Depends On | Depended On By | Risk |
|---|---|---|---|
| E-001 | None | E-002 | Medium |
| E-002 | E-001 | E-003, E-004 | High |
| E-003 | E-002 | E-004 | High |

---

## Requirement Coverage

| REQ / FR | Feature | Epic | Status |
|---|---|---|---|
| FR-001 | F-001 | E-001 | Covered |
| FR-002 | F-001 | E-001 | Covered |
| FR-003 | F-001 | E-001 | Covered |
| FR-004 | F-001 | E-001 | Covered |
| FR-005 | F-001 | E-001 | Covered |
| FR-006 | F-002 | E-002 | Covered |
| FR-007 | F-002 | E-002 | Covered |
| FR-008 | F-002 | E-002 | Covered |
| FR-009 | F-002 | E-002 | Covered |
| FR-012 | F-003 | E-003 | Covered |
| FR-013 | F-003 | E-003 | Covered |
| FR-014 | F-003 | E-003 | Covered |
| FR-015 | F-004 | E-004 | Covered |
| FR-016 | F-004 | E-004 | Covered |
| FR-017 | F-004 | E-004 | Covered |
| FR-018 | F-004 | E-004 | Covered |
| FR-019 | F-004 | E-004 | Covered |
| FR-020 | F-005 | E-005 | Covered |
| FR-021 | F-005 | E-005 | Covered |
| FR-022 | F-005 | E-005 | Covered |
| FR-023 | F-005 | E-005 | Covered |
| FR-024 | F-006 | E-006 | Covered |
| FR-025 | F-006 | E-006 | Covered |
| FR-026 | F-006 | E-006 | Covered |
| FR-027 | F-006 | E-006 | Covered |
| FR-028 | F-007 | E-007 | Covered |
| FR-029 | F-007 | E-007 | Covered |
| FR-030 | F-007 | E-007 | Covered |
| FR-010 | F-005 | E-005 | Covered |
| FR-011 | F-001 | E-001 | Covered |
| C-001 | F-007 | E-007 | Covered |
| NFR-001 | F-001 | E-001 | Covered |
| NFR-002 | F-002 | E-002 | Covered |
| NFR-003 | F-002 | E-002 | Covered |
| NFR-004 | F-007 | E-007 | Covered |
| NFR-005 | F-007 | E-007 | Covered |
| NFR-006 | F-006 | E-006 | Covered |
| NFR-007 | F-002 | E-002 | Covered |
| REQ-001 | F-001 | E-001 | Covered |
| REQ-002 | F-001 | E-001 | Covered |
| REQ-003 | F-001 | E-001 | Covered |
| REQ-006 | F-002 | E-002 | Covered |
| REQ-007 | F-002 | E-002 | Covered |
| REQ-009 | F-002 | E-002 | Covered |
| REQ-010 | F-005 | E-005 | Covered |
| REQ-012 | F-003 | E-003 | Covered |
| REQ-013 | F-003 | E-003 | Covered |
| REQ-016 | F-004 | E-004 | Covered |
| REQ-020 | F-005 | E-005 | Covered |
| REQ-022 | F-005 | E-005 | Covered |
| REQ-023 | F-005 | E-005 | Covered |
| REQ-024 | F-006 | E-006 | Covered |
| REQ-026 | F-006 | E-006 | Covered |

---
*This is a lightweight skeleton. Stories are produced later during epic elaboration. Set Status: Confirmed only after review. Never self-accept.*
