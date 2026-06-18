# Flow Engine — Dispatcher
# Version: 1.0
#
# This file governs dispatch-next (one event) and dispatch-all (up to 50 events).
# Read this file first. Follow every step exactly. Do not shortcut, infer, or skip.

---

## Scope

The dispatcher operates on one active initiative workspace at `initiatives/<id>-<slug>/`.
All paths in this document are relative to that workspace root unless stated otherwise.

**dispatch-next** — execute exactly one event, then stop and report.
**dispatch-all** — execute events sequentially until blocked, done, or 50-event limit reached.

---

## Engine flags (`workflow-state.json → engine_flags`)

Flags are read from `engine_flags` in `workflow-state.json`. All flags default to `false` if absent.

| Flag | Default | Effect |
|---|---|---|
| `chain_break_on_new_events` | `false` | When `true`: after Step 18 creates new downstream events in `pending/`, dispatch-all stops immediately instead of looping. The next dispatch-all picks up fresh. Prevents context-window shortcuts where the dispatcher writes bare runtime events without copying `must_include`/`validation_rules` from the template. Set to `true` for any initiative where artifact quality is a concern. |

---

## Step 0 — Locate the initiative workspace

Before step 1, identify the active initiative:

1. If the user specified a path, use it.
2. Otherwise scan `initiatives/` — select the workspace that has `.flow/events/pending/` and was most recently modified.
3. If no workspace has `.flow/events/pending/`, stop: **"No v2 initiative found. Run the scaffolding script to initialize a v2 initiative workspace."**
4. Confirm: read `.flow/state/workflow-state.json`. If it does not exist, stop: **".flow/state/workflow-state.json missing — workspace may be corrupted. Re-initialize with new_initiative.py --v2 or repair manually."**
5. **Set the initiative workspace root.** Record the full absolute path to the initiative workspace (e.g. `c:/Users/nicol/source/brs-to-spec/initiatives/I008-TEST4/`). Every relative path in every event file (`read_from`, `write_to`, `blocked_by`) resolves from this root — not from the repository root, not from the current working directory. When reading `input/brs.md`, the full path is `<workspace-root>/input/brs.md`. Apply this to every file operation in Steps 1–21.

---

## The dispatch sequence — 21 steps

### Step 1 — Load all engine instruction files

Read all five engine rule files before scanning the queue. All of them govern execution; loading only some risks partial rule application.

```
.flow-engine/instructions/event-execution-rules.md          — persona mode behaviour (steps 11–14)
.flow-engine/instructions/artifact-ownership.md             — engine-protected paths and write-conflict rules
.flow-engine/instructions/state-update-rules.md             — which fields orchestrator may update
.flow-engine/instructions/validation-rules.md               — how must_include and natural_language rules are evaluated
.flow-engine/instructions/template-instantiation-rules.md   — how templates become runtime events (step 18)
```

The domain ownership table (`.brs2spec2/workflow/artifact-ownership.md`) is loaded on demand at Step 9b, not here. Loading it here would couple the generic engine to the domain layer.

If any of these files does not exist → stop: **"Engine rule file missing: [path]. Engine is misconfigured — do not attempt dispatch."**

### Step 2 — Scan the queue

List all `.yaml` files in `.flow/events/pending/`.

If the folder is empty:

Check `current_stage` in `.flow/state/workflow-state.json`.

If `current_stage` is `5-handoff` → stop: **"Queue empty — initiative complete. All stages finished. Say 'archive done' to move completed event files to .flow/events/archive/ and free up space."**

If `current_stage` is anything earlier than `5-handoff`:

Determine the minimum required artifacts for the initiative's `delivery_mode` and `execution_mode`:

| delivery_mode | Minimum artifacts required before queue may be empty |
|---|---|
| OpenSpec | `specs/` (or equivalent handoff folder) |
| Standalone | `standalone-delivery/` |
| FastPath | `handoff/compact-handoff-summary.md` |
| BusinessCopilot | `planning/delivery-structure.md` |

Check whether the minimum artifact exists in `artifacts` map with `status: accepted`.

If it does not exist → **auto-repair: do not stop, do not ask the user**. Execute the following inline chain-repair procedure exactly:

**Inline chain-repair procedure (Step 2 — empty queue, not complete):**

1. Read `last_completed_event` from `workflow-state.json`. This is the EVT-ID whose `on_success` chain should have created downstream events.
2. Find the event file for that EVT-ID in `.flow/events/done/`. Read it. If missing → stop: **"done/EVT-NNNNN-*.yaml for last_completed_event not found. done/ may be corrupted."**
3. Locate the template for this event using the following priority:
   a. **Primary:** Read `meta.template_id` from the runtime event file (e.g. `EVT-TPL-001`). Load `.brs2spec2/workflow/event-templates/EVT-TPL-NNN-*.yaml`. If found → proceed to step 4.
   b. **Fallback (meta.template_id absent or file missing):** Read the `action` field from the runtime event file. Scan `.brs2spec2/workflow/event-templates/` for a template whose filename or `type` field matches the action (e.g. action `route_initiative` → `EVT-TPL-001-route-initiative.yaml`). If exactly one match found → use it, proceed to step 4.
   c. **If no match found after both attempts:** Do NOT ask the user. Stop with: **"Chain-repair could not locate template for [EVT-ID] (action: [action], meta.template_id: [value or absent]). Add meta.template_id to the done event file manually, then re-run dispatch-next."**
4. Read `on_success.create_events` from the **template** (not the runtime event). This is the authoritative list of what must be created next.
5. For each template reference in `on_success.create_events`:
   a. Check whether a runtime event with `meta.template_id` matching this template already exists in `done/`, `failed/`, or `pending/`. If yes → skip (already created).
   b. If no → this event is missing. Instantiate it: follow the full field mapping in `template-instantiation-rules.md` section 2. Increment `event_counter`. Set `meta.notes` to `"Auto-instantiated by dispatcher chain-repair from [last_completed_event] on_success"`. Write to `pending/`.
6. After all missing events are instantiated, update `workflow-state.json`: `active_events`, `event_counter`, `last_updated`.
7. Re-scan `pending/`. If still empty → stop: **"Chain repair ran but queue is still empty. Last completed event: [EVT-ID], template: [EVT-TPL-NNN], on_success.create_events: [list]. Manual intervention required."**
8. If at least one event is now in `pending/` → continue to Step 3 normally. Do NOT report the repair to the user.

**Critical constraint:** Only instantiate templates listed in `on_success.create_events` of the last completed event's template. Do NOT invent additional events, do NOT guess what "should" come next based on stage or domain knowledge. The chain is defined exclusively by the template's `on_success`.

If it does exist → stop: **"Queue empty — initiative complete."**

### Step 3 — Check processing folder

**Step 3a — Integrity check (script-enforced):**

Run:
```
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> check-integrity
```

Read `.flow/state/integrity-check.yaml`. This file is the authoritative integrity report — do not proceed if it is missing or malformed.

- If `overall: fail` and `orphan_results` is non-empty: stop dispatch immediately:
  **"Integrity check failed: [N] result file(s) in done/ have no matching event file. These were produced outside the dispatcher. See .flow/state/integrity-check.yaml. Resolve before continuing: delete the orphan result file and artifact, reset the event to pending, and re-run dispatch-next."**

- If `overall: fail` and `missing_result_files` is non-empty: stop dispatch immediately.
  For each entry:
  - If `has_embedded_result: true`: **"Integrity check failed: [event_id] ([event_file]) in done/ has a result: block embedded inside the event file — dispatcher Step 16-G was bypassed. The event was self-declared as passing without validation. Resolution: delete the event file from done/, remove the artifact it claims to have written, move a clean copy of the event (without result: block) to pending/, update workflow-state.json active_events and artifact_status, then re-run dispatch-next."**
  - If `has_embedded_result: false`: **"Integrity check failed: [event_id] ([event_file]) in done/ has no corresponding result file — Steps 15–17 were not executed. Resolution: move the event file back to pending/ and re-run dispatch-next."**
  List all violations before stopping. Do not proceed until all missing_result_files entries are resolved.

- If `overall: fail` and `embedded_results` is non-empty: stop dispatch immediately.
  For each entry: **"Integrity check failed: [event_id] ([event_file]) has a result: block embedded in the event file alongside a separate result file. The event file must not contain a result: block — remove the result: key from the event file and re-run dispatch-next."**

- If `overall: warn`: log the warning but continue.
- If `overall: pass`: continue.

If `.flow/events/processing/` contains any files, run the full **silent auto-repair** — do not stop, do not ask the user:

For each event file `EVT-NNNNN-<slug>.yaml` (no `-result` suffix) found in `processing/`, apply this classification and recovery:

| Condition | Recovery action |
|---|---|
| Event AND result both exist in `done/` | Completed in a previous session — delete stale copies from `processing/` silently |
| Event exists in `failed/` | Already failed and recorded — delete stale copies from `processing/` silently |
| Event NOT in `done/` or `failed/`, result file in `processing/` with `status: pass` | Step 17 did not finish — move event and result to `done/` |
| Event NOT in `done/` or `failed/`, result file in `processing/` with `status: fail` | Step 17 did not finish — move event and result to `failed/` |
| Event NOT in `done/` or `failed/`, NO result file in `processing/` | Interrupted before Step 15 — move event back to `pending/` for re-execution |

After applying all recovery actions, also purge orphan duplicates from `pending/`: for each file in `pending/` whose EVT-ID already exists in `done/` or `failed/`, delete the `pending/` copy silently.

After repair, if `processing/` is empty → continue to Step 4 normally. No report to the user.

If `processing/` is still non-empty after repair (unexpected — should not happen) → stop: **"Processing/ repair failed unexpectedly. Files remaining: [list]. Manual inspection required."**

### Step 4 — Evaluate blocked_by for each pending event

For each pending event file:

a. Read the event YAML.
b. Check `blocked_by` (list of artifact paths): for each path, look up its status in `.flow/state/workflow-state.json → artifacts`. The event is unblocked only if every `blocked_by` artifact has `status: accepted` OR `status: ai_validated`. Both statuses satisfy blocked_by checks. Any other status (draft, failed, stale, missing, blocked) does NOT satisfy the check.
c. Check `blocked_by_events` (list of event references). Each entry may be either:
   - a runtime EVT-ID (`EVT-NNNNN`) — satisfied when a file named `EVT-NNNNN-*.yaml` exists in `.flow/events/done/`
   - a template reference (`EVT-TPL-NNN`) — satisfied when any event file in `.flow/events/done/` has `meta.template_id` equal to that template reference
   The event is unblocked only if all listed references are satisfied.
d. If `blocked_by` and `blocked_by_events` are both empty or absent → the event is unblocked.

### Step 4a — Confirm events are runtime events, not templates

Before evaluating blocked_by, confirm every pending event file is a **runtime event**, not a raw template.

A file is a runtime event if it has `event_id: EVT-NNNNN` (five-digit numeric ID).
A file is a template if it has `event_template_id: EVT-TPL-NNN`.

If any file in `pending/` has `event_template_id` instead of `event_id`:
- Do not execute it
- Move it to `failed/` with a note: `"Template file found in pending/ — templates must be instantiated before dispatch. See template-instantiation-rules.md."`
- Continue evaluating remaining files

### Step 4c — Validate event schema

For each unblocked event identified in Step 4, validate the YAML against `.flow-engine/schemas/event-schema.yaml` before selecting it for execution.

Required fields that must be present: `event_id`, `event_type`, `action`, `persona`, `task.title`, `task.objective`, `read_from`, `write_to`.

`skill_ref` is required based on `event_type`:
- Required for: `event_type` = `CREATE_ARTIFACT`, `UPDATE_ARTIFACT`, `VALIDATE_ARTIFACT`, `REVIEW_ARTIFACT`, `GENERATE_HANDOFF`, `ENRICH_ARTIFACT`, `REPAIR_ARTIFACT`
- Optional for: `event_type` = `ROUTE_INITIATIVE`, `RAISE_DECISION`, `RESOLVE_DECISION`, `RETRY_FAILED_TASK`, `WAIT_HUMAN`

If a required field is missing from the event file:
- Write result file with `status: fail`, `failure_reason: "schema validation failed: missing required field <field-name>"`
- Move event directly to `failed/` — do not execute it
- Continue evaluating remaining unblocked events

**Template ID / action consistency check:**
If `meta.template_id` is present, look up the registered `action` for that template ID in the mapping table in `template-instantiation-rules.md` section 3.
If the event's `action` field does not match the registered action for that template ID:
- Write result file with `status: fail`, `failure_reason: "fabricated event detected: meta.template_id <X> is registered for action <registered-action> but this event has action <actual-action>. This event was not produced by the framework."`
- Move event directly to `failed/` — do not execute it
- Continue evaluating remaining unblocked events

**Missing template_id check:**
If `meta.template_id` is absent:
1. Look up the event's `action` field in the mapping table in `template-instantiation-rules.md` section 3 to find the matching template.
2. If a matching template exists:
   a. Read the template file.
   b. Compare every path in the event's `write_to` against the template's `outputs.primary` (and `outputs.secondary` if present).
   c. If any `write_to` path does not match the template outputs:
      - Write result file with `status: fail`, `failure_reason: "path mismatch: event write_to <path> does not match template <EVT-TPL-NNN> outputs.primary <expected-path>. This event was hand-crafted with the wrong output path — move or copy the artifact to <expected-path> and re-queue using the correct template."`
      - Move event directly to `failed/` — do not execute it
      - Continue evaluating remaining unblocked events
   d. If `write_to` paths match: the event is hand-crafted but maps to a known template. **Do not proceed as-is.** Instead, repair the event in-place before execution:
      - Read the template file (already open from step a).
      - If `skill_ref` is absent in the event → copy from template.
      - If `must_include` is absent in the event → copy from template verbatim.
      - If `validation_rules` is absent in the event → copy from template verbatim.
      - If `meta.template_id` is absent → set to the matched template ID.
      - If `on_success` is absent → copy from template verbatim.
      - If `on_failure` is absent → copy from template verbatim.
      - Rewrite the event file in `pending/` with the repaired content.
      - Log in result file `notes`: `"meta.template_id was absent — event was hand-crafted. Missing fields injected from template <EVT-TPL-NNN> before execution."`
      - Continue to execution with the repaired event.
3. If no matching template exists for the `action`: the event is genuinely custom. Log a warning in result file `notes`: `"meta.template_id absent and no matching template found for action <action>. Proceeding as custom event — no must_include or validation_rules available."` Continue to execution.

If all unblocked events fail schema validation → stop: **"All unblocked events failed schema validation. See failed/ for details."**

> Note: if an event has `event_template_id` instead of `event_id`, it was caught by Step 4a and already moved to failed/. Step 4c only processes true runtime events.

### Step 5 — Select the next event

From the unblocked, schema-valid events:
- Priority order: `critical` > `high` > `normal` > `low` (from the `priority` field; default `normal` if absent).
- Tie-break within same priority: lowest EVT-NNNNN number first.
- **WAIT_HUMAN priority exception:** if any unblocked event has `event_type: WAIT_HUMAN`, select it first regardless of its declared priority. Human gates must be presented before further AI work proceeds.

If no unblocked events exist → **auto-repair: do not stop, do not ask the user**. Execute the following walk-back procedure:

**Walk-back procedure (inline — no user prompt required):**

1. Collect all unique artifact paths that are blocking pending events.
2. For each blocking artifact path, check whether a pending or done event has that path in its `write_to`. If yes and it is in `done/` → the artifact was produced but not recorded in `workflow-state.json`; update `artifact_status` for that path to `ai_validated` in `workflow-state.json` (orchestrator-only update, Step 18 rules apply) and re-evaluate blocked_by. If this unblocks any event, continue to Step 5.
3. If no done event covers the blocking artifact, find the event template whose `outputs.primary` matches the blocking artifact path. Instantiate that template as a new runtime event in `pending/` (follow full instantiation rules from `template-instantiation-rules.md` section 2). Increment `event_counter`. Set `meta.notes` to `"Auto-instantiated by dispatcher walk-back — blocking artifact <path> had no producer in queue"`. Update `active_events` and `last_updated` in `workflow-state.json`.
4. Repeat for each blocking artifact (depth limit: 10 levels). After each instantiation, re-evaluate blocked_by for all pending events.
5. Return to Step 2 and re-scan the queue.
6. If after walk-back all events are still blocked → stop: **"Walk-back repair ran but all [N] pending events are still blocked. Blocking artifacts: [list]. No matching template could be found to produce them. Manual intervention required."**

This replaces the previous hard stop. The user never needs to resolve blocking manually — the dispatcher self-heals by instantiating the missing upstream event.

### Step 6 — Move event to processing

**Step 6 pre-flight — purge orphan pending duplicates:**

Before moving the selected event, scan all files in `pending/`. For each file:
- Extract the EVT-ID from the filename (e.g. `EVT-00007` from `EVT-00007-create-actors-and-personas.yaml`)
- Check whether a file with that EVT-ID exists in `done/` or `failed/`
- If yes → delete the `pending/` file silently. It is an orphan left by a previous interrupted dispatch. Do not log, do not report, do not count it as a failure.
- If no → leave it in `pending/`

This runs every time Step 6 is reached, before any move happens. It is silent — the user is not notified unless a deletion changes which event would be selected next (in which case return to Step 5 to re-select).

**Move the selected event:**

Move the selected event file from `pending/` to `processing/`.
File name stays the same. Do not rename.

**The file must be deleted from `pending/` — not copied.** After this step, the event file must exist in exactly one location: `processing/`. If the move cannot be completed atomically, write to `processing/` first, then immediately delete from `pending/` before proceeding to Step 6a.

### Step 6a — WAIT_HUMAN short-circuit

If the selected event has `event_type: WAIT_HUMAN`:

1. Do NOT enter persona mode. Do NOT execute steps 7–15.
2. Read the `gate_context` field from the event.
3. Present the gate to the user:

```
--- HUMAN REVIEW GATE ---
Gate:     <gate_context.gate_name>
EVT-ID:   <event_id>

<gate_context.gate_prompt>

Artifacts to review:
<list gate_context.artifacts_under_review — one per line>

Reply with:
  approved           → flow continues, downstream events created
  rejected: <reason> → decision raised, flow stops
```

4. Wait for the user's response.
5. **If approved:**
   - Write result file: `status: pass`, `completed_at: <now>`, `artifacts_written: []`, `notes: "Human approved at gate"`
   - Continue to Step 16 (orchestrator mode) — execute `on_success` normally
   - `on_success.update_state` should set `artifacts.<reviewed-artifact>.status` to `accepted`
   - **dispatch-all after approval:** after completing Steps 16–19, return to Step 2 and continue the loop. Do NOT stop. Do NOT report. Do NOT offer menus. Gate approval is not a stop condition for dispatch-all — it is a resume signal.
6. **If rejected:**
   - Write result file: `status: fail`, `completed_at: <now>`, `failure_reason: "Human rejected: <reason>"`, `artifacts_written: []`
   - Continue to Step 16 — execute `on_failure` (raise_decision)
   - Stop dispatch-all after Step 19. Report the decision raised.
7. **dispatch-all stop — before the user replies:** after presenting the gate and before waiting for the user, dispatch-all MUST stop. Report exactly:
   **"WAIT_HUMAN gate reached: [gate_name] (EVT-ID). Review the artifacts listed above and reply 'approved' or 'rejected: <reason>' to continue."**
   Nothing else. No menus. No "you can also run dispatch-next". Stop here and wait.
   dispatch-next may wait for the user's reply in the same turn.

### Step 7 — Load skill_ref

Read the file at the path in `skill_ref`.
If `skill_ref` is missing and `event_type` requires it (see Step 4c rule) → write result file with `status: fail`, `failure_reason: "skill_ref missing — required for event_type <event_type>"`. Move to failed/. Go to step 17.
If `skill_ref` is missing and `event_type` does not require it → continue without a skill file; the orchestrator handles execution directly.
If the file at `skill_ref` does not exist → write result file with `status: fail`, `failure_reason: "skill_ref file not found: <path>"`. Move to failed/. Go to step 17.

### Step 8 — Load persona_ref

Read the file at the path in `persona_ref`.
If `persona_ref` is absent, derive the default path: `.brs2spec2/personas/<persona>.md` using the `persona` field value.
If the derived or explicit file does not exist → write result file with `status: fail`, `failure_reason: "persona_ref file not found: <path>"`. Move to failed/. Go to step 16.

### Step 9 — Load artifact_template_ref

If `artifact_template_ref` is present: read the file at that path.
If the file does not exist → log a warning in the result file notes, but continue. The template is optional.
If `artifact_template_ref` is absent → continue without a template.

### Step 9b — Check artifact ownership

Before entering persona mode, verify that the executing persona is allowed to write every path listed in `write_to`.

Two ownership sources apply — check both:
1. **Engine-protected paths** — defined in `.flow-engine/instructions/artifact-ownership.md` section 1 (loaded in Step 1). These apply unconditionally for all domains.
2. **Domain ownership table** — defined in the domain layer. For brs-to-spec v2: `.brs2spec2/workflow/artifact-ownership.md`. Load this file now if not already loaded.

For each `write_to` path, apply rules in this order:

1. If the path matches an engine-protected path (`input/*`, `.flow/state/*`, `.flow/events/*`): fail immediately — `failure_reason: "write to <path> is not permitted in persona mode — engine-protected path."` Move to failed/. Go to step 17.
2. If the path is in the domain ownership table and owned by a different persona AND `event_type` is `CREATE_ARTIFACT`: fail — `failure_reason: "artifact <path> is owned by <owner>. Use UPDATE_ARTIFACT or ENRICH_ARTIFACT for cross-persona writes."` Move to failed/. Go to step 17.
3. If the path is in the domain ownership table and owned by a different persona AND `event_type` is `UPDATE_ARTIFACT` or `ENRICH_ARTIFACT`: allowed. Note the cross-persona write in the result file `notes` field.
4. If the path is not in the domain ownership table: allowed. Log a warning in result file `notes`: `"write_to path <path> has no declared owner — proceeding without ownership check."`

### Step 10 — Read input files

**Step 10a — Collect inputs (script-enforced):**

Run:
```
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> collect-inputs <path-to-event-file>
```

Read `.flow/events/processing/<event_id>-inputs.json`. This file is the authoritative input bundle — do not proceed if it is missing or malformed.

- If `overall: fail` (missing_required is non-empty): write result file with `status: fail`, `failure_reason: "required inputs missing: [list from missing_required]"`. Move to failed/. Stop.
- If `overall: pass`: use the `read_evidence` entries from this file as the `read_evidence` block in the result file at Step 15. Do not reconstruct read_evidence manually.

The `read_evidence` block in the result file must be copied verbatim from `<event_id>-inputs.json`. It is machine-written and authoritative — do not paraphrase or summarise it.

Read files listed in `read_from` in order. Use `required_inputs` to distinguish mandatory from optional:

- If `required_inputs` is specified: paths in that list are mandatory; all other `read_from` paths are optional.
- If `required_inputs` is absent: all `read_from` entries without an `optional_inputs` entry are treated as required.
- For each required path: if the file does not exist → write result file with `status: fail`, `failure_reason: "required input missing: <path>"`. Move to failed/. Go to step 16.
- For each optional path: skip silently if not found; note in result file `notes` field.
- Glob patterns (e.g. `input/brs/*.md`): read all matching files. If no files match a required glob → treat as missing required input.
- **Each path in `read_from` must be explicitly read as a file tool call before Step 11 begins.** Do not rely on memory or prior context. If `input/brs.md` is in `read_from`, read it now. If `input/brs/*.md` is in `read_from`, glob and read all matching files now. Reading "in your head" or assuming you already know the content does not count.

**Read evidence recording — mandatory:**

As each file is read, immediately record the following for inclusion in the result file
`read_evidence` block at Step 15:
- `path`: exact path from `read_from`
- `required`: true if in `required_inputs`, false otherwise
- `exists`: true/false
- `lines`: line count (for existing files)
- `bytes`: approximate byte count (for existing files)
- `first_nonempty_line`: first non-blank line (for existing files)
- `read_at`: current ISO-8601 datetime

For glob patterns: record `matched_files` (list of resolved paths) instead of
`lines`/`bytes`/`first_nonempty_line`.

This evidence is NOT optional. If the result file reaches Step 16-G without a
`read_evidence` entry for every `read_from` item, the event will be failed automatically.

> **MODE: Persona mode begins here (steps 10–15).**
> In persona mode: adopt the persona from persona_ref. Apply the skill from skill_ref.
> Do NOT update any `.flow/state/` files while in persona mode.
> Do NOT write to any path not listed in `write_to`.

### Step 11 — Execute the task

Following the `skill_ref` instructions and the `persona_ref` role and quality standards:
- Produce all artifacts listed in `write_to`.
- Use `artifact_template_ref` as the structural contract for output shape.
- Write only to paths listed in `write_to`. No other files.
- If the task cannot complete (ambiguous inputs, missing information): write what can be produced, note gaps in the result file, set status to fail.

### Step 12 — Check required_inputs once more

If `required_inputs` is specified: confirm each listed path now exists on disk (was not consumed or deleted during execution). This is a sanity check — if a file was expected and is missing after execution, something went wrong.

### Step 13 — Verify write_to artifacts exist and no extra files were written

**Part A — confirm declared outputs exist:**

For each path in `write_to`: confirm the file now exists on disk and is not empty.
If any write_to file is missing or empty → set result status to fail; record in failure_reason.

**Part B — detect out-of-bounds writes:**

After Part A, scan for files that should not be in the initiative workspace but were written by the persona during this event.

Two specific checks:

1. **Decision files in artifact folders:** Look for any file whose name matches `decision-*.md`, `DEC-AUTO-*.md`, or `DEC-*.md` anywhere in the initiative workspace except `.flow/state/open-decisions.md`. These are out-of-bounds writes.

2. **Files in the same folder as write_to but not declared in write_to:** For each folder that appears in `write_to` paths (e.g. `business-analysis/`), list the folder contents and check whether any file in that folder is not listed in `write_to` AND its name begins with a pattern that suggests it is an artifact the persona created (e.g. starts with `DEC-`, `decision-`, `ARCH-`, `DRAFT-`). Do not flag pre-existing framework files or files created by earlier events.

For each file detected by either check:
- Record it in result file `notes` as: `"out-of-bounds write detected: <path> was written but is not in write_to"`
- Set result status to fail
- Set `failure_reason: "persona wrote to <path> which is not in write_to — this violates event-execution-rules §3. Decisions must be raised via open_decisions_raised in the result file, not written as loose files. Delete the out-of-bounds file before re-running this event."`

**Decisions written as loose files are the most common out-of-bounds violation.** If the persona wrote a `decision-*.md` or `DEC-AUTO-*.md` file anywhere in the initiative workspace outside `.flow/state/open-decisions.md`, this is an out-of-bounds write and must fail.

### Step 14 — Check must_include

**Mandatory pre-work — count first:**
1. Open the event file. Count the total number of items in the `must_include` list. Write down this number as **N_MUST**.
2. Read every artifact file listed in `write_to` from disk right now — do not rely on memory or the persona's claims.

**Checklist loop — one iteration per must_include item:**

Process items one at a time. For item 1 of N_MUST, 2 of N_MUST, ... N_MUST of N_MUST:
- State which item number you are evaluating (e.g. "Item 3 of 7:")
- Quote the exact must_include text.
- Search the artifact file content for literal evidence.
- Record a `validation_notes` entry immediately:
  ```yaml
  - rule: "<must_include entry text — exact copy, no paraphrase>"
    result: pass  # or fail
    detail: "<quote the matching line from the file, or state exactly what was missing>"
  ```

Do not skip items. Do not batch items. Do not abbreviate. Every item gets its own entry.

**Mandatory count-gate after the loop:**

After iterating, count the `validation_notes` entries you have just written. Call this **N_NOTES**.

If N_NOTES ≠ N_MUST → **do not proceed to Step 15**. Instead:
- Set result `status: fail`
- Set `failure_reason: "must_include count mismatch: event has N_MUST items but only N_NOTES validation_notes entries were written. Re-run Step 14 from the beginning — every must_include item must be evaluated and recorded."`
- Move to failed/ and stop.

Only if N_NOTES = N_MUST proceed to Step 15.

If any must_include item is not satisfied → set result status to fail; record which specific items failed with what was found.

### Step 15 — Write preliminary result file

Write `.flow/events/processing/<event_id>-result.yaml` conforming to `event-result-schema.yaml`.
This is preliminary — natural-language validation in Step 16 may still change the status to fail.

- `event_id`: from the event file
- `status`: `pass` (if steps 12–14 all passed) or `fail`
- `completed_at`: current datetime (ISO-8601)
- `artifacts_written`: list of paths actually written to disk
- `failure_reason`: present and specific if status is fail; empty if pass at this point
- `validation_notes`: one entry per must_include assertion evaluated in Step 14 — must be non-empty if `must_include` is non-empty
- `open_decisions_raised`: list any decisions the persona identified that require human input. Format:
  ```yaml
  open_decisions_raised:
    - question: "specific question requiring human answer"
      owner: "product-owner / architect / stakeholder"
      blocking: true  # or false
      source: "GAP-NNN / FR-NNN / §Section"
  ```
  If no decisions to raise: omit the field or set to `[]`. The orchestrator reads this field at Step 18 and writes each entry to `.flow/state/open-decisions.md`. **Personas must never write directly to `.flow/state/open-decisions.md`.**

> **MODE: Orchestrator mode begins here (steps 16–21).**
> Switch out of persona mode. You are now the orchestrator.
> Only in orchestrator mode may you update `.flow/state/` files.

### Step 16 — Apply natural-language validation and finalize result file

**If `validation_rules.natural_language` is absent from the event:** skip this step. No action required. Proceed to Step 17.

**If `validation_rules.natural_language` is present in the event — mandatory sequence:**

**Step 16-A: Read the rule.**
Open the event file. Read the full text of `validation_rules.natural_language` — every numbered clause (1), (2), (3)... Do not summarize or paraphrase.

**Step 16-B: Read the artifacts — again, fresh.**
For every path in `write_to`, read the file from disk right now. Do not rely on content seen in earlier steps. Count lines, count entities, count IDs explicitly if the rule requires it.

**Step 16-C: Evaluate clause by clause.**
Work through each numbered clause in the natural_language rule:
- State which clause you are evaluating (e.g. "Clause (8):")
- State the specific check it requires.
- Quote concrete evidence from the artifact (actual counts, specific lines, matched IDs).
- Conclude pass or fail for that clause.

**Step 16-D: Write the validation_notes entry.**
Append exactly one entry to `validation_notes`:
```yaml
- rule: "natural_language: <first ~20 words of the rule text verbatim>"
  result: pass  # or fail
  detail: |
    Clause (1): <evidence> — pass/fail
    Clause (2): <evidence> — pass/fail
    ...
    Clause (N): <evidence> — pass/fail
    Overall: pass/fail
```

The `detail` field must quote concrete evidence (counts, specific lines, IDs) — "looks good" or "passed" are not acceptable details.

**Step 16-E: Count-gate.**
After writing the entry, verify the `validation_notes` list contains exactly N_MUST + 1 entries (N_MUST from Step 14, plus this one natural_language entry). If not — something was lost: set status fail, set failure_reason to "validation_notes entry count inconsistency after Step 16".

**Step 16-F: If any clause fails.**
Set result `status: fail`. Set `failure_reason` to the specific failing clause and what was found vs expected.

**Hard-stop: this entry CANNOT be absent.** If `validation_rules.natural_language` is defined and the result file does not contain a `validation_notes` entry whose `rule` field begins with `"natural_language:"`, the event is failed:
- `status: fail`
- `failure_reason: "natural_language validation skipped — Step 16 was not executed. The must_include entries from Step 14 do not substitute for this check. Re-run from Step 16."`
- Move to failed/

**must_include entries from Step 14/15 do NOT satisfy this requirement.** The natural_language entry must be a new, distinct entry appended after Step 14.

### Step 16-G — Validate the result file contract itself

**Step 16-G script checks (run before manual checks):**

Run these commands in order. Read each output file. If any output file is missing, malformed, or reports `overall: fail`, set event result to `status: fail` and stop — do not proceed to Step 17.

```
# 1. Schema and contract check
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> \
  validate-result \
  .flow/events/processing/<event_id>-result.yaml \
  .flow/events/processing/<event_id>-<slug>.yaml

# Read: .flow/events/processing/<event_id>-result-check.yaml
# Gate: overall must be "pass"

# 2. Artifact count check (run for events that produce requirements or intake artifacts)
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> \
  validate-artifact-counts \
  --brs input/brs.md \
  --artifact <write_to path> \
  --event-id <event_id>

# Read: .flow/events/processing/<event_id>-artifact-counts.yaml
# Gate: overall must be "pass"

# 3. Placeholder check
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> \
  validate-no-placeholders \
  --artifact <write_to path> \
  --event-id <event_id>

# Read: .flow/events/processing/<event_id>-placeholder-check.yaml
# Gate: overall must be "pass"
```

Run commands 2 and 3 only when the event has a `write_to` artifact (not for WAIT_HUMAN or ROUTE_INITIATIVE). Run command 2 only for events whose artifact is a requirements catalog or business intake summary (action is `create_requirements` or `create_business_intake_summary`).

If any gating output file is missing: treat as `overall: fail` — the script was not run. Set event to fail with `failure_reason: "script check output missing: <file path>. Script was not executed or failed to write output."`.

Script output overrides the LLM-written result. If `validate-result` reports `overall: fail`, the event fails even if the result file says `status: pass`.

Read `.flow/events/processing/<event_id>-result.yaml` fresh from disk.

Verify all of the following before Step 17:

1. `event_id` exists and matches the event file exactly.
2. `status` exists and is either `pass` or `fail`.
3. `completed_at` exists.
4. `artifacts_written` exists (empty list allowed only on genuine early failure).
5. If the event has any `must_include` items, `validation_notes` exists and has exactly one
   entry per must_include item.
6. If the event has `validation_rules.natural_language`, `validation_notes` contains exactly one
   additional entry whose `rule` begins with `natural_language:`.
7. If the event requires validation notes and the field is absent, empty, or count-mismatched,
   the result file is invalid even if `status: pass` was written earlier.
8. **read_evidence count check:** if the event has a non-empty `read_from` list,
   count the `read_from` items and count the `read_evidence` entries in the result file.
   If `read_evidence` is absent or the count is less than the `read_from` count:
   - set `status: fail`
   - set `failure_reason: "read_evidence incomplete: event has [N] read_from items but
     result file has [M] read_evidence entries. Step 10 was not fully executed."`
9. **generic emptiness claim check:** if result `status` is `fail` AND `failure_reason`
   contains a generic emptiness or content-quality claim (e.g. "no extractable content",
   "no requirements found", "BRS is empty", "insufficient content", "source file does
   not contain"):
   - **First — check if `read_evidence` is absent entirely:**
     If the event has a non-empty `read_from` list AND `read_evidence` is absent from
     the result file:
     - set `failure_reason: "fabricated failure: failure_reason makes a content-quality
       claim but read_evidence is absent — Step 10 was not executed. The inputs were
       never read. Move event back to pending/ and re-run dispatch-next."`
     - keep `status: fail` — do not allow this result to proceed as pass
     - this check supersedes all other checks in item 9; stop here
   - find the corresponding `read_evidence` entry for the referenced input file
   - if the entry shows `exists: true` AND `lines > 20`:
     - the generic claim is invalid — a file with 20+ lines is not empty
     - note: this does NOT mean the file is semantically sufficient — it means a
       generic "empty file" claim is not acceptable for a non-empty file
     - set `status: fail` (keep fail, but replace the reason)
     - set `failure_reason: "generic emptiness claim rejected: '[original reason]' —
       read_evidence shows [path] exists with [lines] lines. A non-empty file requires
       a specific failure_reason quoting the sections found and explaining exactly what
       was missing or insufficient. Re-run with a specific failure_reason."`
   - if the entry shows `exists: true` AND `lines <= 20`:
     - the claim may be plausible but still requires specificity
     - `failure_reason` must quote at least one specific line from the file
     - if no specific line is quoted: same rejection as above
10. **first_nonempty_line contradiction check:** if `read_evidence` shows a meaningful
    `first_nonempty_line` (e.g. `"# Business Requirements Specification"`) AND
    `failure_reason` claims the file was empty or had no content:
    - this is a direct contradiction — a file with a meaningful first line is not empty
    - set `failure_reason: "contradictory failure: read_evidence shows first_nonempty_line
      '[value]' for [path] but failure_reason claims the file was empty or had no content.
      These cannot both be true. Re-run with honest failure evidence."`
11. **required input missing vs exists mismatch:** if `read_evidence` shows
    `exists: true` for a path but `failure_reason` claims that path was missing:
    - set `failure_reason: "contradictory failure: read_evidence shows [path] exists
      but failure_reason claims it was missing. Investigate and re-run."`
12. **read_evidence first_nonempty_line required:** for every `read_evidence` entry
    where `exists: true` and `matched_files` is absent (i.e. a single file, not a glob):
    - `first_nonempty_line` must be present and non-empty
    - if absent: set `status: fail`, set `failure_reason: "read_evidence entry for
      [path] is missing first_nonempty_line — required for contradiction detection.
      Re-run Step 10 and record this field."`
    - this field is what makes content-substitution detectable; omitting it defeats
      checks 9 and 10
13. **validation_notes rule anchoring:** for each entry in `validation_notes` whose
    `rule:` field does NOT start with `"natural_language:"`:
    - the `rule:` text must share at least 2 meaningful words (≥4 chars) with one
      of the event's `must_include` items
    - short freehand labels like `"FR COMPLETENESS"` or `"DOMAIN CORRECTNESS"` that
      share no words with the must_include text are not acceptable
    - if any entry fails this check: set `status: fail`, set `failure_reason:
      "validation_notes entry '[rule text]' does not correspond to any must_include
      item — freehand labels are not permitted. Each entry must quote or paraphrase
      the must_include text it evaluates."`

If any of these checks fail:

- set result `status: fail`
- set `failure_reason` to a specific contract violation such as:
  `"invalid result file: validation_notes missing for event with must_include"`
  or
  `"invalid result file: natural_language validation entry missing"`
- rewrite the result file in processing/

Only after Step 16-G passes may the event proceed to Step 17.

This step finalizes the result file. After Step 16-G, `status` is authoritative — it will not change again.

### Step 17 — Move event and result to done/ or failed/

**If result status is pass:**
- Write event file to `done/` (same filename)
- Write result file to `done/` (same filename)
- Delete event file from `processing/`
- Delete result file from `processing/`

**If result status is fail:**
- Write event file to `failed/` (same filename)
- Write result file to `failed/` (same filename)
- Delete event file from `processing/`
- Delete result file from `processing/`

**Hard rule:** after Step 17, `processing/` must be empty. Both the event file and its result file must have been deleted from `processing/` before proceeding to Step 18. Do not leave copies in `processing/` even as a backup. The file in `done/` or `failed/` is the authoritative copy.

### Step 18 — Execute on_success or on_failure actions

**If pass — execute on_success:**

`create_events`: for each template reference listed in `on_success.create_events`, instantiate a runtime event using the `instantiate-event` script command:

```
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> instantiate-event <EVT-TPL-NNN>
```

Do not hand-build runtime events. The script guarantees `meta.template_id`, `must_include`, `validation_rules`, `on_success`, and `on_failure` are copied from the template. If the script exits non-zero, stop dispatch: **"instantiate-event failed for [EVT-TPL-NNN] — see script output. Do not proceed."**

For reference, the full field mapping the script applies is defined in `template-instantiation-rules.md` (loaded in Step 1). Full procedure (for audit only — the script executes this):

  1. Resolve the template file: glob `.brs2spec2/workflow/event-templates/EVT-TPL-NNN-*.yaml` matching the template ID prefix (e.g. `EVT-TPL-003` matches `EVT-TPL-003-create-business-rules.yaml`)
  2. Read the template file
  3. Check `condition` field if present — skip this template if the condition is false for this initiative's `workflow-state.json`
  4. Apply the full field mapping from `template-instantiation-rules.md` section 2. Every field below MUST be copied — omitting any field silently breaks validation:
     - `type` → split into `event_type` (generic) + `action` (domain) using the mapping table in section 3
     - `persona` → `persona` (verbatim)
     - `priority` → `priority` (verbatim; default `normal` if absent)
     - `description` → `task.objective` (verbatim)
     - `skill_ref` → `skill_ref` (verbatim)
     - `persona_ref` → `persona_ref` (verbatim)
     - `artifact_template_ref` → `artifact_template_ref` (verbatim)
     - `inputs.required` → `required_inputs` AND included in `read_from`
     - `inputs.optional` → `optional_inputs` AND included in `read_from`
     - `outputs.primary` → first entry in `write_to`
     - `outputs.secondary` → additional entries in `write_to` (append after primary)
     - `must_include` → `must_include` (verbatim — **mandatory**; omitting this means validation runs against nothing and stubs will pass)
     - `validation_rules` → `validation_rules` (verbatim — **mandatory**; omitting this skips natural_language validation entirely)
     - `blocked_by_stage` → `blocked_by` resolved artifact list using section 4 stage-to-artifact map
     - `blocked_by_event` → `blocked_by_events` (copy EVT-ID verbatim)
     - `on_success` → `on_success` (verbatim)
     - `on_failure` → `on_failure` (verbatim)
     - `gate_context` → `gate_context` (verbatim; only for WAIT_HUMAN events)
  5. Assign `event_id`: read `event_counter` from `.flow/state/workflow-state.json`, increment by 1, format as `EVT-NNNNN`
  6. Set meta fields:
     - `meta.template_id` → copy `event_template_id` from the template verbatim (e.g. `EVT-TPL-003`) — **MANDATORY. Without this field chain-repair cannot function.**
     - `meta.created_at` → current datetime
     - `meta.created_by` → `orchestrator`
     - `meta.notes` → the `reason` from the template reference
  7. **Before writing** — perform a pre-write self-check on the event object you are about to write:
     - Does it contain `meta.template_id`? If not → STOP. Do not write this event: **"Instantiation self-check failed for [EVT-TPL-NNN]: meta.template_id was not set. Chain-repair depends on this field. Set it to the template's event_template_id value before writing."**
     - Does it contain `must_include`? If the template has `must_include` and the event object does not → STOP. Do not write this event. Stop dispatch entirely: **"Instantiation self-check failed for [EVT-TPL-NNN]: must_include was not copied from the template. This is a dispatcher bug — the template file must be re-read and the field mapping applied in full before retrying."**
     - Does it contain `validation_rules`? If the template has `validation_rules` and the event object does not → same hard stop.
     - Does it contain `write_to` with at least one path? If not → same hard stop.
     This self-check exists because prior runs showed the dispatcher writing bare runtime events without these fields, causing stubs to pass validation silently. The check must run before every write.
  8. Write runtime event to `.flow/events/pending/EVT-NNNNN-<slug>.yaml` where slug is derived from the template slug
  9. **Immediately after writing** — read the file back from disk. Count the items in `must_include` in the file you just wrote. Count the items in `must_include` in the template file (still open from step 2). If the counts differ → delete the written file, stop dispatch: **"Post-write verification failed for EVT-NNNNN (from [EVT-TPL-NNN]): template has [N] must_include items, written file has [M]. The field mapping was not applied correctly. Delete the file and re-instantiate from the template."**
  10. Increment `event_counter` in `.flow/state/workflow-state.json`

`update_state`: write the key-value pairs into `.flow/state/workflow-state.json` (orchestrator-owned fields only — see state-update-rules.md).

`open_decisions_raised`: read the result file's `open_decisions_raised` field (pass or fail — decisions can be raised on either). For each entry, write one entry to `.flow/state/open-decisions.md`:
  - Auto-assign ID: `DEC-AUTO-NNN` — read last DEC-AUTO entry in the file, increment by 1
  - Include: `id`, `question`, `owner`, `blocking`, `raised_by` (EVT-ID), `raised_at` (current datetime), `source` (from result field if present)
  - This is the ONLY way decisions reach `open-decisions.md`. Personas never write there directly.

`append_log`: default true. Append one line to `.flow/state/event-log.jsonl` (see state-update-rules.md for format).
Before appending, scan existing log lines for the same `event_id`. If already present:
  - do not append
  - stop dispatch with failure: **"Duplicate event-log entry detected for EVT-NNNNN. Queue/state repair required before continuing."**

**If fail — execute on_failure:**

`create_events`: same as on_success (retry or escalation events).

`raise_decision` (from event `on_failure`): write one additional entry to `.flow/state/open-decisions.md` using the question/owner/blocking from the event's `on_failure.raise_decision` field. This is separate from `open_decisions_raised` — both may be written in the same step if both are present.

Always append to event-log.jsonl on failure too.

### Step 19 — Update workflow-state.json

**Step 19a — State update (script-enforced):**

Run:
```
python .flow-engine/scripts/engine_cli.py --workspace <workspace-root> \
  update-state \
  .flow/events/done/<event_id>-<slug>.yaml \
  .flow/events/done/<event_id>-result.yaml
```

Read `.flow/events/processing/<event_id>-state-update.json`. If the file is missing or reports failure, stop: **"update-state script failed — workflow-state.json may be inconsistent. Check the output file and resolve before continuing."**

The script updates `workflow-state.json`, appends to `event-log.jsonl`, and writes decisions to `open-decisions.md`. Do not also hand-update these files — that would produce duplicate entries.

Following `state-update-rules.md`, update:
- `last_completed_event`: set to EVT-ID (pass only)
- `failed_events`: append EVT-ID (fail only)
- `active_events`: remove the completed EVT-ID; add any newly created EVT-IDs
- `artifacts.<path>.status`: set to `ai_validated` (pass, non-gate events) or `accepted` (pass, WAIT_HUMAN or ROUTE_INITIATIVE) or `failed` (fail) — see state-update-rules.md artifact status rule
- `artifacts.<path>.produced_by`: set to EVT-ID
- `artifacts.<path>.accepted_at`: set to current datetime (pass only)
- `artifacts.<path>.last_updated`: set to current datetime
- `open_decisions` / `blocking_decisions`: recount from `.flow/state/open-decisions.md`
- `event_counter`: already updated in step 18 if events were created

### Step 20 — Report to user

Write a short fixed-format summary. Nothing else.

```
Event:    EVT-NNNNN — <task.title>
Persona:  <persona>
Result:   PASS / FAIL
Artifacts written: [list paths]
[If PASS] Next events queued: [list EVT-IDs and titles, or "none — queue empty"]
[If FAIL] Failure reason: <failure_reason>
[If FAIL] Decision raised: <DEC-AUTO-NNN if raised>
```

**Hard rule — no menus, no options, no next-step offers, no internal tooling:**
Do NOT add any text after this summary. Do NOT offer choices ("you can do X or Y"). Do NOT ask "which should I do?". Do NOT suggest "you may want to review". Do NOT offer to "auto-dispatch" or "wait for review". Do NOT use todo lists, task trackers, or internal planning tools during dispatch — these are not visible to the user and add noise. The user controls dispatch by typing dispatch-next, dispatch-all, or approved/rejected. Your job is to report what happened, then stop.

### Step 21 — Continue or stop

**dispatch-next:** stop here. Write only the Step 20 summary.

**dispatch-all:**
- Increment dispatch loop counter (internal — not written to any file).
- If counter = 50 → stop: **"dispatch-all limit reached: 50 events executed. Queue state: [N] pending, [N] blocked, [N] failed. Run dispatch-next or dispatch-all again to continue."**
- **Check `engine_flags.chain_break_on_new_events` in `workflow-state.json`:**
  - If `true` AND Step 18 created one or more new events in `pending/` this iteration → stop: **"[chain-break] Event EVT-NNNNN complete. [N] new events queued in pending/: [list EVT-IDs and titles]. Run dispatch-all to continue."** Do NOT loop back to Step 2.
  - If `false` or absent → continue normally: return to Step 2.
- Otherwise: return to Step 2. Do not report between events — only report at the final stop.

---

## MODE SWITCHING — critical rule

> **Persona mode (steps 10–15):** Claude adopts the persona from persona_ref, applies the skill from skill_ref, and produces artifacts. In this mode Claude must NOT update workflow-state.json, event-log.jsonl, or open-decisions.md.
>
> **Orchestrator mode (steps 16–21):** Claude acts as the orchestrator only — validating, moving files, updating state, chaining events. In this mode Claude must NOT re-enter persona behaviour or produce business artifacts.
>
> The result file (step 15) is the boundary. Everything before it is persona mode. Everything after is orchestrator mode.

---

## Stop conditions — full list

Self-healing conditions (auto-repair, no user prompt):

| Condition | When | Behavior |
|---|---|---|
| Queue empty + initiative incomplete | Step 2 | Inline chain-repair: read last_completed_event → read its template → instantiate on_success.create_events. Resume from Step 2. Only stop if repair also leaves queue empty. |
| processing/ not empty | Step 3 | Auto-classify and move/delete stale files silently. Resume from Step 4. |
| All events blocked | Step 5 | Auto-run walk-back: instantiate missing upstream event. Resume from Step 2. Only stop if walk-back finds no matching template. |

Genuine stop conditions (require human input or are truly terminal):

| Condition | When | What to report |
|---|---|---|
| No v2 initiative workspace found | Step 0 | "No v2 initiative found. Run scaffolding script." |
| workflow-state.json missing | Step 0 | "workflow-state.json missing — workspace may be corrupted." |
| Engine rule file missing | Step 1 | "Engine rule file missing: [path]. Do not attempt dispatch." |
| Queue empty — initiative complete | Step 2 | "Queue empty — initiative complete." |
| Chain repair ran but queue still empty | Step 2 | "Chain repair ran but queue is still empty. Check output for details." |
| Walk-back ran but events still blocked | Step 5 | "Walk-back repair ran but all [N] events are still blocked. No template found for: [artifact list]. Manual intervention required." |
| processing/ repair failed unexpectedly | Step 3 | "Processing/ repair failed unexpectedly. Files remaining: [list]. Manual inspection required." |
| WAIT_HUMAN gate reached | Step 6a | "WAIT_HUMAN gate: [gate_name] (EVT-ID). Review artifacts and reply approved/rejected." Stop dispatch-all. |
| Fabricated event detected | Step 4c | Write fail result. Move to failed/. Continue to next event. |
| All unblocked events fail schema validation | Step 4c | "All unblocked events failed schema validation. See failed/ for details." |
| skill_ref missing or not found | Step 7 | Write fail result. Move to failed/. Continue to next event. |
| persona_ref not found | Step 8 | Write fail result. Move to failed/. Continue to next event. |
| Required input missing | Step 10 | Write fail result. Move to failed/. Continue to next event. |
| write_to artifact not produced | Step 13 | Write fail result. Move to failed/. Continue to next event. |
| Blocking decision raised | Step 18 | Report decision raised. Stop dispatch-all. |
| dispatch-all 50-event limit | Step 21 | Report count and queue state. Stop. |
