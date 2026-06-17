# Engineering Readiness Check

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Delivery mode | {{delivery_mode}} |
| Execution mode | {{execution_mode}} |
| Created at | {{date}} |
| Created by | engineering-lead |
| Status | Draft |

## Core Checklist

| # | Item | Status | Evidence / Notes |
|---|---|---|---|
| 1 | BRS is complete and accepted | Pass / Fail | |
| 2 | Business intake summary accepted | Pass / Fail | |
| 3 | Architecture review accepted | Pass / Fail | |
| 4 | Architecture rules defined | Pass / Fail | |
| 5 | Delivery structure confirmed (F-XXX.X IDs) | Pass / Fail | |
| 6 | All blocking gaps from gaps-and-questions resolved | Pass / Fail | |
| 7 | Traceability matrix complete (all FR-NNN mapped) | Pass / Fail | |
| 8 | Existing system impact assessed (brownfield) | Pass / Fail / N/A | |

## Gate Trigger Decisions

| Gate | Triggered | Trigger Evidence / Justification for No | Required |
|---|---|---|---|
| BDD Scenarios | Yes / No | | Yes / No |
| Test Strategy | Yes / No | | Yes / No |
| Security Review | Yes / No | | Yes / No |
| API Contract | Yes / No | | Yes / No |
| Data Contract | Yes / No | | Yes / No |
| Event Contract | Yes / No | | Yes / No |
| Observability Plan | Yes / No | | Yes / No |

**Rule:** Every "No" must have explicit written justification. A blank justification is a framework violation.

## Readiness Decision

| Field | Value |
|---|---|
| Readiness score | NN / 100 |
| Decision | Ready / Ready with risks / Not ready |
| Decision rationale | |
| Required before handoff | |

## Blocking Issues

| Issue | Impact | Required action | Owner |
|---|---|---|---|

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

## Required Quality Gates

| Gate | Required | Owner | Required before |
|---|---|---|---|
| BDD Scenarios | Yes / No | qa-analyst | handoff |
| Security Review | Yes / No | security-reviewer | handoff |

## Self-Review

Before finalizing, confirm:
- [ ] Every triggered gate has explicit trigger evidence
- [ ] Every not-triggered gate has explicit justification
- [ ] Readiness score calculated
- [ ] Challenge questions answered in reasoning
- [ ] Brownfield impact and rollback sensitivity assessed

---
*Status: Draft. Set to Accepted only by the human gate owner when applicable. Never self-accept.*
