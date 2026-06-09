# Data Specs — F-006.1 Audit API

Table: `audit_events`

- Columns: `event_id`, `initiated_by`, `initiated_at`, `action`, `resource_id`, `details` (JSON)
- Retention: 365 days by default; exportable to cold storage
