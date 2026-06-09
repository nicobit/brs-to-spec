# Architecture Rules

## Principles

- Follow least-privilege and privacy-by-design for all onboarding flows. Owner: Security.
- Prefer simplicity in delivery slices: design rules to enable incremental rollout and rollback. Owner: Delivery Lead.

## API Rules

- AR-API-001: The onboarding API surface must expose a clear `POST /onboarding` orchestration endpoint and status endpoints for support tooling. Enforcement: API contract required before implementation. Owner: API/Product.
- AR-API-002: All external integration calls (IDP, Payment Provider) must have documented request/response schemas, error semantics, and retry/backoff strategies. Enforcement: Integration contract sign-off. Owner: Integration.

## Data Rules

- AR-DATA-001: All PII stored for onboarding (profiles, verification records, consents) must be encrypted at rest and transmitted over TLS. Enforcement: Security review and infra controls. Owner: Security/Ops.
- AR-DATA-002: Data residency requirements must be captured per target release region; data partitioning or hosting choices must satisfy GDPR constraints before regional rollout. Enforcement: Legal sign-off for region. Owner: Legal / Architecture.

## Security Rules

- AR-SEC-001: Secrets (API keys, credentials) must be stored in the organization's secret store; no credentials hard-coded. Enforcement: Security review and IaC checks. Owner: Security/Ops.
- AR-SEC-002: Access to support UI and retry operations must require authenticated, auditable access with role-based controls. Enforcement: Security acceptance tests. Owner: Security/Product.

## Deployment Rules

- AR-DEP-001: Deployment topology must be designed to meet a 99.9% monthly availability objective; this requires multi-AZ (or equivalent) deployment and health-check-based failover. Enforcement: Ops sign-off and runbook completion. Owner: Ops/Architecture.
- AR-DEP-002: Observability must emit `onboarding_start`, `onboarding_success`, `onboarding_failure`, and `time_to_onboard` metrics with tracing enabled across integrations. Enforcement: Telemetry dashboards and alerts. Owner: Platform/Observability.

## Resolved Rule Items (decisions recorded)

- AR-OPEN-001: Decision on synchronous vs asynchronous IDP flow — **Asynchronous** chosen (webhook/callback). Owner: Architect / Integration. Resolved: 2026-06-09.
- AR-OPEN-002: Primary data store selection — **Relational** chosen. Owner: Data / Architect. Resolved: 2026-06-09.

Generated from `input/brs.md`, `input/architecture.md`, and `architecture/architecture-review.md` on 2026-06-09.
