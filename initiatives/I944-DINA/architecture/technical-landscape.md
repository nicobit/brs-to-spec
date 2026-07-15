# Technical Landscape

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I944-DINA |
| Created at | 2026-07-02 |
| Created by | architect |
| Status | Draft |
| Source basis | derived |

---

## Landscape Summary

| Metric | Value |
|---|---|
| Total components | 6 |
| Existing | 2 |
| Proposed (new) | 4 |
| Repositories | needs-clarification |
| Integration points | Chainlink CRE, Fund Admin API, Payment Gateway |

---

## Repositories

| Name | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|
| needs-clarification | proposed | service / api / worker | needs-clarification | Internal DTA workflow, investor registry, reconciliation | needs-clarification |

---

## Services

| Service | Repository | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|---|
| Internal DTA workflow engine | needs-clarification | proposed | service | needs-clarification | Order processing, state machine, orchestration | needs-clarification |
| Investor registry | needs-clarification | proposed | database / service | needs-clarification | Investor records, KYC references | needs-clarification |
| Reconciliation engine | needs-clarification | proposed | worker | needs-clarification | Reconciliation, reporting evidence generation | needs-clarification |
| Smart contract gateway / CRE adapter | needs-clarification | proposed | service | needs-clarification | Onchain execution, CRE interactions | needs-clarification |
| Fund Administrator interface | needs-clarification | existing | api | needs-clarification | Provide fund positions and records | needs-clarification |
| Payment gateway integration | needs-clarification | existing | integration | needs-clarification | Payment status and settlement | needs-clarification |

---

## APIs

### Exposed APIs

| API | Service | Protocol | Status | Notes |
|---|---|---|---|---|
| /orders | Internal DTA workflow engine | REST | proposed | Order submission and status |
| /positions | Investor registry | REST | proposed | Query investor positions |

### Consumed APIs (External Integrations)

| Integration | Direction | Protocol | Contract Status | Circuit Breaker | Fallback |
|---|---|---|---|---|---|
| Chainlink CRE | outbound | HTTPS / CRE | existing-contract | yes | retry/backoff |
| Fund Admin API | inbound | REST | needs-negotiation | yes | manual reconciliation |
| Payment Gateway | inbound | REST / webhook | existing-contract | yes | retry/backoff |

---

## Data Stores

| Store | Type | Technology | Status | Owner Service | Notes |
|---|---|---|---|---|---|
| Investor registry DB | database | needs-clarification | proposed | Investor registry | PII offchain; store hashes for onchain references |
| Reconciliation store | blob / db | needs-clarification | proposed | Reconciliation engine | Reconciliation snapshots and evidence |

---

## Infrastructure and Pipelines

| Component | Type | Status | Notes |
|---|---|---|---|
| CI/CD pipeline | deployment | needs-clarification | Pipeline required for deployment and migrations |
| Monitoring & logging | monitoring | existing / proposed | Observability for reconciliation and CRE calls |

---

## System Inventory (structured)

```yaml
repositories: []
services:
  - name: internal-dta-workflow
    repository: needs-clarification
    status: proposed
    type: service
    tech: needs-clarification
    responsibilities:
      - order-processing
      - orchestration

integrations:
  - name: chainlink-cre
    direction: outbound
    protocol: https
    contract_status: existing-contract
    circuit_breaker: true
    fallback: retry

data_stores: []
```

---

*Note: `Source basis` set to `derived` — no `input/repository-context.md` provided, repository names intentionally set to `needs-clarification` per policy.*
