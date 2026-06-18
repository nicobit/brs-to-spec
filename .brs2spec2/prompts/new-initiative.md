# BRS-to-Spec v2 — New Initiative

Create a new v2 initiative workspace by collecting a few details from the user and scaffolding the folder structure directly — no Python script required.

Hard rule: runtime events must be instantiated from templates, not hand-crafted from memory. Any event written into `.flow/events/` must preserve the template's `must_include`, `validation_rules`, `on_success`, and `on_failure` fields exactly where applicable.

---

## Step 1 — Collect required information

Ask the user (in a single message, all at once):

1. **Initiative ID** — e.g. `I006`. If not provided, look at existing `initiatives/` folders and suggest the next available ID.
2. **Initiative name** — short slug, e.g. `loan-origination-platform`.
3. **Delivery mode** — one of: `FastPath`, `Standard`, `Enterprise`, `Enterprise+Modular`. Default: `Standard`.
4. **Execution mode** — one of: `OpenSpec`, `Standalone`, `FastPath`. Default: `OpenSpec`.
5. **Project type** — `greenfield` or `brownfield`. Default: `greenfield`.

If the user already provided any of these in their message, use those values and only ask for what is missing. If all five are clear from context, skip asking and proceed directly to Step 2.

---

## Step 2 — Derive the workspace name and path

```
workspace_name = <initiative-id>-<slugified-name>
  e.g. I006-loan-origination-platform

workspace_root = initiatives/<workspace_name>/
```

Slugify the name: lowercase, replace spaces and special characters with hyphens, collapse multiple hyphens.

---

## Step 3 — Create the folder structure

Create the following files and folders. Use today's date (ISO-8601) for all `created` / `created_at` fields.

### `.flow/` event queue

```
<workspace_root>/.flow/events/pending/
<workspace_root>/.flow/events/processing/
<workspace_root>/.flow/events/done/
<workspace_root>/.flow/events/failed/
```

### `.flow/state/workflow-state.json`

```json
{
  "initiative_id": "<workspace_name>",
  "created": "<today>",
  "current_stage": "0-routing",
  "delivery_mode": "<delivery_mode>",
  "execution_mode": "<execution_mode>",
  "project_type": "<project_type>",
  "readiness_score": null,
  "quality_gates_triggered": [],
  "optional_artifacts_requested": [],
  "engine_flags": {
    "chain_break_on_new_events": true
  },
  "artifact_status": {},
  "event_counter": 1,
  "active_events": ["EVT-00001"],
  "failed_events": [],
  "last_completed_event": null,
  "open_decisions": 0,
  "blocking_decisions": 0,
  "last_updated": "<today>"
}
```

### `.flow/state/event-log.jsonl`

Empty file (no content).

### `.flow/state/open-decisions.md`

```markdown
# Open Decisions — <workspace_name>

| ID | Question | Raised by | Status | Resolution |
|---|---|---|---|---|
```

### `input/brs.md`

```markdown
# BRS

## Source Metadata

| Field | Value |
|---|---|
| Source name |  |
| Source version/date |  |
| Extracted by |  |
| Extraction date |  |

## Executive Summary
```

### `input/architecture.md`

```markdown
# Architecture

No architecture document provided.
```

### `input/input-package.md`

```markdown
# Input Package

## Initiative Workspace

## Input Inventory

## Consolidation Notes

## Known Limitations

## Assumptions
```

### `.flow/events/pending/EVT-00001-route-initiative.yaml`

Do NOT hand-write this YAML from an inline example.

Instead:
1. Read `.flow-engine/instructions/template-instantiation-rules.md`
2. Read `.brs2spec2/workflow/event-templates/EVT-TPL-001-route-initiative.yaml`
3. Instantiate `EVT-00001` using the full field mapping from the template-instantiation rules
4. Set:
   - `event_id: EVT-00001`
   - `stage: "0-routing"`
   - `status: pending`
   - `meta.template_id: EVT-TPL-001`
   - `meta.created_by: orchestrator`
   - `meta.created_at: <today>`
   - `meta.notes: "Auto-created on initiative init"`
5. Before writing, verify that the runtime event contains the same number of `must_include` items as the template and that `validation_rules` is copied verbatim
6. After writing, read the file back and verify those counts again

If the counts do not match, stop and fix the instantiation before continuing.

---

## Step 4 — Confirm and report

After creating all files, report:

```
Initiative created: <workspace_name>
Path:              initiatives/<workspace_name>/
Delivery mode:     <delivery_mode>
Execution mode:    <execution_mode>
Project type:      <project_type>

Next step: add your BRS content to input/brs.md, then say "dispatch-next" to begin.
```

If the user already has BRS content to paste, tell them to paste it into `input/brs.md` before running `dispatch-next`.

---

## Stop conditions

- If `initiatives/<workspace_name>/` already exists: stop and ask the user whether to use it as-is, or choose a different ID.
- Do not create any file outside `initiatives/<workspace_name>/`.
- Do not run `dispatch-next` automatically — wait for the user to say it.
