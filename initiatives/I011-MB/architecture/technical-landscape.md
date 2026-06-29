# Technical Landscape

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |
| Source basis | derived |

---

## Landscape Summary

| Metric | Value |
|---|---|
| Total components | 9 |
| Existing | 5 |
| Proposed (new) | 4 |
| Repositories | needs-clarification |
| Integration points | 3 |

---

## Repositories

| Name | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|
| needs-clarification | existing / proposed | api / ui / service / worker / library | needs-clarification | intake, scoring, underwriter UI, disbursement orchestration | needs-clarification |

---

## Services

| Service | Repository | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|---|
| Intake API | needs-clarification | proposed | api | .NET 8 (assumed) | Accept applicant data; validate; enqueue for scoring | Azure Container Apps |
| Scoring Service | needs-clarification | proposed | service | Python/ML runtime | Run pre-screening ML models; produce score and explainability artifacts | Containerized ML in Azure Kubernetes Service |
| Compliance / KYC Worker | needs-clarification | proposed | worker | Node.js | Call HMRC, sanctions lists; produce compliance flags | Azure Functions |
| Underwriter UI | needs-clarification | existing | ui | React | Underwriter decisioning and manual overrides | Azure Static Web Apps |
| Disbursement Orchestrator | needs-clarification | existing | service | Java | Integrate with Temenos T24 for disbursement | On-prem / VPN Gateway |

---

## APIs

### Exposed APIs

| API | Service | Protocol | Status | Notes |
|---|---|---|---|---|
| /applications | Intake API | REST | proposed | Intake endpoint for applicants |
| /scores/{id} | Scoring Service | REST | proposed | Returns score and explainability payload |

### Consumed APIs (External Integrations)

| Integration | Direction | Protocol | Contract Status | Circuit Breaker | Fallback |
|---|---|---|---|---|---|
| Experian CreditExpert | outbound | REST | existing-contract | yes | manual underwriter fallback |
| HMRC KYC API | outbound | HTTPS | needs-negotiation | yes | manual verification |
| Temenos T24 Disbursement | outbound | SOAP/REST | needs-negotiation | yes | queue + manual ops fallback |

---

## Data Stores

| Store | Type | Technology | Status | Owner Service | Notes |
|---|---|---|---|---|---|
| ApplicantDB | database | Azure SQL | existing | Intake API | PII stored in UK datacentre required |
| FeatureStore | database | Azure Cosmos DB | existing | Scoring Service | Feature store for ML models |
| ExplainabilityStore | blob | Azure Blob | proposed | Scoring Service | Store model explanations and traces |

---

## Infrastructure and Pipelines

| Component | Type | Status | Notes |
|---|---|---|---|
| CI pipeline | ci-pipeline | existing | Build-and-deploy pipelines in Azure DevOps; repository mapping needs-clarification |
| Monitoring | monitoring | existing | App Insights + Log Analytics for services |

---

## System Inventory (structured)

```yaml
repositories: []

services:
  - name: Intake API
    repository: needs-clarification
    status: proposed
    type: api
    tech: .NET 8 (inferred)
    responsibilities: ["accept applicant data", "validation", "enqueue for scoring"]
  - name: Scoring Service
    repository: needs-clarification
    status: proposed
    type: service
    tech: Python / ML runtime
    responsibilities: ["model scoring", "explainability payload"]
  - name: Compliance / KYC Worker
    repository: needs-clarification
    status: proposed
    type: worker
    tech: Node.js
    responsibilities: ["call HMRC", "sanctions checks"]
  - name: Underwriter UI
    repository: needs-clarification
    status: existing
    type: ui
    tech: React
    responsibilities: ["underwriter decisioning"]
  - name: Disbursement Orchestrator
    repository: needs-clarification
    status: existing
    type: service
    tech: Java
    responsibilities: ["integrate with T24", "orchestrate payments"]

integrations:
  - name: Experian CreditExpert
    direction: outbound
    protocol: REST
    contract_status: existing-contract
    circuit_breaker: true
    fallback: manual underwriter
  - name: HMRC KYC API
    direction: outbound
    protocol: HTTPS
    contract_status: needs-negotiation
    circuit_breaker: true
    fallback: manual verification
  - name: Temenos T24 Disbursement
    direction: outbound
    protocol: SOAP/REST
    contract_status: needs-negotiation
    circuit_breaker: true
    fallback: queued/manual ops

data_stores: []
  # see table above for stores
```

---

*Set Status: Draft — derived from `architecture/architecture-review.md` and initiative inputs.*
