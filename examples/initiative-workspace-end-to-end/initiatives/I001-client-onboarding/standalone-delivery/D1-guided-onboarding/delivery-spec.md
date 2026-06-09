# Delivery Spec

## Metadata

| Field | Value |
|---|---|
| Active deliverable | D1 Guided Onboarding |
| Execution mode | Standalone |
| Owner | Engineering Lead |
| Date | Example |

## Purpose

Implement the guided onboarding submission flow using approved identity, storage, and audit services.

## Business Outcome

| Field | Value |
|---|---|
| Story / capability served | US-01 and US-02 from `planning/delivery-structure.md` |
| Main user or operator outcome | reviewers receive more complete onboarding submissions with auditable traceability |
| Why this deliverable exists now | D1 reduces manual triage and establishes controlled onboarding submission behavior |

## Scope

| In scope item | Source requirement / story | Notes |
|---|---|---|
| guided onboarding submission | BRS-01 / US-01 | capture required identity and documents |
| audit event on successful submission | BRS-02 / US-02 | supports downstream operational traceability |

## Out of Scope

| Out of scope item | Why excluded now |
|---|---|
| full reviewer workflow redesign | outside D1 |
| retention-policy redesign | policy clarification is still pending |

## Requirements Covered

| Requirement ID | Summary | Acceptance / validation reference | Evidence expected |
|---|---|---|---|
| BRS-01 | collect identity and document evidence at submission time | `quality-gates/bdd-scenarios.md`, `validation-plan.md` | successful submission and validation behavior |
| BRS-02 | emit auditable onboarding event | `validation-plan.md` | auditable event evidence after success |

## Architecture Constraints

| Constraint ID | Constraint | Applied how | Evidence |
|---|---|---|---|
| AR-01 | use approved identity validation and audit services | guided flow reuses approved controls rather than inventing new ones | task traceability and review evidence |

## Quality Gates Applied

| Gate | Required? | Status | Output |
|---|---|---|---|
| BDD scenarios | Yes | Required | `quality-gates/bdd-scenarios.md` |
| Test strategy | Yes | Required | `quality-gates/test-strategy.md` |
| Security review | Yes | Required | `quality-gates/security-review.md` |

## Risks and Assumptions

| ID | Type | Description | Impact | Owner |
|---|---|---|---|---|
| R-01 | Risk | retention rule detail is still pending | release risk if unresolved | Compliance / Delivery |
| A-01 | Assumption | approved identity validation service remains available and unchanged | affects implementation and validation scope | Architecture |

## Delivery Notes

| Area | Note | Source / reason |
|---|---|---|
| components affected | onboarding flow, document upload, audit event publisher | planning and architecture artifacts |
| existing-system sensitivity | current auditability and access-control behavior must remain stable | brownfield impact and readiness |

## Implementation Boundaries

| Boundary | Rule |
|---|---|
| Approved implementation unit | One approved task at a time |
| Source of business context | Planned user stories and business intake |
| Source of engineering execution | Standalone delivery package tasks |
| Validation source | Referenced validation artifacts, not duplicated acceptance text |

## Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Delivery | Example | Draft example | Example |
