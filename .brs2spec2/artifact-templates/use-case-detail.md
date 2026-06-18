# Use Case: {{UC Title}}

## Overview

| Field | Value |
|---|---|
| Use Case ID | UC-NNN |
| Use Case Name | {{title}} |
| Primary Actor | ACT-NNN / {{role name}} |
| Secondary Actors | ACT-NNN, SYS-NNN |
| Goal | As a {{role}}, I want to {{action}} so that {{outcome}}. |
| Status | Draft |
| FR Sources | FR-NNN, FR-NNN |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |

---

## Preconditions

- {{System state required before this UC can start}}
- {{Actor state required}}

---

## Main Success Scenario

| Step | Actor | Action |
|---|---|---|
| 1 | ACT-NNN | {{action}} |
| 2 | System | {{response}} |
| 3 | ACT-NNN | {{action}} |
| 4 | System | {{response}} |

---

## Alternative Flows

### A1: {{Alternative name}}

Branches from step N when {{condition}}.

| Step | Actor | Action |
|---|---|---|
| A1.1 | ACT-NNN | {{action}} |
| A1.2 | System | {{response}} |

Rejoins main scenario at step N / ends here.

---

## Exception Paths

### E1: {{Exception name}}

Triggered when: BR-NNN — {{condition that causes the exception}}.

| Step | Actor | Action |
|---|---|---|
| E1.1 | System | {{error response}} |
| E1.2 | ACT-NNN | {{actor response or end}} |

---

## Postconditions

**Success:**
- {{Observable system state after UC completes successfully}}

**Failure:**
- {{Observable system state if UC terminates without success}}

---

## Business Rules Referenced

| BR-NNN | Rule Statement | Applied at Step |
|---|---|---|
| BR-001 | {{rule}} | Step N / Exception path E1 |

---

## FR Sources

| FR-NNN | Title | Covered by |
|---|---|---|
| FR-001 | {{title}} | Main scenario step N |

---

*Set Status: Accepted after product owner review. Do not self-accept.*
*One file per use case only. Never merge multiple UCs into this file.*
