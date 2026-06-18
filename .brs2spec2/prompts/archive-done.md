# BRS-to-Spec v2 — Archive Completed Events

Use this prompt when:
- The initiative has reached `current_stage: 5-handoff` and the dispatcher reported "Queue empty — initiative complete"
- The user says "archive done", "archive events", "cleanup done", or "cleanup events"

This prompt is safe to run only after initiative completion. During an active initiative,
`done/` event files are load-bearing for `blocked_by_events` checks — do not archive mid-run.

---

## Step 1 — Confirm initiative is complete

Read `.flow/state/workflow-state.json`.

If `current_stage` is NOT `5-handoff` → stop:
**"Archive is only safe after initiative completion (stage 5-handoff). Current stage is [X]. Do not archive done/ while the initiative is active — blocked_by_events checks depend on event files in done/."**

If `pending/` contains any `.yaml` files → stop:
**"pending/ is not empty — the initiative is not fully complete. Archive aborted."**

If `processing/` contains any files → stop:
**"processing/ is not empty — a dispatch may still be running. Run 'repair processing' first, then archive."**

---

## Step 2 — Count files to archive

Count files in `.flow/events/done/` and `.flow/events/failed/`.

Report the counts before doing anything:
```
Ready to archive:
  done/:   <N> files
  failed/: <N> files
```

---

## Step 3 — Create archive folder

Create `.flow/events/archive/` if it does not exist.

---

## Step 4 — Move done/ and failed/ contents to archive/

Move all files from `.flow/events/done/` into `.flow/events/archive/done/`.
Move all files from `.flow/events/failed/` into `.flow/events/archive/failed/`.

Leave the `done/`, `failed/`, `pending/`, and `processing/` folders themselves in place (empty).

---

## Step 5 — Report

```
Archive complete: <workspace_name>
Archived to:     .flow/events/archive/
  done/:         <N> files moved
  failed/:       <N> files moved

done/ and failed/ are now empty.
The initiative artifacts in <workspace_root>/ are untouched.
```

Nothing else. No menus. No options.

---

## Stop conditions

- Do NOT run if `current_stage` is not `5-handoff`
- Do NOT run if `pending/` or `processing/` are non-empty
- Do NOT touch any files outside `.flow/events/done/` and `.flow/events/failed/`
- Do NOT delete `workflow-state.json`, `event-log.jsonl`, or `open-decisions.md`
- Do NOT delete the business artifacts produced by the initiative (anything outside `.flow/`)
