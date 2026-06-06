# Stop Conditions

Do not proceed to Copilot implementation if any of these are true.

## Business stop conditions

- Critical business rules are unclear.
- User roles are undefined.
- Mandatory fields are missing.
- Approval workflow is ambiguous.
- Reporting output is unclear.
- Acceptance criteria are not testable.

## Engineering stop conditions

- Architecture impact is unknown.
- Database migration impact is unclear.
- Integration contracts are missing.
- Security/authorization rules are not defined.
- Audit/logging expectations are not defined.
- Backward compatibility impact is unknown.

## Copilot stop conditions

- Task is too large.
- Task mixes unrelated backend, frontend, DB, and integration work.
- Task has no Definition of Done.
- Task has no tests.
- Task requires business decisions not yet answered.
- Task asks Copilot to invent architecture.
