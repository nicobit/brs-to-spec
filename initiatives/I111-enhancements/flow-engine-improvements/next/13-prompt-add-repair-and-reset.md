# Prompt 13 - Add Repair and Reset Commands

## Goal

Add deterministic maintenance commands after the core mechanics are stable.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/repair.py`
- any small shared helper modules only if needed

## Commands to implement

### `repair-processing`

Responsibilities:

- inspect `processing/`
- detect stale event/result combinations
- move or clean them using deterministic rules

### `repair-chain`

Responsibilities:

- identify the authoritative last completed event
- inspect expected downstream events from the template chain
- instantiate missing ones without inventing template data

### `reset-to-phase`

Responsibilities:

- create a backup of active state
- clear active queue folders safely
- rebuild queue and workflow state from the chosen phase boundary

## Hard rules

- never rewrite business artifacts in these commands
- preserve backups before destructive state changes
- rebuild from authoritative template and state data only
- if a repair/reset command emits a decision artifact, write it to a fixed output
  path rather than relying on stdout-only behavior

## Verification

Verify:

1. repair commands act only on queue/state mechanics
2. reset creates a backup before clearing active state
3. chain repair recreates missing events from templates, not from guesswork
