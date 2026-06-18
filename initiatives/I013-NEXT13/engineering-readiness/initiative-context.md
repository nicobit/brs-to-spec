## Metadata

- Initiative: I013-NEXT13
- Artifact: Initiative Context
- Author: b2s-agent
- Status: Draft

## Technology Constraints

- Execution mode: Enterprise+Modular
- Data residency: UK-only for audit records
- Core banking integration: Temenos T24 (integration contract pending)

## Architecture Rules in Force

- AR-001..AR-007 (see `architecture/architecture-rules.md`) — enforce explainability, immutable audit, vendor bindings, SLA constraints.

## Governed Boundaries

- Customer data (PII) kept in UK region; audit logs immutable and stored in separate compliance store.

## Active Quality Gates

- Test Strategy, Security Review, API Contract, Data Contract, Observability Plan (triggered — see `engineering-readiness/readiness-check.md`).

## Rollback and Regression Sensitivity

- Regression surface moderate — deployments touching `Loan Origination` and `Decision Engine` require careful rollbacks and blue-green strategies.

## Open Risks

- Payments provider contract pending — impacts end-to-end E2E tests and D2 acceptance.

## Carried-Forward Context

- Key business constraints: UK-only residency, explainable decisioning, idempotent disbursement requirements.
