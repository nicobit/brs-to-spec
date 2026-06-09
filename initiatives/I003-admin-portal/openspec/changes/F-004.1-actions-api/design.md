# Design — F-004.1 Actions API (backend)

What this story touches:
- Actions API endpoint and job processing for async operations; orchestrator component.

API surface: see `quality-gates/api-contract.md` and `specs/api.md`.

Security:
- Enforce Azure AD auth and role checks; require `AdminPortalActionRunner` role for orchestrator to call target subscription APIs.

Observability:
- Emit job lifecycle metrics (`jobs.created`, `jobs.duration`, `jobs.failures`) and trace tokens.
