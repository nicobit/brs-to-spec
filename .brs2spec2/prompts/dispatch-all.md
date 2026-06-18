# BRS-to-Spec v2 — Dispatch All

You are running BRS-to-Spec v2 in continuous mode. Execute events one at a time, looping until a stop condition is reached.

**Before starting — hard constraints:**
- Do NOT use todo lists, task trackers, or any internal planning tools at any point during dispatch. They are not visible to the user and add noise.
- Do NOT paraphrase stop conditions — output them verbatim as written in dispatcher.md.
- Do NOT offer menus or next-step suggestions after reporting.
- Do NOT hand-craft runtime events. Any event created during chain-repair, walk-back, or on_success must be instantiated from its template with `must_include` and `validation_rules` preserved exactly.

---

## Step 1 — Load the dispatcher

Read `.flow-engine/instructions/dispatcher.md` now. This defines the 21-step dispatch sequence and all stop conditions.

## Step 2 — Identify the active initiative

Scan `initiatives/` for the workspace that has a `.flow/` folder. If more than one workspace has `.flow/`, ask the user which initiative to run before continuing.

## Step 3 — Run the dispatch loop

Repeat the following until a stop condition is reached:

1. Follow the full 21-step dispatch sequence from `dispatcher.md`
2. After the event completes and state files are updated, return to step 1 of this loop
3. Do not pause between events unless a stop condition is reached

**50-event runaway guard:** If 50 events complete in this session without a stop condition being reached, stop immediately and report the event count and current queue state.

## Step 4 — Stop conditions

Stop when any of these is true (from dispatcher.md Section 7):

- `pending/` is empty — nothing left to run
- All remaining events in `pending/` are blocked — no unblocked event exists
- A blocking open decision has no assigned human owner
- A ROUTE_INITIATIVE event failed — delivery mode is unknown
- `processing/` already has a file when a new cycle begins — concurrent execution guard
- An event failed 3 times in succession — escalation required
- 50 events have been dispatched in this run — runaway guard
- A required input file for the next event does not exist and cannot be auto-created
- A `GENERATE_HANDOFF` or terminal event has completed — initiative is done
- The user explicitly says "stop"

## Step 5 — End-of-run report

When stopped, report in this format:

```
Run complete — stopped because: <stop condition>

Events executed:  <total count>
  Passed:         <count>
  Failed:         <count>

Artifacts produced:
  <list of files with status: accepted>

Events remaining in pending/:
  <list of EVT-IDs with blocked/unblocked status>

Open decisions:
  Blocking:     <count>
  Non-blocking: <count>
  <list of DEC-AUTO-NNN with question and owner>

```

Nothing else. No menus. No suggestions. Stop here.
