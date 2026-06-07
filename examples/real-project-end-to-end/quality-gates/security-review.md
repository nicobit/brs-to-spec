# Security Review

## Active Deliverable

D1 — Create onboarding request

## Review Decision

Approved with risks

## Controls Checked

| Control area | Required? | Compliant? | Evidence / Notes |
|---|---|---|---|
| Authentication | Yes | Yes | Entra ID constraint ARC-001 |
| Authorization | Yes | Partial | Role matrix still needs confirmation |
| Data classification | Yes | Partial | Client data classification required |
| PII / sensitive data | Yes | Partial | Logging must avoid sensitive fields |
| Audit trail | Yes | Yes | Existing audit service ARC-004 |

## Findings

| Finding ID | Severity | Description | Recommendation |
|---|---|---|---|
| SEC-001 | Medium | Role matrix not yet confirmed | Confirm roles before implementation |
| SEC-002 | Medium | Sensitive fields in logs not explicitly listed | Add logging deny-list before merge |

## Required Actions Before Implementation / Merge

- Confirm role matrix.
- Define sensitive-field logging deny-list.
