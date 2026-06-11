# Readiness Check — I004 IT Portal

## Metadata

| Field | Value |
|---|---|
| Initiative | I004 - IT Portal |
| Reviewer | (TBD) Engineering Lead |
| Review date | 2026-06-11 |
| Status | Not ready |

## Summary

This readiness check assesses whether the initiative is ready to proceed to confirmed delivery structure and handoff. Based on the BRS, draft architecture, review and rules, several quality gates are expected to be triggered.

## Readiness decision

- Decision: **Not ready**
- Reason: Two blocking open decisions remain (D-002: CMDB ownership; D-003: Audit retention/storage). These must be resolved before connector implementation and before handoff.

## Triggered quality gates

The following gates are expected to be created and completed (metadata/status to be recorded in each gate file):

- `quality-gates/security-review.md` — Security review (OWASP, auth, PII, data exposure)
- `quality-gates/data-contract.md` — Data contract for ServiceNow sync (PII, residency, mapping)
- `quality-gates/api-contract.md` — API contract / integration contract for ServiceNow and CI webhook
- `quality-gates/observability-plan.md` — Observability and telemetry plan
- `quality-gates/bdd-scenarios.md` — BDD scenarios for acceptance gates

## Blockers (must be resolved)

| Blocker | Decision / artifact | Owner | Action required |
|---|---|---|---|
| D-002 — CMDB ownership | `planning/open-decisions.md` (blocking) | Product Owner / Platform | Confirm whether ServiceNow remains authoritative or portal will own subset; produce integration contract or scope change. |
| D-003 — Audit retention & storage | `planning/open-decisions.md` (blocking) | Security / Compliance | Define retention policy and storage mechanism (append-only / WORM). Provide required compliance justification for chosen retention. |

## Non-blocking items to complete before Ready

- D-001 — Confirm CI/CD provider (Product Owner / Platform) — impacts connector spike but not blocking.
- D-004 — Claim-to-role mapping PoC (Platform/Identity) — validate in Auth PoC.

## Scaffolds created

To collect the human inputs required by the blockers, the orchestrator created the following stubs for the team to complete:

- `input/contracts/servicenow-integration.md` — questions for ServiceNow connector contract and schema mapping.
- `input/constraints/audit-retention.md` — questionnaire for Security to define retention and storage requirements.

## Next steps (one specific action)

1. Product Owner / Platform: confirm D-002 in `planning/open-decisions.md` or update the ServiceNow integration contract in `input/contracts/servicenow-integration.md` (owner: Product Owner / Platform). Once resolved, the integration spike can proceed.
2. Security / Compliance: complete `input/constraints/audit-retention.md` to define retention and storage (owner: Security). Once D-003 is resolved, update `engineering-readiness/readiness-check.md` and re-run the readiness check.

When both blocking decisions are resolved and the triggered gate artifacts exist with `Status: Accepted`, the workflow will continue to confirm delivery structure and prepare handoff.
