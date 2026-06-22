# Implementation Sequence

## Sequence goal

Deliver value in slices that each reduce a real observed failure mode.

## Step 1 - Scaffold engine core

Create:

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/`

Include modules for:

- workspace
- templates
- inputs
- queue
- results
- state
- repair

Also decide and document the shared script output convention and fixture
directory before implementing behavior.

## Step 2 - Implement runtime instantiation

Implement `instantiate-event`.

Why here:

- malformed runtime events poison every downstream step

## Step 3 - Implement input collection

Implement `collect-inputs`.

Why here:

- this directly addresses fabricated "input missing" failures

## Step 4 - Implement queue moves

Implement `move-event`.

Why here:

- this removes copy/recreate drift and stale `processing/` state

## Step 5 - Implement integrity checks

Implement `check-integrity` and run it before dispatch continues.

Why here:

- it catches dispatcher bypass before more artifacts chain from bad state

## Step 6 - Implement result validation

Implement:

- `validate-result`
- `validate-artifact-counts`
- `validate-no-placeholders`

Why here:

- this moves mechanical validation out of the LLM

## Step 7 - Update template validation anchors

Tighten `must_include` items for intake and requirements-producing events.

Why here:

- prompts should be forced to explain counts explicitly even before script
  output is summarized

## Step 8 - Implement state updates

Implement `update-state`.

Why here:

- once event and result truth are reliable, state can safely derive from them

## Step 9 - Wire dispatcher prompts to commands

Update prompt files to call scripts for deterministic mechanics.

At this step, wire dispatcher gating to required output files rather than
stdout parsing or advisory text.

## Step 10 - Add maintenance commands

Implement:

- `repair-processing`
- `repair-chain`
- `reset-to-phase`

## Recommendation

If the work is split across branches, Step 1 through Step 5 should be one first
delivery slice. That is the highest leverage package.
