# Design — F-005.1 Diagnostics API (backend)

What this story touches:
- Diagnostics probe endpoints and Log Analytics deep-link generator.

API surface:
- `GET /diagnostics/{resourceId}` → returns health summary and `log_analytics_link`.

Observability:
- Ensure probes emit health metrics and include correlation ids.
