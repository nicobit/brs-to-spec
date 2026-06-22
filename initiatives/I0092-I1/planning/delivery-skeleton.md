# Delivery Skeleton

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I0092-I1 |
| Created at | 2026-06-22 |
| Created by | delivery-lead |
| Status | Draft |

---

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant Portal, Underwriter Dashboard | Web-hosted portals, responsive forms |
| Backend API | Yes | Loan Orchestration API, Scoring Service, Compliance Service | Azure-hosted microservices, REST/gRPC as appropriate |
| Infrastructure | Yes | CI/CD, Environments: dev/stage/prod | Azure resources, IaC-managed |
| Integrations | Yes | Experian, HMRC, DocuSign, T24 | External providers with adapters |

---

## Epic Summary

| Metric | Value |
|---|---|
| Total epics | 6 |
| Must | 4 |
| Should | 1 |
| Could | 1 |

---

## Epic and Feature Hierarchy

### E-001 — Intake & Submission

*Accept application, validate, persist, and provide ARN.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | None |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-001 | Application intake and ARN | REQ-001, REQ-002, REQ-003, REQ-004 | Must |

### E-002 — Scoring & Decisioning

*Automated pre-screening, score generation, and decisioning pipeline.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-002 | AI pre-screening & scoring | REQ-005, REQ-013 | Must |
| F-003 | Credit bureau integration | REQ-006 | Must |
| F-004 | Auto-approve / auto-decline rules | REQ-007, REQ-008 | Must |

### E-003 — Compliance & KYC

*AML/KYC screening and compliance handling.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-002 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-005 | AML / KYC screening | REQ-009 | Must |

### E-004 — Underwriting & Manual Review

*Underwriter queue, actions and audit for manual decisions.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | Medium |
| Dependencies | E-002, E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-006 | Underwriter queue and dashboard | REQ-010 | Should |

### E-005 — Offer, Acceptance & Disbursement

*Offer generation, e-sign, and disbursement orchestration.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-004, E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-007 | Offer generation and e-sign | REQ-011 | Must |
| F-008 | Disbursement orchestration | REQ-012 | Must |

### E-006 — Platform & Observability

*Platform non-functional requirements, performance and monitoring.*

| Field | Value |
|---|---|
| Priority | Could |
| Risk | Medium |
| Dependencies | E-001..E-005 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-009 | Observability and metrics | REQ-014 | Could |
| F-010 | Performance and scalability targets | REQ-015 | Could |

---

## Epic Dependency Summary

| Epic | Depends On | Depended On By | Risk |
|---|---|---|---|
| E-001 | None | E-002, E-004 | Medium |
| E-002 | E-001 | E-003, E-004 | High |
| E-003 | E-002 | E-004 | High |
| E-004 | E-002, E-003 | E-005 | Medium |
| E-005 | E-004 | None | High |
| E-006 | E-001..E-005 | None | Medium |

---

## Requirement Coverage

| REQ / FR | Feature | Epic | Status |
|---|---|---|---|
| REQ-001 | F-001 | E-001 | Covered |
| REQ-002 | F-001 | E-001 | Covered |
| REQ-003 | F-001 | E-001 | Covered |
| REQ-004 | F-001 | E-001 | Covered |
| REQ-005 | F-002 | E-002 | Covered |
| REQ-006 | F-003 | E-002 | Covered |
| REQ-007 | F-004 | E-002 | Covered |
| REQ-008 | F-004 | E-002 | Covered |
| REQ-009 | F-005 | E-003 | Covered |
| REQ-010 | F-006 | E-004 | Covered |
| REQ-011 | F-007 | E-005 | Covered |
| REQ-012 | F-008 | E-005 | Covered |
| REQ-013 | F-002 | E-002 | Covered |
| REQ-014 | F-009 | E-006 | Covered |
| REQ-015 | F-010 | E-006 | Covered |

---

### Source Requirement Coverage (FR/NFR/C)

| Source ID | Feature | Epic | Status |
|---|---|---|---|
| FR-001 | F-001 | E-001 | Covered |
| FR-002 | F-001 | E-001 | Covered |
| FR-003 | F-001 | E-001 | Covered |
| FR-004 | F-001 | E-001 | Covered |
| FR-005 | F-001 | E-001 | Covered |
| FR-006 | F-002 | E-002 | Covered |
| FR-007 | F-002 | E-002 | Covered |
| FR-008 | F-002 | E-002 | Covered |
| FR-009 | F-003 | E-002 | Covered |
| FR-010 | F-004 | E-002 | Covered |
| FR-011 | F-004 | E-002 | Covered |
| FR-012 | F-005 | E-003 | Covered |
| FR-013 | F-005 | E-003 | Covered |
| FR-014 | F-005 | E-003 | Covered |
| FR-015 | F-006 | E-004 | Covered |
| FR-016 | F-006 | E-004 | Covered |
| FR-017 | F-006 | E-004 | Covered |
| FR-018 | F-006 | E-004 | Covered |
| FR-019 | F-006 | E-004 | Covered |
| FR-020 | F-007 | E-005 | Covered |
| FR-021 | F-007 | E-005 | Covered |
| FR-022 | F-007 | E-005 | Covered |
| FR-023 | F-007 | E-005 | Covered |
| FR-024 | F-008 | E-005 | Covered |
| FR-025 | F-008 | E-005 | Covered |
| FR-026 | F-008 | E-005 | Covered |
| FR-027 | F-008 | E-005 | Covered |
| FR-028 | F-002 | E-002 | Covered |
| FR-029 | F-009 | E-006 | Covered |
| FR-030 | F-009 | E-006 | Covered |
| NFR-001 | F-010 | E-006 | Covered |
| NFR-002 | F-010 | E-006 | Covered |
| NFR-003 | F-010 | E-006 | Covered |
| C-001 | F-002 | E-002 | Covered |

---

*This is a lightweight skeleton. Stories are produced later during epic elaboration. Set Status: Draft — confirm with delivery lead before acceptance.*

---

*This is a lightweight skeleton. Stories are produced later during epic elaboration. Set Status: Draft — confirm with delivery lead before acceptance.*
