# Prompt 07 — Implement `instantiate-event`

## Goal

Implement the first real deterministic engine command:

`instantiate-event`

This command creates a runtime event from a template and writes it into the workspace
queue with all required fields preserved.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/templates.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`

## Behavior to implement

The command should accept at minimum:

- `--workspace`
- `--template-id`
- `--stage`
- `--note`

### Script responsibilities

1. resolve the workspace root
2. load the matching template from `.brs2spec2/workflow/event-templates/`
3. instantiate a runtime event using the current field-mapping rules
4. assign the next `event_id` from `workflow-state.json`
5. set:
   - `meta.template_id`
   - `meta.created_by`
   - `meta.created_at`
   - `meta.notes`
6. write the runtime event into `.flow/events/pending/`

## Hard guarantees

The implementation must preserve exactly:

- `must_include`
- `validation_rules`
- `on_success`
- `on_failure`
- `artifact_template_ref`
- `skill_ref`
- `persona_ref`

If any of these are absent in the written runtime event when present in the template,
the script must fail before writing or delete the file and fail after verification.

## Output

Print or emit structured JSON containing at least:

- `event_id`
- `event_path`
- `template_id`
- `must_include_count`

## Verification

After implementation, verify:

1. runtime events contain `meta.template_id`
2. `must_include` count matches template count
3. `validation_rules` exists when present in template
4. the command writes into `pending/` only
