# Dynamic Gap Assessment

## Summary

The initiative workspace contains a detailed Business Requirements Specification and a drafted high-level architecture. The atomic requirement catalogue has been created, reducing traceability ambiguity. Remaining gaps concern epic/repository mapping and planning artifacts needed to assign requirements to implementation components.

## Macro Phase

| Field | Value |
|---|---|
| Current macro phase | requirements-and-architecture |
| Assessment confidence | medium |
| Iteration count | 0 |

## Ranked Gaps

| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |
|---|---|---|---|---|---|
| DYN-GAP-001 | requirements_gap | critical | Initiative metadata and source-of-truth mismatch: BRS references `I005` while workspace is `I007_GAB` | `input/brs.md` Initiative ID = I005 vs workspace `I007_GAB` in `.b2s/state/workflow-state.json` | Confirm and correct initiative metadata in `input/brs.md` or reinitialize workspace to match official ID; verify stakeholders/owner fields. |
| DYN-GAP-002 | repository_mapping_gap | high | No epics or repository mapping present; delivery artifacts reference `epics/` but folder missing | `dispatch-next` reported `epics/` as an optional input that does not exist; `.b2s/tmp/dispatch-next.json` | Create `epics/` structure or provide mapping of epics to implementation repositories; populate minimal epic stubs for traceability. |
| DYN-GAP-003 | requirements_gap | low | Canonical `requirements/atomic-requirements.md` now exists but needs verification and mapping to epics | `requirements/atomic-requirements.md` present | Verify the atomic requirements and map them to epics or systems; ensure `## Requirement Catalogue` entries align with epic/linkage strategy. |
| DYN-GAP-004 | planning_gap | medium | No planning artifacts (delivery skeleton, elaboration plan) to guide epic shaping and iteration planning | `planning/delivery-skeleton.md` and `planning/elaboration-plan.md` are absent | Draft a high-level `delivery-skeleton.md` (waves, milestones) and an initial `elaboration-plan.md` for epic decomposition. |
| DYN-GAP-005 | architecture_gap | medium | Some architecture decisions are present but several integration and fallback behaviours are unresolved or duplicated between artifacts | `input/architecture.md` shows open decisions table; `input/brs.md` contains open questions with partially filled answers | Reconcile `Open questions` in `input/brs.md` with `architecture/` decisions; mark definitive owners and update `architecture/` artifacts accordingly. |

## Recommended Focus

Map requirements to implementation systems and create minimal epic shells to hold story-level traceability. Addressing `repository_mapping_gap` next will enable planners to assign requirements to teams and repositories and will unlock planning/elaboration artifacts.

## Notes

- Assumptions: assessment limited to files present in `input/` and top-level architecture. No epics or planning files were created by the CLI init.\
- Confidence is constrained by missing inputs; focus remediation on metadata and canonical requirement inventory to unlock subsequent planning steps.
