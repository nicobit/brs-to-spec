# Epic Clarification Request — E-005 Offer & Acceptance

## Summary

WHEN preparing the Offer & Acceptance epic, THE TEAM REQUIRES CLARIFICATION on actor identities for acceptance, decline handling, and audit binding.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| OAQ-001 | /api/v1/offers/{offerId}/accept | Offer API | Who can accept an offer on behalf of the applicant (underwriter, automated engine, applicant via UI)? | Acceptance method affects API auth and events (`actor_id`, `method`). | API auth, event modelling, story generation |
| OAQ-002 | /api/v1/offers/{offerId} | Offer API | How should declines or expiration be represented and recorded? | Downstream systems need decline reason and timestamp for audit and reporting. | API schema, audit, reporting |
| OAQ-003 | /api/v1/offers/{offerId}/accept | Offer API | Should `acceptance.actor_id` be a user id, system id, or both (and how to format)? | Determines identity schema for audit linking and RBAC. | Audit linkage, RBAC, tests |
| OAQ-004 | webhooks / callbacks | N/A | Is acceptance allowed via asynchronous workflows (webhook/callback) and how to surface status? | Affects API surface and event ordering guarantees. | Integration design, consumer contracts |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-005.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.

## Candidate Answers / Context

- The implementation contract currently defines `acceptance.actor_id` as string; prefer `uuid` for internal actors.
- Offer lifecycle: created -> offered -> accepted | declined | expired. Decline reason should map to the existing decline code taxonomy if available.

## Impact if Unresolved

IF actor identity, decline representation, or async acceptance is unclear, THEN the implementation contract and API schema may require revision, tests will be incomplete, and audit linkage may fail.

## Requested Action

Please answer OAQ-001..OAQ-004 or point to canonical identity & decline schemas.

*End of clarification request.*
