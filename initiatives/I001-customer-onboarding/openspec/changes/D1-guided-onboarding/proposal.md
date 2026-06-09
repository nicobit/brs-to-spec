# Proposal — D1: Guided Onboarding (MVP)

> OpenSpec change proposal. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder (`openspec/changes/D1-guided-onboarding/`) into the target code repository before applying.

## Why

Retail customers in Italy cannot onboard digitally today — the process is manual and requires branch visits. This increment delivers the first automated onboarding flow: account creation, identity verification via Identity Provider B, and confirmation notifications via SendGrid. It enables a pilot with internal users and establishes the telemetry baseline needed to measure conversion (target ≥ 25%) and IDP latency (p95 < 30 s).

## What changes

- New `POST /onboarding` endpoint — creates onboarding record, triggers async IDP verification
- New `GET /onboarding/{id}/status` endpoint — returns current onboarding state
- New webhook handler `POST /webhook/idp` — receives async IDP callback, validates HMAC-SHA256 signature
- New DB tables: `profiles`, `verification_records`, `consents`, `audit_logs`
- SendGrid transactional email integration — sends confirmation on onboarding success
- Background job queue — retries failed IDP verification calls
- Telemetry: `onboarding_start`, `onboarding_success`, `onboarding_failure`, `verification_latency_ms`, `idp_errors_total`

## Scope

### In scope

| Feature | User story summary | Requirement |
|---|---|---|
| F-001.1 Onboarding submission | Customer submits email/phone to create account | FR-001, AC-001 |
| F-001.2 Persist profile & consent | System persists profile, consent, and audit records | FR-003 |
| F-002.1 Identity verification | System calls IDP B async; webhook confirms result | FR-002, NFR-001 |
| F-003.1 Transactional notifications | Customer receives confirmation email/SMS on success | FR-004 |
| F-005.1 Metrics and tracing | Telemetry for onboarding lifecycle; tracing across integrations | NFR-005 |

### Out of scope (explicitly)

- Support UI and operator retry flows (F-002.2, F-004.1, F-004.2) — Increment 2
- Notification template management / SendGrid config UI (F-003.2) — Increment 2
- Observability runbooks and alert hardening (F-005.2) — Increment 2
- CRM sync — deferred pending Legal sign-off (OD-004)
- Regional deployment hardening and data residency enforcement — Increment 3
- Payment Provider A integration — not required for MVP pilot

## Success criteria

| Criterion | Target | Source |
|---|---|---|
| Pilot conversion rate | ≥ 25% of started flows complete | BRS NFR-005 |
| IDP verification latency p95 | < 30 000 ms | BRS NFR-001 |
| Service availability | ≥ 99.9% monthly (target — not enforced in pilot) | BRS NFR-002 |
| Telemetry baseline | `onboarding_start/success/failure` visible in staging dashboard | observability-plan.md SLOs |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| Relational DB for profiles and consents | `input/architecture.md` D-002 |
| IDP verification is async (webhook/callback) with idempotency | `input/contracts/identity-provider-b-contract.md` |
| Secrets in Azure Key Vault — no hardcoded credentials | `architecture/architecture-rules.md` AR-SEC-001 |
| PII fields (email, phone) encrypted at rest via KMS | `architecture/architecture-rules.md` AR-SEC-002 |
| Italy data residency (`eu-south`) — do not store PII outside region | `quality-gates/data-contract.md` |
| TLS 1.2+ for all in-transit data | `quality-gates/security-review.md` |
| Correlation ID propagated through all service boundaries | `quality-gates/observability-plan.md` |

## Reference artifacts

All detail is in `specs/` (distilled from quality gates) and the paths below.

| Artifact | Path | What to read there |
|---|---|---|
| Architecture review | `input/architecture.md` | Deployment topology, integration decisions D-001–D-005 |
| Architecture rules | `architecture/architecture-rules.md` | Binding rules — all must be followed |
| Data contract (full) | `quality-gates/data-contract.md` | Full schema DDL, retention schedule, Legal residency sign-off |
| API contract (full) | `quality-gates/api-contract.md` | Full endpoint specs, sandbox credentials, SLA, rate limits |
| Security review | `quality-gates/security-review.md` | Full security checklist and accepted risks |
| Observability plan (full) | `quality-gates/observability-plan.md` | Full telemetry catalog, alert rules, dashboard queries, runbooks |
