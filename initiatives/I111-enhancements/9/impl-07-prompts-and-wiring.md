# Implementation Prompt — Phase 4 + 5: User Entry Points and Framework Wiring

**Target:** `.brs2spec2/prompts/`, `.brs2spec2/agent-instructions.md`, `CLAUDE.md`, scaffolding script  
**Prerequisites:** Engine complete; Slice 1 validated end-to-end  
**Produces:** `dispatch-next.md`, `dispatch-all.md`, `agent-instructions.md`, CLAUDE.md update, init script update

---

## Context

You are writing the user-facing entry points and framework wiring for brs-to-spec v2. These files are what users actually interact with — they are the front door to the engine.

Read before writing:
- `.flow-engine/instructions/dispatcher.md` — the prompts call this
- `.brs2spec2/agent-instructions.md` once it is written — it defines session startup
- `.brs2spec/agent-instructions.md` — the v1 equivalent to port structure from
- `CLAUDE.md` — must be updated to reference v2 alongside v1

---

## File 1: `.brs2spec2/prompts/dispatch-next.md`

This is what the user pastes into Claude Code chat (or tells Claude to execute) when they want to run one event. It must be completely self-contained — the user should not need to know anything about the engine to use it.

Write it as a user-facing instruction with these characteristics:
- Short preamble: "You are running one BRS-to-Spec v2 event"
- Tells Claude to read `.flow-engine/instructions/dispatcher.md` first
- Tells Claude the active initiative workspace (either from user context or to scan `initiatives/`)
- Instructs Claude to follow the full 21-step dispatch sequence exactly once
- Instructs Claude to stop after one event and report:
  - Which event was executed (EVT-NNNNN, title)
  - Which persona ran
  - Which artifacts were written
  - Pass or fail result
  - If failed: the failure_reason and any decision raised
  - If passed: which events were created in pending/
  - What to run next: "Say 'dispatch-next' to run the next event, or 'dispatch-all' to run until blocked"

Format: simple markdown, readable at a glance. Should fit in a single screen.

---

## File 2: `.brs2spec2/prompts/dispatch-all.md`

This is the continuous execution entry point. Same structure as dispatch-next but instructs Claude to loop until blocked, done, or 50-event limit reached.

Include:
- Preamble: "You are running BRS-to-Spec v2 in continuous mode"
- Same dispatcher.md reference
- Loop instruction: after each event, return to step 2 of the dispatch sequence
- Stop conditions (from dispatcher.md Section 7) — list them briefly so the user understands when Claude will stop
- 50-event runaway guard: "If 50 events complete without stopping, stop and report the event count and queue state"
- End-of-run report format:
  - Total events executed
  - Events passed / failed
  - Artifacts produced
  - Events remaining in pending/ (blocked or new)
  - Open decisions count (blocking vs non-blocking)
  - Recommended next action

---

## File 3: `.brs2spec2/agent-instructions.md`

This is the session startup file loaded by CLAUDE.md. It tells Claude what to do at the start of every session in a v2 initiative.

Structure (port and adapt from `.brs2spec/agent-instructions.md`):

**Section 1: Framework identification**
State clearly: this is brs-to-spec v2, operating on the flow engine. v1 (`.brs2spec/`) is separate.

**Section 2: Session startup sequence**
What to load at the start of every session:
1. Read `.flow-engine/instructions/dispatcher.md`
2. Read `.flow-engine/schemas/event-schema.yaml`
3. Identify the active initiative workspace
4. Read `.flow/state/workflow-state.json`
5. Report current state: current_stage, pending events, blocked events, failed events, open decisions

Do NOT load all persona files or all skill files at startup. Load only what the next event requires.

**Section 3: Bypass prevention**
Port the v1 bypass prevention rules, adapted for v2:
- `input/` is the only folder writable by users directly
- Everything outside `input/` is produced by framework events — never written directly
- Never write to `.flow/state/` files in persona mode
- Never skip the result file step
- Never instantiate events that are not in the event template library

**Section 4: Trigger-to-action mapping**
What to do when the user says specific things:

| User says | Action |
|---|---|
| "dispatch-next" / "run next event" / "next" | Execute dispatch-next.md |
| "dispatch-all" / "run all" / "continue" | Execute dispatch-all.md |
| "status" / "what's the state?" | Read workflow-state.json and report current state |
| "show queue" / "what's pending?" | List pending/ events with blocked/unblocked status |
| "show decisions" / "open decisions" | Read open-decisions.md and summarize |
| "@orchestrator" | Switch to orchestrator mode, read queue, report what's next |
| "initialize v2" / "init v2 initiative" | Run the scaffolding script for this initiative |

**Section 5: Hard rules (numbered)**
Write these as numbered hard rules — same pattern as v1's Hard Rules 1-7:

1. Never write to `.flow/state/` files in persona mode
2. Never move an event to `done/` without writing the result file first
3. Never execute `on_success` actions if validation failed
4. Never process more than one event at a time
5. Never instantiate an event template that doesn't exist in `.brs2spec2/workflow/event-templates/`
6. Never write to paths not listed in the event's `write_to` field
7. `dispatch-all` stops at 50 events — never override this limit

**Section 6: v1 / v2 coexistence**
Explain which to use:
- Initiatives with `state/workflow-state.json` but no `.flow/` folder → v1 (`.brs2spec/`)
- Initiatives with `.flow/` folder → v2 (`.brs2spec2/`)
- Do not mix v1 and v2 in the same initiative workspace

---

## File 4: CLAUDE.md update

Add a section to the existing `CLAUDE.md` for v2, after the existing v1 section. Do not remove v1 references.

Add:

```markdown
## BRS-to-Spec v2 (Flow Engine)

If the active initiative has a `.flow/` folder, it is a v2 initiative.

**Load at session start (v2 initiatives):**
1. `.brs2spec2/agent-instructions.md` — v2 behavioral rules and session startup
2. `.flow-engine/instructions/dispatcher.md` — event dispatch protocol

**User entry points:**
- `dispatch-next` — run one event
- `dispatch-all` — run until blocked or done (max 50 events)

**Hard stop — before writing any file outside `input/` in a v2 initiative:**
Follow the event queue. Do not write artifacts directly. Find the next event in `.flow/events/pending/` and execute it through the dispatcher.

**v1 / v2 coexistence:**
- No `.flow/` folder → v1 initiative, use `.brs2spec/`
- Has `.flow/` folder → v2 initiative, use `.brs2spec2/`
- Never mix v1 and v2 in the same initiative workspace
```

---

## File 5: Initiative scaffolding script update

Update `.brs2spec/tools/scripts/new_initiative.py` (or equivalent) to create the `.flow/` structure when scaffolding a new v2 initiative.

The script must create:

```
initiatives/<id>-<slug>/
  .flow/
    state/
      workflow-state.json         (initialized with initiative_id, initiative_slug, current_stage: "0-routing", event_counter: 0, artifacts: {})
      event-log.jsonl             (empty file — ready for append)
      open-decisions.md           (initialized with empty decisions list using open-decisions template)
    events/
      pending/
        EVT-00001-route-initiative.yaml    (instantiated from EVT-TPL-001)
      processing/                 (empty folder)
      done/                       (empty folder)
      failed/                     (empty folder)
```

The first event (EVT-00001) is instantiated from EVT-TPL-001 automatically at init — this is the only event created without an orchestrator dispatch cycle. It represents the starting state: the initiative exists, and the first thing to do is route it.

The `workflow-state.json` initial content:
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
  "artifacts": {
    "input/brs.md": {"status": "missing"}
  },
  "open_decisions": 0,
  "blocking_decisions": 0,
  "event_counter": 1
}
```

If the script already creates `state/` folder, add the `.flow/` structure alongside it, not instead of it (v1 and v2 coexist).

---

## Quality bar

- `dispatch-next.md` and `dispatch-all.md` must be usable without reading any other file — they are the user's only entry point
- `agent-instructions.md` must load correctly when referenced from CLAUDE.md
- The scaffolding script must produce a working v2 initiative that passes Slice 1 validation immediately after init
- CLAUDE.md update must not break v1 — the v1 section must remain unchanged
- The first pending event (EVT-00001) created by the script must be a valid YAML file conforming to event-schema.yaml
