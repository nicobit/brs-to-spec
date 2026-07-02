# Dynamic Gap Assessment

## Summary

The workspace for I982-ISA contains a populated BRS and a draft high-level architecture, but there are important inconsistencies and missing delivery artifacts that block safe progression to implementation planning. The highest-impact issues are a metadata mismatch between the BRS and workspace, conflicting statements about the Temenos T24 contract, and the absence of a tracked implementation plan and UI specification.

## Macro Phase

| Field | Value |
|---|---|
| Current macro phase | requirements-and-architecture |
| Assessment confidence | medium |
| Iteration count | 0 |

## Ranked Gaps

| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |
|---|---|---|---|---|---|
| DYN-GAP-001 | human_clarification_gap | critical | Initiative identifier mismatch between workspace and BRS metadata — this prevents correct provenance and routing of future artifacts. | `initiatives/I982-ISA/input/brs.md` (Document metadata lists Initiative ID = I005) and `.b2s/state/workflow-state.json` (initiative_id = I982-ISA). | Confirm the intended initiative ID; either update `input/brs.md` to `I982-ISA` or archive/move the BRS for I005 and supply the correct BRS for I982-ISA. Human owner: initiative sponsor or product owner. |
| DYN-GAP-002 | human_clarification_gap | high | Conflicting statements about the Temenos T24 payment gateway contract (TBD vs Resolved). This affects scope of the Payment Gateway Adapter and iteration planning. | `initiatives/I982-ISA/input/brs.md` (OQ-005: "We can define ours") vs `initiatives/I982-ISA/input/architecture.md` (OD-004: Status = Resolved). | Reconcile contract status with IT Architecture and Legal; record final decision in `architecture/solution-decisions.md` and update integration notes and effort estimates. |
| DYN-GAP-003 | planning_gap | high | No implementation-level `tasks.md` or prioritized increment plan exists to move from architecture to delivery. Without a task plan the team cannot estimate, schedule, or allocate work for waves/releases. | `.b2s/workflow/stage-actions.yaml` expects planning artifacts; workspace does not contain `tasks.md` or a `tasks/` planning artifact. | Create `tasks.md` with prioritized increments, dependencies, acceptance criteria, and a first MVP wave. Map tasks to the architecture components and identify owners. |
| DYN-GAP-004 | ui_gap | medium | UI specifications for Applicant Portal and Underwriter Dashboard are not present; UI interaction details and acceptance criteria are missing. | `initiatives/I982-ISA/input/architecture.md` lists UI components but no `architecture/ui-specification.md` artifact exists. | Produce `architecture/ui-specification.md` covering key screens, data shown, error states, and accessibility/consent flows. Include screenshots/wireframes for applicant and underwriter flows. |
| DYN-GAP-005 | solution_design_gap | medium | Details for AI explainability, model operationalisation, and provenance are not captured at the design level despite regulatory constraint that models must be explainable. | `input/brs.md` and `input/architecture.md` show the explainability requirement and that OD-001 is resolved, but there is no detailed `architecture/solution-decisions.md` or design notes describing the explainability approach, model interpretability tooling, or how audit evidence will be produced. | Document the explainability approach (model choices, feature importance reporting, deterministic surrogate models if needed), integration points for explainability telemetry, and acceptance criteria for regulatory audit. |

## Recommended Focus

Address DYN-GAP-001 (initiative metadata mismatch) immediately — it is a gating, low-effort clarification that will remove provenance risk and avoid misrouting future artifacts. After metadata is reconciled, prioritise DYN-GAP-002 (contract clarification) because it changes scope and effort estimates, then create the `tasks.md` planning artifact (DYN-GAP-003) to enable concrete delivery planning.

## Notes

- Confidence is medium because a populated `input/brs.md` and `input/architecture.md` exist, but the workspace lacks several downstream artifacts (tasks, UI spec, solution decisions) and contains inconsistent statements that must be reconciled by named owners.
- This assessment used only artifacts present in the workspace: `input/brs.md`, `input/architecture.md`, and `.b2s/state/workflow-state.json` — no external assumptions were introduced.
- After the metadata and contract clarifications are recorded, re-run the dynamic assessment to capture any newly surfaced gaps (e.g., backlog sizing, non-functional performance targets, or external SLA negotiations). 
