# Initiative Context

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Delivery mode | {{delivery_mode}} |
| Execution mode | {{execution_mode}} |
| AI model version | {{model_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |
| Status | Accepted |

> This file is the single context artifact for all downstream agents (implementation, review, handoff). Load it first. Do not open other artifacts until you have read this file.

## Technology Constraints

| Area | Technology | Version / Constraint | Source |
|---|---|---|---|
| Backend language | | | repository descriptor / architecture.md |
| Backend framework | | | |
| Database | | | |
| Deployment target | | | |
| Auth mechanism | | | |
| Message bus | | | |

## Architecture Rules in Force

| AR-NNN | Rule (verbatim) | Scope |
|---|---|---|
| AR-001 | | All / {{feature area}} |

**These rules are binding. If a design.md note conflicts with an AR-NNN rule, the AR-NNN rule wins.**

## Governed Boundaries

| Boundary | Type | Owner | Contract Location |
|---|---|---|---|
| {{service/API/data store}} | API / Data / Event | {{team/module}} | quality-gates/api-contract.md |

## Active Quality Gates

| Gate | Status | Artifact path |
|---|---|---|
| BDD Scenarios | Required — Accepted | quality-gates/bdd/ |
| Security Review | Required — Accepted | quality-gates/security-review.md |

## Rollback and Regression Sensitivity

| Dimension | Assessment | Reason |
|---|---|---|
| Rollback possible? | Yes / No / Partial | |
| Regression surface | Low / Medium / High | |
| Regression risk components | | |

## Open Risks

| Risk | Impact | Accepted by | Mitigation |
|---|---|---|---|

## Carried-Forward Context

### Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|

> None identified

### Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|

> None identified

### Non-Obvious Constraint Rationale

| AR-NNN | Why the rule exists | What breaks if ignored |
|---|---|---|

> None identified

---
*This file is generated once after readiness check approval and updated if the architecture changes materially.*
