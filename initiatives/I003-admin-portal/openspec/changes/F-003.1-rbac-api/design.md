# Design — F-003.1 RBAC API (backend)

What this story touches:
- APIs to read and map Azure AD groups to internal roles, and an endpoint to assign role mappings.

API surface:
- `GET /roles/{tenantId}/mappings`
- `POST /roles/{tenantId}/assign` (assign role to principal)

Security:
- Must use Azure AD for auth; operations that modify role mappings require elevated role.
