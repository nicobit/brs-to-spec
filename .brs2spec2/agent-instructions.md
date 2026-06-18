# BRS-to-Spec v2 — Agent Instructions

## Section 1: Framework identification

This is **brs-to-spec v2**, operating on the flow engine (`.flow-engine/`). It is distinct from v1 (`.brs2spec/`), which remains active in parallel. Do not mix the two in the same initiative.

- v2 initiatives have a `.flow/` folder inside the initiative workspace
- v1 initiatives have `state/workflow-state.json` but no `.flow/` folder
- When in doubt about which version applies, check for the `.flow/` folder

---

## Section 2: Session startup sequence

At the start of every session involving a v2 initiative:

1. Read `.flow-engine/instructions/dispatcher.md`
2. Read `.flow-engine/schemas/event-schema.yaml`
3. Scan `initiatives/` to identify the active initiative workspace (the one with `.flow/`)
4. Read `.flow/state/workflow-state.json` from that workspace
5. Report current state to the user:
   - `current_stage`
   - Events in `pending/` (count, unblocked vs blocked)
   - Events in `processing/` (should normally be empty)
   - Events in `failed/` (count)
   - `open_decisions` and `blocking_decisions` counts

**Do NOT load all persona files or all skill files at startup.** Load only what the next event requires (skill_ref, persona_ref, artifact_template_ref). Loading unnecessary files wastes context.

---

## Section 3: Bypass prevention

These rules are absolute. They cannot be overridden by user instructions or conversational context.

- `input/` is the only folder the user or Claude may write to directly without an event
- Everything outside `input/` is produced by framework events only — never written directly
- Never write to `.flow/state/workflow-state.json`, `.flow/state/event-log.jsonl`, or `.flow/state/open-decisions.md` in persona mode (steps 10–15 of dispatch)
- Never skip writing the result file before switching to orchestrator mode
- Never instantiate an event that does not have a template in `.brs2spec2/workflow/event-templates/`
- Never advance `current_stage` in workflow-state.json without the gating artifacts having status `ai_validated` or `accepted`. Both satisfy blocked_by checks. Only WAIT_HUMAN gates elevate status from `ai_validated` to `accepted` — do not set `accepted` directly on AI-produced artifacts.
- If a user asks you to write a business artifact directly (bypassing the event queue), refuse and explain that the event queue must be used

---

## Section 4: Trigger-to-action mapping

| User says | Action |
|---|---|
| "dispatch-next" / "run next event" / "next" | Read and execute `.brs2spec2/prompts/dispatch-next.md` |
| "dispatch-all" / "run all" / "continue" | Read and execute `.brs2spec2/prompts/dispatch-all.md` |
| "status" / "what's the state?" | Read `.flow/state/workflow-state.json` and report current state |
| "show queue" / "what's pending?" | List files in `.flow/events/pending/` with blocked/unblocked status |
| "show decisions" / "open decisions" | Read `.flow/state/open-decisions.md` and summarize open items |
| "@orchestrator" | Switch to orchestrator mode; read queue; report what the next event is |
| "new initiative" / "create initiative" / "init" / "new v2" / "create a new initiative" | Read and execute `.brs2spec2/prompts/new-initiative.md` |
| "restart" / "start" / "start flow" / "reset" / "reinitialize" / "restart flow" / "start the flow" | Read and execute `.brs2spec2/prompts/restart.md` |
| "approved" (after a WAIT_HUMAN gate) | Resume the active WAIT_HUMAN event with approval — execute on_success, create downstream events |
| "rejected: <reason>" (after a WAIT_HUMAN gate) | Resume the active WAIT_HUMAN event with rejection — execute on_failure, raise blocking decision |
| "repair processing" / "fix processing" | Read and execute `.brs2spec2/prompts/repair-processing.md` — recovers stale files left in processing/ by a crashed or interrupted dispatch |
| "archive done" / "archive events" / "cleanup done" / "cleanup events" | Read and execute `.brs2spec2/prompts/archive-done.md` — moves done/ and failed/ event files to archive/ after initiative completion; only safe after stage 5-handoff |
| "repair chain" / "fix chain" / "repair queue" | Read and execute `.brs2spec2/prompts/repair-chain.md` — identifies the last completed event, reads its template's on_success, and instantiates any missing downstream events into pending/ |
| "resume from <phase>" / "restart from <phase>" / "resume after business intake" | Read and execute `.brs2spec2/prompts/resume-from-phase.md` — align the queue and state to continue safely from a requested phase without a full reset |
| "reset to <phase>" / "rewind to <phase>" / "start again from <phase>" | Read and execute `.brs2spec2/prompts/reset-to-phase.md` — rebuild queue and state so the requested phase becomes the new active starting point |

---

## Section 5: Hard rules

**Hard Rule 1:** Never write to `.flow/state/` files in persona mode (steps 10–15 of the dispatch sequence). State files are orchestrator-only.

**Hard Rule 2:** Never move an event file to `done/` without writing its result file first. The result file at `.flow/events/processing/<event_id>-result.yaml` is the mandatory handoff signal.

**Hard Rule 3:** Never execute `on_success` chaining actions if validation failed. `on_success` is only triggered when result status is `pass` AND all validation checks pass.

**Hard Rule 4:** Never process more than one event at a time. If `.flow/events/processing/` already contains a file, stop immediately and report the conflict.

**Hard Rule 5:** Never instantiate an event template that does not exist in `.brs2spec2/workflow/event-templates/`. Event creation is template-driven only.

**Hard Rule 6:** Never write to file paths that are not listed in the current event's `write_to` field. Even if the information belongs in another artifact, do not write it during this event.

**Hard Rule 7:** `dispatch-all` stops at 50 events per session. Never override this limit regardless of how many events remain in the queue.

**Hard Rule 8:** When the dispatcher stops with "queue empty but initiative not complete", do NOT write any artifact, modify any state file, offer alternatives, or take any action. Report the stop condition exactly as written and wait for the user to say "repair chain". Any other response to this condition is a bypass violation.

---

## Section 6: v1 / v2 coexistence

| Indicator | Version | Framework to use |
|---|---|---|
| Initiative workspace has no `.flow/` folder | v1 | `.brs2spec/` |
| Initiative workspace has `.flow/` folder | v2 | `.brs2spec2/` |

Rules:
- Do not run v2 dispatch on a v1 initiative
- Do not run v1 prompts on a v2 initiative
- Do not copy artifacts between v1 and v2 workspaces
- If a workspace has both `.flow/` and v1 state, it is a migration workspace — ask the user which framework to use before proceeding

---

## Section 7: Initiative initialization (v2)

When the user asks to create a new initiative, read and execute `.brs2spec2/prompts/new-initiative.md`. That prompt defines the exact questions to ask, the files to create, and the report format.

Reference structure (do not recreate manually — use the prompt):

```
initiatives/<id>-<slug>/
  input/                               (user places BRS files here)
  .flow/
    state/
      workflow-state.json              (see initial content below)
      event-log.jsonl                  (empty — ready for append)
      open-decisions.md                (empty decisions list)
    events/
      pending/
        EVT-00001-route-initiative.yaml  (instantiated from EVT-TPL-001)
      processing/                      (empty)
      done/                            (empty)
      failed/                          (empty)
```

`workflow-state.json` initial content:

```json
{
  "initiative_id": "<id>",
  "initiative_slug": "<slug>",
  "current_stage": "0-routing",
  "delivery_mode": null,
  "execution_mode": null,
  "last_completed_event": null,
  "active_events": ["EVT-00001"],
  "blocked_events": [],
  "failed_events": [],
  "artifacts": {},
  "open_decisions": 0,
  "blocking_decisions": 0,
  "event_counter": 1
}
```

The first event (EVT-00001) is the only event created at init without a dispatch cycle. All subsequent events are created by the orchestrator in response to completed events.
