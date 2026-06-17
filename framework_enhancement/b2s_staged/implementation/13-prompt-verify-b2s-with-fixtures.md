# Prompt 13 - Verify `.b2s` With Fixtures

## Goal

Create the first fixture and verification layer for the new staged framework.

## Files and folders to create

Create:

- `.b2s/tests/fixtures/`
- staged test fixtures for:
  - missing BRS
  - valid business intake flow
  - missing requirements artifact
  - readiness gate pending acceptance
  - stale downstream artifact after upstream change

Add any small verification script or test harness needed.

Use the fixture root established in `05-prompt-scaffold-b2s-core.md`.
Do not invent a second fixture location.

## Required checks

- `next-step` selects the expected action
- `collect-inputs` writes the expected bundle
- `validate-artifact` blocks incomplete output
- `update-state` advances only on success
- repair and reset commands work on staged state

## Verification

Verify:

1. the first thin slice can be exercised with fixtures
2. gating files exist for every command used by the orchestrator
3. the staged engine can restart from compact state without event files
4. fixture workspaces are compatible with the state and output-file contracts
