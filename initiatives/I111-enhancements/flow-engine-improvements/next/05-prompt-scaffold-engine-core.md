# Prompt 05 - Scaffold Engine Core

## Goal

Create the initial Python script package for deterministic flow-engine mechanics.
This prompt is for scaffolding only, not for full behavior.

## Target paths

Create:

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/__init__.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`
- `.flow-engine/scripts/brs2spec_engine/templates.py`
- `.flow-engine/scripts/brs2spec_engine/inputs.py`
- `.flow-engine/scripts/brs2spec_engine/queue.py`
- `.flow-engine/scripts/brs2spec_engine/results.py`
- `.flow-engine/scripts/brs2spec_engine/state.py`
- `.flow-engine/scripts/brs2spec_engine/repair.py`

## Requirements

- use Python standard library only unless the repo already has a dependency
- use `argparse` in `engine_cli.py`
- establish a shared `--output` convention for command results
- add subcommands for:
  - `instantiate-event`
  - `collect-inputs`
  - `move-event`
  - `check-integrity`
  - `validate-result`
  - `validate-artifact-counts`
  - `validate-no-placeholders`
  - `update-state`
  - `repair-processing`
  - `repair-chain`
  - `reset-to-phase`
- use `pathlib.Path`
- add type hints on public functions
- make each command call a stub function that raises a clear
  `NotImplementedError`
- the `NotImplementedError` message must clearly state that the command is not
  yet implemented and should not be wired into dispatcher prompts

## Also define now

Before real implementation, define:

- the fixed output-file convention for command results
- the fixture root for script tests

Use the phase documents in this folder as the contract unless a repo standard
already exists.

## Verification

Verify:

1. all files exist
2. `python .flow-engine/scripts/engine_cli.py --help` works
3. the subcommands appear in help output
4. imports resolve cleanly
