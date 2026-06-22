# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-N11 |
| Created at | 2026-06-22 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data | All personal data (PII) and audit data MUST be stored and processed only in Azure UK South or Azure UK West. | GDPR data residency requirement and BRS constraint | input/architecture.md; input/brs.md | All services handling PII |
| AR-002 | Security | All at-rest data SHALL use AES-256 encryption and all in-transit communication SHALL use TLS 1.3. | NFR-004 — protect PII and regulatory compliance | input/brs.md NFR-004 | Storage and network layers |
| AR-003 | Integration | All third-party integrations (Experian, HMRC, DocuSign, T24) MUST implement circuit-breakers with defined fallback behavior. | Maintain availability and predictable failure handling (NFR-007) | input/brs.md NFR-007 | Integration boundary layer |
| AR-004 | AI / Observability | AI scoring service MUST emit explainability metadata, correlationId, and idempotencyKey for every decision and include these in the audit trail. | FCA explainability requirement and traceability (FR-028) | input/brs.md FR-006..FR-007; architecture-review.md | AI Scoring Service, Audit Log |
| AR-005 | Deployment | All production resources and backups MUST be provisioned in UK regions only; no cross-region replication outside UK. | Data residency and regulatory compliance | input/architecture.md | Infrastructure provisioning |
| AR-006 | Forbidden Pattern | Do not persist raw credit bureau responses beyond the scoring pipeline; persist only derived score/summary. | Minimize sensitive data retention and reduce leakage risk | input/architecture.md; BRS constraints | Scoring pipeline and data store |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-006 | Persisting raw Experian responses in long-term storage | Exposes sensitive third-party data and increases compliance scope | Persist only derived summary and discard raw payloads after scoring write |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Scoring & Pre-screening | AR-003, AR-004, AR-006 |
| Data & Storage | AR-001, AR-002, AR-005 |
| Integrations | AR-003 |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
