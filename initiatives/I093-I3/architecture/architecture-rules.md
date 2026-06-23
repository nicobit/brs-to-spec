# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I093-I3 |
| Created at | 2026-06-22 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data Residency / Security | All production PII and audit data must be stored and processed only in UK-hosted environments and encrypted at rest (AES-256) and in transit (TLS 1.3). | Regulatory compliance (GDPR, FCA) and delivery constitution | architecture/architecture-review.md; input/brs.md (Constraints) | All services handling PII |
| AR-002 | Integration / Availability | Experian CreditExpert integration is mandatory for credit reports; when Experian is unavailable, applications must be routed to underwriter queue or manual processing with clear telemetry. | Contractual dependency and resilience requirement | input/brs.md (FR-009); architecture/architecture-review.md | Scoring pipeline, intake adapters |
| AR-003 | Core Banking Integration | Disbursement must use the existing Temenos T24 payment gateway adapter and follow established message contracts; any change requires ADR. | Existing core banking constraint and operational safety | input/brs.md (Constraints); architecture/architecture-review.md | Disbursement and reconciliation flows |
| AR-004 | AI Explainability | Any AI model used for automated recommendations must provide per-decision explainability artifacts sufficient for underwriter review and regulatory audit; opaque black-box models without explainability are forbidden. | FCA explainability requirement and human oversight | input/brs.md (Constraints); architecture/architecture-review.md | Scoring and model registry |
| AR-005 | Circuit Breakers / Fallbacks | All external API calls (Experian, HMRC, DocuSign) must implement circuit breakers, retry policies, and deterministic fallback routing with observability events emitted. | Prevent cascading failures and ensure traceability | architecture/architecture-review.md | Integration adapters |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-F-001 | Persisting PII to non-UK regions (cloud storage or backups) | Violates data residency and GDPR | Use UK regions only; if off-shore processing required, obtain legal approval and implement data minimisation |
| AR-F-002 | Using opaque, uninterpretable ML models for automated approval decisions | Violates explainability and regulatory requirements | Require interpretable models or explainability layer; limit to human-in-the-loop for automated decisions |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Application Intake | AR-001, AR-002, AR-005 |
| AI Pre-screening & Scoring | AR-004, AR-005, AR-001 |
| Integrations (Experian, HMRC, DocuSign) | AR-002, AR-005 |
| Disbursement (T24) | AR-003, AR-005 |
| Observability & Audit | AR-001, AR-005 |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
