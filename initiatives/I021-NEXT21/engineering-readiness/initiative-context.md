# Initiative Context

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T18:58:00+00:00 |
| Created by | engineering-lead |
| Status | Draft |

## Technology Constraints

- Primary backend: Kubernetes-hosted microservices (AKS)
- Database: Azure PostgreSQL Flexible Server
- Messaging: Azure Service Bus for async events

## Architecture Rules in Force

- AR-001: All external integrations must be behind adapter layer.
- AR-002: Data contracts must be versioned; do not alter existing schemas without migration path.

## Governed Boundaries

- Scoring service (MOD-002) is a private internal service; only adapter exposes to Experian.

## Active Quality Gates

- Security Review, API Contract, Test Strategy, Observability Plan

## Rollback and Regression Sensitivity

- Disbursement flows are high-sensitivity and require sandbox validation; deploy with feature flags.

## Open Risks

- T24 adapter complexity; Experian API limits.

## Carried-Forward Context

- Delivery increments D1..D3 defined; traceability matrix created.
