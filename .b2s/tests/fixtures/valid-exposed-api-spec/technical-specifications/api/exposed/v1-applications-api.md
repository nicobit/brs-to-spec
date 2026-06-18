# Applications API — Exposed API Specification

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | In progress |
| API ID | API-001 |
| Initiative ID | I001-loan-origination |
| Contract mode | product |
| Version | 1.0.0 |
| Owner | platform-team |
| Created at | 2026-06-17 |
| Created by | engineering-lead |

## Purpose

Exposes the loan application lifecycle to external broker partners and internal
origination UI. Consumers submit, retrieve, and update applications via this
surface. The surface is frozen early because external partners build against it.

## Consumer Context

| Consumer | Type | Dependency level | Story ref |
|---|---|---|---|
| Broker portal | external | blocking | F-001.1 |
| Origination UI | internal | non-blocking | F-001.2 |

## Traceability

| Source | Reference | Description |
|---|---|---|
| BRS | FR-001 | Submit a new loan application |
| Architecture | ARCH-C-001 | All external APIs must use OAuth2 client credentials |
| Business rule | BR-001 | Application must include applicant NID |

## Endpoint Catalog

| ID | Method | Path | Purpose | FR ref |
|---|---|---|---|---|
| EP-001 | POST | /v1/applications | Submit a new loan application | FR-001 |
| EP-002 | GET | /v1/applications/{id} | Retrieve application status | FR-002 |

## Endpoint Definitions

### EP-001: POST /v1/applications

**Purpose:** Submit a new loan application from broker or internal origination UI
**Authentication:** OAuth2 client credentials
**Authorization:** scope: applications:write
**Story ref:** F-001.1

**Request:**

| Field | Type | Required | Validation | BR ref |
|---|---|---|---|---|
| applicant_nid | string | Yes | 11 digits | BR-001 |
| requested_amount | decimal | Yes | > 0 | BR-002 |
| term_months | integer | Yes | 12–360 | BR-003 |

**Response — 200 OK:**

| Field | Type | Description |
|---|---|---|
| application_id | uuid | Assigned application identifier |
| status | string | Initial status: pending |

**Error responses:**

| HTTP Status | Code | Condition |
|---|---|---|
| 400 | VALIDATION_ERROR | Missing or invalid required field |
| 401 | UNAUTHORIZED | Invalid or expired token |
| 422 | UNPROCESSABLE | Business rule violation |

**Idempotency:** No
**Rate limit:** 100 req/min per client

## Authentication and Authorisation

| Field | Value |
|---|---|
| Auth mechanism | OAuth2 client credentials |
| Required scope | applications:write, applications:read |
| Role restrictions | broker role may submit; underwriter may read only |
| Token lifetime | 3600 |

## Versioning Policy

| Field | Value |
|---|---|
| Strategy | semver |
| Breaking change process | major version increment, 90-day deprecation notice |
| Deprecation notice period | 90 days |
| Backward compatibility | additive only |

## SLAs

| Endpoint | P50 (ms) | P99 (ms) | Timeout (ms) | Source |
|---|---|---|---|---|
| EP-001 | 120 | 400 | 5000 | BRS §3.2 |
| EP-002 | 80 | 250 | 5000 | BRS §3.2 |

## Contract Tests

| Field | Value |
|---|---|
| Test framework | Pact |
| CI enforcement | Yes |
| Provider verification | consumer-driven |

## Open Questions

| # | Question | Owner | Needed before | Status |
|---|---|---|---|---|

---
*Status: In progress — set to Accepted only after architecture review sign-off. Never self-accept.*
