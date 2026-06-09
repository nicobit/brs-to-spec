# Design — F-002.1 Tenant mapping API (backend)

What this story touches:
- Tenant mapping service, sample data endpoints, and validation logic.

API surface: `GET /tenants/{tenantId}/subscriptions`

Security:
- Require Azure AD auth and ensure callers have rights to query mapping for the requested tenant.

Open questions:
- How to represent multi-subscription tenants if encountered later.
