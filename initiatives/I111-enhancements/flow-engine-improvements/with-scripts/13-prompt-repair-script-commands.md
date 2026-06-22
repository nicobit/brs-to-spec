# Prompt 13 — Implement Repair and Reset Script Commands

## Goal

Add the deterministic maintenance commands after the core mechanics exist.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/repair.py`

## Commands to implement

### `repair-processing`

Responsibilities:

- inspect `processing/`
- classify stale/incomplete entries
- move or delete them deterministically

### `repair-chain`

Responsibilities:

- locate the authoritative last completed event
- load its template
- instantiate any missing downstream events

### `reset-to-phase`

Responsibilities:

- back up current active state
- clear active queue folders
- rebuild queue/state at a chosen phase

## Constraints

- do not invent templates
- do not rewrite business artifacts in these commands
- preserve backup behavior for destructive state changes

## Verification

After implementation, verify:

1. repair commands operate only on queue/state mechanics
2. chain repair uses template-driven instantiation
3. reset-to-phase preserves backups and rebuilds queue consistently
