# Security Review

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |

## Security Findings

| Finding ID | Severity | Domain | Evidence | Risk | Recommendation | Owner | Required Before | Blocking? |
|---|---|---|---|---|---|---|---|---|
| SEC-001 | Critical / High / Medium / Low | Authorization / Authentication / Input Validation / Data Handling / Audit / Integration | | | | | Fix / Merge / Release | Yes / No |

**Severity definitions:**
- Critical: exploitable without authentication or allows data breach
- High: exploitable with user credentials or allows unauthorized access
- Medium: design weakness that increases risk surface
- Low: best practice gap with low exploitation probability

## Security Control Coverage

| Control | Status | Evidence |
|---|---|---|
| Authentication | In place / Missing / Partial | |
| Authorization (RBAC) | | |
| Input validation | | |
| PII encryption at rest | | |
| PII encryption in transit | | |
| Audit trail | | |
| PII-safe logging | | |
| Integration auth | | |

## Accepted Risks

| Risk | Justification | Owner | Review date |
|---|---|---|---|

## Decision

**Decision:** Approved / Request Changes / Blocked  
**Rationale:** {{reason}}

---
*Status: In progress — set to Accepted by security gate owner. Never self-accept.*
