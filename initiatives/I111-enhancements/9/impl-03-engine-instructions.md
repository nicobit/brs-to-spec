# Implementation Prompt — Phase 1: Engine Instruction Files

**Target:** `.flow-engine/instructions/` (4 files)  
**Prerequisites:** `dispatcher.md` exists; all schemas exist  
**Produces:** `event-execution-rules.md`, `artifact-ownership.md`, `state-update-rules.md`, `validation-rules.md`

---

## Context

You are writing four instruction files that support the dispatcher. The dispatcher references these files — it tells Claude to read `event-execution-rules.md` at step 1, and applies `state-update-rules.md` during orchestrator mode. Write them in order; each builds on the previous.

Read first:
- `.flow-engine/instructions/dispatcher.md`
- `.flow-engine/schemas/event-schema.yaml`
- `.flow-engine/schemas/event-result-schema.yaml`
- `.flow-engine/schemas/artifact-status-schema.yaml`

---

## File 1: `event-execution-rules.md`

This file governs how Claude behaves during Steps 10–16 of the dispatch sequence (loading refs, reading inputs, executing, writing result). It is the operational rulebook for event execution.

Write it with these sections:

**1. Loading order**
The exact order in which to load skill_ref, persona_ref, and artifact_template_ref, and what to do if any are missing:
- `skill_ref` missing → stop, move event to failed/, write result with failure_reason: "skill_ref not found"
- `persona_ref` missing → use default: `.brs2spec2/personas/<persona>.md` derived from the `persona` field
- `artifact_template_ref` missing → proceed without template (template is optional)

**2. Reading inputs**
Rules for reading `read_from` files:
- Read in list order
- Files without `# OPTIONAL` comment are required: if missing, stop and move to failed/
- Files with `# OPTIONAL` comment: skip silently if they don't exist, note in result file
- Glob patterns (e.g. `input/brs/*.md`): read all matching files
- Never read files outside the initiative workspace unless explicitly in skill_ref

**3. Execution constraints**
Rules Claude must follow while in persona mode:
- Adopt the persona's role and quality standards from persona_ref
- Follow skill_ref instructions exactly for this task type
- Use artifact_template_ref as the output structure contract
- Write only to the paths listed in `write_to` — never write to other paths
- Do not update any `.flow/` state files during execution
- Do not read files not listed in `read_from` (except skill_ref, persona_ref, artifact_template_ref)
- If the task requires information not available in read_from files: add a note to the result file, do not invent content

**4. Result file requirements**
What the result file must contain before validation begins:
- `event_id` matching the event being processed
- `status: pass` (tentative — may be changed to `fail` after validation)
- `completed_at` — current datetime
- `artifacts_written` — list of every file written during execution
- Any `open_decisions_raised` if the skill raised decisions during execution

**5. What "done" means for each event type**
Per event type from the registry, what constitutes a complete execution:
- `CREATE_ARTIFACT` — write_to file exists and is not empty/stub-only
- `UPDATE_ARTIFACT` — write_to file exists and has changed from its state before execution
- `VALIDATE_ARTIFACT` — no new file required; result file must include a pass/fail judgement on the artifact reviewed
- `REVIEW_ARTIFACT` — at least one finding document written to write_to
- `RAISE_DECISION` — at least one entry written to state/open-decisions.md
- `RESOLVE_DECISION` — the referenced decision entry in open-decisions.md has been updated with resolution
- `GENERATE_HANDOFF` — all write_to paths exist (dependency graph + all story folders)
- `ENRICH_ARTIFACT` — write_to file exists and the specific sections listed in must_include are present
- `REPAIR_ARTIFACT` — write_to file exists and the validation_rules that previously failed now pass
- `ROUTE_INITIATIVE` — write_to (routing-decision.md) exists with delivery_mode and execution_mode fields populated
- `RETRY_FAILED_TASK` — treat as the original event type of the failed event being retried

---

## File 2: `artifact-ownership.md`

This file defines which persona owns each artifact category and what happens when two events try to write the same artifact.

Write it with these sections:

**1. Ownership table**
A table mapping artifact path patterns to owning personas. Cover all major artifact categories:

| Artifact path pattern | Owner persona | Notes |
|---|---|---|
| `input/*` | human | Never overwritten by framework |
| `state/routing-decision.md` | orchestrator | |
| `state/workflow-state.json` | orchestrator | |
| `state/event-log.jsonl` | orchestrator | |
| `state/open-decisions.md` | orchestrator | |
| `business-intake/*` | product-owner | |
| `business-analysis/actors-and-personas.md` | product-owner | |
| `business-analysis/process-flows.md` | product-owner | |
| `business-analysis/use-case-spec.md` | product-owner | |
| `business-analysis/entity-model.md` | architect | |
| `architecture/*` | architect | |
| `planning/delivery-structure.md` | delivery-lead | |
| `planning/software-modules.md` | delivery-lead | |
| `planning/capability-to-module-map.md` | delivery-lead | |
| `planning/delivery-increments.md` | delivery-lead | |
| `planning/traceability-matrix.md` | delivery-lead | |
| `quality-gates/bdd/*` | qa-analyst | |
| `quality-gates/test-strategy.md` | qa-analyst | |
| `quality-gates/test-plans/*` | qa-analyst | |
| `quality-gates/security-review.md` | security-reviewer | |
| `quality-gates/threat-model.md` | security-reviewer | |
| `quality-gates/data-contract.md` | security-reviewer | |
| `quality-gates/api-contract.md` | engineering-lead | |
| `quality-gates/event-contract.md` | engineering-lead | |
| `quality-gates/observability-plan.md` | engineering-lead | |
| `engineering-readiness/*` | engineering-lead | |
| `specs/*` | engineering-lead | |
| `standalone-delivery/*` | engineering-lead | |
| `review-package/*` | delivery-lead | |
| `perspectives/*` | delivery-lead | |

**2. Write conflict rule**
If an event tries to write to an artifact owned by a different persona:
- If the event type is `UPDATE_ARTIFACT` or `ENRICH_ARTIFACT`: allowed, but the result file must note the cross-persona write
- If the event type is `CREATE_ARTIFACT`: stop, move to failed/, failure_reason: "artifact owned by <owner>, use UPDATE_ARTIFACT or ENRICH_ARTIFACT type"
- If the artifact is in `state/` or `input/`: stop unconditionally — these paths have absolute ownership

**3. Shared artifact rule**
Some artifacts are read by many personas but written by one. List the most important shared artifacts and who may read vs write:
- `planning/delivery-structure.md` — written by delivery-lead; read by all personas during quality gates and handoff
- `architecture/architecture-rules.md` — written by architect; read by engineering-lead, qa-analyst, reviewer
- `engineering-readiness/readiness-check.md` — written by engineering-lead; read by qa-analyst, security-reviewer, orchestrator

---

## File 3: `state-update-rules.md`

This file defines exactly what the orchestrator may update in each state file, and when.

Write it with these sections:

**1. The orchestrator-only rule**
State that only the orchestrator (Claude in orchestrator mode, step 17–20 of dispatch) may write to:
- `.flow/state/workflow-state.json`
- `.flow/state/event-log.jsonl`
- `.flow/state/open-decisions.md`

Domain personas (product-owner, architect, etc.) must not write to these files. If a domain skill needs to raise a decision, it records it in the result file under `open_decisions_raised` — the orchestrator writes it to `open-decisions.md`.

**2. workflow-state.json update rules**
Specify exactly which fields may be updated and when:
- `current_stage` — updated when `on_success.update_state.current_stage` is set
- `last_completed_event` — set to the EVT-ID of the event that just completed successfully
- `active_events` — updated to reflect events now in processing/ or newly created in pending/
- `blocked_events` — updated when blocked_by check reveals blocked events
- `failed_events` — add EVT-ID when an event moves to failed/
- `artifacts.<path>.status` — update to `accepted` when a CREATE_ARTIFACT or UPDATE_ARTIFACT event passes validation; update to `failed` when it fails
- `artifacts.<path>.produced_by` — set to EVT-ID of the event that produced it
- `open_decisions` — count of non-resolved entries in open-decisions.md
- `blocking_decisions` — count of entries with `blocking: true` in open-decisions.md
- `event_counter` — increment by 1 on every successful event completion

Fields that must NEVER be updated by orchestrator:
- `initiative_id` — set at init, never changed
- `initiative_slug` — set at init, never changed
- `delivery_mode` / `execution_mode` — set by ROUTE_INITIATIVE event only

**3. event-log.jsonl append rules**
The exact JSON line format to append after every event (pass or fail):
```json
{
  "event_id": "EVT-NNNNN",
  "type": "EVENT_TYPE",
  "persona": "persona-name",
  "status": "done|failed",
  "completed_at": "ISO-8601",
  "artifacts_written": ["path1", "path2"],
  "failure_reason": "only present if status=failed"
}
```
Rule: append only — never rewrite or delete lines from event-log.jsonl.

**4. open-decisions.md update rules**
Format for a new decision entry raised by on_failure.raise_decision:
- Auto-assign ID as `DEC-AUTO-NNN` (increment from last DEC-AUTO entry in the file)
- Include: question, owner, blocking (true/false), raised_by (EVT-ID), raised_at (datetime)
- When a decision is resolved: add a `resolved_at` and `resolution` field to the entry — do not delete the entry

---

## File 4: `validation-rules.md`

This file defines how Claude applies the two validation layers from the event schema.

Write it with these sections:

**1. When validation runs**
Validation runs at step 16 of dispatch — after the result file is written, before deciding pass or fail. Validation is always done by Claude in orchestrator mode, never in persona mode.

**2. natural_language validation**
How Claude evaluates each natural_language rule:
- Read each rule as a plain-English assertion about the produced artifact(s)
- Read the artifact(s) listed in write_to
- For each rule: determine pass or fail based on the actual artifact content
- Record each result in `validation_notes` in the result file
- If all rules pass: set result `status: pass`
- If any rule fails: set result `status: fail`, populate `failure_reason` with the specific failing rule(s)

**3. must_include validation**
`must_include` entries are evaluated before `validation_rules.natural_language`. They are structural presence checks:
- Each must_include entry must be verifiable by reading the artifact
- If a must_include entry is not present: immediate fail, no need to check remaining validation_rules
- must_include failures go in `failure_reason` with prefix "Required content missing:"

**4. machine validation (v2.1 — not executed in v2.0)**
Document the named validators that will be implemented in v2.1. For each, describe what it will check:
- `no_placeholders` — scans artifact for strings: TBD, TODO, [fill in], PLACEHOLDER, [TBD]
- `id_pattern` — checks that every ID matching `args.pattern` regex appears in the artifact
- `traceability_links` — checks that every ID matching `args.from` pattern has at least one corresponding `args.to` pattern in the same row or section
- `markdown_table_required` — checks that at least one markdown table is present
- `status_field_required` — checks that a `Status:` field with a value from `args.allowed` is present in the artifact metadata

In v2.0: these validators are listed in the result file under `validation_notes` with status `skipped (v2.0)`.

**5. Validation failure handling**
When validation fails:
- Do not delete the artifact — leave it in place (it may be partially useful)
- Set result status to `fail`
- Populate `failure_reason` with specific rule names and what was found vs expected
- Move event to failed/ — the artifact path in workflow-state.json gets status `failed`
- Execute on_failure actions per dispatcher rules

---

## Quality bar

- All four files must be readable as standalone instruction documents — each is loaded individually by the dispatcher
- `event-execution-rules.md` must cover every event type from the registry
- `artifact-ownership.md` ownership table must cover every artifact path that exists in a v1 initiative workspace
- `state-update-rules.md` must specify the exact JSON fields and format — no ambiguity
- `validation-rules.md` must make the pass/fail decision deterministic — Claude applying these rules twice should reach the same result
