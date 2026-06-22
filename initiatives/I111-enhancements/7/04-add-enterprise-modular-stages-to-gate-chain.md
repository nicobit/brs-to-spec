# Enhancement 7.4 — Add Enterprise + Modular Stages to the Gate Chain Table

## Problem

The routing decision for I005 correctly set `delivery_mode: Enterprise + Modular`. This mode requires three additional planning stages before engineering readiness:

| Artifact | Skill |
|---|---|
| `planning/software-modules.md` | `delivery_lead.identify_software_modules` |
| `planning/capability-to-module-map.md` | `delivery_lead.map_capabilities_to_modules` |
| `planning/delivery-increments.md` | `delivery_lead.define_delivery_increments` |

None of these were produced. The orchestrator advanced from delivery structure directly to engineering readiness, skipping all three.

**Root cause:** in `brs-to-spec-run-workflow.md`, these three stages are mentioned only once, at the bottom of the "Delivery mode behavior" section, as a prose note:

> "Enterprise + Modular (12–14): All stages required. Also run:
> - `.brs2spec/skills/3-planning-and-modular-delivery/06-define-delivery-increments.md`
> - `.brs2spec/skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md`"

These skills are listed as prose only. They are **not rows in the Step 3 stage gate chain table** that the orchestrator walks to decide what to execute next. Because the table is the authoritative execution sequence, stages that exist only in prose are invisible to the orchestrator's sequential walk. The orchestrator correctly skips anything not in the table.

A secondary issue: the prose note itself is incomplete — it lists only two of the three skills and uses an old numbering (`06-define-delivery-increments`, `07-create-traceability-matrix`) that may not match the current skill file names.

---

## What needs to change

### Change 1 — Insert three new rows into the Step 3 stage gate chain table in `brs-to-spec-run-workflow.md`

**Location:** Step 3 stage gate chain table, between stages 4 (Draft delivery shape) and 5 (Architecture review).

The three new rows are conditional on `delivery_mode = Enterprise + Modular`. They must appear after stage 4 because the delivery structure draft is the input for module identification. They must appear before stage 5 because the architecture review uses the module structure as input.

**Current table excerpt (stages 4 and 5):**

```
| 4 | Draft delivery shape | `planning/delivery-structure.md` (epics + features only) | Epics with IDs and features visible; stories may be stubs | `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` | (2)(2b)(2c) |
| 5 | Architecture review | `architecture/architecture-review.md` | Initiative-specific constraints; every open decision has an owner; not generic statements | `skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` | (2) + draft delivery-structure |
```

**Insert these three rows between stages 4 and 5:**

```
| 4a | Software modules (Enterprise + Modular only) | `planning/software-modules.md` | Module table present with IDs, names, owning team, and capability boundary; no empty rows; each module traces to at least one epic | `skills/3-planning-and-modular-delivery/04-identify-software-modules.md` | delivery_mode = Enterprise + Modular; (4) |
| 4b | Capability-to-module map (Enterprise + Modular only) | `planning/capability-to-module-map.md` | Every epic and feature maps to at least one module; no unmapped features; module IDs match `planning/software-modules.md` | `skills/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` | delivery_mode = Enterprise + Modular; (4a) |
| 4c | Delivery increments (Enterprise + Modular only) | `planning/delivery-increments.md` | Increment table present; each increment references module IDs and feature IDs; dependency order stated | `skills/3-planning-and-modular-delivery/06-define-delivery-increments.md` | delivery_mode = Enterprise + Modular; (4a)(4b) |
```

**Renumber:** stage 5 and all subsequent stages retain their existing numbers. Stages 4a, 4b, 4c are sub-steps that only exist in the Enterprise + Modular path. The gate chain walk skips them for other delivery modes.

---

### Change 2 — Add hard gate rules for stages 4a–4c

**Location:** Step 3, "Hard gate rules" table.

**Add these three rows:**

```
| Architecture review (5) — Enterprise + Modular only | `planning/software-modules.md` present and complete; `planning/capability-to-module-map.md` present and complete |
| Engineering readiness (8) — Enterprise + Modular only | `planning/delivery-increments.md` present and complete |
| Handoff (13) — Enterprise + Modular only | `planning/delivery-increments.md` with delivery increment assignments for every story; `planning/traceability-matrix.md` present (if traceability gate triggered) |
```

---

### Change 3 — Add the skip rule for non-Enterprise + Modular modes

**Location:** Step 3, immediately before the stage gate chain table.

**Add:**

```markdown
**Delivery mode gate-chain rule:**

Stages 4a, 4b, and 4c are gated on `delivery_mode`. Apply this rule before walking the gate chain:

| Delivery mode | Stages 4a, 4b, 4c |
|---|---|
| Fast Path (0–3) | Skip entirely — do not check for these artifacts |
| Standard (4–7) | Skip entirely — do not check for these artifacts |
| Enterprise (8–11) | Skip entirely — do not check for these artifacts |
| Enterprise + Modular (12–14) | Required — treat as blocking gates before stage 5 |

Read `state/routing-decision.md` to determine delivery mode. If the routing decision is missing, assess the delivery mode from `state/workflow-state.json`. If neither is available, treat delivery mode as unknown and run the full gate chain (including 4a–4c) as a safe default.
```

---

### Change 4 — Update the "Enterprise + Modular" prose section to remove duplicate instructions

**Location:** "Delivery mode behavior" section, "Enterprise + Modular (12–14)" subsection.

**Current text:**
```
### Enterprise + Modular (12–14)
All stages required. Also run:
- `.brs2spec/skills/3-planning-and-modular-delivery/06-define-delivery-increments.md`
- `.brs2spec/skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md`
```

**Replace with:**

```markdown
### Enterprise + Modular (12–14)

All stages required. Stages 4a (software modules), 4b (capability-to-module map), and 4c (delivery increments) are part of the gate chain for this mode — see the gate chain table in Step 3.

Additionally, after stage 7 (open decisions):
- If traceability is required: run `skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md` to produce `planning/traceability-matrix.md`. This is required before handoff when delivery_mode is Enterprise + Modular.

All other stages follow the standard sequence.
```

---

### Change 5 — Add stages 4a–4c to `skills/0-repair/repair-workspace-state.md` scan list

**Location:** Step 3 "Artifacts to scan" table, after stage 4 (delivery structure draft) and before stage 5 (architecture review).

**Add these three rows:**

```
| 4a | Software modules (Enterprise + Modular) | `planning/software-modules.md` | Module table present with IDs, names, owning teams, capability boundaries; complete only if delivery_mode = Enterprise + Modular and file has real content |
| 4b | Capability-to-module map (Enterprise + Modular) | `planning/capability-to-module-map.md` | Every feature maps to a module; module IDs match software-modules.md; complete only if delivery_mode = Enterprise + Modular |
| 4c | Delivery increments (Enterprise + Modular) | `planning/delivery-increments.md` | Increments present with module and feature references; complete only if delivery_mode = Enterprise + Modular |
```

**Add to Step 4 "Absolute rule" table:**

```
| If `planning/software-modules.md` is missing AND delivery_mode = Enterprise + Modular | next_action cannot be later than stage 4a |
| If `planning/capability-to-module-map.md` is missing AND delivery_mode = Enterprise + Modular | next_action cannot be later than stage 4b |
| If `planning/delivery-increments.md` is missing AND delivery_mode = Enterprise + Modular | next_action cannot be later than stage 4c |
```

---

### Change 6 — Add stages 4a–4c to `state/workflow-state.json` template

**Location:** `.brs2spec/templates/state/workflow-state.json`, the `artifacts` block.

**Add after `planning/delivery-structure/` entry:**

```json
"planning/software-modules.md":        { "status": "not-triggered", "note": "Required only for Enterprise + Modular delivery mode" },
"planning/capability-to-module-map.md": { "status": "not-triggered", "note": "Required only for Enterprise + Modular delivery mode" },
"planning/delivery-increments.md":      { "status": "not-triggered", "note": "Required only for Enterprise + Modular delivery mode" },
```

For Enterprise + Modular initiatives, these statuses must be changed to `missing` (not `not-triggered`) when the routing decision confirms the delivery mode.

**Add a note to the `maintain-workflow-state.md` skill:** after reading `state/routing-decision.md`, if `delivery_mode` contains "Modular", set the status of these three entries to `missing` rather than `not-triggered`.

---

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`.
   - In Step 3, immediately before the stage gate chain table, insert the delivery mode gate-chain rule from Change 3.
   - In Step 3 stage gate chain table, between stage 4 and stage 5 rows, insert the three new rows from Change 1.
   - In Step 3 "Hard gate rules" table, add the three new rows from Change 2.
   - In the "Delivery mode behavior" section, replace the "Enterprise + Modular" subsection with the new text from Change 4.

2. Open `.brs2spec/skills/0-repair/repair-workspace-state.md`.
   - In Step 3 "Artifacts to scan" table, add the three new rows from Change 5.
   - In Step 4 "Absolute rule" table, add the three new rows from Change 5.

3. Open `.brs2spec/templates/state/workflow-state.json`.
   - Add the three new artifact entries from Change 6.

4. Open `.brs2spec/skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md`.
   - Add a note: when `delivery_mode` is Enterprise + Modular (read from `state/routing-decision.md`), change the status of `planning/software-modules.md`, `planning/capability-to-module-map.md`, and `planning/delivery-increments.md` from `not-triggered` to `missing`.

---

## Quality bar

After these changes:

- Running the orchestrator on an initiative with `delivery_mode: Enterprise + Modular` must stop at stage 4a after completing stage 4, and produce `planning/software-modules.md` before advancing to architecture review.
- The repair skill identifies missing Enterprise + Modular artifacts and sets `next_action` to stage 4a when they are absent.
- The state template records all three artifacts as `not-triggered` by default and the maintain-state skill upgrades them to `missing` for Enterprise + Modular initiatives.
- The "Also run" prose note in the delivery mode section no longer duplicates the gate chain table — it only mentions the traceability matrix (which is not in the main gate chain).
