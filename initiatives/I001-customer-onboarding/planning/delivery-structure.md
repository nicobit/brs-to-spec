# Delivery Structure

> Primary consumer: Delivery lead, Product Owner, Architects
> Purpose: break objectives into epics, features, and initial user stories traceable to source requirements

## Epics

| Epic ID | Epic title | Summary | Owner | Related requirements |
|---|---|---|---|---|
| E-001 | Core Onboarding Flow | Orchestrate account creation, profile capture, consent, and happy-path completion | Product / Engineering | FR-001, FR-003, NFR-001, NFR-005 |
| E-002 | Identity Verification | Integrate with Identity Provider B for verification, handle failure/retry | Integration / Security | FR-002, NFR-001, NFR-003 |
| E-003 | Notifications & Communications | Deliver email/SMS notifications for onboarding progress and outcomes | Product / Ops | FR-004 |
| E-004 | Support Tools & Recovery | Support UI and APIs for support agents to view and retry onboarding steps | Ops / Support | FR-005 |
| E-005 | Observability & Ops Readiness | Telemetry, alerts, runbooks, and deployment topology to meet availability targets | Platform / Ops | NFR-002, NFR-005 |

## Features and Candidate User Stories

Epic: E-001 — Core Onboarding Flow

| Feature | User story (As a..., I want..., so that...) | Acceptance / traceability |
|---|---|---|
| F-001.1 Onboarding submission | As a new retail customer, I want to submit my email or phone to create an account, so that I can start onboarding. | FR-001; AC-001 in `input/brs.md` |
| F-001.2 Persist profile & consent | As the system, I will persist profile and consent records for audit and legal traceability. | FR-003 |

Epic: E-002 — Identity Verification

| Feature | User story | Acceptance / traceability |
|---|---|---|
| F-002.1 Verification request | As the onboarding system, I want to call Identity Provider B to verify identity, so that only verified users progress. | FR-002; NFR-001 |
| F-002.2 Verification failure handling | As a support agent, I want to see failure details and retry verification, so that users can complete onboarding. | FR-005 |

Epic: E-003 — Notifications & Communications

| Feature | User story | Acceptance |
|---|---|---|
| F-003.1 Transactional notifications | As a user, I want to receive confirmation emails/SMS when onboarding completes, so I have a record. | FR-004 |
| F-003.2 Notification template management | As a product/operator, I want notification templates and SendGrid configuration managed, so that messages are consistent and compliant. | FR-004; Note: provider = SendGrid (OD-005) |

Epic: E-004 — Support Tools & Recovery

| Feature | User story | Acceptance |
|---|---|---|
| F-004.1 Support UI | As a support agent, I want to view onboarding state and retry steps, so I can resolve failures quickly. | FR-005 |
| F-004.2 Support RBAC & audit | As an operator, I want role-based access and audit logs for support actions, so that actions are accountable and auditable. | FR-005; AR-SEC-002; acceptance: RBAC matrix and audit log examples attached |

Epic: E-005 — Observability & Ops Readiness

| Feature | User story | Acceptance |
|---|---|---|
| F-005.1 Metrics and tracing | As an SRE, I want telemetry for onboarding_start/onboarding_success/onboarding_failure and tracing across integrations, so that we can measure KPIs and alert on regressions. | NFR-005 |
| F-005.2 Runbooks & alerting | As an SRE, I want runbooks and alerting for high-failure-rate and IDP webhook issues, so that on-call can respond and restore service quickly. | NFR-005; acceptance: runbooks present and alerts tested in staging |

## Candidate Increments and Minimum Viable Slice

- Increment 1 (MVP): E-001 core flow + F-002.1 synchronous verification path + F-003.1 notifications + basic telemetry. Goal: enable pilot with internal users.
- Increment 2: Support UI, verification failure handling, and retry flows (E-004, F-002.2).
- Increment 3: Regional deployments, data residency, and hardened availability (E-005), CRM sync if in-scope.

## Governed Boundaries and Traceability Rules

- All stories must reference source requirement IDs (e.g., FR-001) and acceptance criteria in `input/brs.md`.
- Integration stories must include an integration contract checklist (endpoints, fields, SLAs, retry semantics) before implementation.
- Any story affecting PII or data residency must include Security and Legal sign-off as part of readiness.

## Known Gaps / Decisions Required for Planning

- Decision: synchronous vs asynchronous IDP verification (D-001) — required to finalize story acceptance and UX for MVP.
- Numeric success targets in `input/brs.md` (conversion %, latency target) — Product to confirm (Q-001).
- CRM sync scope (D-004) — affects slice for Increment 3.

Note: Several planning gaps have been resolved in the input package and architecture review. In particular D-001 (IDP verification) was resolved as asynchronous (webhook/callback) and numeric success targets were applied as defaults (Conversion=25%; Latency 95th=30s). Update stories and acceptance criteria as needed to reflect these decisions.

Generated from `input/brs.md` and `input/architecture.md` on 2026-06-09.
