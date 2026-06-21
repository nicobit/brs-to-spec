# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I988-N8 |
| Created at | 2026-06-21 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data | All PII and audit data must reside only in UK datacenters and use AES-256 at rest and TLS1.3 in transit. | Regulatory GDPR/FCA requirements and delivery constitution. | architecture-review.md / delivery-constitution.md | All services storing PII or audit data |
| AR-002 | Security | All service-to-service authentication must use managed identities; no embedded secrets in code or config. | Prevent secret leakage and ensure least-privilege. | architecture-review.md / delivery-constitution.md | All backend services and CI/CD pipelines |
| AR-003 | Observability | AI scoring must emit explainability and input provenance with each decision (score, rationale, contributing features). | Auditability and regulator explainability requirements. | architecture-review.md / REQ-004 | AI Scoring Service and downstream stores |
| AR-004 | Data | Experian credit data must be transient and not persisted beyond the scoring pipeline; any persisted derivative must be approved by Compliance. | Minimize retention of third-party PII and reduce residency risk. | architecture-review.md / REQ-005 | Scoring pipeline and data stores |
| AR-005 | Integration | Disbursement instructions to T24 must include confirmation and reconciliation hooks; adapter must support idempotency and retry semantics. | Financial reconciliation and settlement safety. | architecture-review.md / REQ-012 | Payment/disbursement adapters |
| AR-006 | Forbidden Pattern | Do not deploy black-box models without explainability outputs and test coverage for input transformations. | Prevent un-auditable AI decisions and regulatory exposure. | architecture-review.md / delivery-constitution.md | AI model deployment pipelines |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-006 | Deploying AI model without explainability exports or provenance | Regulatory non-compliance and auditability failure | Require explainability exporter and model contract tests |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Intake & Submission | AR-001, AR-002 |
| AI Scoring | AR-003, AR-004, AR-006 |
| Compliance & AML/KYC | AR-001, AR-004 |
| Disbursement | AR-005, AR-001 |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
