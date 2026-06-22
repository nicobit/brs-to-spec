# Implementation Prompt — Slice 1 End-to-End Validation

**When to run:** After Phase 1 (engine) and Slice 1 skills are built, before writing any further event templates  
**Gate:** Do not proceed to Slice 2 (EVT-TPL-002 and beyond) until this validation passes completely  
**Produces:** Confidence that the full dispatch lifecycle works end-to-end on a real initiative

---

## What you are validating

Slice 1 covers one event: EVT-TPL-001 (ROUTE_INITIATIVE). This is the simplest possible event — no domain complexity, no blocked_by dependencies, single write_to artifact. If the engine cannot complete this event cleanly, nothing else will work.

You are validating:
1. Initiative scaffolding creates a valid v2 workspace
2. The dispatcher reads and executes the event correctly
3. The result file is written in the correct schema
4. Validation runs and produces the correct pass/fail outcome
5. Orchestrator mode updates all three state files correctly
6. The chained event (EVT-TPL-002) appears in pending/ after success
7. The failure path works when validation is deliberately forced to fail

---

## Setup

Before running:
1. Create a test initiative using the scaffolding script: `python .brs2spec/tools/scripts/new_initiative.py test-001 slice1-validation-test`
2. Verify the workspace has `.flow/events/pending/EVT-00001-route-initiative.yaml`
3. Verify `.flow/state/workflow-state.json` exists with `current_stage: "0-routing"` and `event_counter: 1`
4. Add a minimal `input/brs.md` — it just needs to exist with enough content to route. Use this:

```markdown
# BRS — Slice 1 Validation Test

## Objectives
- Test that the flow engine routing event works end-to-end

## Functional Requirements
FR-001: The system shall route initiatives correctly
FR-002: The system shall produce a routing decision document
FR-003: The system shall chain the next event on success
FR-004: The system shall record the event in the event log
FR-005: The system shall update workflow-state.json after completion

## Scope
Single-service, single-team change. Fewer than 5 meaningful FRs. Standalone delivery mode expected.
```

---

## Test A — Happy path (dispatch-next, expected: pass)

Run: `dispatch-next` (or tell Claude to execute `.brs2spec2/prompts/dispatch-next.md`)

**Check after execution — all of these must be true:**

### Queue state
- [ ] `pending/EVT-00001-route-initiative.yaml` no longer exists
- [ ] `processing/` is empty
- [ ] `done/EVT-00001-route-initiative.yaml` exists
- [ ] `done/EVT-00001-result.yaml` exists

### Result file (`done/EVT-00001-result.yaml`)
- [ ] `event_id: EVT-00001`
- [ ] `status: pass`
- [ ] `completed_at` is a valid ISO-8601 datetime
- [ ] `artifacts_written` contains `state/routing-decision.md`

### Artifact (`state/routing-decision.md`)
- [ ] File exists and is not empty
- [ ] Contains `delivery_mode:` field with one of the four allowed values
- [ ] Contains `execution_mode:` field with one of the three allowed values
- [ ] Contains rationale for each decision
- [ ] No placeholder text (TBD / TODO / [fill in])
- [ ] Given the minimal BRS above: `delivery_mode` should be `Standalone` (fewer than 5 meaningful FRs, single-team)

### Event log (`state/event-log.jsonl`)
- [ ] Contains exactly one line
- [ ] Line parses as valid JSON
- [ ] `event_id: EVT-00001`
- [ ] `status: done`
- [ ] `type: ROUTE_INITIATIVE`
- [ ] `persona: orchestrator`
- [ ] `artifacts_written` matches result file

### Workflow state (`state/workflow-state.json`)
- [ ] `current_stage: "2-business-intake"` (updated by on_success)
- [ ] `last_completed_event: "EVT-00001"`
- [ ] `active_events` contains `"EVT-00002"` (or the next event ID)
- [ ] `event_counter: 2`
- [ ] `artifacts["state/routing-decision.md"].status: "accepted"`
- [ ] `artifacts["state/routing-decision.md"].produced_by: "EVT-00001"`

### Chaining (`pending/`)
- [ ] `pending/EVT-00002-create-business-intake-summary.yaml` exists
- [ ] File is valid YAML conforming to event-schema.yaml
- [ ] `blocked_by` contains `state/routing-decision.md`
- [ ] `event_id: EVT-00002`

**If any check fails:** fix the issue before running Test B. Do not proceed.

---

## Test B — Failure path (forced validation failure, expected: fail)

Reset the workspace: delete done/, failed/, processing/ contents. Move EVT-00001 back to pending/ (or re-scaffold).

Edit `.brs2spec2/skills/orchestrator/route-initiative.md` temporarily to instruct Claude to produce a routing-decision.md that is missing the `delivery_mode` field. (Alternatively: after execution, manually edit the produced routing-decision.md to remove `delivery_mode` before validation runs, then re-run validation only.)

The goal is to force a validation failure on the `delivery_mode is one of the four allowed values` rule.

**Check after execution — all of these must be true:**

### Queue state
- [ ] `failed/EVT-00001-route-initiative.yaml` exists
- [ ] `failed/EVT-00001-result.yaml` exists
- [ ] `processing/` is empty
- [ ] `pending/` does not contain EVT-00002 (chaining must not fire on failure)

### Result file (`failed/EVT-00001-result.yaml`)
- [ ] `status: fail`
- [ ] `failure_reason` is present and mentions the specific failing rule
- [ ] `artifacts_written` is an empty list (or contains the partial artifact path)

### Open decisions (`state/open-decisions.md`)
- [ ] Contains a new `DEC-AUTO-001` entry
- [ ] Entry includes the `question` from `on_failure.raise_decision`
- [ ] `blocking: true`
- [ ] `raised_by: EVT-00001`

### Workflow state (`state/workflow-state.json`)
- [ ] `failed_events` contains `"EVT-00001"`
- [ ] `current_stage` is still `"0-routing"` (not advanced)
- [ ] `blocking_decisions: 1`
- [ ] `artifacts["state/routing-decision.md"].status: "failed"` (if artifact was partially written)

### Event log (`state/event-log.jsonl`)
- [ ] Contains one line for EVT-00001 with `status: failed`
- [ ] `failure_reason` is present in the log line

**If any check fails:** fix the issue. Do not proceed to Slice 2.

---

## Slice 1 pass criteria

Slice 1 is complete when:
- [ ] Test A passes with all checks green
- [ ] Test B passes with all checks green
- [ ] No manual intervention was needed during either test (Claude followed the dispatcher protocol automatically)
- [ ] The workspace state after Test A is clean enough to serve as the starting point for Slice 2

Record the result in a brief note in `framework_enhancement/9/` — what passed, what needed fixing, and the date.

---

## If Slice 1 fails

Common failure modes and where to look:

| Symptom | Likely cause |
|---|---|
| Result file not written | Dispatcher step 15 not followed — check dispatcher.md mode-switching rule |
| Event not moved to done/ | Dispatcher missing the file move step — check dispatcher.md step 13/14 |
| event-log.jsonl not updated | Orchestrator mode not triggered — check state-update-rules.md |
| EVT-00002 not created in pending/ | on_success.create_events not executed — check dispatcher.md Section 4 |
| workflow-state.json not updated | State update rules not applied — check state-update-rules.md |
| Failure path does not write open-decisions.md | on_failure.raise_decision handler missing — check dispatcher.md Section 5 |
| Wrong delivery_mode in routing-decision.md | Skill file routing logic — check route-initiative.md selection rules |
