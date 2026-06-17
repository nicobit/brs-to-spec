# `.b2s` List Actions

## Purpose

Show every action in the staged workflow for the active initiative, with its
current status, next pointer, and human gate flag. Read-only — writes nothing.

## Execution Sequence

1. Identify the active initiative workspace — record its absolute path as WORKSPACE_ROOT.
2. Run `list-actions --workspace-root WORKSPACE_ROOT`.
   - Pass `--stage-id <id>` if the user asked to filter by phase.
3. Read the stdout output.
4. Present it to the user as-is. Do not paraphrase, reorder, or summarise.

## Optional filter

If the user supplied a phase name or stage ID (e.g. "planning", "3-planning"),
map it to the canonical stage ID and pass it as `--stage-id`.

Recognised stage IDs:
- `0-routing`
- `2-business-intake`
- `2b-business-analysis`
- `3-planning`
- `4-engineering-readiness`
- `4b-quality-gates`
- `5-handoff`
- `6-review-package`

## Stop condition

Stop immediately after printing the output. Do not run any other command.
Do not offer to execute any action shown in the list.
