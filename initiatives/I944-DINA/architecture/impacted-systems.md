# Impacted Systems

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I944-DINA |
| Created at | 2026-07-02 |
| Created by | architect |
| Status | Draft |

---

## Impact Summary

| Metric | Value |
|---|---|
| Requirements mapped | 6 |
| Existing services impacted | 2 |
| New services proposed | 4 |
| New APIs required | 2 |
| New schemas required | 2 |
| Cross-cutting concerns | Audit logging, security/allowlist, reconciliation |

---

## Requirement Impact Map

### FR-001 — Maintain internal golden record

| Dimension | Details |
|---|---|
| Existing services impacted | Fund Administrator API (read), Reconciliation Engine (proposed) |
| New services needed | Reconciliation Engine (proposed), Investor Registry (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | /positions (Investor Registry) |
| New data schemas | Internal ledger snapshot schema |
| Integration changes | Add reconciliation event producers to CRE adapter |
| Notes | Needs mapping of event fields to onchain references |

### FR-002 — Invoke Chainlink for onchain actions

| Dimension | Details |
|---|---|
| Existing services impacted | Smart contract gateway / CRE adapter (proposed) |
| New services needed | Smart contract gateway (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | n/a (internal CRE adapter) |
| New data schemas | Onchain transaction reference schema |
| Integration changes | CRE integration and callbacks handling |
| Notes | Must preserve audit linkage between internal order and onchain tx |

### FR-003 — Eligibility and compliance decisioning

| Dimension | Details |
|---|---|
| Existing services impacted | KYC/AML services (existing) |
| New services needed | Eligibility & Compliance service (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | /eligibility-checks |
| New data schemas | Eligibility result schema |
| Integration changes | Connect to Chainlink ACE for enforcement hooks |
| Notes | Compliance service remains policy owner per constitution |

### FR-004 — Reconciliation between internal ledger and onchain state

| Dimension | Details |
|---|---|
| Existing services impacted | Fund Admin exports (existing) |
| New services needed | Reconciliation Engine (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | /reconciliation/status |
| New data schemas | Reconciliation snapshot schema |
| Integration changes | Periodic pull from fund admin; onchain balance queries via CRE |
| Notes | Define reconciliation cadence and thresholds (open question)

### FR-005 — Workflow state transitions for orders

| Dimension | Details |
|---|---|
| Existing services impacted | Internal DTA workflow engine (proposed) |
| New services needed | None beyond workflow engine |
| Impacted repositories | needs-clarification |
| New APIs | /orders (submission and status) |
| New data schemas | Order state machine schema |
| Integration changes | Hooks for eligibility, payment, and CRE execution |
| Notes | Must record timestamps for each state transition

### FR-006 — Audit and reporting evidence

| Dimension | Details |
|---|---|
| Existing services impacted | Reporting pipelines (existing) |
| New services needed | Reconciliation evidence store (proposed) |
| Impacted repositories | needs-clarification |
| New APIs | /reports/audit |
| New data schemas | Audit evidence schema linking internal and onchain events |
| Integration changes | Expose evidence to auditors; WORM storage consideration |
| Notes | Ensure immutability or WORM-capable storage for audit artifacts

---

## Impact Summary Table

| Requirement | Existing Services | New Services | Impacted Repos | New APIs | New Schemas |
|---|---|---|---|---|---|
| FR-001 | Fund Admin export | Reconciliation Engine, Investor Registry | needs-clarification | /positions | ledger snapshot |
| FR-002 | - | Smart contract gateway / CRE adapter | needs-clarification | - | onchain tx ref |
| FR-003 | KYC/AML | Eligibility & Compliance service | needs-clarification | /eligibility-checks | eligibility result |
| FR-004 | Fund Admin exports | Reconciliation Engine | needs-clarification | /reconciliation/status | reconciliation snapshot |
| FR-005 | - | Internal DTA workflow engine | needs-clarification | /orders | order state schema |
| FR-006 | Reporting pipelines | Evidence store | needs-clarification | /reports/audit | audit evidence schema |

---

## Cross-Cutting Concerns

| Concern | Affected Components | Requirements | Notes |
|---|---|---|---|
| Audit logging | All components | FR-001, FR-004, FR-006 | Centralized audit pipeline required |
| Security / allowlist | Smart contract gateway, CRE adapter | FR-002, FR-004 | Enforce AR-004 rules |
| Observability | CRE interactions, reconciliation | FR-002, FR-004 | Monitoring for retries and failures |

---

## Non-Functional Requirement Impacts

| NFR | Affected Components | Impact Type | Notes |
|---|---|---|---|
| NFR-001 (Controlled rollout) | Deployment and release pipelines | availability / deployment | ADR required to expand beyond initial scope |

---

## New-Proposed Components

| Component | Type | Rationale | Triggered by Requirements |
|---|---|---|---|
| Reconciliation Engine | service | Needed to compare internal ledger vs onchain and produce evidence | FR-001, FR-004 |
| Investor Registry | database/service | Central golden record of investor attributes | FR-001 |
| Smart contract gateway / CRE adapter | service | Interface to Chainlink CRE and onchain contracts | FR-002 |
| Evidence store | blob/db | Store reconciliation snapshots and audit evidence WORM-capable | FR-006 |

---

## Open Questions

| ID | Question | Impact | Owner |
|---|---|---|---|
| Q-001 | Does onchain ever become legal source? | High — affects reconciliation and ADR | Legal/Product |
| Q-002 | Reconciliation cadence and SLA | Medium — affects architecture and infra | Product/Ops |

---
*Status: Draft — architect to review.*
