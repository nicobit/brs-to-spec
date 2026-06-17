# Implementation Prompt — Phase 1: Dispatcher

**Target:** `.flow-engine/instructions/dispatcher.md`  
**Prerequisites:** All three schemas in `.flow-engine/schemas/` exist  
**Produces:** 1 file — the Claude entry point for the entire engine

---

## Context

You are writing the dispatcher — the single most important file in the flow engine. It is the file Claude reads when the user says "run the next event" or "dispatch-next". Everything else in the engine depends on this file being correct, complete, and unambiguous.

Read these files before writing:
- `.flow-engine/schemas/event-schema.yaml` — the event YAML contract
- `.flow-engine/schemas/event-result-schema.yaml` — the result file contract
- `.flow-engine/schemas/artifact-status-schema.yaml` — artifact status values

---

## What the dispatcher must do

The dispatcher is a Claude-readable instruction file, not code. It tells Claude exactly what to do when operating the event queue for a brs-to-spec v2 initiative.

Write it as a markdown instruction document with the following sections:

### Section 1: Identity and scope

State clearly:
- This file governs `dispatch-next` (one event) and `dispatch-all` (up to 50 events)
- The dispatcher operates on the active initiative workspace at `initiatives/<id>-<slug>/`
- Claude must follow this protocol exactly — no shortcuts, no inferred steps

### Section 2: Locate the initiative workspace

Before doing anything else, Claude must identify which initiative is active:
1. Check if the user specified an initiative path
2. If not, scan `initiatives/` for the most recently modified workspace
3. Confirm the workspace has `.flow/events/pending/` — if not, stop and tell the user the workspace is not initialized for v2

### Section 3: The 16-step dispatch sequence

Write the full dispatch sequence as numbered steps. Each step must be precise enough that Claude cannot misinterpret it. The sequence (adapt and expand from the architecture doc):

```
Step 1:  Read .flow-engine/instructions/event-execution-rules.md
Step 2:  Scan .flow/events/pending/ — list all .yaml files
Step 3:  If pending/ is empty → stop and report "No pending events. Queue is empty."
Step 4:  For each pending event file, read blocked_by and blocked_by_events fields
Step 5:  Check each blocked_by artifact: does it exist and have status accepted in workflow-state.json?
Step 6:  Check each blocked_by_events EVT-ID: is that event in done/?
Step 7:  Filter to unblocked events only. If none are unblocked → stop and report blocked events list.
Step 8:  Select the highest-priority unblocked event (priority: critical > high > normal > low; tie-break: lowest EVT-NNNNN)
Step 9:  Move the selected event file from pending/ → processing/
Step 10: Load skill_ref file (contains how to do the task)
Step 11: Load persona_ref file (contains role + quality standards) — default: .brs2spec2/personas/<persona>.md
Step 12: Load artifact_template_ref file if present (contains expected output shape)
Step 13: Read all files in read_from — skip files marked # OPTIONAL that do not exist; stop if any required_inputs are missing
Step 14: [PERSONA MODE] Execute the task — produce the write_to artifacts following the skill_ref instructions
Step 15: Write result file to .flow/events/processing/<event_id>-result.yaml (see event-result-schema.yaml)
Step 16: [VALIDATION] Evaluate must_include and validation_rules.natural_language against the produced artifacts
Step 17: [ORCHESTRATOR MODE] If validation passes:
         - Move event file and result file from processing/ → done/
         - Execute on_success actions (see Section 4)
         Step 18: [ORCHESTRATOR MODE] If validation fails:
         - Move event file and result file from processing/ → failed/
         - Execute on_failure actions (see Section 5)
Step 19: [ORCHESTRATOR MODE] Append one line to .flow/state/event-log.jsonl
Step 20: [ORCHESTRATOR MODE] Update .flow/state/workflow-state.json (see state-update-rules.md)
Step 21: For dispatch-next: stop. Report one-paragraph summary of what happened.
         For dispatch-all: increment event counter. If counter = 50, stop and report limit reached. Otherwise return to Step 2.
```

Note: steps renumber cleanly — adjust the numbering so they are sequential 1–21.

### Section 4: on_success actions (orchestrator mode)

Explain precisely how each on_success sub-field is executed:
- `create_events` — how to instantiate an event template from `.brs2spec2/workflow/event-templates/` into pending/, including how to assign the next EVT-NNNNN ID
- `update_state` — which fields in workflow-state.json to update and how
- `append_log` — the exact JSON structure to append to event-log.jsonl

### Section 5: on_failure actions (orchestrator mode)

Explain precisely how each on_failure sub-field is executed:
- `create_events` — same as on_success
- `raise_decision` — the exact format to append to open-decisions.md, including auto-generated DEC-AUTO-NNN ID

### Section 6: Mode switching rule

This is a critical rule — write it as a prominent callout:

> **Persona mode vs orchestrator mode are strictly separated.**
> Steps 14–15 run in persona mode: Claude adopts the persona from persona_ref, applies the skill from skill_ref, and produces the artifact.
> Steps 17–20 run in orchestrator mode: Claude acts as the orchestrator only, updating state, logs, and queue. The orchestrator does not re-enter persona mode during state updates.
> Claude must not update workflow-state.json, event-log.jsonl, or open-decisions.md while in persona mode.

### Section 7: Stop conditions

List every condition that causes dispatch to stop immediately (before or during execution):
- No pending events
- All pending events are blocked
- A required_input is missing and not marked OPTIONAL
- The processing/ folder already has a file (previous dispatch did not complete cleanly — instruct user to check)
- dispatch-all counter reaches 50
- A blocking open decision is raised during on_failure

For each stop condition: what to report to the user, and what (if anything) to do before stopping.

### Section 8: What Claude must never do

Explicit prohibition list:
- Never skip the result file step (step 15)
- Never update state files while in persona mode
- Never move an event to done/ without writing the result file first
- Never execute on_success if validation failed
- Never process more than one event at a time (processing/ must be empty before starting)
- Never invent events not defined in pending/ or instantiated from a template

---

## Quality bar

- The dispatcher must be self-contained: a Claude session that reads only this file and the schemas should be able to run a complete dispatch cycle without needing any other instructions
- Every step must be unambiguous — if two Claude sessions would interpret a step differently, rewrite it
- The mode-switching rule must appear visually prominent (box or callout)
- The stop conditions must be exhaustive — Claude should never encounter a situation not covered
