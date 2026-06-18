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

Purpose: establish one UC per epic with primary actor, goal, preconditions, main success scenario steps, and known alternative/exception paths. Story references and AC-NNN coverage are stubs. Draft use cases validate that the epic structure covers the right user goals before stories are finalized.

### Confirmed mode (stage 9c)

Run when:
- `planning/delivery-structure.md` has confirmed F-XXX.X story IDs
- `business-analysis/use-case-spec.md` already exists (produced by draft mode)

Purpose: enrich the draft with F-XXX.X story IDs, AC-NNN coverage table, and alternative/exception flows derived from confirmed story edge cases. Do not re-author from scratch — only enrich.

If `business-analysis/use-case-spec.md` does not yet exist when running confirmed mode: run draft mode first, then immediately run confirmed mode in the same pass.

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
- UC name: verb + object, goal-oriented ("Submit Loan Application", not "Loan Application Process")
- If an epic is too broad (completely unrelated user goals), split: UC-NNN.A / UC-NNN.B

### Overview table

- Primary actor: ACT-NNN — must match actors-and-personas.md exactly
- Supporting actors: other ACT-NNN or SYS-NNN involved
- Goal: one sentence — what the primary actor achieves
- Related requirements: FR-NNN IDs from BRS
- **Draft mode:** Related stories → `<!-- to be linked after delivery structure is confirmed -->`
- **Confirmed mode:** Related stories → F-NNN.N IDs from confirmed delivery structure

### Main success scenario

- Derive from: happy-path BRS narrative; epic-level goal progression; PF-NNN main flow steps if process-flows.md exists
- Each step: one observable action by one actor or the system — no compound steps, no implementation detail
- "System" as actor means the system does something autonomously (validates, sends notification, records state)
- Number steps sequentially; keep to 5–12 steps
- **Draft mode:** steps derived from BRS and PF-NNN; no F-XXX.X or AC-NNN references required
- **Confirmed mode:** same steps; add `Story: F-NNN.N` annotations where applicable

### Preconditions

- **Draft mode:** derive from BRS preconditions and epic entry criteria
- **Confirmed mode:** also from first story's dependencies and BDD "Given" clauses if available

### Postconditions

- Observable state when the use case succeeds — not implementation state
- **Draft mode:** from BRS success criteria and epic "so that" language
- **Confirmed mode:** also from last story's AC-NNN pass conditions

### Alternative flows

- **Draft mode:** derive from BRS "if/when/unless" language; PF-NNN alternative flows if they exist
- **Confirmed mode:** also derive from stories scoped as alternative paths and AC-NNN failure criteria
- Each alternative flow: triggered at step N if condition; numbered steps; explicit outcome (returns to main flow at step M, or terminates)

### Exception flows

- **Draft mode:** derive from BRS error handling and known failure conditions
- **Confirmed mode:** also from AC-NNN failure criteria and BDD "Given an invalid X" patterns
- Each exception: trigger condition, system response, user-visible message, recovery path

### Business rules applied

- Only BR-NNN rules from business-rules.md that govern this UC's behaviour
- Both modes: cite BR-NNN ID and the step where it applies

### Acceptance criteria coverage table

- **Draft mode:** leave as stub — `<!-- AC-NNN coverage to be filled after delivery structure is confirmed -->`
- **Confirmed mode:** list every AC-NNN from stories in this epic; map each to main flow step, alternative flow, or exception flow; flag unmapped: `<!-- AC-NNN: not yet mapped — review with PO -->`

---

## Draft mode quality bar

- Every epic has exactly one UC entry
- All actor references use ACT-NNN from actors-and-personas.md
- Main success scenario has 5–12 steps with no implementation detail
- Story references and AC coverage marked as stubs — not invented
- A `> **Draft** — story references and AC coverage to be filled after delivery structure is confirmed.` notice appears at the top of the artifact

## Confirmed mode quality bar

- Every AC-NNN from epic stories appears in the coverage table
- F-NNN.N story annotations added to main scenario steps
- Alternative and exception flows enriched from confirmed story edge cases
- Draft notice removed; version updated

---

## Anti-patterns to avoid

- One UC per story (too granular — UC = epic-level goal)
- One UC for the entire initiative (too broad — stay at epic level)
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
- [ ] **Draft mode only:** story references and AC coverage marked as stubs; draft notice present
- [ ] **Confirmed mode only:** all AC-NNN from epic stories in coverage table; draft notice removed
