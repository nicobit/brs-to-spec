# BRS-to-Spec v2 — Repair Broken On_Success Chain

Use this prompt when:
- The dispatcher stopped at Step 2 with "Queue empty but initiative is not complete"
- pending/ is empty but the initiative has not reached stage 5-handoff
- A completed event's on_success chain was never executed (events were not created downstream)

This prompt does NOT re-execute any event. It only instantiates the missing downstream events
that should have been created by on_success chaining.

---

## Step 1 — Load engine rules

Read the following files before proceeding:
- `.flow-engine/instructions/template-instantiation-rules.md`
- `.flow-engine/instructions/state-update-rules.md`

---

## Step 2 — Confirm broken chain condition

Read `.flow/state/workflow-state.json`. Confirm:
- `current_stage` is NOT `5-handoff`
- `pending/` is empty (the dispatcher already confirmed this — double-check)
- `failed_events` array is empty or contains only non-blocking failures

If `failed_events` is non-empty AND `blocking_decisions > 0` → stop:
**"Chain repair blocked: there are open blocking decisions that must be resolved first. Run 'show decisions' to see them."**

---

## Step 3 — Identify the last completed event

Read `last_completed_event` from `workflow-state.json`. This is the EVT-ID whose `on_success`
chain should have created the next events but did not.

Find the event file for that EVT-ID in `.flow/events/done/`. Read it.

If the event file does not exist in `done/` → stop:
**"Cannot find done/EVT-NNNNN-*.yaml for last_completed_event [EVT-ID]. The done/ folder may be corrupted. Run 'repair processing' first."**

---

## Step 3b — Scan done/ for path-mismatched hand-crafted events

For every event file in `.flow/events/done/`:

1. Read the event file.
2. Check whether `meta.template_id` is present.
3. If `meta.template_id` is absent:
   a. Look up the `action` field in `template-instantiation-rules.md` section 3 to find the matching template.
   b. If no matching template exists → skip (genuinely custom event, no check needed).
   c. If a matching template exists → read it.
   d. Compare each path in the event's `write_to` against the template's `outputs.primary` (and `outputs.secondary` if present).
   e. If any `write_to` path does not match the template outputs → record a **path mismatch**:
      - Hand-crafted event: `<EVT-ID>` (`<action>`)
      - Wrong path written: `<write_to path>`
      - Expected path from template `<EVT-TPL-NNN>`: `<outputs.primary>`
      - Artifact exists at wrong path: yes/no (check disk)
      - Artifact exists at correct path: yes/no (check disk)

Collect all path mismatches found. These do not block chain repair but must be reported and may explain why downstream events fail their required_inputs check.

**If any path mismatches are found where the artifact exists at the wrong path but NOT at the correct path:**
- Do NOT copy or move the file — that is outside the scope of this prompt.
- Record these as **path-mismatch warnings** to include in the Step 8 report.
- The user must manually copy the artifact from the wrong path to the correct path before the downstream event can execute.

---

## Step 4 — Identify which template produced the last event

Read `meta.template_id` from the event file found in Step 3.

If `meta.template_id` is absent → the event was hand-crafted without a template.
In this case: look up the action field and find the matching template by action name in
`.brs2spec2/workflow/event-templates/` (glob `EVT-TPL-*-<action-slug>.yaml`).
If no matching template is found → stop:
**"Last completed event [EVT-ID] has no template_id and no matching template file could be found for action '[action]'. Cannot determine on_success chain. Manual intervention required."**

Load the template file.

---

## Step 5 — Determine which on_success events were already created

List all EVT-IDs in `done/`, `failed/`, and `pending/` (combined).

Read `on_success.create_events` from the template loaded in Step 4.

For each template reference in `on_success.create_events`:
- Read the template file it points to
- Check its `condition` field against `workflow-state.json` (skip if condition is false)
- Check whether a runtime event with `meta.template_id` matching this template already exists
  in `done/`, `failed/`, or `pending/`
- If it already exists in any of those folders → mark as **already created** (skip)
- If it does NOT exist in any folder → mark as **missing** (needs instantiation)

---

## Step 6 — Instantiate missing events

For each template reference marked as **missing** in Step 5:

Follow the full instantiation procedure from `template-instantiation-rules.md` section 2:

1. Read the template file
2. Apply the complete field mapping (section 2)
3. Resolve `blocked_by_stage` if present (section 4)
4. Assign `event_id`: read `event_counter` from `workflow-state.json`, increment by 1, format as `EVT-NNNNN`
5. Set `meta.created_at` to current datetime, `meta.created_by` to `orchestrator`
6. Set `meta.notes` to: `"Instantiated by chain-repair from [last_completed_event] on_success"`
7. Before writing, verify the runtime event contains:
   - every `must_include` item from the template
   - the full `validation_rules` block from the template
   - `on_success` and `on_failure` copied verbatim
8. Write runtime event to `.flow/events/pending/EVT-NNNNN-<slug>.yaml`
9. Read the written file back immediately and verify the `must_include` count matches the template count exactly
10. Increment `event_counter` in `workflow-state.json`

After instantiating all missing events, update `workflow-state.json`:
- `active_events`: add all newly created EVT-IDs
- `last_updated`: current ISO-8601 datetime

---

## Step 7 — Walk forward if still blocked

After Step 6, check whether `pending/` events are unblocked (run the blocked_by check from
dispatcher Step 4 against the newly created events).

If all new events are still blocked by artifacts that don't exist yet:
- This means the chain gap is deeper than one level — the missing artifact itself was
  never produced because an even earlier on_success chain was broken
- Walk back one more step: find the event that should have produced the blocking artifact,
  check its template's on_success, and repeat Steps 4–6 for that event
- Repeat until at least one pending event is unblocked, or until you reach EVT-00001
- Maximum walk-back depth: 10 events. If still blocked after 10 → stop and report

---

## Step 8 — Report

```
Chain repair complete: <workspace_name>
Last completed event: <EVT-ID> (<action>)
Template:            <EVT-TPL-NNN>

Missing events instantiated:
  <EVT-NNNNN> — <task.title> (from EVT-TPL-NNN)
  ... (one line per event, or "none")

Already present (skipped):
  <EVT-NNNNN> — <task.title>
  ... (one line per event, or "none")

Blocked events (unresolved blocked_by):
  <EVT-NNNNN> — blocked by <artifact path>
  ... (or "none — all new events are unblocked")

event_counter updated to: <N>

PATH MISMATCH WARNINGS — manual action required before dispatch:
  <EVT-ID> (<action>): wrote to <wrong-path>, template <EVT-TPL-NNN> expects <correct-path>
    → artifact at wrong path: <yes/no>
    → artifact at correct path: <yes/no>
    → action needed: copy <wrong-path> to <correct-path>
  ... (one block per mismatch, or "none")
```

Nothing else. No menus. No options. No "would you like to...".

---

## Stop conditions

- If `current_stage` is `5-handoff` → stop: "Initiative is already complete — no chain repair needed."
- If `blocking_decisions > 0` → stop before instantiating anything
- If no template can be found for the last completed event → stop and report (Step 4)
- If walk-back depth exceeds 10 events → stop and report what was found
- Do NOT re-execute any event that already has output in `done/` or `failed/`
- Do NOT modify any business artifact files — only write to `.flow/events/pending/` and `.flow/state/workflow-state.json`
- Do NOT invent event templates that don't exist in `.brs2spec2/workflow/event-templates/`
