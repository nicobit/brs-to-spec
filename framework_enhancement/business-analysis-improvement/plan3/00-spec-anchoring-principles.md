# Step 0 — Spec-Anchoring Principles

## Purpose

Define the design decisions that anchor all other steps in plan 3. This document must be read before executing any other step. No framework files are modified here.

---

## Principle 1 — The Canonical Spec Spine

The brs-to-spec v2 framework has two classes of business-analysis artifact:

### Canonical artifacts (execution-driving)

These four artifacts are the authoritative specification of what the initiative must deliver. All downstream phases — architecture, planning, quality gates, handoff — must read them first and must not contradict them.

| Artifact | Path | Produced by |
|---|---|---|
| Requirements catalog | `business-analysis/requirements.md` | EVT-TPL-043 |
| Entity model | `business-analysis/entity-model.md` | EVT-TPL-030 |
| Use-case diagram | `business-analysis/use-cases.puml` + `business-analysis/use-cases.md` | EVT-TPL-044 |
| Use-case specs | `business-analysis/use-cases/UC-NNN.md` | EVT-TPL-007 |

These artifacts are:
- Numbered and traceable (FR-NNN, ENT-NNN, UC-NNN)
- Structured (tables, Mermaid diagrams, per-file UC specs)
- Validation-gated before downstream phases can use them
- The source of truth for all traceability

### Support artifacts (review-friendly)

These artifacts are produced alongside the canonical spine and support it. They are valuable for stakeholder review, gap surfacing, and cross-cutting analysis, but they do not drive implementation and cannot substitute for the canonical set.

| Artifact | Path | Role |
|---|---|---|
| Business intake summary | `business-intake/business-intake-summary.md` | Source material for requirements derivation; not a requirements document |
| Business rules | `business-analysis/business-rules.md` | Derived from FR-NNN rows; annotates use-case specs |
| Actors and personas | `business-analysis/actors-and-personas.md` | Derived from use-cases.puml; annotates UC specs and process flows |
| Process flows | `business-analysis/process-flows.md` | Cross-UC journey synthesis; does not replace UC specs |
| Gaps and questions | `business-analysis/gaps-and-questions.md` | Gap catalog; blocking gaps prevent planning from starting |
| Business test expectations | `business-intake/business-test-expectations.md` | PO-level expectations; not a substitute for BDD |

---

## Principle 2 — Summary Artifacts vs. Canonical Artifacts

The distinction that must be encoded in every prompt and event template:

| Summary artifact | What it is | What it is NOT |
|---|---|---|
| `business-intake-summary.md` | A human-readable distillation of the BRS for PO sign-off | A requirements specification. Once `requirements.md` exists, intake-summary is background context only. |
| `process-flows.md` | Cross-UC operational journey view | A substitute for use-case specs. Does not define preconditions, alternative flows, or exception paths per use case. |
| `business-rules.md` | A derived catalog of constraint rules | A substitute for functional requirements. BR-NNN rules annotate FR-NNN requirements; they do not replace them. |

**Encoding rule:** In any event template where `requirements.md` is a required input, `business-intake-summary.md` must be demoted to optional. It may be read for additional context, but it is never the primary source once the canonical spine exists.

---

## Principle 3 — Semantic Adequacy, Not Just File Existence

The current validation rules check structural presence (does the file exist, are tables present, is Status: Draft). They do not check semantic adequacy.

A framework is spec-anchored only when downstream work is blocked by **weak specs**, not only by **missing specs**.

### Adequacy criteria for each canonical artifact

**`requirements.md` is adequate when:**
- FR-NNN, NFR-NNN, and C-NNN tables all have at least one row
- Every FR-NNN has a Priority (Must / Should / Could)
- No FR-NNN row has a blank acceptance criteria column
- The count of FR-NNN rows is consistent with the scope described in intake-summary

**`use-cases.puml` is adequate when:**
- Every major user goal implied by FR-NNN rows has at least one UC-NNN
- Every actor named in FR-NNN rows appears in the diagram
- No UC-NNN was invented without a traceable FR-NNN source

**`use-cases/UC-NNN.md` is adequate when:**
- Every UC-NNN declared in use-cases.puml has exactly one UC file
- Every UC file traces to at least one FR-NNN
- Every UC file has preconditions, main success scenario, at least one alternative flow, and postconditions
- No UC file references actors not in `actors-and-personas.md`

**`entity-model.md` is adequate when:**
- Every persistent business object implied by FR-NNN rows has an ENT-NNN
- Every ENT-NNN has at least one FR-NNN source
- Every ENT-NNN has an attribute table

These criteria are already partially encoded in `must_include` fields. Plan 3 promotes the cross-artifact checks (e.g. UC coverage of FR-NNN rows) into `validation_rules.natural_language`.

---

## Principle 4 — Gap-to-Planning Gate

The current framework allows delivery structure (EVT-TPL-011) to proceed even when `gaps-and-questions.md` contains unresolved blocking gaps.

This is a structural weakness: blocking gaps mean the scope is not fully defined, but planning can still decompose into stories.

**The gate:**
- EVT-TPL-011 (CREATE_DELIVERY_STRUCTURE) must check whether `gaps-and-questions.md` exists and contains any gaps with `Severity: Blocking`.
- If blocking gaps exist and have no stated assumption or resolution, the event must fail and raise a decision.
- If blocking gaps exist but each has a stated assumption (explicitly recorded in the artifact), planning may proceed with those assumptions noted in delivery-structure.md.

This does not change the `blocked_by` dependency — it changes the `validation_rules` and `must_include` for EVT-TPL-011.

---

## Principle 5 — Traceability Chain Enforcement

The spec-to-implementation traceability chain:

```
FR-NNN (requirements.md)
  → BR-NNN (business-rules.md)          [annotates constraints on FRs]
  → UC-NNN (use-cases/UC-NNN.md)        [specifies behavioral realization of FRs]
  → F-NNN.X story (delivery-structure)  [decomposes UC into deliverable stories]
  → AC-NNN (delivery-structure)         [acceptance criteria per story]
  → SCN-NNN (BDD scenarios)             [executable test of AC-NNN]
  → TC-NNN (test plans)                 [unit-level branch coverage of BR-NNN]
  → tasks.md / coding-prompt.md         [implementation anchored to AC-NNN + AR-NNN]
```

**Enforcement points:**

| Event | What must be checked |
|---|---|
| EVT-TPL-011 (delivery structure) | Every F-NNN.X story must cite at least one UC-NNN or FR-NNN source. No stories invented without a requirements trace. |
| EVT-TPL-012 (traceability matrix) | FR-NNN → story matrix must be complete. Every FR-NNN either has a story or is explicitly excluded with a reason. |
| EVT-TPL-017 (BDD) | Every SCN-NNN must cite the AC-NNN it validates. |
| EVT-TPL-024 / 025 (handoff) | Every story folder / task must cite FR-NNN and UC-NNN sources. No story delivered without a spec trace. |

---

## Design Decisions for Steps 1–6

| Decision | Choice | Rationale |
|---|---|---|
| Where to store the spine definition | New file `.brs2spec2/spec-anchoring.md` + section in `artifact-ownership.md` | Keeps the principle in the framework core, not in enhancement docs |
| Validation rule style | Extend `validation_rules.natural_language` with cross-artifact checks | Consistent with current pattern; machine checks remain file-level only |
| Gap gate approach | Fail EVT-TPL-011 if blocking gaps lack stated assumptions | Does not require a new event; adds a check to an existing one |
| Intake-summary demotion | Optional in all templates where `requirements.md` is required | Clean cutover; no dual-read |
| Traceability enforcement | Add to `must_include` and `validation_rules` of planning and handoff events | Structural, not procedural; enforced at the event level |
| New framework file | `spec-anchoring.md` in `.brs2spec2/` root | Framework principle files live alongside `agent-instructions.md` |

---

## Files This Step Produces

None. This is a design-only step.

## Files the Subsequent Steps Will Modify

| Step | Files modified |
|---|---|
| 1 | `.brs2spec2/spec-anchoring.md` (new), `.brs2spec2/workflow/artifact-ownership.md` |
| 2 | EVT-TPL-043, EVT-TPL-044, EVT-TPL-007, EVT-TPL-005 |
| 3 | EVT-TPL-008, EVT-TPL-011, EVT-TPL-012, EVT-TPL-015, EVT-TPL-017, EVT-TPL-024, EVT-TPL-025, EVT-TPL-028, EVT-TPL-031 |
| 4 | EVT-TPL-011 (validation_rules + must_include) |
| 5 | EVT-TPL-011, EVT-TPL-012, EVT-TPL-024, EVT-TPL-025 (traceability enforcement) |
| 6 | Validation report only |
