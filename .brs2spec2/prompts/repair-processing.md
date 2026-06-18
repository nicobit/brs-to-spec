# BRS-to-Spec v2 — Repair Processing Folder

Use this prompt when:
- The dispatcher stopped at Step 3 because `.flow/events/processing/` is not empty
- A previous dispatch session was interrupted (context reset, session crash, user abort mid-run)
- You need to recover without losing completed work or restarting the whole initiative

This prompt does NOT restart the initiative. It repairs the stale processing state only.

---

## Step 1 — Identify the initiative workspace

Use the same workspace identified in dispatcher Step 0.

---

## Step 2 — Audit processing/

List every file in `.flow/events/processing/`.

Classify each file as one of:

| File type | Pattern | Classification |
|---|---|---|
| Event file | `EVT-NNNNN-<slug>.yaml` (no `-result` suffix) | stale event |
| Result file | `EVT-NNNNN-result.yaml` | stale result |

---

## Step 3 — Cross-reference with done/ and failed/

For each stale event file `EVT-NNNNN-<slug>.yaml` in `processing/`:

a. Check if `EVT-NNNNN-<slug>.yaml` exists in `done/`
b. Check if `EVT-NNNNN-result.yaml` exists in `done/`
c. Check if `EVT-NNNNN-<slug>.yaml` exists in `failed/`

Determine the recovery action per event:

| Condition | Recovery action |
|---|---|
| Event AND result both in `done/` | The event completed successfully — delete stale copies from `processing/` |
| Event in `done/`, result in `done/` | Same as above — delete stale copies from `processing/` |
| Event in `failed/` | The event failed and was recorded — delete stale copies from `processing/` |
| Event NOT in `done/` or `failed/`, BUT result file exists in `processing/` with `status: pass` | Event completed but Step 17 did not run — move event and result to `done/` |
| Event NOT in `done/` or `failed/`, BUT result file exists in `processing/` with `status: fail` | Event failed but Step 17 did not run — move event and result to `failed/` |
| Event NOT in `done/` or `failed/`, NO result file in `processing/` | Event was interrupted mid-execution (before Step 15) — move event back to `pending/`; it will be re-executed |

---

## Step 4 — Apply recovery actions

Execute each recovery action identified in Step 3:

- **Delete stale copy:** Remove the file from `processing/`. Do not touch `done/` or `failed/`.
- **Move to done/:** Move event file and result file from `processing/` to `done/`.
- **Move to failed/:** Move event file and result file from `processing/` to `failed/`.
- **Move back to pending/:** Move event file only from `processing/` to `pending/`. Do not create a result file.

After all actions: `processing/` must be empty.

---

## Step 5 — Check pending/ for orphan duplicates

An orphan duplicate is a file in `pending/` whose EVT-ID already exists in `done/` or `failed/`.

For each file in `pending/`:
- If the same EVT-ID exists in `done/` → delete the `pending/` copy (the event already completed)
- If the same EVT-ID exists in `failed/` → delete the `pending/` copy (the event already failed; a retry event would have been created by on_failure)
- Otherwise → leave it in `pending/`

---

## Step 6 — Report

```
Repair complete: <workspace_name>
Processing/ files found:  <N>
  Deleted (already in done/):   <list EVT-IDs or "none">
  Moved to done/:               <list EVT-IDs or "none">
  Moved to failed/:             <list EVT-IDs or "none">
  Returned to pending/:         <list EVT-IDs or "none">
Orphan pending/ duplicates removed: <list EVT-IDs or "none">

processing/ is now empty. Run dispatch-next to continue.
```

Nothing else. No menus. No options. No "would you like to...".

---

## Stop conditions

- If `processing/` is already empty when this prompt runs → report "processing/ is already empty — no repair needed." and stop.
- Do not modify `done/` or `failed/` contents except as stated above.
- Do not modify `workflow-state.json` — state repair is not in scope here. If `active_events` or `failed_events` in workflow-state.json appear inconsistent after this repair, the dispatcher's normal Step 19 will reconcile them on the next successful dispatch.
- Do not run `dispatch-next` automatically — wait for the user to say it.
