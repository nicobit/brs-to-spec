# Design — F-001.2 Inventory UI (frontend)

What this story touches:
- React UI list component for inventory, filters, CSV export button

Integration points:
- Calls `GET /inventory` (F-001.1)

Observability:
- Emit UI telemetry for export and filter usage

Open questions:
- Export size limits and background export job requirements
