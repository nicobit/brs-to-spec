# Use Case Specifications

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |
| Status | Draft |

## Use Case Catalog

| UC-NNN | Title | Primary Actor | Goal | FR Coverage |
|---|---|---|---|---|
| UC-001 | | ACT-NNN | | FR-NNN, FR-NNN |

---

## UC-001: {{Use Case Title}}

**Primary actor:** ACT-NNN  
**Secondary actors:** ACT-NNN, SYS-NNN  
**Goal:** As a {{role}}, I want to {{action}} so that {{outcome}}.

**Preconditions:**
- {{System state required before UC can start}}

**Main success scenario:**

| Step | Actor | Action |
|---|---|---|
| 1 | ACT-NNN | {{action}} |
| 2 | System | {{response}} |

**Alternative flows:**

| AF | Branches from | Condition | Steps |
|---|---|---|---|
| UC-001-A | Step N | {{condition}} | ... |

**Exception paths:**

| EP | Triggered by | Outcome |
|---|---|---|
| UC-001-E1 | BR-NNN violation | {{system response}} |

**Postconditions:**
- {{Observable system state after UC completes}}

**Business rules in force:** BR-NNN, BR-NNN

**AC coverage:**

| AC-NNN | Criterion | Covered by |
|---|---|---|
| AC-001 | {{verbatim criterion}} | Main scenario step N |

**Related stories:** F-XXX.X, F-XXX.X  
**BRS source:** FR-NNN, §Section

---

## FR Coverage Table

| FR-NNN | Description summary | Covered by UC-NNN | Step / Path |
|---|---|---|---|
| FR-001 | {{summary}} | UC-NNN | Main scenario step N |

## Coverage Summary

| Item | Count |
|---|---|
| Total FR-NNN in BRS | N |
| FR-NNN covered by at least one UC | N |
| FR-NNN explicitly excluded (with justification) | N |
| FR-NNN uncovered (must be zero for Status: Draft — complete) | N |
| Total UC-NNN produced | N |
| Total ACT-NNN covered as primary actor | N |

**Exclusions (if any):**
- FR-NNN: {{justification for exclusion}}

---
*Set Status: Accepted after review. Do not self-accept.*
