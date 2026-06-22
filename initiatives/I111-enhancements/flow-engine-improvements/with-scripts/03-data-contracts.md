# Data Contracts Between Scripts and Prompts

## Principle

Scripts should exchange structured data with prompts using small JSON/YAML payloads.
Prompts should not reconstruct these structures from prose.

## Contract 1 — Runtime event object

Produced by:

- `instantiate-event`

Consumed by:

- dispatcher / prompt orchestration

Contains:

- complete runtime event YAML
- preserved template-derived fields
- assigned `event_id`

## Contract 2 — Input bundle

Produced by:

- `collect-inputs`

Consumed by:

- persona execution step
- result writer

Contains:

- resolved required inputs
- resolved optional inputs
- glob expansion results
- canonical `read_evidence`
- machine-detected missing-input status

## Contract 3 — Result validation report

Produced by:

- `validate-result`

Consumed by:

- orchestrator step before Step 17/18 behavior

Contains:

- pass/fail
- missing required result fields
- `validation_notes` count status
- `read_evidence` count status
- contradiction findings

## Contract 4 — State update plan

Produced by:

- `update-state`

Consumed by:

- state writer

Contains:

- artifact status changes
- active/failed/completed event changes
- event-log append payload
- open decision inserts

## Recommended storage form

Short term:

- ephemeral JSON produced by the script and read immediately by the prompt/orchestrator

Later:

- optionally write under `.flow/tmp/` for debugging:

```text
.flow/tmp/
  EVT-00002-read-evidence.json
  EVT-00002-result-validation.json
  EVT-00002-state-update.json
```

This should remain debug/audit support, not a replacement for the canonical result file.
