# Initiative Context — I001 Customer Onboarding

> Primary consumer: Delivery lead, Architect, Security, Legal
> Purpose: concise context for engineering handoff, including impacted components, integrations, data residency, and runbook needs

## Summary

This document summarizes the initiative intent, primary scope, external integrations, PII residency constraints, and immediate engineering considerations for handoff.

## Initiative overview

- Initiative: I001 — Customer Onboarding
- Active deliverable: D1 — Initial onboarding flow (frontend, API/orchestrator, DB, background workers, support UI)
- Delivery mode: Standard / OpenSpec
- Readiness: Ready (security, data, and observability gates pending sign-off)

## Key stakeholders

- Product Owner: (placeholder) — see `business-intake/business-intake-summary.md`
- Architect: (placeholder) — see `input/architecture.md`
- Integration owner: (placeholder) — see `input/contracts/`
- Security owner: Security Lead (assign)
- Legal reviewer: Legal Lead (assign)
- Platform / SRE: Platform Lead (assign)

## Impacted components

- Frontend (web/mobile) — onboarding UI
- API / Orchestration service — `POST /onboarding`, status endpoints
- Relational DB — profiles, consents, verification records, audit logs
- Background job queue — async processing, retries, notifications
- Support UI — internal tooling for retries and incident handling
- External systems: Identity Provider B, Payment Provider A, Email/SMS Gateway (SendGrid), CRM

## External integrations & contracts

- Identity Provider B — asynchronous verification via webhook/callback (owner: Integration). Contract artifacts: `input/contracts/identity-provider-b-contract.md`, `input/contracts/identity-provider-b-api.md`.
- Payment Provider A — validation endpoints (owner: Integration). Contract artifacts: `input/contracts/payment-provider-a-contract.md`, `input/contracts/payment-provider-a-api.md`.
- Email/SMS Gateway — SendGrid selected for notifications (owner: Product/Ops). Template ownership pending.
- CRM sync — in-scope for initial delivery (owner: Product). Mapping and data-sharing contract required in `input/contracts/`.

## Data residency & PII

- Residency region: Italy (per `planning/open-decisions.md` and `input/input-package.md`). Legal sign-off required before regional rollout.
- Data store: Relational (per architect decision). PII fields include profile identifiers, verification artifacts, and contact details. See `quality-gates/data-contract.md` for required evidence.

## Security & compliance highlights

- IDP integration is asynchronous; webhook auth, HMAC/mTLS, and replay protection required.
- Encryption at rest required for all PII stores; keys must be in managed KMS (Azure Key Vault recommended).
- Audit logging and retention policies need to be defined and attached to the data contract.
- Security review in-progress: `quality-gates/security-review.md` (evidence to be attached)

## Observability

- SLOs: availability 99.9% monthly; verification latency p95 < 30s
- Required telemetry events: `onboarding_start`, `onboarding_success`, `onboarding_failure`, `verification_latency_ms`
- Observability plan drafted: `quality-gates/observability-plan.md` — Platform/SRE to finalize dashboards and alerts

## Open actions (required before handoff)

- Security: complete `quality-gates/security-review.md`, attach evidence, and sign off.
- Integration: finalize `input/contracts/*` with webhook examples, signed SLAs, and staging endpoints.
- Legal: append residency sign-off to `input/input-package.md`.
- Architecture/Planning: rebuild `planning/delivery-structure.md` to ensure each feature has ≥2 user stories.
- Platform/SRE: finalize `quality-gates/observability-plan.md` deliverables (dashboards, alerts, runbooks).

## Quick links

- Architected system: `input/architecture.md`
- Open decisions: `planning/open-decisions.md`
- Readiness check: `engineering-readiness/readiness-check.md`
- Security gate: `quality-gates/security-review.md`
- API contract gate: `quality-gates/api-contract.md`
- Data contract gate: `quality-gates/data-contract.md`
- Observability plan: `quality-gates/observability-plan.md`


## Contact & sign-off

- Delivery lead: (assign)
- Engineering lead: (assign)
- Security lead: (assign)

Sign-off template

- Delivery lead: Name — Date
- Architect: Name — Date
- Security: Name — Date
- Legal: Name — Date
