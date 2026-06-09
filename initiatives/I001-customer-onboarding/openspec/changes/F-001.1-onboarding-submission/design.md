# Design — F-001.1: Onboarding Submission

> Scoped to this user story only. Implement from this file + tasks.md + specs/.

## What this story touches

Adds the `POST /onboarding` endpoint to the Onboarding API service. Creates the `profiles` table in the relational DB (`eu-south`). Emits `onboarding_start` metric. No external integrations are called in this story — IDP verification is triggered in F-002.1.

## API surface

| Method | Path | Purpose | Auth | Request | Response | Full spec |
|---|---|---|---|---|---|---|
| POST | `/onboarding` | Create onboarding record | API key (`X-API-Key`) | `{ email, phone?, consent_marketing }` | `202 { id, status: "pending" }` | `specs/api.md` |

## Data model changes

| Table | Change | Key columns | PII? | Encryption | Full spec |
|---|---|---|---|---|---|
| `profiles` | Create | `profile_id (PK)`, `email`, `email_hash`, `phone`, `residency_region`, `status` | email, phone | Field-level KMS (Azure Key Vault) | `specs/data.md` |

## Architecture constraints applied

| Rule ID | Constraint | How applied |
|---|---|---|
| AR-SEC-001 | API key from Key Vault — no hardcoding | `X-API-Key` header value loaded from Key Vault at startup |
| AR-SEC-002 | email and phone encrypted at rest via KMS | Field-level encryption at DB write; `email_hash` stored for duplicate detection |
| AR-OBS-001 | W3C trace context injected at entry | `traceparent` header set on incoming request; span `onboarding.request` created |
| AR-DATA-001 | Italy residency | DB provisioned in `eu-south` — enforced at infrastructure level |

## Security decisions

| Concern | Decision | Gate reference |
|---|---|---|
| PII in logs | Redact `email` and `phone` at emission point in structured logger | `quality-gates/security-review.md` |
| Duplicate detection | Store `email_hash` (SHA-256 of normalised email) — never index plaintext | `quality-gates/data-contract.md` |

## Observability requirements

| Signal | Type | Emitted when | Labels | Gate reference |
|---|---|---|---|---|
| `onboarding_start` | Counter | On 202 response from `POST /onboarding` | none | `quality-gates/observability-plan.md` |

Span: `onboarding.request` — covers entire handler. Sampling: 100% errors, 10% success.

## Open questions

| # | Question | Owner | Needed before |
|---|---|---|---|
| 1 | Key Vault instance provisioned in `eu-south`? | Platform | First task — secrets needed at startup |
