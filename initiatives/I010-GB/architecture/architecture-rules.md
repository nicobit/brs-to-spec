# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data | All production personal data MUST reside in UK datacenters. | Legal requirement: UK GDPR and data residency constraints. | architecture/architecture-review.md (ARCH-C-001) | All services handling PII |
| AR-002 | Integration | Use Experian CreditExpert for credit reports; implement a credit adapter with circuit-breaker. | Enterprise supplier contract and resilience requirement. | architecture/architecture-review.md (ARCH-C-002) | Scoring pipeline, compliance flows |
| AR-003 | Integration / Security | Use DocuSign for e-signatures and capture timestamp and IP for acceptance records. | Enterprise contract and audit traceability for acceptance. | architecture/architecture-review.md (ARCH-C-003) | Offer acceptance flows |
| AR-004 | Integration / Boundary | Disbursement must integrate with Temenos T24 via the internal payment gateway; adapter must support idempotency and retry semantics. | Core banking integration requirement; avoids duplicate disbursements and operational risk. | architecture/architecture-review.md (ARCH-C-004) | Disbursement orchestration |
| AR-005 | AI / Security | All automated decision models used in scoring must produce explainability artifacts (rationale, feature contributions) compatible with FCA review and be retained in the audit store. | Regulatory requirement for explainability and auditability. | architecture/architecture-review.md (ARCH-C-005) | Scoring pipeline, audit store |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-F01 | Storing production PII in non-UK regions | Violates UK data residency / GDPR | Use UK-only storage endpoints and region-restricted services |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| AI Pre-Screening & Scoring | AR-002, AR-005 |
| AML / KYC / Compliance | AR-002, AR-005 |
| Disbursement | AR-004 |
| Intake & Portal | AR-001, AR-F01 |
| Observability & Audit | AR-005 |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
