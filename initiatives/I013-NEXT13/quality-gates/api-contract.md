## Metadata

- Initiative: I013-NEXT13
- Artifact: API Contract
- Author: b2s-agent
- Status: Draft

## API Overview

- Public APIs: `POST /loans`, `GET /loans/{id}`, `POST /decisions`, `GET /decisions/{id}`.

## Schemas

- LoanRequest, LoanResponse, DecisionRequest, DecisionResponse (define canonical fields and required/optional attributes).

## Endpoint Catalog

| Path | Method | Purpose |
|---|---:|---|
| /loans | POST | Create loan application |
| /loans/{id} | GET | Retrieve loan status |
| /decisions | POST | Submit decision request |
| /decisions/{id} | GET | Fetch decision result |

## Endpoint Definitions

- `POST /loans`: accepts `LoanRequest` JSON; returns `LoanResponse` with status and reference ID.
- `GET /loans/{id}`: returns `LoanResponse` or 404 if not found.

## Error Code Reference

- 400: Bad Request — validation errors (provide field-level errors).
- 401: Unauthorized — invalid token.
- 403: Forbidden — insufficient scope.
- 404: Not Found — resource missing.
- 500: Internal Server Error — retryable error with correlation id.

## Versioning and Consumer Impact

- Follow semantic versioning for public APIs; incompatible schema changes require a major version update and migration guide.

## Accepted Risks

- Some non-critical telemetry fields may change; consumers should ignore unknown fields (forward-compatible).

## Decision

- API contract provisionally accepted; consumer contract tests must be implemented in CI before release.

## Versioning and Compatibility

- Semantic versioning for API surface; breaking changes require major version bump and migration notes.

## Contract Tests

- Use Pact or equivalent for consumer-driven contract tests; include CI verification for all provider changes.

## Security and Authentication

- APIs use OAuth2 introspection for service-to-service calls; client credentials for backend integrations.

## SLAs and Error Handling

- Define expected response times and error codes for client guidance.

## CI Integration

- Contract tests run in CI and must pass before merge to main.
