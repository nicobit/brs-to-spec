---
description: Re-execute the last completed action for the active initiative, discarding its artifact and re-running the skill from scratch.
---

**You** are the executor. Do not modify state manually. Do not copy or patch the previous artifact.

Use this when the last completed action produced a poor-quality artifact and you want to regenerate it — without rejecting a gate and without resetting the entire stage.

**Cannot be used** when the action status is `accepted` (human-approved). In that case use `reject-current-gate` first, then `retry-action`.

## Steps

1. Identify the active initiative workspace (`initiatives/<id>-<slug>/`).
2. Run:
   ```
   python .b2s/scripts/b2s_cli.py rerun-last-action --workspace-root <WORKSPACE_ROOT>
   ```
3. Read `.b2s/tmp/current-state-update.json` (written to `rerun-last-action.json` in tmp).
   - Verify `overall == pass` and `applied_changes.action_reopened` is the expected action.
   - If `overall != pass`, stop and surface the error.
4. Read `.b2s/prompts/run-workflow.md` in full.
5. Follow its Execution Sequence from step 7 (`collect-inputs`) — the action is already selected; skip steps 1–6.
6. Generate the artifact from scratch using the skill prompt. Do not reuse or patch the previous version.
7. After `update-state`, if a human gate reopens (`awaiting_human: true`), stop and report — do not self-approve.

## Stop conditions

- `rerun-last-action` CLI exits with an error (action is `accepted` or no last action recorded)
- Required inputs are missing
- Validation fails and cannot be self-corrected
- Human gate opens
