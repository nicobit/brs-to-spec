# Dynamic Next Action Decision

## Summary

Select `create-atomic-requirements` to generate a canonical `requirements/atomic-requirements.md` from the Business Requirements Specification. Producing atomic requirements addresses traceability and validation gaps and enables reliable epic mapping and downstream planning.

## Decision

| Field | Value |
|---|---|
| Selected action | create-atomic-requirements |
| Persona | product-owner |
| Current macro phase | requirements-and-architecture |
| Primary gap addressed | DYN-GAP-001 (requirements_gap) |
| Decision confidence | medium |

## Justification

| Reason Type | Detail |
|---|---|
| Blocking issue | Initiative metadata mismatch and missing canonical requirements inventory prevent validation and artifact generation. |
| Why this action now | Creating atomic requirements directly targets traceability gaps, is low-risk, and unlocks many downstream actions (epic creation, planning). |
| Why not other actions | Fixing epics or planning before establishing canonical requirements risks propagating inconsistent IDs and will likely require rework. |

## Expected Outcome

`requirements/atomic-requirements.md` will exist with canonical requirement IDs and titles aligned to the BRS, enabling validators and downstream artifact generators to produce traceable epics and stories.

## Reassessment Rule

- After validation, re-run the dynamic gap assessment to confirm that the primary gaps (traceability and metadata) are resolved and that epics can be created without renaming IDs.

