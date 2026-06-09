# Proposal — F-004.2: Support RBAC and Audit

**As an** operator,
**I want** role-based access and audit logs for support actions,
**so that** actions are accountable and auditable.

**Requirement:** FR-005, AR-SEC-002
**Acceptance criteria:** RBAC matrix attached; audit log examples confirmed

## Why now

Support endpoints exist (F-004.1). Before any support agent uses them in staging or production, RBAC must be enforced and all actions must be audit-logged.

## What changes

- RBAC middleware on all `/support/` routes — `support_agent` role claim required; 403 on missing role
- Audit log entries for every support action — `support_view`, `support_retry`

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-004.1 | RBAC added to endpoints created in F-004.1 |
| Can run in parallel with | F-002.2, F-003.2, F-005.2 | No shared schema or API |
| Blocks | none | Terminal for support track |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | Request without `support_agent` role returns 403 | Test without role | 403 response |
| AC-002 | Request with role succeeds | Test with role | 200/202 response |
| AC-003 | Every support action writes audit_log row | DB query after view and retry | Rows with `action = support_view`, `support_retry`, actor, entity_id |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| Least-privilege: support_agent role, not admin | `architecture/architecture-rules.md` AR-SEC-002 |
| All support actions audit-logged | AR-SEC-002 |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Security review | `quality-gates/security-review.md` | RBAC requirements |
| Data contract | `quality-gates/data-contract.md` | `audit_logs` table spec |
