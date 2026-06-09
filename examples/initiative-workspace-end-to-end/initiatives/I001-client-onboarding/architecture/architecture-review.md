# Architecture Review

## Constraints Identified

| Constraint ID | Constraint | Evidence | Delivery impact |
|---|---|---|---|
| AR-01 | Reuse approved identity verification services | `input/architecture.md` | D1 must not introduce a parallel identity mechanism |
| AR-02 | Keep document storage behind service-layer controls | `input/architecture.md` | uploads must flow through approved access checks |
| AR-03 | Emit auditable onboarding events | `input/architecture.md` | D1 must preserve downstream traceability and event evidence |

## Existing-System Impact Summary

| Area | Impact | Evidence | Owner |
|---|---|---|---|
| onboarding platform | guided submission changes an existing onboarding flow | `architecture/existing-system-impact.md` | Architecture |
| audit event consumers | downstream consumers may depend on event shape and timing | `architecture/existing-system-impact.md` | Architecture / Operations |
| document access controls | existing service controls must stay intact | `input/architecture.md` | Security / Engineering |

## BRS Alignment

| Requirement | Alignment assessment | Notes |
|---|---|---|
| BRS-01 | aligned | approved identity and document services can support the required submission flow |
| BRS-02 | aligned with follow-up | audit event is supported, but downstream schema dependencies still need confirmation |

## Conflicts

| Conflict ID | Description | Evidence | Action |
|---|---|---|---|
| C-01 | retention rule detail is not fully defined while document handling is in scope | business intake and readiness | keep as release risk until clarified |

## Open Decisions

| Decision ID | Decision needed | Owner | Needed before |
|---|---|---|---|
| D-01 | confirm downstream consumers and event schema expectations | Architecture / Operations | Handoff |
| D-02 | confirm retention handling obligations for uploaded documents | Compliance / Security | Release |
