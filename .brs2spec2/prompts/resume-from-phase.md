# BRS-to-Spec v2 — Resume From Phase

Use this prompt when:
- The user says "resume from business analysis", "resume from phase X", "restart from after business intake", or similar
- The initiative has a `.flow/` workspace but the user wants to continue from a specific stage instead of doing a full reset
- The queue/state may need light repair before dispatch can continue

This prompt does NOT wipe `.flow/`.
It does NOT regenerate business artifacts directly.
Its job is to align the queue and state so the next dispatch starts from the requested phase safely.

---

## Supported phase names

Map the user's request to one of these canonical targets:

| User phrasing | Canonical target |
|---|---|
| beginning, start over, from scratch, routing, re-route | `0-routing` |
| business intake, intake, from the start, before analysis | `2-business-intake` |
| after business intake, business analysis, requirements/use cases | `2b-business-analysis` |
| architecture, planning | `3-planning` |
| engineering readiness, readiness | `4-engineering-readiness` |
| quality gates, bdd/contracts/security | `4b-quality-gates` |
| handoff, openspec, standalone package | `5-handoff` |

If the user names a phase outside this list, stop:
**"Unsupported resume target: [user text]. Use one of: routing, business intake, business analysis, planning, engineering readiness, quality gates, handoff."**

---

## Step 1 — Identify the initiative workspace

1. If the user named an initiative, locate `initiatives/<id>*/`.
2. Otherwise scan `initiatives/` and select the workspace with `.flow/` most recently modified.
3. Set `workspace_root = initiatives/<workspace_name>/`.

If no v2 workspace is found, stop:
**"No v2 initiative workspace found. Use 'new initiative' or 'restart' first."**

---

## Step 2 — Load current state

Read:
- `<workspace_root>/.flow/state/workflow-state.json`
- `<workspace_root>/.flow/state/open-decisions.md`

Also inspect:
- `.flow/events/pending/`
- `.flow/events/processing/`
- `.flow/events/done/`
- `.flow/events/failed/`

If `.flow/state/workflow-state.json` is missing, stop:
**"workflow-state.json missing. Run 'restart' to reinitialize the flow engine."**

If `blocking_decisions > 0`, stop:
**"Resume blocked: there are open blocking decisions that must be resolved first. Run 'show decisions' to review them."**

---

## Step 3 — Normalize the queue first

Before deciding how to resume:

1. If `.flow/events/processing/` is non-empty, execute the logic from `repair-processing.md` first.
2. If `.flow/events/pending/` is empty and the initiative is not complete, execute the logic from `repair-chain.md` first.
3. Re-read queue folders after any repair.

Do not report intermediate repair details unless a stop condition is hit.

---

## Step 4 — Determine the resume strategy

Let `target_phase` be the canonical target from the user's request.

Use these rules:

### Target = `0-routing`

Goal: full reset — wipe all queue folders and restart from EVT-00001.

1. Warn the user: **"This will delete all pending, processing, and failed events and reset the queue to EVT-00001. Completed artifacts in `done/` are preserved but their workflow-state entries will be cleared. Confirm with 'yes reset' to proceed."** Stop and wait for confirmation.
2. On confirmation:
   - Delete all files in `.flow/events/pending/`, `.flow/events/processing/`, `.flow/events/failed/`
   - Leave `.flow/events/done/` intact (artifacts are preserved for reference)
   - Reset `workflow-state.json`: `current_stage: "0-routing"`, `artifact_status: {}`, `event_counter: 1`, `active_events: ["EVT-00001"]`, `last_completed_event: null`, `failed_events: []`
   - Instantiate EVT-00001 from EVT-TPL-001 and write to `pending/`
3. Report: **"Full reset complete. Queue restarted from EVT-00001. Say 'dispatch-next' to begin."**

### Target = `2-business-intake`

Goal: reset to before business intake — preserve routing, restart from EVT-TPL-002.

1. Check whether `routing/routing-decision.md` exists and is `accepted` in `workflow-state.json`.
   - If not → stop: **"Cannot resume from business intake: routing is not complete. Resume from routing instead."**
2. Clear all events in `pending/`, `processing/`, `failed/` whose stage is `2-business-intake` or later.
3. Remove from `workflow-state.json artifact_status` all entries except `routing/routing-decision.md`.
4. Reset `workflow-state.json`: `current_stage: "0-routing"`, `last_completed_event: EVT-00001`, `event_counter` to reflect only EVT-00001 done.
5. Instantiate EVT-00002 from EVT-TPL-002 and write to `pending/`.
6. Report: **"Reset to business intake. Routing preserved. Say 'dispatch-next' to re-run business intake."**

### Target = `2b-business-analysis`

Goal: resume from the first valid event after business intake.

1. Check whether the business intake review gate event already exists:
   - in `pending/` or `processing/` as a WAIT_HUMAN event → stop and present that gate normally; do not bypass it
   - in `done/` with pass → continue
2. If the gate has not yet been created but `business-intake/business-intake-summary.md` exists and is `ai_validated`, instantiate the gate event via its template chain if missing.
3. If the gate is already approved, ensure the requirements event (`EVT-TPL-043`) exists in `pending/`, `done/`, or `failed/`.
4. If the requirements event is missing, instantiate it from the gate's `on_success.create_events`.
5. Prefer the earliest uncompleted event in business analysis as the next dispatch target.

### Target = `3-planning`

Goal: resume from architecture/planning only if business analysis prerequisites are actually complete.

Required completed prerequisites:
- `business-analysis/requirements.md`
- `business-analysis/use-cases.puml`
- `business-analysis/use-cases/`
- `business-analysis/gaps-and-questions.md`

If any required prerequisite is missing or failed, stop:
**"Cannot resume from planning: business-analysis prerequisites are incomplete. Resume from business analysis first."**

If prerequisites are complete, ensure the appropriate planning events exist in queue or done/ by repairing the chain from the last completed upstream event.

### Target = `4-engineering-readiness`

Required completed prerequisites:
- planning/delivery-structure.md
- architecture/architecture-review.md

If either is missing, stop:
**"Cannot resume from engineering readiness: planning prerequisites are incomplete. Resume from planning first."**

### Target = `4b-quality-gates`

Required completed prerequisite:
- engineering-readiness/readiness-check.md

If missing, stop:
**"Cannot resume from quality gates: readiness-check.md is incomplete. Resume from engineering readiness first."**

### Target = `5-handoff`

Required completed prerequisites:
- engineering-readiness/initiative-context.md when applicable
- all triggered quality-gate prerequisites present

If missing, stop:
**"Cannot resume from handoff: readiness or quality-gate prerequisites are incomplete. Resume from the earlier phase first."**

---

## Step 5 — Offer a bounded choice only when the request is ambiguous

Only if the user's request is ambiguous between two nearby safe targets, present exactly these options and stop:

```
Resume target is ambiguous for <workspace_name>.

Choose one:
1. Resume from the business intake gate / first business-analysis event
2. Resume from the first planning event after business analysis
3. Cancel
```

Do not present options if the user named a clear phase.
Do not present options with more than 3 choices.

---

## Step 6 — Report the resume point

If a valid resume point was prepared, report:

```
Resume prepared: <workspace_name>
Target phase:     <canonical target>
Current stage:    <workflow-state current_stage>
Next queue event: <EVT-ID> — <title>
Queue status:     <unblocked/blocked>

Say "dispatch-next" to continue one event, or "dispatch-all" to continue the flow.
```

If the next thing is a WAIT_HUMAN gate, report instead:

```
Resume prepared: <workspace_name>
Target phase:     <canonical target>
Next step is a human gate:
<gate name> — <EVT-ID>

Review the artifact and reply "approved" or "rejected: <reason>".
```

---

## Stop conditions

- Do not wipe `.flow/` — use `restart` for full reinitialization
- Do not bypass WAIT_HUMAN gates
- Do not instantiate events whose prerequisites are clearly incomplete
- Do not modify business artifacts directly
- Do not invent templates not present in `.brs2spec2/workflow/event-templates/`
