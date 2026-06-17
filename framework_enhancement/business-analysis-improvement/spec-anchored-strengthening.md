# Spec-Anchored Framework — Strengthening Note

## The Problem

Plan 2 introduced a canonical artifact spine. The framework became artifact-rich.
But artifact-rich is not the same as spec-anchored.

The remaining weakness has five faces:

1. No document names the canonical set or distinguishes it from support artifacts
2. Downstream phases can proceed when specs are structurally present but semantically weak
3. `business-intake-summary.md` is still quietly treated as a requirements source in several templates
4. Traceability from spec into implementation is declared but not enforced — stories can exist without a UC trace
5. Planning can start even when blocking gaps have no stated assumptions

Plan 3 fixes all five.

---

## The Canonical Spec Spine

Four artifact groups drive implementation. Everything else supports them.

| # | Artifact | Path | Role |
|---|---|---|---|
| 1 | Requirements catalog | `business-analysis/requirements.md` | FR / NFR / Constraint source of truth |
| 2 | Entity model | `business-analysis/entity-model.md` | Domain data source of truth |
| 3 | Use-case diagram | `business-analysis/use-cases.puml` + `.md` | Scope and actor source of truth |
| 4 | Use-case specs | `business-analysis/use-cases/UC-NNN.md` | Behavioral specification source of truth |

Support artifacts (`business-rules.md`, `actors-and-personas.md`, `process-flows.md`, `gaps-and-questions.md`, `business-intake-summary.md`) annotate and supplement the spine. They do not drive implementation and cannot substitute for it.

---

## The Traceability Chain

```
FR-NNN (requirements.md)
  → BR-NNN (business-rules.md)       constraint rules annotating FRs
  → UC-NNN (use-cases/UC-NNN.md)     behavioral realization of FRs
  → F-NNN.X story (delivery)         decomposition of UC into deliverable stories
  → AC-NNN (delivery)                acceptance criteria per story
  → SCN-NNN (BDD)                    executable test of AC-NNN
  → TC-NNN (test plans)              branch coverage of BR-NNN
  → tasks / coding-prompt            implementation anchored to AC-NNN + AR-NNN
```

Any artifact that skips a link must document why.

---

## The Five Fixes (Plan 3 Steps 1–5)

### Step 1 — Name the spine
Create `.brs2spec2/spec-anchoring.md`. Add a Spec role column (CANONICAL / SUPPORT) to `artifact-ownership.md`.

### Step 2 — Strengthen validation rules
Add cross-artifact adequacy checks to EVT-TPL-043, 044, 007, 005:
- Does `requirements.md` have enough FR-NNN rows with Priority and non-blank AC?
- Does `use-cases.puml` cover all major user goals from FR-NNN rows?
- Does every UC file trace to FR-NNN and cite BR-NNN?
- Does every blocking gap in `gaps-and-questions.md` have an Owner?

### Step 3 — Demote intake summary
Remove `business-intake-summary.md` from `inputs.required` in all templates where `requirements.md` is already required. It becomes optional background context.

### Step 4 — Gap-to-planning gate
EVT-TPL-011 must check `gaps-and-questions.md` before writing delivery structure. If blocking gaps exist without stated assumptions → fail with `blocking: true`.

### Step 5 — Enforce traceability into planning and handoff
- Every story in `delivery-structure.md` must cite a UC-NNN or FR-NNN source
- Every story folder in OpenSpec handoff must have a Spec Sources section
- Every task in standalone handoff must have FR-NNN + UC-NNN + AC-NNN populated
- Traceability matrix must have a UC-NNN to Story matrix, not just FR-NNN to Story

---

## Checklist for a Spec-Anchored Initiative

Use this to verify an initiative is truly anchored before planning begins:

### Canonical spine
- [ ] `requirements.md` exists with FR-NNN, NFR-NNN, C-NNN tables all populated
- [ ] Every FR-NNN has Priority (Must/Should/Could) and non-blank Acceptance Criteria
- [ ] `use-cases.puml` covers every major user goal from FR-NNN rows
- [ ] Every actor named in FR-NNN rows appears in `use-cases.puml`
- [ ] Every UC-NNN.md file traces to at least one FR-NNN
- [ ] Every UC-NNN.md file has preconditions, main scenario, ≥1 alternative flow, postconditions
- [ ] `entity-model.md` exists if any FR-NNN references persistent data objects

### Gap gate
- [ ] `gaps-and-questions.md` has been produced and reviewed
- [ ] Every Severity: Blocking gap has an Owner assigned
- [ ] Every Severity: Blocking gap has a stated assumption or resolution
- [ ] Delivery structure has not started with open blocking gaps

### Traceability into planning
- [ ] Every F-NNN.X story in delivery-structure.md cites a UC-NNN or FR-NNN source
- [ ] FR Coverage table in delivery-structure.md accounts for every FR-NNN
- [ ] Traceability matrix has UC-NNN → Story mapping, not just FR-NNN → Story

### Traceability into handoff
- [ ] Every story.md in OpenSpec has a Spec Sources section (UC-NNN + FR-NNN)
- [ ] Every coding-prompt.md quotes AC-NNN verbatim
- [ ] Every task in standalone tasks.md has FR-NNN + UC-NNN + AC-NNN + Evidence populated

---

## What Plan 3 Does NOT Change

- Event dependency graph (blocked_by) — plan 2 is final on this
- Artifact paths or naming — all hyphen, all unchanged
- Persona ownership — no changes to who produces what
- Workflow stage structure — no new stages
- Skill prompt content for producing artifacts — only prerequisites and validation are touched
