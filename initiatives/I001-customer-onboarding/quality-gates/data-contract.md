# Data Contract Quality Gate

> Primary consumer: Architecture, Security, Legal
> Purpose: define and approve data model, residency, retention, and PII controls before handoff

## Metadata

| Field | Value |
|---|---|
| Initiative | I001 — Customer Onboarding |
| Gate owner | Architecture / Data |
| Review date | 2026-06-09 |
| Status | Accepted |
| Triggered | Yes |

## Scope

- PII storage and residency controls for Italy (`eu-south`)
- Data model for profiles, verification records, consents, and audit logs
- Data retention, deletion APIs, and retention schedules
- Data sharing with CRM (in-scope per OD-004)

## Data Model

### Table: profiles

| Column | Type | PII | Notes |
|---|---|---|---|
| `profile_id` | UUID (PK) | No | |
| `email` | string | Yes — encrypted at rest | Store hashed copy for lookup |
| `phone` | string | Yes — encrypted at rest | |
| `first_name` | string | Yes | |
| `last_name` | string | Yes | |
| `created_at` | timestamp | No | |
| `updated_at` | timestamp | No | |
| `residency_region` | string | No | e.g. `IT` for Italy |

Index: `idx_profiles_email` (hashed) — use hashed values for search; do not index plaintext PII.
Retention: per PII retention policy; see Retention section below.

### Table: verification_records

| Column | Type | PII | Notes |
|---|---|---|---|
| `verification_id` | UUID (PK) | No | |
| `profile_id` | UUID (FK → profiles) | No | |
| `idp_request_id` | string | No | Vendor request identifier |
| `status` | enum | No | `pending`, `verified`, `failed`, `retrying` |
| `submitted_at` | timestamp | No | |
| `completed_at` | timestamp | No | |
| `idp_payload` | jsonb | Partial | Minimal vendor response; redact / tokenize raw PII fields |
| `idp_signature` | string | No | Webhook signature header for audit |
| `region` | string | No | Residency region applied |

Index: `idx_verification_profile` on `profile_id`.
Data minimisation: store only vendor-provided fields required for audit and traceability.

### Table: consents

| Column | Type | PII | Notes |
|---|---|---|---|
| `consent_id` | UUID (PK) | No | |
| `profile_id` | UUID (FK → profiles) | No | |
| `consent_type` | string | No | `terms`, `marketing`, `data_sharing` |
| `granted` | boolean | No | |
| `granted_at` | timestamp | No | |
| `source` | string | No | `web`, `mobile`, `crm` |

### Table: audit_logs

| Column | Type | PII | Notes |
|---|---|---|---|
| `audit_id` | UUID (PK) | No | |
| `entity` | string | No | e.g. `profile`, `verification_record` |
| `entity_id` | UUID | No | |
| `action` | string | No | `create`, `update`, `delete`, `verification_requested` |
| `actor` | string | No | Service or user id — do not store PII names |
| `details` | jsonb | No | Non-PII details only |
| `timestamp` | timestamp | No | |

## Data Residency

| Requirement | Value |
|---|---|
| Primary residency region | Italy (`eu-south`) |
| Backup residency | Same region unless Legal approves cross-region backups |
| GDPR basis | To be confirmed by Legal before regional rollout |

## PII Field Mapping and Minimisation

| Field | Table | Sensitivity | Control | Minimisation action |
|---|---|---|---|---|
| `email` | profiles | High | Encrypted at rest (KMS); hashed for lookups | Do not log; redact in traces |
| `phone` | profiles | High | Encrypted at rest (KMS) | Do not log; redact in traces |
| `first_name`, `last_name` | profiles | Medium | Encrypted at rest | Redact in external logs |
| `idp_payload` | verification_records | Partial | Tokenize / redact raw PII fields before storage | Store only required audit fields |

Encryption: field-level encryption for `email` and `phone` using Azure Key Vault. TLS 1.2+ for all in-transit data.

## Retention and Deletion

| Data type | Retention period | Deletion mechanism |
|---|---|---|
| Profile PII | Per regulatory requirement (confirm with Legal) | `DELETE /profiles/{id}` — soft-delete then physical purge per retention schedule |
| Verification records | Audit retention period (confirm with Legal) | Purge after retention window; redact PII fields first |
| Consents | Duration of consent + regulatory buffer | Purge on subject deletion request |
| Audit logs | Minimum 1 year (adjust per Legal) | Archive after retention; no PII in `details` field |

Subject access / deletion requests: implement `DELETE /profiles/{profile_id}` with soft-delete and scheduled physical purge. Provide export endpoint for subject access requests.

## CRM Data Sharing (OD-004 — in scope)

- CRM sync scope: profile data and consent records
- Data-sharing contract required before CRM sync is implemented
- PII fields shared with CRM: confirm with Legal and CRM owner which fields are permitted
- Attach CRM mapping and data-sharing agreement to `input/contracts/` before CRM implementation begins

## Acceptance Checklist

- [ ] Data model schema reviewed and approved by Architecture
- [ ] Residency plan for Italy documented and Legal sign-off attached
- [ ] Retention and deletion policies documented and implementable via APIs
- [ ] PII field mapping and minimisation validated by Security
- [ ] CRM mapping and data-sharing contract documented
- [ ] Audit logging and retention for verification / audit records defined
- [ ] Final schema DDL or ERD attached as evidence
- [x] Accepted by owner — see Status field in Metadata

## Acceptance

Status: `Accepted`
