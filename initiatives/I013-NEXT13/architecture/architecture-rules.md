# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data | All PII and audit records MUST be stored and processed only in UK-hosted infrastructure and storage services. | Compliance with GDPR and UK data residency requirements. | architecture/architecture-review.md; input/brs.md | All services handling PII and audit data |
| AR-002 | Security / AI | All decisioning models and pipelines MUST produce an explainable output for each recommendation; black-box-only models are not permitted. | FCA explainability requirement and regulatory auditability. | architecture/architecture-review.md; input/brs.md | Scoring and decisioning services |
| AR-003 | Integration | All Experian and DocuSign integrations MUST use enterprise-approved contracts and connectors; do not introduce alternative vendor bindings without procurement approval. | Maintain contractual compliance and reduce procurement risk. | architecture/architecture-review.md; input/brs.md | External vendor integrations |
| AR-004 | Data / Audit | The system MUST provide an immutable, tamper-evident audit trail for all application state transitions and decision artifacts. | Regulatory auditability and forensic trace requirements. | architecture/architecture-review.md; input/brs.md | Audit storage and state transition recording |
| AR-005 | Integration / Performance | Integration points with Experian, HMRC and Temenos T24 MUST meet declared SLA windows or degrade to safe, auditable fallbacks (e.g., refer-to-underwriter). | To meet decision-time objectives and preserve user experience under external failures. | architecture/architecture-review.md; input/brs.md | External integrations and scoring pipeline |
| AR-006 | Integration / Reliability | Disbursement orchestrator MUST be idempotent and require explicit acknowledgment semantics from the payment gateway; support staged/shadow mode for rollout. | Prevent incorrect or duplicate disbursements and enable safer rollouts into core banking. | architecture/architecture-review.md | Disbursement / payment integration |
| AR-007 | Performance / Scalability | Applicant-facing intake flows MUST remain lightweight; heavy validation should be asynchronous and back-pressured to protect scoring pipelines. | Protect UX and avoid cascading failures in downstream services. | architecture/architecture-review.md | Intake and validation subsystem |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-F-001 | Storing PII in non-UK regions | Violates data residency and GDPR constraints | Use UK-only storage accounts and services |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Application intake & validation | AR-007 |
| AI scoring & decisioning | AR-002, AR-005 |
| Compliance (AML / KYC) | AR-005, AR-004 |
| Offer & disbursement | AR-006, AR-003 |
| Observability & audit | AR-004 |

---
*Set Status: Draft — derived from `architecture/architecture-review.md`.*
