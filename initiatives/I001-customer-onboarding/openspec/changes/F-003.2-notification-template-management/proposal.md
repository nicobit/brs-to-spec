# Proposal — F-003.2: Notification Template Management

**As a** product/operator,
**I want** notification templates and SendGrid configuration managed,
**so that** messages are consistent, compliant, and updatable without code deploys.

**Requirement:** FR-004
**Acceptance criteria:** Template update in SendGrid reflected without redeploy; template ID stored in config

## Why now

SendGrid integration is live (F-003.1). This story makes templates manageable — operators can update copy and layout without engineering involvement.

## What changes

- Template IDs and SendGrid configuration stored in Key Vault / config — not hardcoded
- Operator runbook for updating SendGrid templates documented

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-003.1 | SendGrid integration must exist |
| Can run in parallel with | F-004.2, F-002.2, F-005.2 | No shared schema or API |
| Blocks | none | Terminal for notifications track |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | Template ID updatable via config without redeploy | Update template ID in config; trigger notification | Email uses new template |
| AC-002 | SendGrid config documented in operator runbook | Review runbook | Runbook present in `docs/` or `input/` |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| API contract | `quality-gates/api-contract.md` | SendGrid integration spec |
| Architecture rules | `architecture/architecture-rules.md` | AR-SEC-001 — secrets in Key Vault |
