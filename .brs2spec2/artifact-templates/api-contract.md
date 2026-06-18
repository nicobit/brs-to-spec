# API Contract

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |

## Endpoint Catalog

| EP-NNN | Method | Path | Purpose | Auth | Consumer Impact |
|---|---|---|---|---|---|
| EP-001 | GET / POST / PUT / PATCH / DELETE | /api/v1/... | | JWT / API key / None | None / Breaking / Additive |

## Endpoint Definitions

### EP-001: {{Method}} {{Path}}

**Purpose:** {{one line}}  
**Authentication:** {{JWT — required claims: sub, role:X / API key / None}}  
**Authorization:** ACT-NNN ({{role name}}) only / ACT-NNN and ACT-NNN

**Request:**

| Field | Type | Required | Constraints | BR-NNN |
|---|---|---|---|---|
| | string/int/date/decimal | Yes / No | | |

**Response (200 OK):**

| Field | Type | Description |
|---|---|---|

**Error responses:**

| HTTP Code | Condition | Response body |
|---|---|---|
| 400 | Invalid input — {{specific field}} | `{"error": "VALIDATION_ERROR", "field": "..."}` |
| 401 | Missing or invalid auth token | `{"error": "UNAUTHORIZED"}` |
| 403 | Insufficient role | `{"error": "FORBIDDEN"}` |
| 404 | Resource not found | `{"error": "NOT_FOUND"}` |
| 409 | Conflict — {{condition}} | `{"error": "CONFLICT", "detail": "..."}` |

**Idempotency:** Yes / No — {{behaviour on retry}}  
**Rate limit:** {{N req/min per client / None}}  
**Backward compatible:** Yes / No — {{if No: breaking change description}}

## Error Code Reference

| Code | HTTP Status | Condition |
|---|---|---|
| VALIDATION_ERROR | 400 | |
| UNAUTHORIZED | 401 | |
| FORBIDDEN | 403 | |
| NOT_FOUND | 404 | |

## Versioning and Consumer Impact

| EP-NNN | Change type | Affected consumers | Migration plan | Deprecation window |
|---|---|---|---|---|
| | Additive / Breaking | | | |

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

## Decision

**Decision:** Approved / Request Changes / Blocked

---
*Status: In progress — set to Accepted by engineering/arch gate owner. Never self-accept.*
