# Solution Decisions

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I944-DINA |
| Created at | 2026-07-02 |
| Created by | architect |
| Status | Draft |

---

## Decision Summary

| Metric | Value |
|---|---|
| Total decisions | 7 |
| Create new | 4 |
| Modify existing | 0 |
| Extend existing | 2 |
| Reuse as-is | 1 |
| New repositories | 4 |
| Flagged conflicts | 0 |

---

## Service Decisions

| ID | Component | Decision | Target Repository | Technology | Rationale | AR Constraints |
|---|---|---|---|---|---|---|
| SD-001 | Reconciliation Engine | create-new | needs-clarification | needs-clarification | Needed to compare internal ledger and onchain state and produce evidence | AR-002 |
| SD-002 | Investor Registry | create-new | needs-clarification | needs-clarification | Central golden record for investor attributes and KYC references | AR-001, AR-002 |
| SD-003 | Smart contract gateway / CRE adapter | create-new | needs-clarification | needs-clarification | Interface to Chainlink CRE and onchain contracts | AR-004 |
| SD-004 | Evidence store | create-new | needs-clarification | needs-clarification | WORM-capable store for reconciliation snapshots and audit evidence | AR-002 |
| SD-005 | Fund Admin integration | reuse-as-is | external/fund-admin | existing | Use existing fund admin APIs; adapt via adapters | AR-002 |
| SD-006 | Internal DTA workflow engine | extend-existing | needs-clarification | needs-clarification | Extend workflow to record new order states and event emissions | AR-002 |

---

## API Decisions

| ID | API / Endpoint | Decision | Target Service | Protocol | Versioning | Rationale |
|---|---|---|---|---|---|---|
| SD-007 | /orders | create-new | Internal DTA workflow engine | REST | v1 | Order submission and state tracking |

---

## Data Decisions

| ID | Schema / Table | Decision | Target Data Store | Migration Strategy | Rationale |
|---|---|---|---|---|---|
| SD-008 | Internal ledger snapshot | create-new | Evidence store / Investor Registry | additive | Capture snapshots for reconciliation and audit |

---

## Integration Decisions

| ID | Integration | Decision | Contract Approach | Test Strategy | Rationale |
|---|---|---|---|---|---|
| SD-009 | Chainlink CRE | extend-existing | existing-contract | contract tests via CRE sandbox | Use CRE for orchestration; keep policy offchain |
| SD-010 | Fund Admin API | extend-existing | adapter / needs-negotiation | integration tests; data contracts | Consume fund admin exports; adapter required |

---

## Repository Summary

| Repository | Status | Technology | Deployment Target | Decisions |
|---|---|---|---|---|
| needs-clarification | new | needs-clarification | needs-clarification | SD-001, SD-002, SD-003, SD-004, SD-006, SD-007, SD-008 |

---

## Architecture Rule Compliance

| Decision | AR Rule | Status | Notes |
|---|---|---|---|
| SD-002 | AR-001 | compliant | ensures PII offchain |
| SD-003 | AR-004 | compliant | enforces allowlists and audit logging |

---

## UI Decisions

No UI changes are required for the initial DTA MVP scope. Any frontend work (investor portals or ops UI) will be handled during epic elaboration and is out of scope for this document.
 
| ID | Page / Module | Decision | Target Application | Routing | Rationale |
|---|---|---|---|---|---|
| SD-000 | None (MVP) | reuse-as-is | n/a | n/a | No UI changes required for initial scope |
## Infrastructure Decisions

CI/CD and monitoring requirements are recognized but require repository-level decisions. Create lightweight pipelines per new repository with monitoring and alerts for CRE interactions; final pipeline definitions will be finalized during delivery planning once repositories are confirmed.

| ID | Component | Decision | Target | CI/CD | Rationale |
|---|---|---|---|---|---|
| SD-INF-001 | CI/CD pipelines | create-new | needs-clarification | new-pipeline | Create lightweight pipelines per new repository; defer finalization to delivery planning |

## Open Solution Design Questions

| ID | Question | Affects Decision(s) | Blocking? | Required Before | Status |
|---|---|---|---|---|---|
| SDQ-001 | Does onchain ever become legal source? | SD-002, SD-004 | Yes | delivery-planning | open |
| SDQ-002 | Reconciliation cadence and SLA | SD-001 | No | epic-elaboration | open |

---

## Carried-Forward Open Questions

| ID | Question | From | Impact | Owner |
|---|---|---|---|---|
| Q-001 | Does onchain ever become legal source? | architecture-review | High | Legal/Product |
| Q-002 | Reconciliation cadence and SLA | impacted-systems | Medium | Product/Ops |

---
*Status: Draft — architect to review.*
