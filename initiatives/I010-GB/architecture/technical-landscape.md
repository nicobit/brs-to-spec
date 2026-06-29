# Technical Landscape

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |


**Derived from:** `architecture/architecture-review.md` (derived, not verified)

---

## Landscape Summary

| Metric | Value |
|---|---|
| Total components | 14 |
| Existing | 5 |
| Proposed (new) | 9 |
| Repositories | needs-clarification |
| Integration points | Experian, HMRC, DocuSign, Temenos T24 |

---

## Repositories

| Name | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|
| needs-clarification | needs-clarification | needs-clarification | needs-clarification | needs-clarification | needs-clarification |

---

## Services

| Service | Repository | Status | Type | Technology | Responsibilities | Deployment Target |
|---|---|---|---|---|---|---|
| Web frontend (applicant portal) | needs-clarification | existing | ui | needs-clarification | Intake form, applicant status | needs-clarification |
| Intake API | needs-clarification | proposed | api | needs-clarification | Accept application payload, validate fields, assign ARN | needs-clarification |
| ARN service | needs-clarification | proposed | service | needs-clarification | Generate and persist ARNs | needs-clarification |
| Scoring pipeline | needs-clarification | proposed | service/pipeline | needs-clarification | Run scoring models, produce score and recommendation | needs-clarification |
| Explainability service | needs-clarification | proposed | service | needs-clarification | Produce and store model rationale | needs-clarification |
| AML/KYC orchestration | needs-clarification | proposed | service | needs-clarification | Coordinate AML screening and HMRC identity verification | needs-clarification |
| Underwriter dashboard | needs-clarification | proposed | ui/api | needs-clarification | Underwriter review and decision actions | needs-clarification |
| Disbursement orchestration | needs-clarification | proposed | service | needs-clarification | Trigger disbursement to Temenos T24 | needs-clarification |

---

## APIs

### Exposed APIs

| API | Service | Protocol | Status | Notes |
|---|---|---|---|---|
| Intake API | Intake API | REST | proposed | Accepts application submissions |

### Consumed APIs (External Integrations)

| Integration | Direction | Protocol | Contract Status | Circuit Breaker | Fallback |
|---|---|---|---|---|---|
| Experian CreditExpert | outbound | REST/HTTPS | existing-contract (assumed) | yes | route to underwriter |
| HMRC identity verification | outbound | REST/HTTPS | needs-clarification | yes | manual verification |
| DocuSign | outbound | REST/HTTPS | existing-contract (assumed) | yes | manual acceptance capture |
| Temenos T24 payment gateway | outbound/inbound | REST/AS2/partner | needs-clarification | yes | manual operational intervention |

---

## Data Stores

| Store | Type | Technology | Status | Owner Service | Notes |
|---|---|---|---|---|---|
| Immutable audit store | log/blob | needs-clarification | proposed | Explainability / Audit | Tamper-evident storage required |
| Event bus / logging | log/stream | needs-clarification | existing | All services | Structured events for observability |

---

## Infrastructure and Pipelines

| Component | Type | Status | Notes |
|---|---|---|---|
| CI/CD pipelines | ci-pipeline | needs-clarification | pipelines need defining per repository |
| Monitoring / APM | monitoring | existing | Integrate scoring telemetry and explainability metrics |

---

## System Inventory (structured)

```yaml
repositories: []
services: []
integrations:
	- name: Experian CreditExpert
		direction: outbound
		protocol: REST/HTTPS
		contract_status: existing-contract
		circuit_breaker: true
		fallback: route to underwriter
	- name: HMRC identity verification
		direction: outbound
		protocol: REST/HTTPS
		contract_status: needs-clarification
		circuit_breaker: true
		fallback: manual verification
	- name: DocuSign
		direction: outbound
		protocol: REST/HTTPS
		contract_status: existing-contract
		circuit_breaker: true
		fallback: manual acceptance capture
	- name: Temenos T24 payment gateway
		direction: outbound/inbound
		protocol: REST/partner
		contract_status: needs-clarification
		circuit_breaker: true
		fallback: manual operational intervention

data_stores: []
```

---

## Notes and Flags

- Repository mapping is `needs-clarification` for all components because `input/repository-context.md` is not present.
- Technology stacks and deployment targets are intentionally `needs-clarification` where not specified; do not assume repository names or hosting.
- This inventory is derived from the architecture review and must be verified with `input/repository-context.md` or engineering owners before implementation.


---
*Set Status: Draft — derived, not verified.*
