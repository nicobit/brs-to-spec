# `.b2s` Reset To Phase

## Purpose

This prompt rewinds `.b2s` state to a chosen stage boundary so work can restart
from that stage without event buckets.

## When To Use

Use this when:

- an upstream artifact changed and downstream artifacts must be reconsidered
- the user wants to restart from a known stage boundary
- staged state must be downgraded safely without deleting the full workspace

## Required Behavior

1. choose the target `stage_id`
2. run `reset-to-phase --stage-id <target>`
3. back up current staged state before rewinding
4. clear downstream action and artifact progression from the target stage onward
5. set `next_action` to the first executable non-gate action in the target stage
6. read `.b2s/tmp/current-state-update.json`

## Rules

- reset rewinds compact staged truth; it does not delete business artifacts by default
- always create a staged state backup first
- do not rewind to an invented stage ID
- after reset, the next step must be mechanically selectable again

## Output Files

- `.b2s/tmp/current-state-update.json`
- backup file under `.b2s/state/backups/`
- updated `.b2s/state/workflow-state.json`

## Script Authority

The `reset-to-phase` script owns the rewind mechanics and the backup.
