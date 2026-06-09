# Data Spec — F-001.2: Persist Profile and Consent

## consents — created

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `consent_id` | UUID (PK) | No | — | |
| `profile_id` | UUID (FK → profiles) | No | — | CASCADE on profile delete |
| `consent_type` | string | No | — | `terms`, `marketing` |
| `granted` | boolean | No | — | |
| `granted_at` | timestamp | No | — | UTC |
| `source` | string | No | — | `web`, `mobile` |

Migration notes: new table.

## audit_logs — created

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|
| `audit_id` | UUID (PK) | No | — | |
| `entity` | string | No | — | `profile`, `verification_record`, etc. |
| `entity_id` | UUID | No | — | |
| `action` | string | No | — | `create`, `update`, `delete`, etc. |
| `actor` | string | No | — | Service name or internal user ID — never display names |
| `details` | jsonb | No | — | Non-PII details only — never include email, phone, or raw IDP payload |
| `timestamp` | timestamp | No | — | UTC |

Migration notes: new table. Retention: minimum 1 year — archive after retention window.
