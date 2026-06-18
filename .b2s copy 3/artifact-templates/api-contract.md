# API Contract

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | engineering-lead |

## Endpoint Catalog

| EP-NNN | Method | Path | Purpose | Auth | Consumer Impact |
|---|---|---|---|---|---|
| EP-001 | GET / POST / PUT / PATCH / DELETE | /api/v1/... | | JWT / API key / None | None / Breaking / Additive |

## Endpoint Definitions

### EP-001: Method Path

**Purpose:** one line  
**Authentication:** JWT / API key / None  
**Authorization:** ACT-NNN roles

**Request:**

| Field | Type | Required | Constraints | BR-NNN |
|---|---|---|---|---|
| | string / int / date / decimal | Yes / No | | |

**Response (200 OK):**

| Field | Type | Description |
|---|---|---|

**Error responses:**

| HTTP Code | Condition | Response body |
|---|---|---|
| 400 | Invalid input | `{"error":"VALIDATION_ERROR"}` |

**Idempotency:** Yes / No - behavior on retry  
**Rate limit:** N req/min per client / None  
**Backward compatible:** Yes / No - change description

## Error Code Reference

| Code | HTTP Status | Condition |
|---|---|---|
| VALIDATION_ERROR | 400 | |

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
*Status: In progress - set to Accepted by the engineering or architecture gate owner. Never self-accept.*
