# Observability — F-001.1 Inventory API

- Emit metric: `inventory.request.count` (by tenant, status)
- Emit metric: `inventory.request.duration` (histogram)
- Trace: include `trace_id` and `tenant_id` in request telemetry
