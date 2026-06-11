# Architecture Rules

These rules are derived from the reviewed draft architecture and BRS for I004 — IT Portal. Each rule is actionable, has an owner, and explains enforcement or validation during readiness/handoff.

## Principles

| Rule ID | Rule | Rationale | Owner | Enforcement / Validation |
|---|---|---|---|---|
| AR-001 | Follow least-privilege and role-based access for all API endpoints and UIs | BRS requires RBAC and auditability; reduces blast radius | Platform / Security | Automated tests + policy checks; verify with sample role mappings in PoC |
| AR-002 | Treat ServiceNow as authoritative for tickets and CMDB for MVP (no portal ownership of CMDB records) | Minimizes data duplication and reconciliation risk for MVP (aligned to BRS) | Product Owner / Platform | Confirmed in architecture review (D-002). Enforce via connector contract and read-only sync for MVP |

## API Rules

| Rule ID | Rule | Rationale | Owner | Enforcement / Validation |
|---|---|---|---|---|
| AR-010 | All external-facing APIs must use HTTPS and enforce token-based auth (OIDC/SAML for user flows) | Security and NFRs (encryption in transit) | Platform / Security | Integration tests & CI policy; TLS required in infra templates |
| AR-011 | Integration adapter must present a single internal contract for external systems (ServiceNow, CI, Monitoring) | Simplifies connectors and isolates vendor-specific logic | Platform | Contract tests and adapter unit tests; adapter documented in handoff |
| AR-012 | All external integrations must declare data sensitivity and PII levels in their contract metadata | Enables data-contract and masking decisions | Product Owner / Security | Data-contract artifact required before handoff; gate: data-contract.md |

## Data Rules

| Rule ID | Rule | Rationale | Owner | Enforcement / Validation |
|---|---|---|---|---|
| AR-020 | Audit events must be stored in an append-only store with configurable retention and export capability | BRS mandates immutable audit trails and exportability | Security / Platform | Validate storage choice and retention in `engineering-readiness`; infra templates must support immutability or WORM features |
| AR-021 | Non-production environments must use masked or synthetic data by default | BRS test-data policy and privacy requirements | Platform / QA | CI pipelines must include data-masking step; readiness check verifies masked datasets |

## Security Rules

| Rule ID | Rule | Rationale | Owner | Enforcement / Validation |
|---|---|---|---|---|
| AR-030 | Secrets must be stored in Azure Key Vault and accessed via managed identities only | Prevents secret leakage and centralizes rotation | Platform / Security | Validate Key Vault usage in infra templates and sample deployment; readiness gate checks Key Vault access patterns |
| AR-031 | Any feature that allows assistant-triggered actions must include an explicit approval and audit trail | Prevents unauthorized actions via AI assistant and supports audit requirements | Product Owner / Security | Feature checklist and BDD scenarios; gate: security-review.md and BDD scenarios must include audit verification |

## Deployment Rules

| Rule ID | Rule | Rationale | Owner | Enforcement / Validation |
|---|---|---|---|---|
| AR-040 | Environments must be defined for dev/qa/stg/prod with subscription and resource-group mapping documented in `engineering-readiness` | BRS specifies environments; infra mapping required to plan deployments | Platform / Delivery Lead | `engineering-readiness` entry required; infra IaC templates reference mappings |
| AR-041 | Design for 99.9% availability in primary region using redundancy and autoscaling patterns | Meets NFR-1 availability target | Platform / SRE | Architecture review confirmed; infra templates and deployment plan must show AZs and autoscaling policies |

## Contracts & Gates

| Rule ID | Rule | Trigger | Required artifact / gate |
|---|---|---|---|
| AR-C1 | Integration contract for ServiceNow must be agreed before connector implementation | When integrating with ServiceNow | `quality-gates/data-contract.md` and integration spike deliverables |
| AR-C2 | Audit retention policy must be defined before handoff | Before handoff / production deployment | `engineering-readiness/readiness-check.md` and `architecture/architecture-review.md` update (D-003) |

## Open decisions referenced

- D-001 — CI/CD provider selection (affects webhook contract and adapter implementation). Owner: Product Owner / Platform.
- D-002 — CMDB ownership and reconiliation strategy. Owner: Product Owner / Platform. Blocking: yes for connector design.
- D-003 — Audit retention policy and storage choice. Owner: Security / Compliance. Blocking: yes before handoff.
- D-004 — Claim-to-role mapping approach for Azure AD. Owner: Platform/Identity.

## Review notes

These rules are derived from the architecture review and BRS. They must be reviewed and signed off by the architect and Product Owner. Rules that require vendor or policy input are marked with owners and gating artifacts.
