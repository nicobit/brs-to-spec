# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Created at | 2026-06-16 |
| Created by | architect (draft) |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Owner | Affects |
|---|---|---|---|---|---|
| AR-001 | Deployment | All services and data stores must be provisioned in Azure UK South (primary) and UK West (DR) only. | Satisfy GDPR / data residency constraints. | Architect | All components, storage |
| AR-002 | Identity & Access | All service-to-service calls must use managed identities; no secrets in code or config. | Reduce secret sprawl and improve rotation. | Security | APIs, functions, services |
| AR-003 | Ingress | Use Azure API Management as the single ingress point; apply WAF and rate limits per API. | Centralize auth, throttling, and protection. | Architect | Applicant Portal, APIs |
| AR-004 | Data Protection | PII must be encrypted at rest (AES-256) and masked in logs; PII in third-party integrations must be transient or redacted. | Compliance and privacy. | Security | Data stores, logs, integrations |
| AR-005 | Auditability | All state transitions and critical actions must emit immutable audit entries to the Audit Log Store (append-only Cosmos DB). | Forensic and regulatory needs. | Architect | Audit system |
| AR-006 | Observability | Emit structured telemetry for key events (submission, scoring, decisioning, offer, disbursement) with correlation id. | Enables tracing and SLAs. | Ops | Event pipeline, monitoring |
| AR-007 | Integration Resilience | External integrations (Experian, DocuSign, T24) must implement circuit breakers and retries with bounded backoff; fallback behaviours must be defined (e.g., REFER_TO_UNDERWRITER). | Prevent cascading failures and ensure graceful degradation. | Architect / Dev | Integration adapters |
| AR-008 | Performance | AI Scoring Service must meet 60s SLA for scoring under normal load and be autoscalable; define performance tests and warm-pool strategy. | Meets business requirement FR-006 and NFR-002. | AI Team | AI service |
| AR-009 | Data Retention | Audit records retention policy to be defined; transactional PII retention limited per legal requirements; implement automated purging where applicable. | Cost and compliance management. | Ops / Legal | Audit store, DBs |
| AR-010 | Secure Defaults | APIs must enforce RBAC via Azure AD; admin and underwriter roles limited by least privilege. | Principle of least privilege. | Security | API gateway, services |

## Rule Enforcement

- CI/CD pipeline must include policy checks (IaC scanning) for `AR-001`, `AR-002`, and `AR-004`.  
- Automated tests and synthetic monitors enforce `AR-006` and `AR-008`.  
- Integrations must publish SLAs and fallback behaviours documented in the integration catalog.

## Exceptions

- Any exception to `AR-001` (data residency) must be approved by Security & Legal and logged as an OD (open decision).

---

*Set Status: Accepted only by workflow or human approval when applicable.*
