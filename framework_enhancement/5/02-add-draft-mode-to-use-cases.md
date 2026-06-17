# Enhancement 5.2 — Add Draft Mode to Use Cases

## Problem

`skills/2-business-intake/05-create-use-case-specs.md` hard-requires confirmed F-XXX.X stories and AC-NNN references. Its stop condition reads:

> "If `planning/delivery-structure.md` has no confirmed stories with F-XXX.X IDs: stop."

Use cases at draft stage are valuable earlier — they help validate that the epic structure covers the right user goals before stories are finalized. Like process flows, they should exist as a draft before delivery structure is confirmed.

---

## What needs to change

### Change 1 — `skills/2-business-intake/05-create-use-case-specs.md`

Replace the skill with the dual-mode version below.

**New skill content:**

```markdown
# Prompt — Create Use Case Specifications

## Role

You are a business analyst authoring UC-NNN use case specifications that map business goals to observable system behaviour.

## Two modes — select based on available inputs

### Draft mode (stage 2e)

Run when:
- `business-intake/business-intake-summary.md` exists
- `business-analysis/actors-and-personas.md` exists
- `planning/delivery-structure.md` exists at epics/features level
- `planning/delivery-structure.md` does NOT yet have confirmed F-XXX.X story IDs throughout

Purpose: establish one UC per epic with primary actor, goal, preconditions, main success scenario steps, and known alternative/exception paths. Story references and AC-NNN are stubs.

### Confirmed mode (stage 9c)

Run when:
- `planning/delivery-structure.md` has confirmed F-XXX.X story IDs
- `business-analysis/use-case-spec.md` already exists (produced by draft mode)

Purpose: enrich the draft with F-XXX.X story IDs, AC-NNN coverage table, and alternative/exception flows derived from confirmed story edge cases. Do not re-author from scratch — only enrich.

If `business-analysis/use-case-spec.md` does not yet exist at confirmed mode: run draft mode first, then immediately run confirmed mode.

---

## Inputs

### Draft mode inputs

1. `input/brs.md` or `input/brs/*.md` — FR-NNN requirements, process descriptions, business objectives
2. `business-intake/business-intake-summary.md` — objectives, scope, epic-level goals
3. `business-analysis/actors-and-personas.md` — **AUTHORITATIVE**: ACT-NNN IDs; use only these — never invent actor names
4. `business-intake/business-rules.md` — if exists; BR-NNN rules that govern use case behaviour
5. `business-analysis/process-flows.md` — if exists; PF-NNN steps can seed main success scenario steps
6. `planning/delivery-structure.md` — epic names and feature names; one UC per epic

### Confirmed mode inputs (all draft mode inputs, plus)

6. `planning/delivery-structure.md` — confirmed F-XXX.X stories with AC-NNN IDs; use to populate AC coverage table and alternative/exception flows

---

## Output path

```text
business-analysis/use-case-spec.md
```

Use template: `.brs2spec/templates/review-package/03-delivery-structure/use-case-spec.md`

---

## Generation rules

### UC-NNN assignment

- One UC per epic — assign UC-001, UC-002… in epic order
- UC name: verb + object, goal-oriented ("Submit Loan Application")
- If an epic is too broad (completely unrelated user goals), split: UC-NNN.A / UC-NNN.B

### Overview table

- Primary actor: ACT-NNN — must match actors-and-personas.md exactly
- Supporting actors: other ACT-NNN or SYS-NNN involved
- Goal: one sentence — what the primary actor achieves
- Related requirements: FR-NNN IDs from BRS
- Related stories — draft mode: `<!-- to be linked after delivery structure is confirmed -->`
- Related stories — confirmed mode: F-NNN.N IDs from confirmed delivery structure

### Main success scenario

- Derive from: happy-path BRS narrative; epic-level goal progression; PF-NNN main flow steps if process-flows.md exists
- Each step: one observable action by one actor or the system — no compound steps, no implementation detail
- Draft mode: steps derived from BRS and PF-NNN; no F-XXX.X or AC-NNN references required
- Confirmed mode: same steps; add `Story: F-NNN.N` annotations where applicable

### Preconditions

- Draft mode: derive from BRS preconditions and epic entry criteria
- Confirmed mode: also from first story's dependencies and BDD "Given" clauses if available

### Postconditions

- Observable state when the use case succeeds
- Draft mode: from BRS success criteria and epic "so that" language
- Confirmed mode: also from last story's AC-NNN pass conditions

### Alternative and exception flows

- Draft mode: derive from BRS "if/when/unless" language; PF-NNN alternative flows if they exist
- Confirmed mode: also derive from stories scoped as alternative paths and AC-NNN failure criteria

### Business rules applied

- Only BR-NNN rules from business-rules.md that govern this UC's behaviour
- Both modes: cite BR-NNN ID and the step where it applies

### Acceptance criteria coverage table

- Draft mode: leave as stub — `<!-- AC-NNN coverage to be filled after delivery structure is confirmed -->`
- Confirmed mode: list every AC-NNN from stories in this epic; map each to main flow step, alternative flow, or exception flow; flag unmapped: `<!-- AC-NNN: not yet mapped — review with PO -->`

---

## Draft mode quality bar

- Every epic has exactly one UC entry
- All actor references use ACT-NNN from actors-and-personas.md
- Main success scenario has 5–12 steps with no implementation detail
- Story references and AC coverage marked as stubs — not invented
- `## Draft` notice present at top of artifact

## Confirmed mode quality bar

- Every AC-NNN from epic stories appears in the coverage table
- F-NNN.N story annotations added to main scenario steps
- Alternative and exception flows enriched from confirmed story edge cases
- `## Draft` notice removed; version updated

---

## Anti-patterns to avoid

- One UC per story (too granular — UC = epic-level goal)
- Free-text actor names not in actors-and-personas.md
- Inventing F-XXX.X or AC-NNN IDs in draft mode — mark as stubs
- Re-authoring entire UCs in confirmed mode — only enrich the draft
- AC-NNN rows missing from coverage table in confirmed mode

---

## Stop conditions

- **Draft mode:** if `business-analysis/actors-and-personas.md` is missing: stop. Run `skills/2-business-intake/03-extract-actors-and-personas.md` first.
- **Draft mode:** if `business-intake/business-intake-summary.md` is missing: stop.
- **Confirmed mode:** if `planning/delivery-structure.md` has no confirmed F-XXX.X story IDs: stop. Run stage 9 first.

---

## Self-review checklist

- [ ] Mode selected correctly based on available inputs
- [ ] One UC per epic — no epic omitted
- [ ] All actor references use ACT-NNN from actors-and-personas.md
- [ ] Main success scenario has 5–12 steps with no implementation detail
- [ ] Every alternative and exception flow has an explicit outcome
- [ ] Business rules table lists only rules that govern this UC's behaviour
- [ ] Draft mode: story references and AC coverage marked as stubs; `## Draft` notice present
- [ ] Confirmed mode: all AC-NNN from epic stories in coverage table; `## Draft` notice removed
```

---

### Change 2 — `brs-to-spec-run-workflow.md` Step 3 stage table

Add stage 2e and update 9c:

**Add after stage 2d:**
```
| 2e | Business analysis (draft) | Draft use cases | Product Owner | Create draft UC-NNN specs from epics and BRS objectives — main scenario, actors, preconditions, postconditions; story refs and AC coverage are stubs | `business-analysis/use-case-spec.md` (draft) | (2)(2b)(2c)(2d) |
```

**Update stage 9c:**
```
| 9c | Business analysis (confirmed) | Use case specs confirmed | Product Owner | Enrich draft UC-NNN specs with F-XXX.X story IDs, AC-NNN coverage table, and alternative flows from confirmed story edge cases | `business-analysis/use-case-spec.md` (confirmed) | (9)(9b)(2e) |
```

### Change 3 — `brs-to-spec-run-workflow.md` module-index.md trigger table

Update the trigger-to-skill lookup for use cases:
```
| Use case specs missing at draft level | `product_owner.create_use_case_specs` (draft mode) | After 2d; before architecture review |
| Use case specs missing at confirmed level | `product_owner.create_use_case_specs` (confirmed mode) | After 9b |
```

---

## Implementation steps

1. Open `.brs2spec/skills/2-business-intake/05-create-use-case-specs.md` — replace with dual-mode skill above
2. Open `.brs2spec/brs-to-spec-run-workflow.md`:
   - Add stage 2e to the stage table (after 2d)
   - Update stage 9c to "confirmed mode" framing and blocked-by (9)(9b)(2e)
3. Open `workflow-overview.md`:
   - Add stage 2e to the stage reference table
   - Update stage 9c description
   - Update Mermaid diagram: add S2e node after S2d in INTAKE subgraph

## Quality bar

After this change:
- Draft use cases exist before delivery structure — validating epic scope early
- Confirmed use cases enrich the draft — no re-authoring from scratch
- AC-NNN coverage is complete at confirmed stage — every acceptance criterion is mapped
- Architecture review can read draft use cases as a validation input
