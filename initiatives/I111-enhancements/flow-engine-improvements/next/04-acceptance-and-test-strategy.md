# Acceptance and Test Strategy

## Test philosophy

Each command should be provable with fixture-based tests against small initiative
workspaces. The tests should verify filesystem outcomes, not just return values.

## Fixture location

Decide this before implementation and keep it stable across commands.

Recommended location:

- `.flow-engine/tests/fixtures/`

Recommended structure:

- `.flow-engine/tests/fixtures/valid-intake/`
- `.flow-engine/tests/fixtures/orphan-result-done/`
- `.flow-engine/tests/fixtures/orphan-result-processing/`
- `.flow-engine/tests/fixtures/missing-required-input/`
- `.flow-engine/tests/fixtures/bad-result-schema/`
- `.flow-engine/tests/fixtures/missing-fr-rows/`

## Acceptance checks by command

### `instantiate-event`

- template fields are preserved exactly
- generated event gets a valid `EVT-` identifier
- event is written to `pending/`

### `collect-inputs`

- required files are resolved relative to workspace
- glob expansion is stable
- `read_evidence` count matches `read_from` count
- missing required inputs fail before artifact generation starts
- required output file is written at the agreed fixed path

### `move-event`

- files move rather than being recreated
- result file follows the event when appropriate
- duplicate bucket presence is rejected

### `check-integrity`

- orphan result file in `done/` is detected
- orphan result file in `processing/` is detected
- stale `artifact_status` reference is reported
- dispatcher-facing output file is written and can gate dispatch

### `validate-result`

- bad schema is rejected
- missing `read_evidence` is rejected when `read_from` exists
- contradictory pass/no-artifact situations are flagged
- a failing result-check output prevents dispatcher continuation

### `validate-artifact-counts`

- missing FR/NFR rows fail with explicit IDs
- matching counts pass

### `validate-no-placeholders`

- placeholder strings outside allowed sections fail
- allowed gap sections do not fail

### `update-state`

- event log appends once
- stage progression matches authoritative event outcome
- failed/completed/active lists stay aligned

## Suggested fixture scenarios

- valid business-intake flow
- BRS path exists but is not read by the prompt
- orphan result file in `done/`
- duplicated event across `pending/` and `processing/`
- requirements artifact with missing FR rows
- result file with `status: done`
- missing script output file for a dispatcher-required command
- malformed script output file for a dispatcher-required command

## Minimum delivery bar

Do not wire a command into dispatcher prompts until:

- its filesystem behavior is tested
- its failure mode is clear and machine-readable
- it can run without human interpretation of its raw output
- the dispatcher stop/fail behavior is tested when the output file is missing or failing
