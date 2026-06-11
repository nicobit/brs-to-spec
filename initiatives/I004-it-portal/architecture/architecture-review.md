# Architecture Review — I004: IT Portal

> Primary consumer: Architect, tech lead, delivery lead
> Purpose: confirm architecture constraints, alignment, conflicts, and decisions that shape delivery
> Downstream use: architecture rules, delivery structure, readiness, governed contract decisions

## Metadata

| Field | Value |
|---|---|
| Initiative | I004 - IT Portal |
| Architecture input | `input/architecture.md` |
| Reviewer | (TBD) |
| Review date | 2026-06-11 |
| Status | Approved with conditions |

## Constraints identified

| Constraint ID | Constraint | Source | Impact on delivery |
|---|---|---|---|
| C-001 | Audit trail must be append-only and exportable | FR-10, NFR-5 (BRS) | Requires append-only storage selection, export tooling, and retention policy before handoff |
| C-002 | SSO via Azure AD and group mapping for RBAC | FR-1 (BRS) | Implementation of SAML/OIDC integration and group-to-role mapping in auth layer |
| C-003 | Test-data masking in non-prod | Data & Privacy (BRS) | Requires masked/synthetic datasets and test-data pipeline for dev/qa; impacts CI pipelines and seeded data |
| C-004 | High availability (99.9%) for primary region | NFR-1 (BRS) | Design for redundancy, autoscaling, and deployment across AZs; affects infra and runbook requirements |

## Existing system impact

| System / Component | Impact | Risk | Required action | Owner |
|---|---|---|---|---|
| ServiceNow (Ticketing & CMDB) | Bi-directional sync and linking from portal; portal will not initially own CMDB | High — data-model mismatches, reconciliation risks | Confirm contract, API quotas, and reconciliation strategy; create connector spike | Platform/PO |
| Azure AD | SSO and group claims mapping required | Medium — claim mapping and group sync complexity | Validate IdP claim structure and test SSO PoC | Platform/Identity |
| CI/CD provider (unspecified) | Build linking and webhook integration required | Medium — webhook formats and auth vary | Select provider (D-001) and validate webhook/ API contract | Platform/PO |

## Integration review

| Integration | Protocol | Contract status | Risk | Required action |
|---|---|---|---|---|
| ServiceNow (tickets & CMDB) | REST API, webhooks, scheduled sync | Unknown / Not negotiated | High (PII, rate limits, schema drift) | Confirm API capabilities, data schemas, and ownership (D-002). Create integration spike. |
| Azure AD (auth) | SAML / OIDC | Existing | Medium | Confirm group-to-role mapping approach and test. |
| CI/CD (build status) | Webhooks / API | Unknown | Medium | Confirm provider and webhook format (D-001). |
| Monitoring | SDK / API | Existing | Low | Configure App Insights + alerts in infra plan. |

## Data and residency

| Data entity | Owner | PII? | Residency requirement | Risk |
|---|---|---|---|---|
| Audit records | Portal / Security | May include user identifiers | Retention per policy (D-003) | High — retention and access controls must be defined |
| CMDB records (synced) | ServiceNow (authoritative) | Varies | As per CMDB policy | Medium — reconciliation and mapping risk |
| Request & change metadata | Portal | Low | Standard residency (TBD) | Medium |

## Deployment and infrastructure

| Area | Current state | Change required | Risk | Owner |
|---|---|---|---|---|
| Environments | dev/qa/stg/prod defined in BRS | Need subscription/rg mapping recorded in `engineering-readiness` | Medium — missing infra mapping delays deployment | Platform/PO |
| Secrets management | Key Vault recommended | Integrate managed identity and Key Vault access patterns | Medium | Platform/Security |
| Audit store | Not specified (draft suggests append-only store) | Decide storage technology and retention (D-003) | High | Security/Platform |

## Observability and operations

| Concern | Required? | Gap | Owner |
|---|---|---|---|
| Telemetry & tracing | Yes — App Insights / Prometheus | Instrumentation plan and dashboards missing | Platform/Observability |
| Runbooks availability | Yes — tied to incidents and changes | Runbook storage and linkage need implementation plan | Ops/Platform |
| Alerting & on-call | Yes | No on-call runbooks or escalation policy documented | Ops/SRE |

## BRS alignment

| Requirement | Alignment | Gap / conflict | Decision needed |
|---|---|---|---|
| FR-1 Authentication & Authorization | Aligned — Azure AD chosen in draft | Need claim mapping details and admin flows | D-004: Approve claim-to-role mapping approach (Owner: Platform/Identity) |
| FR-5 CMDB Integration | Aligned as read-only for MVP | Ownership of certain asset types unclear — may require portal-side ownership decisions (D-002) | D-002 |
| FR-10 Audit & Compliance | Aligned conceptually | Retention and storage mechanism undefined (D-003) | D-003 |

## Conflicts

| Conflict | Between | Impact | Owner | Resolution needed by |
|---|---|---|---|---|
| CMDB ownership and write-back | PO/Platform expectations vs ServiceNow authority | High — affects data contracts and reconciliation | Product Owner / Platform | Before connector implementation |

## Open decisions

| Decision ID | Question | Options | Recommended | Owner | Blocking? | Required before |
|---|---|---|---|---|---|---|
| D-001 | Which CI/CD provider for MVP? | GitHub Actions / Azure DevOps / Other | GitHub Actions (if org uses GH) or Azure DevOps per platform preference | Product Owner / Platform | No | Integration spike |
| D-002 | Will portal own any asset types or is ServiceNow authoritative? | ServiceNow authoritative / Portal owns subset | Recommend ServiceNow authoritative for MVP; defer portal ownership to later | Product Owner / Platform | Yes | Connector design & data contracts |
| D-003 | Audit retention policy and storage choice | Short (1 year) / Long (3+ years) / Configurable | Define policy per compliance; start with 1 year as BRS suggests default | Security / Compliance | Yes | Handoff & infra decisions |
| D-004 | Claim-to-role mapping approach (Azure AD groups vs custom claims) | Map groups to roles / Use custom claims | Map groups to roles (simpler) | Platform/Identity | No | Auth PoC |

## Optional visual view

A compact sequence (request intake → create ticket → reconcile) is present in `input/architecture.md` and clarifies async reconciliation responsibilities; no additional visual added here.

## Architecture review decision

| Field | Value |
|---|---|
| Decision | Approved with conditions |
| Conditions | Resolve D-001..D-003; complete integration spike for ServiceNow; define audit retention and storage; architect to validate claim-to-role mapping in PoC |
| Decision owner | (TBD) Product Owner / Architect |
| Date | 2026-06-11 |
