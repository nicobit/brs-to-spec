# Prompt — Create OpenAPI Contract

Use when API contract-first implementation, mocking, validation, or frontend/backend alignment is needed.

Output:
Create or update:

```text
features/<feature-name>/architecture-contracts/openapi.yaml
```

Rules:
- Use OpenAPI 3.x.
- Follow existing API conventions.
- Include schemas, status codes, security requirements, and common error responses.
- Endpoints must match `api-contract.md`.
