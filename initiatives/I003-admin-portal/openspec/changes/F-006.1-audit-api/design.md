# Design — F-006.1 Audit API (backend)

What this story touches:
- Append-only audit store, write API and export endpoint.

Data model: `audit_events` table with fields `event_id`, `initiated_by`, `timestamp`, `action`, `resource_id`, `details`.

Security:
- Audit write operations must be authenticated and validated; exports require elevated access.
