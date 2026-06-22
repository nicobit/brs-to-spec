# Prompt 06 — Scaffold the Python Engine Package

## Goal

Create the initial Python package structure for the scripted engine core.
This step should create files and stubs only — no business logic yet beyond
minimal CLI parsing and shared dataclasses/helpers.

## Target paths

Create these files:

```text
.flow-engine/scripts/engine_cli.py
.flow-engine/scripts/brs2spec_engine/__init__.py
.flow-engine/scripts/brs2spec_engine/workspace.py
.flow-engine/scripts/brs2spec_engine/templates.py
.flow-engine/scripts/brs2spec_engine/queue.py
.flow-engine/scripts/brs2spec_engine/inputs.py
.flow-engine/scripts/brs2spec_engine/results.py
.flow-engine/scripts/brs2spec_engine/state.py
.flow-engine/scripts/brs2spec_engine/repair.py
```

## What to implement

### 1. `engine_cli.py`

Create a minimal Python CLI using only the standard library:

- use `argparse`
- support subcommands with placeholders for:
  - `instantiate-event`
  - `collect-inputs`
  - `move-event`
  - `validate-result`
  - `update-state`
  - `repair-processing`
  - `repair-chain`
  - `reset-to-phase`

For now, each subcommand may call a stub function that raises `NotImplementedError`
with a clear message.

### 2. Package modules

In each module, add:

- a short module docstring
- a placeholder function or dataclass that defines the intended responsibility
- only standard-library imports unless an existing dependency is already present in the repo

### 3. Shared design conventions

Use these conventions from the start:

- Python 3.11+ compatible syntax only
- no external dependency added in this step
- ASCII only
- type hints on public functions
- paths handled with `pathlib.Path`

## Output expectation

This step is only scaffolding. Do not implement real engine behavior yet.

## Verification

After the change, verify:

1. all target files exist
2. `python .flow-engine/scripts/engine_cli.py --help` works
3. the listed subcommands appear in help output
4. there are no imports from non-existent local modules
