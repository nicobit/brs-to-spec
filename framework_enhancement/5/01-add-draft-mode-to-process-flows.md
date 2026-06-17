# Enhancement 5.1 — Add Draft Mode to Process Flows

## Problem

`skills/2-business-intake/04-create-process-flows.md` hard-requires `planning/delivery-structure.md` with confirmed F-XXX.X stories. Its stop condition reads:

> "If `planning/delivery-structure.md` has no confirmed stories (still at draft/epics-only stage): stop."

This means process flows are always created at stage 9b — after stories are confirmed. But process flows often reveal missing stories, wrong story boundaries, or missing decision branches. By the time they are created at 9b, the delivery structure is already confirmed and costly to change.

## Solution

Add a **draft mode** to the skill. Draft mode runs at stage 2d (after actors and personas). It works from BRS narrative and epic-level delivery structure, not confirmed stories. Confirmed mode stays at 9b and enriches the draft with F-XXX.X IDs and AC-NNN references.

The same artifact (`business-analysis/process-flows.md`) is used for both modes. Draft mode marks story references as stubs. Confirmed mode fills them in.

---

## What needs to change

### Change 1 — `skills/2-business-intake/04-create-process-flows.md`

Replace the entire skill with the dual-mode version below.

**New skill content:**

```markdown
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

Purpose: establish the process flow structure — main path, decision points, and alternative branches — before delivery structure is confirmed. Story references are stubs to be linked later.

### Confirmed mode (stage 9b)

Run when:
- `planning/delivery-structure.md` has confirmed F-XXX.X story IDs for all features
- `business-analysis/process-flows.md` already exists (produced by draft mode)

Purpose: enrich the draft with confirmed F-XXX.X story IDs, AC-NNN references, and correct step ordering derived from confirmed story dependencies. Do not re-author flows from scratch — only enrich existing PF-NNN entries.

If `business-analysis/process-flows.md` does not yet exist at confirmed mode: run draft mode first, then immediately run confirmed mode.

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
- Draft mode: Related stories field → `<!-- to be linked after delivery structure is confirmed -->`
- Confirmed mode: Related stories field → F-NNN.N IDs from confirmed delivery structure

### Main flow steps

- Derive from: BRS workflow narrative; "if/when/unless" conditions; epic-level goal progression
- Each step: one observable action by one actor or the system — no compound steps
- System response column: what the system does or confirms
- Do not describe implementation — describe observable behaviour only
- Draft mode: steps derived from BRS narrative and epic goal; no F-XXX.X story IDs required
- Confirmed mode: add `Story: F-NNN.N` annotation to each step that maps to a confirmed story

### Decision points

- Source: BR-NNN rules that create a branch; BRS "if/when/unless/except" language
- Each decision point references the BR-NNN or BRS section that drives it
- Branch A = continue main flow; Branch B = named alternative flow
- Both modes: decision points must cite BR-NNN or BRS section — never invented

### Alternative flows

- One AF-NNN.N per branch identified in decision points
- Also derive from: BRS alternative path language; stories scoped as edge cases (confirmed mode only)
- Each alternative flow: triggered at step N if condition; numbered steps; explicit outcome (returns to main flow at step M, or terminates)

### Error / exception paths

- Source: BRS error handling requirements; AC-NNN failure criteria (confirmed mode only when AC-NNN available)
- Each error: trigger condition, system behaviour, user-visible message or outcome

### Postconditions

- Observable state when the process completes successfully
- Draft mode: derive from BRS success criteria and epic goal ("so that" language)
- Confirmed mode: derive from last story's "so that" clause and AC-NNN pass conditions

---

## Draft mode quality bar

- Every epic in `planning/delivery-structure.md` has exactly one PF-NNN entry
- Every step references ACT-NNN or "System" — no unnamed actors
- Every decision point cites a BR-NNN rule or BRS section
- Story references are marked as stubs — not invented F-XXX.X IDs
- The `## Draft` notice is present at the top of the artifact

## Confirmed mode quality bar

- Every epic has exactly one PF-NNN entry — same IDs as draft
- Every step that maps to a confirmed story has `Story: F-NNN.N` annotation
- Every decision point still cites BR-NNN or BRS section
- Alternative flows derived from edge-case stories are added
- The `## Draft` notice is removed; version updated

---

## Anti-patterns to avoid

- One process per story (too granular — process = epic-level goal)
- Steps that describe database operations or API calls instead of observable behaviour
- Decision points without a cited BR-NNN or BRS source
- Inventing F-XXX.X story IDs in draft mode — mark as stub instead
- Re-authoring entire flows in confirmed mode — only enrich the existing draft

---

## Stop conditions

- **Draft mode:** if `business-analysis/actors-and-personas.md` is missing: stop. Actors must be extracted first. Run `skills/2-business-intake/03-extract-actors-and-personas.md`.
- **Draft mode:** if `business-intake/business-intake-summary.md` is missing: stop.
- **Confirmed mode:** if `planning/delivery-structure.md` has no confirmed F-XXX.X story IDs: stop. Run stage 9 (confirmed delivery structure) first.

---

## Self-review checklist

- [ ] Mode selected correctly based on available inputs
- [ ] One PF-NNN per epic — no epic silently omitted
- [ ] Every actor reference uses ACT-NNN from actors-and-personas.md
- [ ] Every decision point cites a BR-NNN or BRS section — no invented branch conditions
- [ ] Alternative flows have explicit outcomes (return step or termination)
- [ ] Postconditions are observable outcomes, not implementation state
- [ ] No step describes internal system mechanics
- [ ] Draft mode: `## Draft` notice present; story references marked as stubs
- [ ] Confirmed mode: `## Draft` notice removed; F-NNN.N story annotations added to steps
```

---

### Change 2 — `brs-to-spec-run-workflow.md` Step 3 stage table

Add stage 2d and update 9b:

**Add after stage 2c:**
```
| 2d | Business analysis (draft) | Draft process flows | Product Owner | Create draft PF-NNN flows from epics and BRS narrative — decision points, alternative branches, actors; story refs are stubs | `business-analysis/process-flows.md` (draft) | (2)(2b)(2c) |
```

**Update stage 9b:**
```
| 9b | Business analysis (confirmed) | Process flows confirmed | Product Owner | Enrich draft PF-NNN flows with confirmed F-XXX.X story IDs, AC-NNN references, and correct step ordering | `business-analysis/process-flows.md` (confirmed) | (9)(2d) |
```

### Change 3 — `brs-to-spec-run-workflow.md` Step 5 pre-generation gate check

Add to the stage 9 confirmed delivery structure block:
```
- [ ] `business-analysis/process-flows.md` exists at draft level — process flows should have been drafted before delivery structure; if missing, run draft mode of `skills/2-business-intake/04-create-process-flows.md` now before confirming stories (this is a quality gap but not a hard blocker)
```

### Change 4 — `brs-to-spec-run-workflow.md` Hard gate rules

Update the Architecture review (5) hard gate row to include 2d:
```
| Architecture review (5) | `business-intake/business-intake-summary.md`; `business-intake/business-rules.md`; `business-analysis/actors-and-personas.md`; `business-analysis/process-flows.md` (draft); `planning/delivery-structure.md` draft with epics |
```

### Change 5 — Story enrichment check (stage 9d)

The 9d check already requires a PF-NNN reference per story. This is now satisfiable because draft process flows exist before stories are confirmed. No change needed to 9d logic.

---

## Implementation steps

1. Open `.brs2spec/skills/2-business-intake/04-create-process-flows.md` — replace with dual-mode skill above
2. Open `.brs2spec/brs-to-spec-run-workflow.md`:
   - Add stage 2d to the stage table (after 2c)
   - Update stage 9b to "confirmed mode" framing
   - Update hard gate rules for architecture review (5) to include 2d
   - Add soft check in stage 9 pre-gen gate for draft process flows
3. Open `workflow-overview.md`:
   - Add stage 2d to the stage reference table
   - Update stage 9b description
   - Update Mermaid diagram: add S2d node in the INTAKE subgraph; update arrow from S2c to S4 to pass through S2d

## Quality bar

After this change:
- Draft process flows are created before the delivery structure draft — revealing missing stories early
- Confirmed process flows enrich the draft — no re-authoring from scratch
- The 9d enrichment check can reference PF-NNN IDs because they exist before stories are confirmed
- The architecture review reads draft process flows as input — better boundary decisions
