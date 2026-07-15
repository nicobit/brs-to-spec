# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I944-DINA |
| Created at | 2026-07-02 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Category | Rule Statement | Rationale | Source | Scope |
|---|---|---|---|---|---|
| AR-001 | Data | Personal and KYC data must remain offchain; only hashes/attestations onchain | Regulatory/privacy and audit requirements | architecture/architecture-review.md | All |
| AR-002 | Boundary | Internal DTA golden record is authoritative unless ADR specifies otherwise | Legal ownership and auditability | architecture/architecture-review.md | Reconciliation, Reporting |
| AR-003 | Deployment | Initial rollout restricted to one controlled fund and one controlled chain; ADR required to expand | Reduce blast radius and risk for first release | architecture/architecture-review.md | Deployment |
| AR-004 | Security | Wallets and operator actions must be allowlisted and audited; access controls enforced | Prevent unauthorized onchain actions | architecture/architecture-review.md | Integration / Smart contract gateway |

## Forbidden Patterns

| AR-NNN | Forbidden Pattern | Why Forbidden | Alternative |
|---|---|---|---|
| AR-F-001 | Store PII onchain | Regulatory and privacy risk | Store hashes / attestations offchain and reference them onchain |

## Coverage

| Feature Area | Governing AR-NNN Rules |
|---|---|
| Onchain integration | AR-001, AR-002, AR-004 |
| Reconciliation & reporting | AR-002 |
| Deployment & rollout | AR-003 |

---
*Status: Draft — architect to review.*
