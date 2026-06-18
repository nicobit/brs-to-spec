# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Created at | 2026-06-18 |
| Created by | Solutions Architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Boundary | All personal data and PII MUST remain in UK-only data regions. | Regulatory/GDPR requirement and residency constraint. | architecture/architecture-review.md / input/brs.md | System-wide |
| AR-002 | Security | All sensitive data at rest MUST be encrypted with AES-256 and in transit with TLS 1.3. | Protect customer data and meet compliance requirements. | input/brs.md | Data storage and transport |
| AR-003 | Integration | External credit and identity integrations (Experian, HMRC) MUST be isolated behind an integrations layer with circuit breakers and retry policies. | Prevent cascading failures and provide deterministic fallbacks. | architecture/architecture-review.md | Integrations |
| AR-004 | AI Explainability | AI scoring service MUST expose an explainability payload for every decision that includes feature attributions, score, and rule hits. | FCA explainability requirement and auditability. | architecture/architecture-review.md | AI Scoring Service |
| AR-005 | Observability | All scoring and decisioning flows MUST emit structured events for tracing and monitoring (submission, scoring, AML/KYC, underwriter decision, disbursement). | Ensure traceability and support SLA and audit requirements. | input/brs.md | System-wide |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-F01 | Direct database access from UI or third-party integrations | Bypasses API contracts, breaks auditability and RBAC boundaries | Use the Integration Layer and well-defined service contracts |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Application Intake | AR-001, AR-002, AR-005 |
| AI Scoring | AR-003, AR-004, AR-005 |
| Integrations (Experian, DocuSign, Temenos) | AR-003, AR-F01 |

---
*Set Status: Draft. Status will change to Accepted by workflow/human approval.*
