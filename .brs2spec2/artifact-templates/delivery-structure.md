# Delivery Structure

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Delivery mode | {{delivery_mode}} |
| Execution mode | {{execution_mode}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |
| Status | Draft |

## Story Count Assertion

**Total stories:** N  
**Must:** N | **Should:** N | **Could:** N  
**Delivery increments:** D1 (N stories), D2 (N stories)  *(Enterprise+Modular only)*

---

## E-001: {{Epic Name}}

*{{One sentence: the business capability this epic delivers}}*

### F-001: {{Feature Name}}

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-001.1 | As a {{actor}}, I want to {{action}}, so that {{outcome}}. | AC-NNN | Must | D1 |
| F-001.2 | As a {{actor}}, I want to {{action}}, so that {{outcome}}. | AC-NNN | Should | D1 |

---

## E-002: {{Epic Name}}

### F-002: {{Feature Name}}

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-002.1 | | | | |

---

## FR Coverage

<!-- One row per FR-NNN from input/brs.md. Do NOT bundle as ranges (FR-001..FR-023 is forbidden).
     Every FR must appear as its own row with at least one specific F-NNN.X story ID. -->

| FR-NNN | Stories | Status |
|---|---|---|
| FR-001 | F-001.1, F-001.2 | Covered |
| FR-002 | F-002.1 | Covered |
| FR-003 | F-001.3 | Covered |

---
*Set Status: Confirmed once all stories are approved for engineering handoff.*
