# Script Architecture Proposal

## Overview

Introduce a small Python package for engine mechanics, for example under:

```text
.flow-engine/scripts/
  brs2spec_engine/
    __init__.py
    workspace.py
    templates.py
    inputs.py
    queue.py
    results.py
    state.py
    repair.py
```

And a small CLI entrypoint:

```text
.flow-engine/scripts/engine_cli.py
```

## Module responsibilities

### `workspace.py`

Owns:

- detecting the active initiative workspace
- resolving relative event paths against workspace root
- normalizing path separators
- rejecting paths outside the workspace

Why:

- removes ambiguity about whether `input/brs.md` means repo-root or workspace-root

### `templates.py`

Owns:

- loading event templates
- validating template existence
- mapping template fields to runtime event fields
- preserving:
  - `must_include`
  - `validation_rules`
  - `on_success`
  - `on_failure`
  - `meta.template_id`

Why:

- prevents broken runtime events like the malformed `EVT-00002` we observed

### `inputs.py`

Owns:

- resolving `read_from`
- expanding globs
- checking required vs optional inputs
- generating authoritative `read_evidence`

Why:

- prevents fabricated “BRS empty” failures when the file was never read

### `queue.py`

Owns:

- selecting events from `pending/`
- moving event files through `pending -> processing -> done/failed`
- orphan cleanup
- processing-folder recovery

Why:

- makes queue transitions real and consistent instead of partly prompt-reconstructed

### `results.py`

Owns:

- parsing result files
- validating:
  - `status`
  - `artifacts_written`
  - `validation_notes`
  - `read_evidence`
  - natural-language validation entry presence
- flagging contradictory or incomplete results

Why:

- turns result-file correctness into a deterministic check

### `state.py`

Owns:

- updating `workflow-state.json`
- appending `event-log.jsonl`
- writing `open-decisions.md`
- enforcing consistency between state and event outcomes

Why:

- prevents “event log says failed, queue/state still says active” drift

### `repair.py`

Owns:

- repair-processing
- repair-chain
- reset-to-phase
- queue rebuilds after corruption

Why:

- these are deterministic maintenance operations and are strong script candidates

## CLI shape

The CLI should be command-oriented, not one giant script.

Example:

```text
python .flow-engine/scripts/engine_cli.py instantiate ...
python .flow-engine/scripts/engine_cli.py collect-inputs ...
python .flow-engine/scripts/engine_cli.py move-event ...
python .flow-engine/scripts/engine_cli.py validate-result ...
python .flow-engine/scripts/engine_cli.py update-state ...
python .flow-engine/scripts/engine_cli.py repair-processing ...
```

Each command should do one deterministic thing well and emit structured output.
