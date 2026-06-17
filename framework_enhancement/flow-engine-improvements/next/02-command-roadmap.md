# Command Roadmap

## Core commands

## Common output rule

Each command should support a required `--output` path for machine-readable
results.

Do not rely on stdout as the only interface for dispatcher-critical behavior.
Stdout may be used for a short human-readable summary, but the dispatcher should
gate on the written output file.

### `instantiate-event`

Creates a runtime event from a template and writes it to `pending/`.

Must guarantee:

- `meta.template_id` is set
- `must_include` is preserved
- `validation_rules` is preserved
- `on_success` and `on_failure` are preserved

Recommended output:

- `.flow/events/pending/<event_id>-instantiation.json`

### `collect-inputs`

Resolves all `read_from` entries and emits an authoritative input bundle.

Must guarantee:

- every `read_from` item produces a `read_evidence` entry
- required vs optional missing inputs are classified mechanically
- paths are resolved relative to the initiative workspace

Recommended output:

- `.flow/events/processing/<event_id>-inputs.json`

### `move-event`

Moves an event and its related result file between queue buckets.

Must guarantee:

- move semantics, not recreate semantics
- the event exists in exactly one bucket after the move
- invalid source/target combinations fail clearly

Recommended output:

- `.flow/events/processing/<event_id>-move.json` or equivalent bucket-local
  audit output when needed

### `check-integrity`

Detects files that indicate dispatcher bypass or interrupted queue behavior.

Must detect:

- result file in `done/` without event file in `done/`
- result file in `processing/` without event file in `processing/`
- unverifiable `artifact_status` references

Recommended output:

- `.flow/state/integrity-check.yaml`

### `validate-result`

Checks the result file contract before finalization.

Must validate:

- status values
- required fields
- `validation_notes` presence and count
- `read_evidence` presence and count
- contradiction patterns

Recommended output:

- `.flow/events/processing/<event_id>-result-check.yaml`

## Validation helper commands

### `validate-artifact-counts`

For selected artifacts, compare FR/NFR IDs in the source and output.

Recommended output:

- `.flow/events/processing/<event_id>-artifact-counts.yaml`

### `validate-no-placeholders`

Scan artifacts for placeholder strings outside allowed sections.

Recommended output:

- `.flow/events/processing/<event_id>-placeholder-check.yaml`

## Maintenance commands

### `update-state`

Updates `workflow-state.json`, `event-log.jsonl`, and related state artifacts.

Recommended output:

- `.flow/events/processing/<event_id>-state-update.json`

### `repair-processing`

Repairs stale or partial `processing/` contents.

### `repair-chain`

Reinstantiates missing downstream events from the authoritative chain.

### `reset-to-phase`

Backs up active state, clears active queue buckets, and rebuilds from a chosen
phase boundary.

## Dispatcher gating rule

For commands with an `overall` or equivalent decision field:

- missing output file -> fail/stop
- malformed output file -> fail/stop
- output says fail -> fail/stop
- output says pass -> proceed

This rule should be encoded in dispatcher prompts explicitly.
