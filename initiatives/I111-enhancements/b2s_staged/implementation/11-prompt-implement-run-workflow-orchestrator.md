# Prompt 11 - Implement `.b2s` Run Workflow Orchestrator

## Goal

Create the main staged orchestrator prompt for `.b2s`.

## Files to modify

- `.b2s/prompts/run-workflow.md`
- `.b2s/module-index.md`
- `.b2s/agent-instructions.md`

## Required behavior

The orchestrator should:

1. identify the active initiative workspace
2. read staged state
3. run `next-step`
4. read `.b2s/state/next-step.json`
5. run `collect-inputs`
6. read `.b2s/tmp/current-inputs.json`
7. load only the selected skill prompt
8. generate the artifact
9. run `validate-artifact`
10. read `.b2s/tmp/current-validation.yaml`
11. if validation passes, run `update-state`
12. read `.b2s/tmp/current-state-update.json`
13. reassess or stop

## Mandatory rule

Do not use stdout summaries as gating truth.
Gate only on required output files.

Use the output-file contracts from `04a-output-file-contracts.md` exactly.

## Verification

Verify:

1. the orchestrator is staged, not event-based
2. it loads only the active skill prompt
3. progression is gated by script output files
4. it can execute one thin-slice action end to end on paper
5. it assumes only one active action at a time
