# BRS-to-Spec v2 — Restart / Start Flow

Use this prompt when:
- The user says "restart", "start", "start flow", "reset", or "reinitialize" for an existing initiative
- The `.flow/` folder is missing, empty, or corrupted but `input/` has BRS content
- A previous run left the workspace in an unrecoverable state

This prompt does NOT create a new initiative. It resets the flow engine state for an existing one.
To create a brand-new initiative workspace, use `new-initiative.md` instead.

Hard rule: any runtime event written during restart must be instantiated from its source template using `.flow-engine/instructions/template-instantiation-rules.md`. Never hand-craft a partial event file.

---

## Step 1 — Identify the initiative workspace

1. If the user named an initiative (e.g. "restart I006"), locate `initiatives/<id>*/`.
2. Otherwise scan `initiatives/` — select the workspace most recently modified that has an `input/` folder.
3. Set `workspace_root = initiatives/<workspace_name>/`.

If no workspace is found → stop:
**"No initiative workspace found. Say 'new initiative' to create one."**

---

## Step 2 — Verify input/ has BRS content

Check that at least one of these exists and is not empty:
- `<workspace_root>/input/brs.md`
- any file matching `<workspace_root>/input/brs/*.md`

If none exist or all are empty → stop:
**"input/ has no BRS content. Add your BRS to input/brs.md before restarting."**

---

## Step 3 — Read existing workflow-state.json if present

If `<workspace_root>/.flow/state/workflow-state.json` exists, read it and extract:
- `delivery_mode` (preserve if set, null if not)
- `execution_mode` (preserve if set, null if not)
- `project_type` (preserve if set, null if not)

If the file does not exist, default all three to null.

---

## Step 4 — Wipe .flow/ and re-scaffold

Delete all contents of `<workspace_root>/.flow/` **except** any `backups/` subfolder.

Re-create the following structure:

```
<workspace_root>/.flow/
  state/
    workflow-state.json
    event-log.jsonl
    open-decisions.md
  events/
    pending/
    processing/
    done/
    failed/
```

### workflow-state.json

```json
{
  "initiative_id": "<workspace_name>",
  "initiative_slug": "<slug>",
  "created": "<original created date if known, else today>",
  "current_stage": "0-routing",
  "delivery_mode": "<preserved or null>",
  "execution_mode": "<preserved or null>",
  "project_type": "<preserved or null>",
  "event_counter": 1,
  "active_events": ["EVT-00001"],
  "blocked_events": [],
  "failed_events": [],
  "last_completed_event": null,
  "open_decisions": 0,
  "blocking_decisions": 0,
  "last_updated": "<today ISO-8601>",
  "artifacts": {}
}
```

### event-log.jsonl

Empty file.

### open-decisions.md

```markdown
# Open Decisions — <workspace_name>

| ID | Question | Raised by | Status | Resolution |
|---|---|---|---|---|
```

---

## Step 5 — Instantiate EVT-00001

Do NOT write a hand-crafted YAML example.

Instead:
1. Read `.flow-engine/instructions/template-instantiation-rules.md`
2. Read `.brs2spec2/workflow/event-templates/EVT-TPL-001-route-initiative.yaml`
3. Instantiate a runtime event from that template as `EVT-00001`
4. Set:
   - `stage: "0-routing"`
   - `status: pending`
   - `meta.created_by: orchestrator`
   - `meta.created_at: <today ISO-8601>`
   - `meta.notes: "Workspace restarted via restart command."`
5. Before writing, verify:
   - the runtime `must_include` count matches the template count exactly
   - `validation_rules` is present and copied verbatim
   - `on_success` and `on_failure` are present
6. After writing, read the file back and verify those same conditions again

If any verification fails, stop and correct the event file before reporting success.

---

## Step 6 — Report

```
Workspace restarted: <workspace_name>
Path:               initiatives/<workspace_name>/
BRS input:          ✅ present
State:              reset to stage 0-routing
Event counter:      1
Queue:              EVT-00001 (route-initiative) — ready

Say "dispatch-next" to begin.
```

Nothing else. No menus. No options. No "would you like to...".

---

## Stop conditions

- If `input/` has no BRS content → stop at Step 2
- If the workspace folder does not exist → stop at Step 1
- Do not delete `input/` or any files inside it
- Do not delete `<workspace_root>/.flow/backups/` if it exists
- Do not run `dispatch-next` automatically — wait for the user to say it
