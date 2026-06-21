# Test Data Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | qa-analyst |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Stories covered | N |
| Data entities required | N |
| PII fields identified | N |
| Mocks / stubs required | N |

---

## Test Data by Story

### {{Story ID}} — {{Story Title}}

#### Required Data Entities

| Entity | Fields Required | Volume | Constraints | Source |
|---|---|---|---|---|
| {{entity}} | {{field list}} | {{N records}} | {{validation rules, FK constraints}} | REQ-NNN / BR-NNN |

#### PII Handling

| Field | Entity | PII Type | Test Environment Treatment |
|---|---|---|---|
| {{field}} | {{entity}} | Name / Email / DOB / Financial / Identity | Masked / Pseudonymised / Synthetic |

#### Mock and Stub Requirements

| External System | Endpoint / Event | Mock Type | Behaviour | Failure Scenarios |
|---|---|---|---|---|
| {{system}} | {{endpoint}} | HTTP mock / Event stub / Service fake | {{success response}} | Timeout / 5xx / Auth failure / Rate limit |

#### Test Data Seeding

| Scenario | Precondition Data | Setup Method |
|---|---|---|
| {{SCN-NNN}} | {{what data must exist before test}} | Seed script / API call / DB insert |

---

## Shared Test Data

| Entity | Shared Across Stories | Volume | Notes |
|---|---|---|---|
| | | | |

---

## Non-Functional Test Data

| Test Type | Data Requirements | Volume | Notes |
|---|---|---|---|
| Performance | | {{N records}} | |
| Load | | {{N concurrent}} | |
| Security | | | |

---
*Set Status: Accepted only after QA review. Never self-accept.*
