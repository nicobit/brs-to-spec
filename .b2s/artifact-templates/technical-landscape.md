# Technical Landscape

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | architect |
| Status | Draft |
| Source basis | {{source_basis}} |

*Set `Source basis` to `verified` if `input/repository-context.md` was available, or `derived` if the landscape was inferred from the architecture review only.*

---

## Landscape Summary

| Metric | Value |
|---|---|
| Total components | |
| Existing | |
| Proposed (new) | |
| Repositories | |
| Integration points | |

---

## Repositories

| Name | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|
| | existing / proposed | api / ui / service / worker / library | | | |

---

## Services

| Service | Repository | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|---|
| | | existing / proposed | api / worker / background / gateway | | | |

---

## APIs

### Exposed APIs

| API | Service | Protocol | Status | Notes |
|---|---|---|---|---|
| | | REST / gRPC / GraphQL | existing / proposed | |

### Consumed APIs (External Integrations)

| Integration | Direction | Protocol | Contract Status | Circuit Breaker | Fallback |
|---|---|---|---|---|---|
| | outbound / inbound | REST / AMQP / HTTPS | existing-contract / needs-negotiation | yes / no | |

---

## Data Stores

| Store | Type | Technology | Status | Owner Service | Notes |
|---|---|---|---|---|---|
| | database / cache / queue / blob / log | | existing / proposed | | |

---

## Infrastructure and Pipelines

| Component | Type | Status | Notes |
|---|---|---|---|
| | ci-pipeline / deployment / monitoring / gateway | existing / proposed | |

---

## System Inventory (structured)

```yaml
repositories: []
#  - name: ""
#    status: existing | proposed
#    type: api | ui | service | worker | library
#    tech: ""
#    responsibilities: []
#    deployment_target: ""

services: []
#  - name: ""
#    repository: ""
#    status: existing | proposed
#    type: api | worker | background | gateway
#    tech: ""
#    responsibilities: []

integrations: []
#  - name: ""
#    direction: outbound | inbound
#    protocol: ""
#    contract_status: existing-contract | needs-negotiation
#    circuit_breaker: true | false
#    fallback: ""

data_stores: []
#  - name: ""
#    type: database | cache | queue | blob | log
#    tech: ""
#    status: existing | proposed
#    owner_service: ""
```

---

*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
