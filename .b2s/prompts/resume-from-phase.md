# `.b2s` Resume From Phase

## Purpose

This prompt is the human-facing companion to reset and repair. It explains how
to resume safely from a chosen stage once state has been repaired or reset.

## Resume Flow

1. if state is inconsistent, run `repair-state`
2. if only a single gate-rejected action needs to be retried (no stage rewind
   required), run `retry-action --action-id <id>` — see
   `.b2s/prompts/retry-action.md`
3. if a full stage rewind is needed, run `reset-to-phase --stage-id <target>`
4. run `next-step`
5. read `.b2s/state/next-step.json`
6. continue staged execution from the selected action

## Rules

- resuming never bypasses `next-step`
- if a gate is still pending, do not resume generation; resolve the gate first
- if validation previously failed, regenerate the artifact before attempting to advance state

## Output Files To Read

- `.b2s/state/workflow-state.json`
- `.b2s/state/next-step.json`
- `.b2s/tmp/current-state-update.json` when repair or reset was used

## Source Of Truth

Resume decisions come from staged state plus engine output files, not from memory
of prior chat steps.
