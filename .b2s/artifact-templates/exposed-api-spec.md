# {{API Name}} — Exposed API Specification

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| API ID | {{api_id}} |
| Initiative ID | {{initiative_id}} |
| Contract mode | {{product / internal / coordinated}} |
| Version | {{semver, e.g. 1.0.0}} |
| Owner | {{team or role}} |
| Created at | {{date}} |
| Created by | engineering-lead |

## Purpose

{{One paragraph: what this API does, who consumes it, and why it exists as a published surface.}}

## Consumer Context

| Consumer | Type | Dependency level | Story ref |
|---|---|---|---|
| {{consumer name}} | {{internal / external}} | {{blocking / non-blocking}} | {{FR-NNN or F-NNN.N}} |

## Traceability

| Source | Reference | Description |
|---|---|---|
| BRS | FR-NNN | {{requirement that mandates this API surface}} |
| Architecture | ARCH-C-NNN | {{constraint on auth, versioning, or transport}} |
| Business rule | BR-NNN | {{rule enforced at this boundary}} |

## Endpoint Catalog

| EP-NNN | Method | Path | Purpose | FR ref |
|---|---|---|---|---|
| EP-001 | GET / POST / PUT / PATCH / DELETE | /v1/... | {{one line}} | FR-NNN |

## Endpoint Definitions

### EP-001: {{METHOD}} {{/v1/path}}

**Purpose:** {{one line}}
**Authentication:** {{OAuth2 / API key / mTLS — must match architecture rules}}
**Authorization:** {{roles or scopes required}}
**Story ref:** {{F-NNN.N or FR-NNN}}

**Request:**

| Field | Type | Required | Validation | BR ref |
|---|---|---|---|---|
| {{field}} | {{string / int / date / decimal / uuid}} | {{Yes / No}} | {{rule}} | {{BR-NNN or —}} |

**Response — 200 OK:**

| Field | Type | Description |
|---|---|---|
| {{field}} | {{type}} | {{description}} |

**Error responses:**

| HTTP Status | Code | Condition |
|---|---|---|
| 400 | VALIDATION_ERROR | {{when}} |
| 401 | UNAUTHORIZED | {{when}} |
| 404 | NOT_FOUND | {{when}} |
| 422 | UNPROCESSABLE | {{when}} |

**Idempotency:** {{Yes / No — behaviour on retry}}
**Rate limit:** {{N req/min per client / None}}

## Authentication and Authorisation

| Field | Value |
|---|---|
| Auth mechanism | {{OAuth2 client credentials / API key / mTLS}} |
| Required scope | {{scope name}} |
| Role restrictions | {{which roles may call which endpoints}} |
| Token lifetime | {{seconds}} |

## Versioning Policy

| Field | Value |
|---|---|
| Strategy | {{semver / date-based}} |
| Breaking change process | {{describe}} |
| Deprecation notice period | {{N weeks / months}} |
| Backward compatibility | {{additive only / versioned contract}} |

## SLAs

| EP-NNN | P50 (ms) | P99 (ms) | Timeout (ms) | Source |
|---|---|---|---|---|
| EP-001 | {{ms}} | {{ms}} | {{ms}} | {{BRS §N / architecture constraint}} |

## Contract Tests

| Field | Value |
|---|---|
| Test framework | {{Pact / other / not yet decided}} |
| CI enforcement | {{Yes / No}} |
| Provider verification | {{how — consumer-driven / provider mock}} |

## Open Questions

| # | Question | Owner | Needed before | Status |
|---|---|---|---|---|
| 1 | {{question}} | {{owner}} | {{milestone}} | Open |

---
*Status: In progress — set to Accepted only after architecture review sign-off. Never self-accept.*
