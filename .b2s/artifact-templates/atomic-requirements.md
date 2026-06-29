# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | N |
| Business objectives | N |
| Functional | N |
| Non-functional | N |
| Data | N |
| Integration | N |
| Security | N |
| Operational | N |
| Reporting | N |
| Constraints | N |
| Blocking questions | N |

---

## Source Inventory

| Source ID | Type | Title / Summary | Preserved In |
|---|---|---|---|
| OBJ-001 | Objective | {{Business objective summary}} | OBJ-001 |
| FR-001 | Functional | {{Original BRS functional requirement title}} | FR-001 |
| NFR-001 | Non-functional | {{Original BRS non-functional requirement title}} | NFR-001 |
| C-001 | Constraint | {{Constraint summary}} | C-001 |

---

## Requirement Catalogue

### FR-001 - {{Short title}}

**Source:** {{BRS section}} | **Actor:** {{actor}} | **Deps:** {{FR-NNN or None}}

WHEN {{trigger}},
THE SYSTEM SHALL {{behaviour with concrete values from BRS}}.

IF {{error/edge condition}},
THEN THE SYSTEM SHALL {{fallback behaviour}}.

> **Ambiguities:** {{if any, otherwise omit this line}}
> **Blocking:** {{if any, otherwise omit this line}}

---

## Source ID Mapping

| Source ID | Optional REQ Alias | Mapping Type | Notes |
|---|---|---|---|
| FR-001 | {{REQ-001 or blank}} | Direct / Grouped / Deferred / Alias omitted | {{Why this source ID maps here}} |
| NFR-001 | {{REQ-00N or blank}} | Direct / Grouped / Deferred / Alias omitted | {{Why this source ID maps here}} |
| OBJ-001 | {{REQ-00N or blank}} | Context / Grouped / Deferred / Alias omitted | {{How the objective is preserved}} |
| C-001 | {{REQ-00N or blank}} | Direct / Constraint / Deferred / Alias omitted | {{How the constraint is preserved}} |

---

## Open Questions

| ID | Question | Source ID | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | | FR-NNN / NFR-NNN / OBJ-NNN / C-NNN | Yes / No | | Open / Proposed answer from architecture input |

---

## Assumptions

| ID | Assumption | Source ID | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | | FR-NNN / NFR-NNN / OBJ-NNN / C-NNN | | | Open |

---

## Traceability Notes

{{Notes on BRS coverage, optional REQ aliases, grouped mappings, deferred items, or sections that produced no implementation-ready requirement. Silent loss is not allowed.}}

## Loss Check

| Check | Result | Notes |
|---|---|---|
| Every `FR-` from BRS preserved | Yes / No | |
| Every `NFR-` from BRS preserved | Yes / No | |
| Every `OBJ-` from BRS preserved | Yes / No | |
| Every explicit constraint preserved | Yes / No | |
| Every optional `REQ-` alias has source mapping | Yes / No | |
| Any intentionally deferred item explained | Yes / No | |

---
*Set Status: Accepted only after human review. Never self-accept.*
