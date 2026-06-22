# Plan 3 — Spec-Anchored Strengthening

## What this plan is

Plan 2 introduced the canonical artifact spine (`requirements.md`, `use-cases.puml`, `use-cases/UC-*.md`, `entity-model.md`) and restructured the business-analysis dependency graph.

Plan 3 makes that spine **authoritative**. The current state is artifact-rich but not truly anchored: the framework knows which files exist but does not enforce that they are strong enough before downstream work begins, and it does not name the canonical set as a first-class framework concept.

This plan does not restructure the workflow. It strengthens what plan 2 built.

## The five structural problems this plan fixes

| # | Problem | Root cause |
|---|---|---|
| 1 | No single document names the canonical spec set | Missing principle document |
| 2 | Downstream phases can proceed when specs are structurally present but semantically weak | Validation rules check existence, not adequacy |
| 3 | `business-intake-summary.md` is still treated as a requirements source in several templates | Summary / canonical distinction not enforced |
| 4 | Traceability from specs into implementation is declared but not enforced | No chain check in planning or handoff events |
| 5 | No quality gate prevents planning from starting with unresolved blocking gaps | Gap-to-planning gate missing |

## Execution order

| Step | File | What it does |
|---|---|---|
| 0 | `00-spec-anchoring-principles.md` | Defines the canonical spine, summary vs. canonical distinction, traceability chain. The design anchor for all other steps. |
| 1 | `01-name-canonical-spine.md` | Writes the spine definition into `artifact-ownership.md` and creates `spec-anchoring.md` framework file |
| 2 | `02-strengthen-validation-rules.md` | Adds semantic adequacy checks to EVT-TPL-043, 044, 007, 005 |
| 3 | `03-demote-intake-summary.md` | Demotes `business-intake-summary.md` to support role in event templates where `requirements.md` now exists |
| 4 | `04-add-gap-to-planning-gate.md` | Blocks delivery structure when blocking gaps are unresolved |
| 5 | `05-enforce-traceability-chain.md` | Adds traceability enforcement to planning (EVT-TPL-011, 012) and handoff (EVT-TPL-024, 025) |
| 6 | `06-validate-end-to-end.md` | Validates all changes; produces validation report |

## Done when

- `spec-anchoring.md` exists in `.brs2spec2/` as a named framework principle
- `artifact-ownership.md` explicitly marks the four canonical artifacts as such
- Validation rules in EVT-TPL-043, 044, 007, 005 check semantic adequacy, not just file existence
- `business-intake-summary.md` is demoted to optional in all templates where `requirements.md` is required
- Delivery structure is blocked when `gaps-and-questions.md` contains unresolved blocking gaps
- Planning and handoff events enforce FR-NNN / UC-NNN traceability
