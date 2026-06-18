# `.b2s` Run Action

## Purpose

Re-execute any named action for the active initiative, discarding its current
artifact and regenerating it from scratch. Works on any action whose status is
`not_run`, `ai_validated`, or `failed`. Blocked on `accepted` (human-approved)
— use `reject-current-gate` first in that case.

## When To Use

Use this when:

- a specific action produced a poor-quality artifact and you want to redo it
- an action was skipped or stale and you want to force it to run now
- you want to redo any action by name, not just the most recent one

Do not use this when:

- the action status is `accepted` — use `reject-current-gate` then `run-action`
- you want to rewind an entire stage — use `reset-to-phase` instead

## Execution Sequence

1. Identify the active initiative workspace — record its absolute path as WORKSPACE_ROOT.
2. Identify the action ID from the user's request.
   - If unclear, run `list-actions --workspace-root WORKSPACE_ROOT` and ask the user to confirm.
3. Run:
   ```
   python .b2s/scripts/b2s_cli.py run-action --workspace-root WORKSPACE_ROOT --action-id <action_id>
   ```
4. Read the output JSON (written to `.b2s/tmp/run-action.json`).
   - If `overall != pass`, stop and surface the error (e.g. action is `accepted`).
5. Read `.b2s/prompts/run-workflow.md` in full.
6. Follow its Execution Sequence from step 7 (`collect-inputs`) — the action is
   already selected in state; skip steps 1–6.
7. Generate the artifact from scratch using the skill prompt. Do not reuse or
   patch the previous version.
8. After `update-state`, if a human gate opens (`awaiting_human: true`), stop
   and present the artifact for review — do not self-approve.

## Stop Conditions

- `run-action` CLI exits with an error (action is `accepted` or unknown)
- Required inputs are missing
- Validation fails after generation
- Human gate opens — wait for user approval before continuing
