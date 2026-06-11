# Decision Log — I004 IT Portal

> Generated from initiative workspace. Last updated: 2026-06-11.
> Authoritative source is `planning/open-decisions.md` — this document is a readable narrative.

## Summary

| Stat | Count |
|---|---|
| Total decisions | 4 |
| Resolved | 0 |
| Open | 4 |
| Blocking | 2 |
| Deferred | 0 |

---

## Resolved decisions

No decisions have been resolved yet.

---

## Open decisions

| ID | Decision | Owner | Blocking? | Needed before | Notes |
|---|---|---|---|---|---|
| D-001 | Which CI/CD provider for MVP? GitHub Actions, Azure DevOps, or other? | Product Owner / Platform | No | Integration spike | Recommend GitHub Actions if org uses GitHub; Azure DevOps otherwise. Platform to confirm and run integration spike. |
| D-002 | Will the portal own any asset types, or does ServiceNow remain authoritative for all CMDB records? | Product Owner / Platform | **Yes** | Connector design and data contracts | Recommended: ServiceNow authoritative for MVP; defer portal ownership to later iteration. Must be confirmed before connector implementation begins. |
| D-003 | What is the audit retention policy and storage technology? (1 year / 3+ years / configurable; WORM / append-only store) | Security / Compliance | **Yes** | Handoff and infrastructure decisions | BRS default is 1 year. Security must define retention period and storage mechanism (append-only / WORM) with compliance justification. Questionnaire at `input/constraints/audit-retention.md`. |
| D-004 | Azure AD claim-to-role mapping approach: map Azure AD groups to portal roles, or use custom claims? | Platform / Identity | No | Auth PoC | Recommend group-to-role mapping (simpler). Platform to validate in SSO PoC and document mapping table. |

---

## Deferred decisions

No decisions deferred.

---

## Architecture decisions

Decisions that resulted in binding architecture rules:

| Rule ID | Decision | Rule summary | Enforcement |
|---|---|---|---|
| AR-001 | RBAC must be enforced at all API and UI boundaries | Least-privilege access for all endpoints and UIs | Automated tests + policy checks; verified with sample role mappings in PoC |
| AR-002 | ServiceNow is authoritative for CMDB records in MVP (pending D-002) | Portal treats CMDB as read-only and reconciles against ServiceNow sync | Connector contract enforces read-only; confirmed in architecture review once D-002 resolved |
| AR-010 | All external APIs use HTTPS with token-based auth | Security and NFR compliance — encryption in transit | Integration tests and CI policy; TLS required in infrastructure templates |
| AR-011 | Integration adapter presents a single internal contract per external system | Isolates vendor-specific logic and simplifies connectors | Contract tests and adapter unit tests; adapter documented in handoff |
| AR-012 | External integrations must declare data sensitivity and PII levels in contract metadata | Enables data-contract and masking decisions | Data-contract gate required before handoff |
| AR-020 | Audit events stored in append-only store with configurable retention and export | BRS mandates immutable audit trails (pending D-003) | Storage choice validated in `engineering-readiness`; infra templates must support WORM / immutability |
| AR-021 | Non-production environments use masked or synthetic data by default | BRS test-data policy and privacy requirements | CI pipelines include data-masking step; verified in readiness check |
| AR-030 | Secrets stored in Azure Key Vault and accessed via managed identities only | Prevents secret leakage and centralises rotation | Key Vault usage validated in infra templates and sample deployment |
| AR-031 | AI assistant-triggered actions require explicit approval and audit trail | Prevents unauthorised actions via AI assistant | BDD scenarios and security review must include audit verification |
| AR-040 | Environments defined for dev/qa/stg/prod with subscription and resource-group mapping in `engineering-readiness` | BRS specifies environments; infra mapping required for deployment planning | `engineering-readiness` entry required |
| AR-041 | Design for 99.9% availability using redundancy and autoscaling | Meets NFR-1 availability target | Infra templates and deployment plan must show AZs and autoscaling policies |

---

## Readiness decision

| Field | Value |
|---|---|
| Decision | Not ready |
| Date | 2026-06-11 |
| Blockers resolved | 0 of 2 |
| Conditions | D-002 (CMDB ownership) and D-003 (audit retention) must be resolved; five quality gates must be completed and accepted |
