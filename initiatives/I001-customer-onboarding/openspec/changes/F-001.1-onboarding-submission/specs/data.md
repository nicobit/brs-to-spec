# Data Spec — F-001.1: Onboarding Submission

## profiles — created

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `profile_id` | UUID (PK) | No | — | Generated on insert |
| `email` | string | Yes — High | Field-level KMS (Azure Key Vault) | Never index plaintext |
| `email_hash` | string | No | — | SHA-256 of normalised email; used for duplicate detection |
| `phone` | string (nullable) | Yes — High | Field-level KMS (Azure Key Vault) | Optional |
| `residency_region` | string | No | — | Always `IT` for this initiative |
| `status` | enum | No | — | `pending` on insert |
| `created_at` | timestamp | No | — | UTC |
| `updated_at` | timestamp | No | — | UTC |

Indexes:
- `idx_profiles_email_hash` UNIQUE on `email_hash` — duplicate detection

Constraints:
- `email_hash` UNIQUE NOT NULL
- `residency_region` NOT NULL DEFAULT `'IT'`

Migration notes: new table — additive migration, no locking issues.

## PII handling (this story)

| Field | Table | Sensitivity | Control | Do not... |
|---|---|---|---|---|
| `email` | profiles | High | Field-level KMS encryption | Log, index plaintext, return in API responses |
| `phone` | profiles | High | Field-level KMS encryption | Log, index plaintext |
