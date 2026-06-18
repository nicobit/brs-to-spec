# Initiative Context

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Delivery mode | OpenSpec |
| Execution mode | Enterprise+Modular |
| AI model version | unspecified |
| Created at | 2026-06-16 |
| Created by | engineering-lead |
| Status | Accepted |

> Load this file first. It is the compact binding context for downstream implementation, review, and handoff work.

## Technology Constraints

| Area | Technology | Version / Constraint | Source |
|---|---|---|---|
| Backend language | Python / .NET (team choice) | N/A | repository / architecture notes |
| Backend framework | FastAPI / ASP.NET Core | N/A | architecture review |
| Database | Cosmos DB (append-only for audit) | AZURE COSMOS APPEND-ONLY | architecture rules AR-005 |
| Deployment target | Azure UK South (primary), UK West (DR) | Data residency enforced | AR-001 |
| Auth mechanism | Azure AD / Managed Identities | No secrets in code | AR-002 |
| Message bus | Azure Service Bus | Durable messaging | architecture review |

## Architecture Rules in Force

| AR-NNN | Rule (verbatim) | Scope |
|---|---|---|
| AR-001 | All services and data stores must be provisioned in Azure UK South (primary) and UK West (DR) only. | All / feature area |
| AR-002 | All service-to-service calls must use managed identities; no secrets in code or config. | All / feature area |
| AR-003 | Use Azure API Management as the single ingress point; apply WAF and rate limits per API. | All / feature area |
| AR-004 | PII must be encrypted at rest (AES-256) and masked in logs; PII in third-party integrations must be transient or redacted. | All / feature area |
| AR-005 | All state transitions and critical actions must emit immutable audit entries to the Audit Log Store (append-only Cosmos DB). | All / feature area |
| AR-006 | Emit structured telemetry for key events (submission, scoring, decisioning, offer, disbursement) with correlation id. | All / feature area |
| AR-007 | External integrations (Experian, DocuSign, T24) must implement circuit breakers and retries with bounded backoff; fallback behaviours must be defined (e.g., REFER_TO_UNDERWRITER). | All / feature area |
| AR-008 | AI Scoring Service must meet 60s SLA for scoring under normal load and be autoscalable; define performance tests and warm-pool strategy. | All / feature area |
| AR-009 | Audit records retention policy to be defined; transactional PII retention limited per legal requirements; implement automated purging where applicable. | All / feature area |
| AR-010 | APIs must enforce RBAC via Azure AD; admin and underwriter roles limited by least privilege. | All / feature area |

## Governed Boundaries

| Boundary | Type | Owner | Contract Location |
|---|---|---|---|
| Applicant Portal / APIs | API / Data | Portal / API teams | quality-gates/api-contract.md |
| Audit Store | Data | Platform / Ops | architecture/architecture-rules.md |

## Active Quality Gates

| Gate | Status | Artifact path |
|---|---|---|
| BDD Scenarios | Required - Accepted | quality-gates/bdd/ |
| Test Strategy | Required - Accepted | quality-gates/test-strategy.md |
| Security Review | Required - Accepted | quality-gates/security-review.md |
| API Contract | Required - Accepted | quality-gates/api-contract.md |
| Observability Plan | Required - Accepted | quality-gates/observability-plan.md |

## Rollback and Regression Sensitivity

| Dimension | Assessment | Reason |
|---|---|---|
| Rollback possible? | Partial | Cross-service state (audit store) requires coordinated rollback |
| Regression surface | Medium | Integrations and AI scoring introduce non-determinism |
| Regression risk components | AI scoring, Experian integration, T24 integration | |

## Open Risks

| Risk | Impact | Accepted by | Mitigation |
|---|---|---|---|
| Vendor SLA shortfall (Experian) | Delays in scoring → manual hold | Product/PO | Define fallback (refer to underwriter) and monitor SLAs |

## Carried-Forward Context

### Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| UK-only data residency required | Business intake | Engage Legal & Security for exemptions |

### Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact scoring model infra requirements | Performance & cost | Performance spike testing during sprint 2 |

---

*Update this file only when architecture, readiness, or gates change materially.*
