# Data Spec — D1: Guided Onboarding (MVP)

> Distilled from `quality-gates/data-contract.md` for this increment only.
> Full DDL, retention schedule, and Legal residency sign-off are in `quality-gates/data-contract.md`.

## Tables created in this increment

### profiles

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `profile_id` | UUID (PK) | No | — | Generated on insert |
| `email` | string | Yes — High | Field-level KMS (Azure Key Vault) | Store hashed copy `email_hash` for lookups; never index plaintext |
| `email_hash` | string | No | — | SHA-256 of normalised email; used for duplicate detection |
| `phone` | string (nullable) | Yes — High | Field-level KMS (Azure Key Vault) | Optional; encrypt same as email |
| `residency_region` | string | No | — | Always `IT` for D1 pilot |
| `status` | enum | No | — | `pending`, `verified`, `failed`, `complete` |
| `created_at` | timestamp | No | — | UTC |
| `updated_at` | timestamp | No | — | UTC; updated on every status change |

Indexes:
- `idx_profiles_email_hash` on `email_hash` — unique; used for duplicate detection
- Do not index `email` or `phone` plaintext columns

Constraints:
- `email_hash` UNIQUE
- `residency_region` NOT NULL DEFAULT `'IT'`

Migration notes: new table — no existing data; run as additive migration, no locking issues.

---

### verification_records

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `verification_id` | UUID (PK) | No | — | |
| `profile_id` | UUID (FK → profiles) | No | — | CASCADE on profile delete |
| `idp_request_id` | string | No | — | Our generated UUID — idempotency key for IDP and webhook |
| `status` | enum | No | — | `pending`, `verified`, `failed`, `retrying` |
| `submitted_at` | timestamp | No | — | UTC |
| `completed_at` | timestamp (nullable) | No | — | UTC; set on webhook receipt |
| `idp_payload` | jsonb (nullable) | Partial | Tokenize/redact raw PII | Store only `requestId`, `result`, `errorCode` — strip any raw PII fields |
| `idp_signature` | string (nullable) | No | — | Webhook signature header — retained for audit |
| `region` | string | No | — | `IT` for D1 |

Indexes:
- `idx_verification_profile` on `profile_id`
- `idx_verification_idp_request` on `idp_request_id` UNIQUE — deduplication

Migration notes: new table.

---

### consents

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `consent_id` | UUID (PK) | No | — | |
| `profile_id` | UUID (FK → profiles) | No | — | |
| `consent_type` | string | No | — | `terms`, `marketing` |
| `granted` | boolean | No | — | |
| `granted_at` | timestamp | No | — | UTC |
| `source` | string | No | — | `web`, `mobile` |

---

### audit_logs

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `audit_id` | UUID (PK) | No | — | |
| `entity` | string | No | — | `profile`, `verification_record` |
| `entity_id` | UUID | No | — | |
| `action` | string | No | — | `create`, `update`, `verification_requested`, `webhook_received`, `email_sent` |
| `actor` | string | No | — | Service name or internal user ID — never store display names |
| `details` | jsonb | No | — | Non-PII details only — do not include email, phone, or IDP payload |
| `timestamp` | timestamp | No | — | UTC |

---

## PII handling

| Field | Table | Sensitivity | Control | Do not... |
|---|---|---|---|---|
| `email` | profiles | High | Field-level KMS encryption; hash for lookups | Log, index plaintext, return in API responses beyond confirmation |
| `phone` | profiles | High | Field-level KMS encryption | Log, index plaintext |
| `idp_payload` | verification_records | Partial | Tokenize/redact raw PII before storage | Store raw vendor PII fields |

Encryption: Azure Key Vault — field-level encryption for `email` and `phone`. Application decrypts only when needed (not on every read). Key rotation policy: defined in Key Vault; application must support key version rotation without re-encryption downtime.

Logging: structured logger must redact `email`, `phone`, and `idp_payload` at emission point. Do not rely on log aggregation-layer filtering.

## Residency

| Requirement | Value |
|---|---|
| Primary region | Italy (`eu-south`) |
| Backup region | Same region — no cross-region replication without Legal approval |
| Regulatory basis | GDPR — basis to be confirmed by Legal before regional rollout |

## Retention (D1 — interim, confirm with Legal before production)

| Data type | Retention | Deletion mechanism |
|---|---|---|
| Profile PII | Per regulatory requirement | `DELETE /profiles/{id}` — soft-delete flag, then physical purge per schedule |
| Verification records | Audit retention period | Purge after window; redact `idp_payload` PII fields first |
| Consents | Duration of consent + regulatory buffer | Purge on subject deletion request |
| Audit logs | Minimum 1 year | Archive after retention; no PII in `details` field |

## Subject access / deletion

`DELETE /profiles/{profile_id}` — not implemented in D1 (deferred to D3). Soft-delete flag added to `profiles` table now so the column exists when the endpoint is built. Physical purge handled by scheduled job (to be implemented in D3).
