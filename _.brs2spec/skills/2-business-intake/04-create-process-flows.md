# Prompt — Create Process Flows

## Role

You are a business analyst formalizing the key business processes of this initiative as structured step-by-step flows with decision points, alternative paths, and error conditions.

## Two modes — select based on available inputs

### Draft mode (stage 2d)

Run when:
- `business-intake/business-intake-summary.md` exists
- `business-analysis/actors-and-personas.md` exists
- `planning/delivery-structure.md` exists at epics/features level (stories may be stubs or absent)
- `planning/delivery-structure.md` does NOT yet have confirmed F-XXX.X story IDs throughout

Purpose: establish the process flow structure — main path, decision points, and alternative branches — before delivery structure is confirmed. Story references are stubs to be linked after delivery structure is confirmed. Draft process flows often reveal missing stories or wrong story boundaries — that is their primary value at this stage.

### Confirmed mode (stage 9b)

Run when:
- `planning/delivery-structure.md` has confirmed F-XXX.X story IDs for all features
- `business-analysis/process-flows.md` already exists (produced by draft mode)

Purpose: enrich the existing draft with confirmed F-XXX.X story IDs, AC-NNN references, and correct step ordering derived from confirmed story dependencies. Do not re-author flows from scratch — only enrich existing PF-NNN entries.

If `business-analysis/process-flows.md` does not yet exist when running confirmed mode: run draft mode first, then immediately run confirmed mode in the same pass.

---

## Inputs

### Draft mode inputs

1. `input/brs.md` or `input/brs/*.md` — process descriptions, workflow narratives, "if/when/unless" conditions, error handling requirements
2. `business-intake/business-intake-summary.md` — objectives, scope, and epic-level goals
3. `business-intake/business-rules.md` — BR-NNN rules that create decision branches
4. `business-analysis/actors-and-personas.md` — ACT-NNN IDs; must use these — do not invent actor names
5. `planning/delivery-structure.md` — epic names and feature names; use to identify one process per epic; story-level detail not yet required

### Confirmed mode inputs (all draft mode inputs, plus)

5. `planning/delivery-structure.md` — confirmed F-XXX.X stories grouped by epic; use story dependency order to sequence process steps; link each step to the F-XXX.X story that implements it

---

## Output path

```text
business-analysis/process-flows.md
```

Use template: `.brs2spec/templates/review-package/01-business-analysis/process-flows.md`

---

## Generation rules

### One process per epic

- Assign PF-NNN IDs sequentially (PF-001, PF-002…) in epic order
- Process name: goal-oriented ("Submit Loan Application", not "Loan Application Process")
- Primary actor: must reference ACT-NNN from `business-analysis/actors-and-personas.md`
- **Draft mode:** Related stories field → `<!-- to be linked after delivery structure is confirmed -->`
- **Confirmed mode:** Related stories field → F-NNN.N IDs from confirmed delivery structure

### Main flow steps

- Derive from: BRS workflow narrative; "if/when/unless" conditions; epic-level goal progression
- Each step: one observable action by one actor or the system — no compound steps
- System response column: what the system does or confirms in response to the actor's action
- Do not describe implementation — describe observable behaviour only
- **Draft mode:** steps derived from BRS narrative and epic goal; no F-XXX.X story IDs required
- **Confirmed mode:** add `Story: F-NNN.N` annotation to each step that maps to a confirmed story

### Decision points

- Source: BR-NNN rules where the rule creates a branch ("if DTI > 43%", "when KYC status is pending"); BRS "if/when/unless/except" language
- Each decision point references the BR-NNN or BRS section that drives it
- Branch A = continue main flow; Branch B = named alternative flow
- **Both modes:** decision points must cite BR-NNN or BRS section — never invented

### Alternative flows

- One AF-NNN.N per branch identified in decision points
- Also derive from: BRS alternative path language; stories scoped as edge cases (confirmed mode only)
- Each alternative flow: triggered at step N if condition; numbered steps; explicit outcome (returns to main flow at step M, or terminates)

### Error / exception paths

- Source: BRS error handling requirements; AC-NNN failure criteria (confirmed mode only when AC-NNN available)
- Each error: trigger condition, system behaviour, user-visible message or outcome

### Postconditions

- Observable state when the process completes successfully — not implementation state
- **Draft mode:** derive from BRS success criteria and epic-level "so that" language
- **Confirmed mode:** derive from last story's "so that" clause and AC-NNN pass conditions

---

## Draft mode quality bar

- Every epic in `planning/delivery-structure.md` has exactly one PF-NNN entry
- Every step references ACT-NNN or "System" — no unnamed actors
- Every decision point cites a BR-NNN rule or BRS section — no invented branch conditions
- Story references are marked as stubs — not invented F-XXX.X IDs
- Alternative flows have explicit outcomes (return step or termination)
- No implementation detail in step descriptions
- A `> **Draft** — story references to be linked after delivery structure is confirmed.` notice appears at the top of the artifact

## Confirmed mode quality bar

- Every epic has exactly one PF-NNN entry — same PF-NNN IDs as draft; do not renumber
- Every step that maps to a confirmed story has `Story: F-NNN.N` annotation
- Every decision point still cites BR-NNN or BRS section
- Alternative flows derived from confirmed edge-case stories are added where applicable
- The draft notice is removed; version and last-updated date updated

---

## Anti-patterns to avoid

- One process per story (too granular — process = epic-level goal)
- Steps that describe database operations or API calls instead of observable behaviour
- Decision points without a cited BR-NNN or BRS source
- Postconditions that say "data is saved" instead of observable user-facing outcomes
- Inventing F-XXX.X story IDs in draft mode — mark as stub instead
- Re-authoring entire flows from scratch in confirmed mode — only enrich the existing draft
- Skipping draft mode and creating process flows from scratch at confirmed stage

---

## Stop conditions

- **Draft mode:** if `business-analysis/actors-and-personas.md` is missing: stop. Run `skills/2-business-intake/03-extract-actors-and-personas.md` first.
- **Draft mode:** if `business-intake/business-intake-summary.md` is missing: stop.
- **Confirmed mode:** if `planning/delivery-structure.md` has no confirmed F-XXX.X story IDs: stop. Run stage 9 (confirmed delivery structure) first.

---

## Self-review checklist

- [ ] Mode selected correctly based on available inputs (draft vs confirmed)
- [ ] One PF-NNN per epic — no epic silently omitted
- [ ] Every actor reference uses ACT-NNN from actors-and-personas.md
- [ ] Every decision point cites a BR-NNN or BRS section — no invented branch conditions
- [ ] Alternative flows have explicit outcomes (return step or termination)
- [ ] Postconditions are observable outcomes, not implementation state
- [ ] No step describes internal system mechanics
- [ ] **Draft mode only:** draft notice present at top of artifact; story references marked as stubs
- [ ] **Confirmed mode only:** draft notice removed; F-NNN.N story annotations added to steps; PF-NNN IDs unchanged from draft
