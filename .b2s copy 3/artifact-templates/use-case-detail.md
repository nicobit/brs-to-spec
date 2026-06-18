# Use Case: {{UC Title}}

## Overview

| Field | Value |
|---|---|
| Use Case ID | UC-NNN |
| Use Case Name | {{title}} |
| Primary Actor | ACT-NNN / role name |
| Secondary Actors | ACT-NNN, SYS-NNN |
| Goal | As a role, I want to do something so that an outcome is achieved. |
| Status | Draft |
| FR Sources | FR-NNN, FR-NNN |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | product-owner |

---

## Preconditions

- System state required before this UC can start
- Actor state required before this UC can start

---

## Main Success Scenario

| Step | Actor | Action |
|---|---|---|
| 1 | ACT-NNN | action |
| 2 | System | response |

---

## Alternative Flows

### A1: Alternative name

Branches from step N when condition applies.

| Step | Actor | Action |
|---|---|---|
| A1.1 | ACT-NNN | action |
| A1.2 | System | response |

Rejoins main scenario at step N or ends here.

---

## Exception Paths

### E1: Exception name

Triggered when BR-NNN condition is violated.

| Step | Actor | Action |
|---|---|---|
| E1.1 | System | error response |
| E1.2 | ACT-NNN | actor response or end |

---

## Postconditions

**Success:**
- Observable business state after successful completion

**Failure:**
- Observable business state if the use case ends without success

---

## Business Rules Referenced

| BR-NNN | Rule Statement | Applied at Step |
|---|---|---|
| BR-001 | rule | Step N / Exception path E1 |

---

## FR Sources

| FR-NNN | Title | Covered by |
|---|---|---|
| FR-001 | title | Main scenario step N |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
*One file per use case only. Never merge multiple UCs into this file.*
