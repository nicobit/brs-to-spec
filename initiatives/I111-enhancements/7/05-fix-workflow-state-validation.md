# Enhancement 7.5 — Require Skill Invocation for State Updates and Tighten Validation

## Problem

On the I005 run, `state/workflow-state.json` ended in a contradictory state:
- `current_stage: "pre-intake"` (nothing started) alongside `next_action.stage: "complete"` (everything done)
- `review-package/status.md` listed twice — once as `complete`, once as `missing`
- `quality_gates_complete` missing the security gate even though it appeared in `quality_gates_triggered`
- Gate notes contained `"forced"` but `state_validated: true`

The root cause: the orchestrator updated the state file **inline** — by directly constructing and writing JSON — rather than invoking the `orchestrator.maintain_state` skill (`skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md`). The `maintain-workflow-state.md` skill has explicit validation logic: status value checks, forced-acceptance detection, staleness rules, and consistency checks between `current_stage` and `next_action`. None of this logic ran because the skill was bypassed.

A second issue: `state_validated: true` was written even though the file had forced-acceptance notes. The `maintain-workflow-state.md` skill says not to set `state_validated: true` without physically reading every artifact, but there is no explicit rule that forced-acceptance notes block `state_validated`.

A third issue: the `workflow-state.json` template allows `state_validated: true` to be set in the same operation that writes the rest of the file. This makes it trivially easy to claim validation without performing it.

---

## What needs to change

### Change 1 — Require the `maintain_state` skill for every state file update in `brs-to-spec-run-workflow.md`

**Location:** Step 10 (Reassess), and Step 7 (Execute the next stage) — after completing each stage.

**Add to Step 7, immediately after "Save to the correct path inside the initiative workspace":**

```markdown
### State update rule — mandatory after every stage

After completing any stage (writing an artifact, accepting a gate, repairing a stale file):

1. **Invoke `orchestrator.maintain_state`** — load `.brs2spec/skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md` and execute it.
2. **Do not write `state/workflow-state.json` directly.** Inline JSON edits to the state file are a framework violation. The only permitted way to update the state file is via the `maintain-workflow-state.md` skill.
3. **Why:** the skill performs consistency checks (duplicate entries, forced-acceptance detection, `current_stage` vs `next_action` alignment) that cannot be replicated inline. An inline write will always produce a state file that the orchestrator will reject on the next session as `state_validated: false`.

**Exception:** if the state file is being repaired by `skills/0-repair/repair-workspace-state.md`, that skill writes the state file directly as part of the repair process — this is the only permitted exception.
```

---

### Change 2 — Add forced-acceptance detection to `skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md`

**Location:** Step 6 "Set state_validated = true and last_updated."

**Current text:**
```
Set `state_validated` to `true` only when you have physically read every artifact file in this session,
not just checked for existence.
```

**Replace with:**

```markdown
### Step 6 — Set state_validated and last_updated

Set `state_validated` to `true` **only when ALL of the following are true:**

1. You have physically read (opened and checked content of) every artifact file listed in the `artifacts` block.
2. No artifact has status `corrupt` (see Enhancement 7.1). A corrupt artifact cannot be read reliably — set `state_validated: false` if any `corrupt` entries exist.
3. No quality gate has a note containing any of these patterns: `"forced"`, `"force-accepted"`, `"Accepted (forced)"`, `"force accepted"`. If any gate note matches: set `state_validated: false`. A state file with forced-acceptance notes is not validated — it is a record of a bypass.
4. `current_stage` and `next_action.stage` are logically consistent. Specifically:
   - `next_action.stage` must be a later stage in the gate chain than `current_stage`, OR equal to `current_stage` if the stage is still in progress.
   - If `next_action.stage = "complete"` then `current_stage` must be the last required stage for the delivery mode (not `"pre-intake"`, `"routing"`, or any early stage).
   - If these contradict each other: set `state_validated: false`; add a `_validation_error` note to `workflow-state.json` explaining the contradiction; do not advance.
5. No artifact path appears more than once in the `artifacts` block. Duplicate keys indicate a JSON merge error — remove the duplicate and keep the entry with the most accurate status.

**If any of conditions 1–5 fail:** set `state_validated: false`. Add a `_validation_errors` array to `workflow-state.json` listing each failure reason. The orchestrator will detect `state_validated: false` on the next session and trigger a full artifact scan before advancing.

Set `last_updated` to today's date in ISO-8601. Set `updated_by` to `"orchestrator.maintain_state"` (never `"orchestrator.run"` — the maintain skill, not the orchestrator, owns the state file).
```

---

### Change 3 — Add a `_validation_errors` field to the `workflow-state.json` template

**Location:** `.brs2spec/templates/state/workflow-state.json`.

**Add after the `_note` field:**

```json
"_validation_errors": [],
```

This field is populated by the `maintain-workflow-state.md` skill when `state_validated` is set to `false`. It lists specific reasons why validation failed. The orchestrator reads it on the next session to understand what was wrong without scanning all artifacts.

**Also add a note to the template:**

```json
"_note": "Machine-readable workflow state. Read first to avoid scanning all artifacts. state_validated must be set by the maintain-workflow-state skill, never inline. If state_validated is false, run repair-workspace-state.md before advancing."
```

---

### Change 4 — Add consistency checks to the repair skill

**Location:** `skills/0-repair/repair-workspace-state.md`, Step 4, at the end of the "Determine the correct `current_stage` and `next_action`" section.

**Add:**

```markdown
### Consistency check — run after determining current_stage and next_action

Before writing the repaired state file, verify:

1. **Stage consistency:** `next_action.stage` must be at a later position in the gate chain than `current_stage`. If `next_action.stage = "complete"` then `current_stage` must be the last completed stage for this delivery mode. If they contradict: use the gate chain walk result as authoritative — ignore the prior values.

2. **No duplicate keys:** scan the artifacts block for duplicate path keys. If any path appears twice, keep the entry with the lower-trust status (prefer `missing` over `complete`, `incomplete` over `complete`) and log the duplicate in the repair report.

3. **Gate consistency:** `quality_gates_complete` must be a subset of `quality_gates_triggered`. A gate cannot be complete if it was not triggered. Remove any entries in `quality_gates_complete` that are not in `quality_gates_triggered`.

4. **Forced-acceptance gates:** any gate name in `quality_gates_complete` whose corresponding artifact has a forced-acceptance note must be moved from `quality_gates_complete` to `quality_gates_triggered` (triggered but not genuinely complete).

Add a `### Consistency checks` section to the repair report, listing every consistency violation found and how it was resolved.
```

---

### Change 5 — Tighten the Step 1b fast-path rejection rule in `brs-to-spec-run-workflow.md`

**Location:** Step 1b "Read workflow-state.json (fast path)."

The existing rule says: "If any quality gate entry has a note containing 'forced' → treat `state_validated` as `false`."

**Extend this rule to also cover:**

```markdown
**Reject the fast path and treat `state_validated` as `false` if ANY of the following are true:**

- Any quality gate entry has a note containing `"forced"`, `"force-accepted"`, or `"Accepted (forced)"`.
- `_validation_errors` is non-empty.
- `current_stage` and `next_action.stage` are logically inconsistent (e.g. `current_stage: "pre-intake"` with `next_action.stage: "complete"`).
- Any artifact path appears more than once in the `artifacts` block.
- `updated_by` is `"orchestrator.run"` — the state file was written inline, not by the maintain skill.

When the fast path is rejected: proceed with full artifact scan (Steps 2 and 3) and invoke the repair skill if the inconsistencies are structural. Do not use any value from the rejected state file as a starting point — treat every field as unknown and re-derive from disk.
```

---

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`.
   - In Step 7, after "Save to the correct path inside the initiative workspace": insert the state update rule from Change 1.
   - In Step 1b: extend the fast-path rejection rule with the new conditions from Change 5.

2. Open `.brs2spec/skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md`.
   - Replace Step 6 with the new text from Change 2.

3. Open `.brs2spec/templates/state/workflow-state.json`.
   - Add the `_validation_errors` field and updated `_note` from Change 3.

4. Open `.brs2spec/skills/0-repair/repair-workspace-state.md`.
   - At the end of Step 4, add the consistency check block from Change 4.

---

## Quality bar

After these changes:

- `state/workflow-state.json` is always written by the `maintain-workflow-state.md` skill. `updated_by` always says `"orchestrator.maintain_state"`. An inline write is detectable and rejected on the next session.
- `state_validated: true` cannot be set if any gate note contains "forced", if any artifact is `corrupt`, or if `current_stage` and `next_action.stage` contradict.
- Consistency violations (duplicate keys, gate lists out of sync, stage contradiction) are logged in `_validation_errors` and surfaced in the repair report.
- The fast-path detection in Step 1b catches all known patterns of corrupted state files and falls through to full artifact scan rather than advancing on bad data.
- A future run on I005 would immediately detect that `current_stage: "pre-intake"` contradicts `next_action.stage: "complete"`, set `state_validated: false`, and start from the full scan rather than using the corrupted state as a shortcut.
