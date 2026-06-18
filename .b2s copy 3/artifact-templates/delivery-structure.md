# Delivery Structure

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Delivery mode | {{delivery_mode}} |
| Execution mode | {{execution_mode}} |
| Created at | {{date}} |
| Created by | delivery-lead |
| Status | Draft |

## Story Count Assertion

**Total stories:** N  
**Must:** N | **Should:** N | **Could:** N  
**Delivery increments:** D1 (N stories), D2 (N stories)

---

## E-001: {{Epic Name}}

*{{One sentence: the business capability this epic delivers}}*

### F-001: {{Feature Name}}

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-001.1 | As a {{actor}}, I want to {{action}}, so that {{outcome}}. | AC-NNN | Must | D1 |
| F-001.2 | As a {{actor}}, I want to {{action}}, so that {{outcome}}. | AC-NNN | Should | D1 |

#### F-001.1 — Story Detail

| Field | Value |
|---|---|
| Actor | {{actor name — specific role, not "user"}} |
| Linked requirements | FR-NNN, FR-NNN |
| Linked business rules | BR-NNN, BR-NNN |
| Primary component | {{component name from architecture review}} |
| Out of scope | {{one sentence: what a developer might assume is included but is not}} |

#### F-001.2 — Story Detail

| Field | Value |
|---|---|
| Actor | {{actor name — specific role, not "user"}} |
| Linked requirements | FR-NNN, FR-NNN |
| Linked business rules | BR-NNN, BR-NNN |
| Primary component | {{component name from architecture review}} |
| Out of scope | {{one sentence: what a developer might assume is included but is not}} |

---

## FR Coverage

<!-- One row per FR-NNN from the source inputs. Do not bundle as ranges. -->

| FR-NNN | Stories | Status |
|---|---|---|
| FR-001 | F-001.1, F-001.2 | Covered |

---
*Set Status: Confirmed only after review and readiness progression. Never self-accept.*
