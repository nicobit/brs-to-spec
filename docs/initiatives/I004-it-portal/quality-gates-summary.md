# Quality Gates Summary — I004 IT Portal

> Generated from initiative workspace. Last updated: 2026-06-11.
> Authoritative source is each gate artifact in `quality-gates/` — this is a readable snapshot.

## Overall status

| Stat | Count |
|---|---|
| Gates triggered | 5 |
| Gates accepted | 0 |
| Gates in progress | 0 |
| Gates not yet created | 5 |
| Gates not triggered | 5 |
| Blocking items remaining | 2 open decisions must be resolved before gates can be created |

---

## Gate status

| Gate | Triggered | Status | Notes |
|---|---|---|---|
| BDD scenarios | Yes | Not yet created | Will be created after readiness = Ready |
| Test strategy | No | Not triggered | Not required for Standard mode at this stage |
| Security review | Yes | Not yet created | Triggered by RBAC, PII, AI assistant, and ServiceNow integration |
| Threat model | No | Not triggered | Not explicitly triggered; may be added if security review surfaces high-risk boundaries |
| Data contract | Yes | Not yet created | Triggered by ServiceNow CMDB sync and PII handling |
| API contract | Yes | Not yet created | Triggered by ServiceNow REST API, CI/CD webhooks, and Azure AD |
| Event contract | No | Not triggered | No event-driven integration identified in MVP scope |
| Observability plan | Yes | Not yet created | Triggered by App Insights / Prometheus integration requirement |
| QA review | No | Not triggered | Not required at this stage |
| Release readiness | No | Not triggered | Will be triggered before production deployment |

---

## Why each gate was triggered

### BDD scenarios
Required because the initiative has complex approval workflows, RBAC enforcement, and audit trail requirements that need structured acceptance criteria. The BRS acceptance criteria explicitly call for end-to-end demonstrations of request intake, RBAC validation, and audit export.

### Security review
Triggered by:
- RBAC enforcement across API and UI (FR-1)
- PII handling in audit records and CMDB sync data
- AI assistant with action-triggering capability (AR-031)
- Secrets management requirement (AR-030)
- ServiceNow integration with data sensitivity (AR-012)

### Data contract
Triggered by:
- ServiceNow CMDB sync — data ownership, schema, PII, and residency must be documented (AR-012)
- Audit record storage — PII may be present in user identifiers; retention policy required (D-003)
- Non-prod masking requirement — data contract must define masking rules (AR-021)

### API contract
Triggered by:
- ServiceNow REST API integration — schema, rate limits, auth, and versioning
- CI/CD provider webhooks — format, auth, and retry behaviour (pending D-001)
- Azure AD OIDC/SAML endpoints — claim structure and group sync

### Observability plan
Triggered by:
- App Insights and Prometheus integration requirement (BRS integrations section)
- SLA monitoring requirement — 99.9% availability and MTTA tracking
- Dashboard requirement for operational health (FR-9)
- On-call alerting and runbook context linkage

---

## Remaining blockers before gates can be created

| Blocker | Owner | Action required |
|---|---|---|
| D-002 — CMDB ownership decision | Product Owner / Platform | Confirm ServiceNow authoritative scope; complete `input/contracts/servicenow-integration.md` |
| D-003 — Audit retention and storage | Security / Compliance | Define retention period and storage technology; complete `input/constraints/audit-retention.md` |

Once both blocking decisions are resolved, the readiness check can be re-run as Ready and gate artifacts can be created and worked through in this order:

1. `quality-gates/security-review.md`
2. `quality-gates/data-contract.md`
3. `quality-gates/api-contract.md`
4. `quality-gates/observability-plan.md`
5. `quality-gates/bdd-scenarios.md`
