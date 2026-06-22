# Phase 2 Implementation Plan — Ordered Script Adoption

## Goal

Convert the phase-2 design into an implementable sequence of small changes.
Each step should leave the framework in a coherent state and reduce risk before the
next step begins.

## Strategy

Start with **script-assisted orchestration**:

- scripts perform deterministic engine mechanics
- prompts still orchestrate the overall sequence
- artifact generation remains AI-owned

Do **not** attempt a full dispatcher rewrite in the first pass.

## Ordered implementation steps

### Step 1 — Scaffold the Python engine package

Create the script package structure and shared utilities:

- `.flow-engine/scripts/brs2spec_engine/__init__.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`
- `.flow-engine/scripts/brs2spec_engine/templates.py`
- `.flow-engine/scripts/brs2spec_engine/queue.py`
- `.flow-engine/scripts/brs2spec_engine/inputs.py`
- `.flow-engine/scripts/brs2spec_engine/results.py`
- `.flow-engine/scripts/brs2spec_engine/state.py`
- `.flow-engine/scripts/brs2spec_engine/repair.py`
- `.flow-engine/scripts/engine_cli.py`

Why first:

- establishes the package boundary
- prevents later scripts from inventing inconsistent helper logic

### Step 2 — Implement `instantiate-event`

Script responsibility:

- load a template
- map it to a runtime event
- preserve all template-derived fields
- assign `event_id`
- write the event into `pending/`

Why second:

- malformed runtime events are one of the most damaging observed failures

### Step 3 — Implement `collect-inputs`

Script responsibility:

- resolve `read_from`
- expand globs
- classify required vs optional inputs
- generate authoritative `read_evidence`

Why third:

- directly addresses the I012-style “file was never actually read” problem

### Step 4 — Implement `move-event`

Script responsibility:

- move event/result files between queue buckets
- enforce “exists in exactly one bucket” semantics

Why fourth:

- directly addresses the stale `processing/` and copy/recreate drift seen in I010

### Step 5 — Implement `validate-result`

Script responsibility:

- validate the result-file contract
- check `validation_notes`, `read_evidence`, and contradiction rules

Why fifth:

- makes Step 16-G deterministic

### Step 6 — Implement `update-state`

Script responsibility:

- update `workflow-state.json`
- append `event-log.jsonl`
- update `open-decisions.md`

Why sixth:

- fixes state/log drift like the one seen in I012

### Step 7 — Wire prompts to the scripts

Update the prompt layer so it stops describing low-level mechanics in prose and calls
the scripts instead.

Priority prompt wiring targets:

- `dispatch-next.md`
- `dispatch-all.md`
- `new-initiative.md`
- `restart.md`

### Step 8 — Add repair/reset script commands

Implement:

- `repair-processing`
- `repair-chain`
- `reset-to-phase`

Why last:

- these are valuable, but they depend on the core mechanics being script-owned first

## Acceptance criteria by step

### After Step 2

- no runtime event can be created without `meta.template_id`
- `must_include` and `validation_rules` counts match the template exactly

### After Step 3

- every event with `read_from` can produce machine-generated `read_evidence`

### After Step 4

- queue transitions become real moves, not copy/recreate behavior

### After Step 5

- result contract validation no longer depends only on prompt fidelity

### After Step 6

- state, log, and queue outcomes stay aligned after pass/fail

## Prompt files in execution order

1. `06-prompt-scaffold-python-engine.md`
2. `07-prompt-instantiate-event-script.md`
3. `08-prompt-collect-inputs-script.md`
4. `09-prompt-move-event-script.md`
5. `10-prompt-validate-result-script.md`
6. `11-prompt-update-state-script.md`
7. `12-prompt-wire-prompts-to-scripts.md`
8. `13-prompt-repair-script-commands.md`

## Recommendation

Implement Steps 1–4 first as one slice. That gives the best value early:

- correct event creation
- trustworthy input reads
- correct queue transitions

Then decide whether to continue to result/state scripting in the same branch or a
follow-up slice.
