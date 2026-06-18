# API Contract

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T19:20:00+00:00 |
| Created by | engineering-lead |

## Endpoint Catalog

| EP-NNN | Method | Path | Purpose | Auth | Consumer Impact |
|---|---|---|---|---|---|
| EP-001 | POST | /api/v1/applications | Submit new loan application (creates ARN) | JWT (app) / API key (partner) | Additive (new)
| EP-002 | GET | /api/v1/applications/{arn}/status | Retrieve application status by ARN | JWT / API key | Additive
| EP-003 | POST | /api/v1/applications/{arn}/score | Trigger/receive scoring result (internal) | Mutual TLS / Service JWT | Internal API — consumer: scoring service
| EP-004 | POST | /api/v1/underwriter/queue | Create underwriter queue item | Service JWT | Additive (internal)
| EP-005 | POST | /api/v1/offers/{arn}/generate | Generate loan offer document | Service JWT | Additive
| EP-006 | POST | /api/v1/disbursements | Trigger disbursement to T24 (adapter) | Service JWT, signed payload | Breaking (financial) — high impact
| EP-007 | GET | /api/v1/metrics/health | Health and readiness | None / API key internal | Additive

## Endpoint Definitions

### EP-001: POST /api/v1/applications

**Purpose:** Receive applicant-submitted loan application and return ARN.
**Authentication:** JWT for portal users; API key for partner integrations.
**Authorization:** Public submission allowed; partner tokens limited by scopes.

**Request (201 Created expected):**

| Field | Type | Required | Constraints | BR-NNN |
|---|---|---|---|---|
| firstName | string | Yes | max 255 | FR-001 |
| lastName | string | Yes | max 255 | FR-001 |
| dateOfBirth | date | Yes | ISO-8601 | FR-001 |
| nationalInsuranceNumber | string | Yes | normalized, encrypted at rest | FR-001 |
| employmentStatus | string | Yes | enum: [Employed, SelfEmployed, Unemployed] | FR-008 |
| annualIncome | decimal | Yes | >=0 | FR-008 |
| amountRequested | decimal | Yes | 1000..50000 | FR-001 |
| termMonths | int | Yes | 12..84 | FR-001 |

**Response (201):**

| Field | Type | Description |
|---|---|---|
| arn | string | Application Reference Number (ARN) |
| status | string | Initial status (SUBMITTED) |

**Error responses:**

| HTTP Code | Condition | Response body |
|---|---|---|
| 400 | Validation error | {"error":"VALIDATION_ERROR","details":...} |
| 429 | Rate limit exceeded | {"error":"RATE_LIMIT"} |

**Idempotency:** Clients SHOULD send an `Idempotency-Key` header for retries; server will dedupe within 24h.
**Rate limit:** 60 req/min per client (adjustable per SLAs).
**Backward compatible:** Additive for fields; breaking changes require versioning.

---

### EP-002: GET /api/v1/applications/{arn}/status

**Purpose:** Allow applicants (or partners) to check status by ARN and DOB.
**Authentication:** JWT or API key with read scope; applicants may use ARN+DOB flow (no login) with ephemeral token.

**Response (200):**

| Field | Type | Description |
|---|---|---|
| arn | string | ARN |
| status | string | e.g. SUBMITTED, SCORING, OFFERED, DISBURSED |
| decision | string | AI recommendation where available |

**Errors:** 404 for unknown ARN, 403 for missing DOB verification.
**Idempotency:** N/A
**Rate limit:** 120 req/min per client

---

### EP-003: POST /api/v1/applications/{arn}/score

**Purpose:** Internal endpoint for the scoring service to POST results or for controller to request synchronous scoring.
**Authentication:** Mutual TLS or Service JWT.

**Request:**

| Field | Type | Required | Description |
|---|---|---|---|
| score | int | Yes | 0..1000 |
| recommendation | string | Yes | AUTO_APPROVE / REFER_TO_UNDERWRITER / AUTO_DECLINE |
| details | object | No | Optional scoring metadata |

**Response:** 200 OK with acceptance. 202 if handled async.
**Idempotency:** Endpoint supports idempotent replays when `Idempotency-Key` provided.

---

### EP-004: POST /api/v1/underwriter/queue

**Purpose:** Create a queue item for manual review.
**Authentication:** Service JWT.

**Request:** include ARN, reason, payload snapshot.
**Idempotency:** Ensure single queue item per ARN per reason.

---

### EP-005: POST /api/v1/offers/{arn}/generate

**Purpose:** Generate offer document and persist offer state.
**Authentication:** Service JWT.

**Response:** 201 with offer id and download link.

---

### EP-006: POST /api/v1/disbursements

**Purpose:** Trigger disbursement adapter to send instruction to Temenos T24.
**Authentication:** Service JWT; request must include signed payload and transaction reference.

**Request:** accountNumber, sortCode, amount, valueDate, arn, idempotencyKey

**Idempotency:** MUST be idempotent by `idempotencyKey` to prevent duplicate payments.
**Rate limit:** Low; bulk and single; ops to set limits.
**Backward compatible:** Breaking — changes must be versioned; adapter shields callers.

---

### EP-007: GET /api/v1/metrics/health

**Purpose:** Readiness and health probe for load balancer and orchestration.
**Auth:** None for local, API key for external.

---

## Error Code Reference

| Code | HTTP Status | Condition |
|---|---|---|
| VALIDATION_ERROR | 400 | Input validation failure |
| RATE_LIMIT | 429 | Throttling |
| NOT_FOUND | 404 | Resource not found |

## Versioning and Consumer Impact

| EP-NNN | Change type | Affected consumers | Migration plan | Deprecation window |
|---|---|---|---|---|
| EP-006 | Breaking | Payments / Ops | Adapter versioning; consumer migration doc; 90d deprecation |
| EP-001 | Additive | Partners, Portal | Additive fields are safe; document optional fields | 30d notice for contract changes |

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Experian latency affects scoring SLA | Scoring delay → user experience | Circuit breaker, fallback to refer-to-underwriter, surface degraded status | engineering-lead |
| Disbursement adapter mapping errors | Financial misrouting | Idempotency, reconciliation, ops manual remediation | ops |

## Decision

**Decision:** In progress — requires engineering and ops review for EP-006 and final auth model.

---
*Status: In progress - set to Accepted by the engineering or architecture gate owner. Never self-accept.*
# API Contract

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T19:18:00+00:00 |
| Created by | engineering-lead |
| Status | Draft |

## APIs

### Intake API

- POST /applications — creates application (F-XXX.X)
- Schema: application_id, applicant_id, amount, term_months, status

### Decision API

- POST /decisions — records decision result; includes score and recommendation

## Versioning and Contracts

- Use semantic versioning for API contracts; publish OpenAPI specs to repo.

## Endpoint Catalog

| Path | Method | Description |
|---|---:|---|
| /applications | POST | Create new application |
| /decisions | POST | Record decision result |

## Endpoint Definitions

### POST /applications

- Request: application payload with applicant details, requested amount, term
- Response: 201 Created with `application_id`

### POST /decisions

- Request: decision payload (application_id, score, recommendation)
- Response: 200 OK

## Error Code Reference

| Code | Meaning |
|---|---|
| 400 | Bad request — validation failed |
| 401 | Unauthorized |
| 500 | Internal server error |

## Accepted Risks

- Partial parity between T24 sandbox and production — mitigated via feature flags and staged rollout.

## Versioning and Consumer Impact

- Minor version bumps allowed for non-breaking changes; breaking changes require consumer notice and migration plan.
