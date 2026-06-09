# Engineering Readiness Check

## Metadata

| Field | Value |
|---|---|
| Initiative / Feature | Password reset email delay — async fix |
| Active deliverable | D1 Password Reset Async |
| Delivery mode | Fast Path |
| Execution mode | Standalone |
| Reviewer | Backend team lead |
| Review date | 2026-06-09 |
| Source BRS version | Bug report 2026-06-09 |
| Architecture version | N/A — no new architecture |

## Readiness Decision

| Decision | Value |
|---|---|
| Status | Ready |
| Decision owner | Backend team lead |
| Decision date | 2026-06-09 |
| Conditions / caveats | Confirm job-queue message schema is unchanged before implementation |

## Decision Rationale

Root cause is confirmed. Fix approach is established (move email send to existing `job-queue`). No new boundaries, no schema changes, no security scope change. Existing tests cover the reset token flow. The only open question is whether the job-queue message schema requires documenting — readiness assessment says no: `auth-service` already sends notification emails through this queue using the same schema. No new contract is introduced.

## Core Checklist

| Area | Status | Evidence | Gap / Risk | Required action | Owner | Required before |
|---|---|---|---|---|---|---|
| Business scope clear | Yes | Problem statement and success criteria in input-package.md | None | None | | Handoff |
| Requirements traceable | Yes | Single requirement maps directly to input-package.md | None | None | | Handoff |
| Initial architecture reviewed | Yes | Existing queue and email service confirmed in input-package.md | None | None | | Handoff |
| Architecture constraints applied | Yes | No new boundaries; existing queue pattern reused | None | None | | Implementation |
| Architecture conflicts resolved or accepted | Yes | No conflicts — fix uses established queue pattern | None | None | | Implementation |
| Governed service / API boundaries identified | Yes | No new API boundary created | None | None | | Handoff |
| Governed data boundaries identified | Yes | No schema change | None | None | | Handoff |
| Governed event boundaries identified | Yes | Job-queue message schema unchanged — same schema as notification emails | Confirm schema version before coding | Verify queue schema in codebase | Dev | Implementation |
| Existing-system impact reviewed when relevant | Yes | `auth-service` handler change only; queue integration already exists | None | None | | Handoff |
| Impacted modules known | Yes | `auth-service` → `POST /auth/password-reset` handler | None | None | | Implementation |
| Existing behavior stability expectations clear | Yes | Reset token logic unchanged; only delivery mechanism changes | None | None | | Implementation |
| Acceptance expectations clear | Yes | HTTP 200 within 200ms; email within 30 seconds; existing tests pass | None | None | | Implementation |
| Validation approach clear | Yes | Existing integration tests + manual smoke test in staging | None | None | | Implementation |
| Dependencies known | Yes | `job-queue` service (existing), `email-service` (existing) | None | None | | Implementation |
| Open questions assigned | Yes | Queue schema verification assigned to dev | None | None | | Handoff |

## Governed Boundary Assessment

| Boundary ID | Boundary type | Producer / Owner | Consumer(s) | Created / Changed? | External or cross-team? | Governed contract needed? | Expected gate |
|---|---|---|---|---|---|---|---|
| B01 | Event (job-queue message) | auth-service | email-service | No — existing schema reused | No — same team owns both | No | None — schema unchanged, same pattern as notification emails |

## Conditional Quality Gates

| Quality Gate | Triggered? | Required? | Trigger evidence | Risk if skipped | Owner | Required before | Output |
|---|---|---|---|---|---|---|---|
| BDD scenarios | No | No | Simple async refactor, no new business rules | None | | | |
| Test strategy | No | No | Existing integration tests sufficient | None | | | |
| QA review | No | No | No new acceptance criteria | None | | | |
| Architecture review | No | No | No new architecture decisions | None | | | |
| Security review | No | No | No auth flow change, no data exposure | None | | | |
| Release readiness review | No | No | Standard deployment, existing rollback procedure | None | | | |
| API contract | No | No | No new or changed API boundary | None | | | |
| Data contract | No | No | No schema change | None | | | |
| Event contract | No | No | Existing queue schema reused unchanged | None | | | |
| Threat model | No | No | No security scope change | None | | | |
| Observability plan | No | No | Existing queue monitoring covers this flow | None | | | |

## Blocking Issues

None.

## Accepted Risks

| Risk ID | Risk | Impact | Mitigation | Accepted by | Expiry / Review date |
|---|---|---|---|---|---|
| R01 | Queue schema version not pinned in code | Low — schema is stable and shared | Verify schema before implementation | Backend team lead | At implementation |

## Required Actions Before Handoff

| Action ID | Action | Owner | Required before | Status |
|---|---|---|---|---|
| A01 | Verify job-queue message schema version in codebase | Dev | Implementation | Open |

## Recommended Handoff

| Field | Value |
|---|---|
| Execution mode | Standalone |
| Reason | No OpenSpec in project |
| Active deliverable only? | Yes |

## Challenge

1. Strongest argument this is wrong: the `job-queue` integration could introduce a hidden event contract if the schema differs from what `email-service` expects — making the "no gate needed" decision wrong. Mitigated by A01 (schema verification before implementation).
2. Assumption that breaks it: if `auth-service` is the first producer of password-reset events on `job-queue` (not notification emails as assumed), an event contract gate would trigger. A01 confirms this before coding starts.
3. What a skeptical architect would object to: "You're calling this no new boundary, but any queue message is a contract." Correct — and the response is that the schema is pre-existing and unchanged, which A01 will confirm. If A01 reveals a new schema, the event contract gate triggers.
