# Enhancement 12 — Direct Execution Mode (Feature Flag)

## Status: DESIGN ONLY — not implemented

---

## 1. Problem statement

v1 (`.brs2spec`) runs skills directly: the orchestrator reads `workflow-state.json`, picks the next persona skill, executes it, and writes the artifact — all in one continuous flow, no event queue. This is fast, low-overhead, and simple for the user.

v2 (`.brs2spec2`) introduced the event queue for auditability, retry, chaining, and external call support. But it has higher token cost per step (loading engine rule files, event files, result files, state files on every dispatch) and more cognitive overhead for the user.

The goal is: v2 keeps the event model as its foundation but offers a **direct execution mode** that skips the queue mechanics and behaves like v1 — while reusing all of v2's skills, personas, artifact templates, validation rules, and **the same prompt files**.

---

## 2. What v1 actually does (the direct model)

```
1. Read workflow-state.json → detect current stage
2. Select next persona + skill based on stage
3. Load persona file + skill file
4. Read required inputs (BRS, prior artifacts)
5. Execute skill → produce artifact content
6. Write artifact to disk
7. Update workflow-state.json
8. Loop to step 1
```

No event files. No pending/processing/done/failed folders. No result files. No dispatcher steps 1–21. The orchestrator IS the dispatcher.

Token cost per step: skill file + persona file + inputs + generation. No engine rule files, no event YAML, no result YAML.

---

## 3. Design: `flow_mode` feature flag

### 3.1 Where the flag lives

In `workflow-state.json`, a new top-level field:

```json
{
  "flow_mode": "event"
}
```

| Value | Behaviour |
|---|---|
| `event` | Current v2 behaviour — full event queue, dispatcher 21 steps (default) |
| `direct` | New — orchestrator runs skills sequentially without event queue |

Default is `event` — no change to existing initiatives. Only initiatives that explicitly set `flow_mode: direct` use the new path.

Set at `new initiative` or `restart` time. Immutable for the life of an initiative — restart resets it.

---

## 4. Shared prompt architecture

### 4.1 Core principle

`dispatch-next.md` and `dispatch-all.md` remain **single files** handling both modes. There is no `direct-run.md`. The flag is read at Step 0 of each prompt and routes the agent into the correct branch. Everything after the branch point — validation, state update, report format, stop conditions, hard rules — is shared.

**Why shared prompts, not separate files:**
- Every fix to the report format, no-menu rule, or stop conditions applies once and propagates to both modes automatically
- No risk of the two files drifting apart over time
- The user sees and learns nothing different — same commands, same output format
- The branch point is shallow (steps 1–15 differ; steps 16–21 are identical)

### 4.2 Structure of `dispatch-next.md` (revised)

```
## Step 0 — Read flow_mode

Read .flow/state/workflow-state.json.
Check flow_mode field.

If flow_mode = "event"  → YOU ARE IN EVENT MODE.  Follow EVENT BRANCH steps 1–15 below.
If flow_mode = "direct" → YOU ARE IN DIRECT MODE. Follow DIRECT BRANCH steps D1–D10 below.
If flow_mode is absent  → treat as "event" (backward compatibility).

Do not mix steps from both branches. Once you enter a branch, stay in it until Step 16.

---

## EVENT BRANCH — steps 1–15
[current dispatcher steps 1–15, unchanged]

---

## DIRECT BRANCH — steps D1–D10

### Step D1 — Load skill-sequence.yaml

Read .brs2spec2/workflow/skill-sequence.yaml.
Find the sequence for this initiative's delivery_mode + execution_mode.
If not found → stop: "No skill sequence defined for [delivery_mode] / [execution_mode]."

### Step D2 — Find next skill

Read last_completed_skill from workflow-state.json.
Find the entry after last_completed_skill in the sequence.
If last_completed_skill is null → start from the first entry.
If no entry follows → stop: "Skill sequence complete — initiative done."

### Step D3 — Load skill and persona

Read the skill file at skill_ref.
Read the persona file at persona_ref.
Read the event template at template_ref (for must_include, validation_rules,
required_inputs, optional_inputs, digest_rules).

### Step D4 — Check required inputs

For each path in required_inputs: verify the file exists and is not empty.
If any required input is missing → write to open-decisions.md, update
workflow-state.json open_decisions count, stop:
"Required input missing: [path]. Resolve before re-running."

### Step D5 — Read optional inputs

For each path in optional_inputs: read if present, skip silently if not.

### Step D6 — Execute skill (persona mode)

Adopt the persona from persona_ref. Apply the skill from skill_ref.
Produce the artifact content for write_to.
If digest is declared in template_ref outputs.digest: also produce the digest content.
Do NOT update workflow-state.json or open-decisions.md in this step.

### Step D7 — Validate

For each must_include item: verify it is satisfied in the produced content.
For each validation_rules.natural_language rule: evaluate against produced content.
If any check fails → set result to FAIL. Record which checks failed.

### Step D8 — Write artifacts

If result is PASS:
  Write artifact to write_to path.
  If digest declared: write digest to outputs.digest path.
If result is FAIL:
  Do not write the artifact.
  Write a one-line failure note to .flow/state/run-log.md.
  Stop.

### Step D9 — Update state (orchestrator mode)

Update workflow-state.json:
  - artifact_status.<write_to>.status: "ai_validated" (pass) or "failed" (fail)
  - artifact_status.<write_to>.produced_by: <skill_ref stem>
  - artifact_status.<write_to>.last_updated: <now ISO-8601>
  - last_completed_skill: <skill_ref stem> (pass only)
  - current_stage: update if this skill's template_ref declares a stage change
  - open_decisions / blocking_decisions: recount from open-decisions.md

Append one line to .flow/state/run-log.md:
  [<timestamp>] <skill_ref stem> — PASS/FAIL — <write_to>

### Step D10 — WAIT_HUMAN check

If the next skill in the sequence has event_type WAIT_HUMAN in its template_ref:
  Present the gate using the same format as EVENT BRANCH Step 6a.
  Stop (dispatch-all must stop here too).
  Wait for "approved" or "rejected: <reason>" before continuing.

---

## Steps 16–21 — SHARED (both branches converge here)

### Step 16 — Finalize result

[shared — same as current dispatcher Step 16]

### Step 17 — Move files (event mode only)

If flow_mode = "event": move event and result files to done/ or failed/ as today.
If flow_mode = "direct": skip — no event files exist.

### Step 18 — Chain next events / update state (event mode only)

If flow_mode = "event": execute on_success / on_failure as today.
If flow_mode = "direct": skip — sequencing is handled by skill-sequence.yaml.

### Step 19 — State update

If flow_mode = "event": follow current Step 19.
If flow_mode = "direct": already done in Step D9. Skip.

### Step 20 — Report (SHARED — identical for both modes)

Write the fixed-format summary. Nothing else.

Event mode:
  Event:    EVT-NNNNN — <task.title>
  Persona:  <persona>
  Result:   PASS / FAIL
  Artifacts written: [list]
  [If PASS] Next events queued: [list or "none"]
  [If FAIL] Failure reason: <reason>
  [If FAIL] Decision raised: <DEC-AUTO-NNN if raised>

Direct mode:
  Skill:    <skill_ref stem> — <task.title>
  Persona:  <persona>
  Result:   PASS / FAIL
  Artifact: <write_to path>
  Next:     <next skill in sequence> or "sequence complete"
  [If FAIL] Failure reason: <reason>

HARD RULE — applies to BOTH modes:
Do NOT add any text after this summary. Do NOT offer choices. Do NOT ask
"which should I do?". Do NOT suggest next steps. Do NOT offer to auto-dispatch.
The user controls dispatch by typing dispatch-next, dispatch-all, or approved/rejected.

### Step 21 — Continue or stop (SHARED)

dispatch-next: stop after Step 20.
dispatch-all: loop to Step 0 (re-read flow_mode each iteration). Stop at 50 iterations.
```

### 4.3 `dispatch-all.md` (revised)

Same Step 0 branch logic. Loops the correct branch up to 50 iterations. Stop conditions are the same for both modes: blocked input, WAIT_HUMAN gate, sequence complete, 50-iteration limit.

---

## 5. What is reused unchanged from v2

| Component | Reused? |
|---|---|
| All skill files (`.brs2spec2/skills/**`) | Yes — identical |
| All persona files (`.brs2spec2/personas/**`) | Yes — identical |
| All artifact templates (`.brs2spec2/artifact-templates/**`) | Yes — identical |
| Event templates — `must_include`, `validation_rules`, `required_inputs`, `optional_inputs`, `digest_rules` | Yes — read as reference, not dispatched |
| `dispatch-next.md` | Yes — shared, internal branch |
| `dispatch-all.md` | Yes — shared, internal branch |
| `restart.md` | Yes — gains flow_mode question at Step 1 |
| `new-initiative.md` | Yes — gains flow_mode question at Step 1 |
| `agent-instructions.md` trigger table | Yes — no new rows; dispatch-next/all already listed |
| `open-decisions.md` format | Yes — identical |
| WAIT_HUMAN gate format | Yes — identical |
| Step 20 report hard rules | Yes — identical |
| Digest support (Enhancement 11) | Yes — template_ref provides digest_rules in both modes |

## 6. What is skipped in direct mode

| Component | Skipped |
|---|---|
| `.flow/events/` folder (pending/processing/done/failed) | Not created |
| Engine rule files (5 files loaded at Event Branch Step 1) | Not loaded |
| Event YAML files | Not written |
| Result YAML files | Not written |
| `event-log.jsonl` | Replaced by `run-log.md` (human-readable, one line per skill) |
| `active_events`, `blocked_events`, `event_counter` in workflow-state.json | Not present |
| `blocked_by` evaluation | Not performed — sequencing is linear |
| `on_success` / `on_failure` chaining | Not performed — sequencing is defined by skill-sequence.yaml |
| External calls — Enhancement 10 | Not supported (no CALL_EXTERNAL event type in direct mode) |

---

## 7. Direct mode workspace structure

```
initiatives/<id>-<slug>/
  input/                              (same as event mode)
  routing/                            (same artifact folders, written directly)
  business-intake/
  business-analysis/
  planning/
  ...
  .flow/
    state/
      workflow-state.json             (simplified — no event fields, has last_completed_skill)
      open-decisions.md               (same format as event mode)
      run-log.md                      (replaces event-log.jsonl — human-readable)
    (no events/ folder)
```

`workflow-state.json` in direct mode — simplified schema:

```json
{
  "initiative_id": "I006-my-app",
  "initiative_slug": "my-app",
  "created": "2026-06-14",
  "flow_mode": "direct",
  "current_stage": "0-routing",
  "delivery_mode": "OpenSpec",
  "execution_mode": "Enterprise+Modular",
  "project_type": "greenfield",
  "last_completed_skill": null,
  "open_decisions": 0,
  "blocking_decisions": 0,
  "last_updated": "2026-06-14T16:00:00Z",
  "artifacts": {}
}
```

---

## 8. New file: `.brs2spec2/workflow/skill-sequence.yaml`

The only genuinely new content required by this enhancement. Defines the ordered skill execution sequence per `delivery_mode` + `execution_mode`. Derived from the `on_success.create_events` chain in event templates — no duplication of must_include or validation_rules (those are read from `template_ref` at runtime).

```yaml
# skill-sequence.yaml
# Direct mode execution order per delivery_mode + execution_mode.
# template_ref is read at runtime for must_include, validation_rules,
# required_inputs, optional_inputs, and digest_rules.
# Do not duplicate those fields here.

sequences:
  OpenSpec:
    Enterprise+Modular:
      - skill_ref: ".brs2spec2/skills/orchestrator/route-initiative.md"
        persona: orchestrator
        template_ref: EVT-TPL-001
        write_to: "routing/routing-decision.md"

      - skill_ref: ".brs2spec2/skills/product-owner/create-business-intake-summary.md"
        persona: product-owner
        template_ref: EVT-TPL-002
        write_to: "business-intake/business-intake-summary.md"

      - skill_ref: ".brs2spec2/skills/product-owner/create-business-rules.md"
        persona: product-owner
        template_ref: EVT-TPL-003
        write_to: "business-intake/business-rules.md"

      - skill_ref: ".brs2spec2/skills/product-owner/create-actors-and-personas.md"
        persona: product-owner
        template_ref: EVT-TPL-004
        write_to: "business-analysis/actors-and-personas.md"

      - skill_ref: ".brs2spec2/skills/product-owner/find-gaps-and-questions.md"
        persona: product-owner
        template_ref: EVT-TPL-005
        write_to: "business-intake/gaps-and-questions.md"

      - skill_ref: ".brs2spec2/skills/product-owner/create-process-flows.md"
        persona: product-owner
        template_ref: EVT-TPL-006
        write_to: "business-analysis/process-flows.md"

      - skill_ref: ".brs2spec2/skills/product-owner/create-use-case-specs.md"
        persona: product-owner
        template_ref: EVT-TPL-007
        write_to: "business-analysis/use-case-spec.md"

      # ... continues through all templates for this delivery_mode + execution_mode

    Standard:
      # Shorter sequence — fewer skills, same artifact paths

  Standalone:
    Enterprise+Modular:
      # Different sequence
    Standard:
      # Different sequence

  FastPath:
    Standard:
      # Minimal sequence
```

**Maintenance rule:** when a new event template is added to the workflow, `skill-sequence.yaml` must be updated to include it in the correct position for each affected sequence. The agent can be asked to "sync skill sequence from templates" to regenerate it.

---

## 9. Changes to `restart.md` and `new-initiative.md`

Both prompts gain one question at Step 1:

```
6. Flow mode — "event" (default, full audit trail) or "direct" (faster, lower token cost, no event files).
   Default: event.
   Choose "direct" for fast iteration, testing, or low-overhead runs.
   Choose "event" for audited initiatives, brownfield work, or when external integrations are needed.
```

If the user says "direct" or "fast mode" or "no event files": set `flow_mode: direct` in `workflow-state.json` and skip creating `.flow/events/` folders.

---

## 10. Token cost comparison

| | Event mode | Direct mode | Saving |
|---|---|---|---|
| Engine rule files loaded per dispatch | ~2,000 tokens (5 files) | 0 | ~2,000 |
| Event YAML read + written | ~300 tokens | 0 | ~300 |
| Result YAML written | ~200 tokens | 0 | ~200 |
| skill-sequence.yaml loaded | 0 | ~400 tokens (once per dispatch-all) | −400 |
| Per-skill net saving | — | — | **~2,100 tokens/skill** |
| Full OpenSpec Enterprise+Modular run (~12 skills) | — | — | **~25,000 tokens** |

The persona execution cost (reading BRS + prior artifacts + generating content) is identical in both modes — it is the unavoidable cost. The saving is entirely in framework overhead.

Combined with Enhancement 11 (digests), estimated total saving on a full run: **~50,000–65,000 tokens**.

---

## 11. Files to create/modify when implementing

| File | Action | Notes |
|---|---|---|
| `.brs2spec2/workflow/skill-sequence.yaml` | **CREATE** | Only genuinely new content — ordered skill list per mode |
| `.brs2spec2/prompts/dispatch-next.md` | **MODIFY** | Add Step 0 branch; add DIRECT BRANCH steps D1–D10; Steps 17–19 get mode guards; Step 20 gets dual report format |
| `.brs2spec2/prompts/dispatch-all.md` | **MODIFY** | Add Step 0 branch; loop routes on flow_mode |
| `.brs2spec2/prompts/restart.md` | **MODIFY** | Add flow_mode question; skip events/ folder when direct |
| `.brs2spec2/prompts/new-initiative.md` | **MODIFY** | Add flow_mode question; skip events/ folder when direct |
| `.brs2spec2/agent-instructions.md` | **MODIFY** | Section 2: startup reads flow_mode and reports it in status; no trigger table changes needed |
| `.flow-engine/schemas/workflow-state-schema.yaml` | **MODIFY** | Add `flow_mode` (enum: event, direct); add `last_completed_skill` (string, nullable) |

---

## 12. Open questions before implementation

1. **skill-sequence.yaml sync** — who is responsible for keeping it in sync with event templates? Proposed: the agent regenerates it on request ("sync skill sequence"); a note in the template header reminds maintainers to update it when adding templates.
2. **Parallel skills in direct mode** — event mode supports parallel unblocked events; direct mode is strictly sequential. Acceptable for v1 of this enhancement. Parallel direct mode is a future enhancement.
3. **Migration between modes** — can an initiative switch `flow_mode` mid-run? Proposed: no — immutable for the life of an initiative. Restart to change mode (backup is preserved in `.flow/backups/`).
4. **Enhancement 10 (external calls) in direct mode** — CALL_EXTERNAL is event-mode only. If a skill sequence entry has `event_type: CALL_EXTERNAL` in its template_ref, direct mode skips it with a warning in run-log.md rather than failing. User is notified to switch to event mode for that capability.
