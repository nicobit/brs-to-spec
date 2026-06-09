# Design — F-002.2 Tenant selector UI (frontend)

What this story touches:
- Tenant/stage selector component, free-text search, and tag filters.

Integration points:
- Calls `GET /tenants/{tenantId}/subscriptions` and `GET /inventory` for context.
