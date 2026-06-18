# BRS-to-Spec v2 — Dispatch Next

You are running one BRS-to-Spec v2 event. Execute exactly one event from the queue, then stop and report.

**Before starting — hard constraints:**
- Do NOT use todo lists, task trackers, or any internal planning tools at any point during dispatch. They are not visible to the user and add noise.
- Do NOT paraphrase stop conditions — output them verbatim as written in dispatcher.md.
- Do NOT offer menus or next-step suggestions after reporting.
- Do NOT hand-craft runtime events. Any event created during chain-repair, walk-back, or on_success must be instantiated from its template with `must_include` and `validation_rules` preserved exactly.

---

## Step 1 — Load the dispatcher

Read `.flow-engine/instructions/dispatcher.md` now. This defines the 21-step dispatch sequence you must follow exactly.

## Step 2 — Identify the active initiative

Scan `initiatives/` for the workspace that has a `.flow/` folder. If more than one workspace has `.flow/`, ask the user which initiative to run before continuing.

## Step 3 — Follow the 21-step dispatch sequence

Execute the full dispatch sequence from `dispatcher.md` once. Stop after the single event completes (pass or fail) and state files are updated.

Do not execute more than one event. Do not skip steps. Do not write to `.flow/state/` files in persona mode.

## Step 4 — Report to the user

After the event completes, report in this format:

```
Event:      EVT-NNNNN — <title>
Persona:    <persona>
Result:     PASS | FAIL
Artifacts:  <list of files written, or "none">
```

**If PASS:**
```
Events created in pending/: <list of new EVT-IDs, or "none">
Decisions raised:           <count or "none">
```

**If FAIL:**
```
Failure reason:   <from result file>
Decision raised:  <DEC-AUTO-NNN if applicable, or "none">
```

---

Nothing else. No menus. No suggestions. Stop here.
