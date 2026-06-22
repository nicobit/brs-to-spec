# Prompt 05 - Scaffold `.b2s` Core

## Goal

Create the initial `.b2s/` framework structure for a staged engine.

## Files and folders to create

Create:

- `.b2s/agent-instructions.md`
- `.b2s/module-index.md`
- `.b2s/workflow/workflow-definition.yaml`
- `.b2s/workflow/stage-actions.yaml`
- `.b2s/prompts/run-workflow.md`
- `.b2s/prompts/reset-to-phase.md`
- `.b2s/prompts/resume-from-phase.md`
- `.b2s/prompts/repair-state.md`
- `.b2s/templates/state/workflow-state.json`
- `.b2s/templates/state/open-decisions.md`
- `.b2s/tests/fixtures/sample-initiative/`
- `.b2s/tests/fixtures/missing-brs/`
- `.b2s/tests/fixtures/pending-gate/`
- `.b2s/tests/fixtures/stale-downstream/`
- `.b2s/scripts/b2s_cli.py`
- `.b2s/scripts/b2s_engine/__init__.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `.b2s/scripts/b2s_engine/next_step.py`
- `.b2s/scripts/b2s_engine/inputs.py`
- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/scripts/b2s_engine/state.py`
- `.b2s/scripts/b2s_engine/reset.py`
- `.b2s/scripts/b2s_engine/gates.py`

## Requirements

- use Python standard library only unless an existing repo dependency is already used
- use `argparse` for the CLI
- add stub subcommands for:
  - `next-step`
  - `collect-inputs`
  - `validate-artifact`
  - `update-state`
  - `repair-state`
  - `reset-to-phase`
  - `approve-current-gate`
  - `reject-current-gate`
- every stub should raise a clear `NotImplementedError`
- create minimal placeholder prompt and workflow files, but do not implement logic yet
- scaffold files in a way that is consistent with:
  - `02-stage-action-model.md`
  - `04a-output-file-contracts.md`
  - `04b-state-and-gate-model.md`

## Verification

Verify:

1. all target files exist
2. `python .b2s/scripts/b2s_cli.py --help` works
3. the command names appear in help output
4. there are no broken local imports
5. the fixture root exists and is ready for later population
