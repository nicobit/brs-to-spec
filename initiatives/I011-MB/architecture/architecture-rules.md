# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data / Boundary | All personal data must remain in UK datacentres | UK GDPR and data residency requirements | architecture/architecture-review.md (ARCH-C-001) | All |
| AR-002 | Integration | Experian CreditExpert must be used for credit reports | Enterprise contract requirement | architecture/architecture-review.md (ARCH-C-002) | Scoring pipeline |
| AR-003 | AI / Security | AI models must be explainable and auditable; model decisions must include traceable features | FCA explainability requirements; auditability for regulatory review | architecture/architecture-review.md (ARCH-C-003) | Scoring & ML services |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-101 | Storing PII outside UK datacentres | Violates AR-001 and regulatory requirements | Use UK-region storage or pseudonymize before export |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Scoring / ML | AR-002, AR-003 |
| Data residency | AR-001, AR-101 |
| Integrations / Disbursement | AR-002 |

---
*Set Status: Draft — for architecture-rules and downstream engineering.*
