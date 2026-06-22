# `.b2s` Run Workflow

## Purpose

This prompt orchestrates the staged `.b2s` workflow. The engine (Python CLI) handles
all state management. You handle only artifact generation.

## Critical Rule — CLI Commands Are Mandatory

Every step below that says "Run" means: **execute the Python CLI command using your shell tool.**

```
python .b2s/scripts/b2s_cli.py <command> --workspace-root WORKSPACE_ROOT
```

You MUST run these commands via your shell tool. Do NOT:
- Skip CLI commands and write state files manually
- Fabricate `.b2s/tmp/` output files — they are produced ONLY by the CLI
- Tell the user to run commands — run them yourself
- Guess what `next-step`, `validate-artifact`, or `update-state` would return

The CLI produces machine files. You read those files. That is the contract.

## Execution Sequence

1. Identify the active initiative workspace — record its absolute path as `WORKSPACE_ROOT`.

2. Read `WORKSPACE_ROOT/.b2s/state/workflow-state.json` in full.

3. **Run CLI:**
   ```
   python .b2s/scripts/b2s_cli.py next-step --workspace-root WORKSPACE_ROOT
   ```

4. Read `WORKSPACE_ROOT/.b2s/state/next-step.json` in full.

5. Branch on the result:

   **Branch A — `overall == pass` and `selected_action` is non-null:**
   Note the `selected_action`. If `current_item` is present, this is a per-item action —
   the engine wants you to process only that one item (e.g., one epic). Go to step 7.

   **Branch B — `overall == pass` and `selected_action` is null:**
   Stop. Report "Workflow complete — no further actions."

   **Branch C — `overall == fail`:**
   Do NOT stop. Execute the Blocked Diagnosis Protocol (step 6) before reporting.

6. [Branch C only] **Blocked Diagnosis Protocol:**
   a. Note `current_stage` and `blocked_reason` from `workflow-state.json`.
   b. Read `WORKSPACE_ROOT/.b2s/workflow/stage-actions.yaml` in full.
   c. Find the CAUSE stage (look at `blocked_by_stage` on the symptom stage's actions).
   d. Classify each action in the CAUSE stage: `skipped`, `already_done`, `needs_execution`, `stale`, `failed`.
   e. Act: `needs_execution` → go to step 7; `stale` → run `validate-artifact` + `update-state` then go to step 3; `failed` → stop.
   f. If all done/skipped → run `repair-state --workspace-root WORKSPACE_ROOT`, then go to step 3.

7. **Run CLI:**
   ```
   python .b2s/scripts/b2s_cli.py collect-inputs --workspace-root WORKSPACE_ROOT
   ```

8. Read `WORKSPACE_ROOT/.b2s/tmp/current-inputs.json` in full.
   If `overall != pass`, stop — surface missing inputs.

9. Read every path listed in `{resolved_required_inputs}` in full.
   Read `{resolved_optional_inputs}` and `{resolved_policy_inputs}` if non-empty.
   If `computed_inputs` is present and non-empty, read every path listed there.
   Computed inputs contain engine-derived data that is authoritative — use it
   as the primary source and do not re-derive or override its content.
   Do not start generating until all resolved inputs are read.

10. Check `current-inputs.json` for a `current_item` field in `prompt_placeholders`.
    If present and non-null, this is a **per-item invocation** — generate output for ONLY
    that one item (e.g., only epic `E-001`). Do not generate for other items.

11. Load the skill prompt from `skill_ref` in `stage-actions.yaml`.
    If `artifact_template_ref` is non-null, read that template file.

12. **Generate the artifact(s).**
    - Write to `{primary_output}` and `{secondary_outputs}`.
    - If `current_item` is set, scope output to that item only.
    - Follow the skill prompt and template exactly.

13. **Run CLI:**
    ```
    python .b2s/scripts/b2s_cli.py validate-artifact --workspace-root WORKSPACE_ROOT
    ```

14. Read `WORKSPACE_ROOT/.b2s/tmp/current-validation.yaml` in full.

15. If validation fails — **auto-resolve protocol**:
    a. Read every failure in `current-validation.yaml` — each has `name`, `rule_name`, `detail`.
    b. For each failure, diagnose and fix:
       - `no_unknown_requirement_references`: find the unknown IDs in the artifact; either
         remove them or replace with canonical IDs from `atomic-requirements.md`.
       - `requirement_title_consistency`: read the canonical title from `atomic-requirements.md`
         and update the downstream artifact to match exactly.
       - `open_questions_propagated`: read the requirement's blocking questions / ambiguities
         from `atomic-requirements.md` and add them to the story's `## Open Questions` section.
       - `coverage_claim_matches_evidence`: re-read actual story files, rebuild the matrix from
         evidence, and recalculate summary metrics.
       - `requirement_semantics_preserved`: ensure the story's User Story, Business Context,
         and Acceptance Criteria contain keywords from the linked requirement text.
       - Any other failure: read the `detail` field for the specific issue and edit to fix.
    c. NEVER delete and recreate an artifact. Edit the specific section that failed.
    d. Go back to step 13 (re-validate).
    e. After 3 consecutive failures on the SAME rule, stop and report the unresolvable issue.

16. **Run CLI:**
    ```
    python .b2s/scripts/b2s_cli.py update-state --workspace-root WORKSPACE_ROOT
    ```

17. Read `WORKSPACE_ROOT/.b2s/tmp/current-state-update.json` in full.

18. If `awaiting_human: true` — present the artifact for review:
    a. Read the primary output artifact.
    b. Present a readable summary to the user.
    c. Ask: **approve** or **reject: reason**.
    d. Wait for user response.
    e. On **approve**: run `python .b2s/scripts/b2s_cli.py approve-current-gate --workspace-root WORKSPACE_ROOT`
    f. On **reject**: run `python .b2s/scripts/b2s_cli.py reject-current-gate --workspace-root WORKSPACE_ROOT --reason "reason"`
    g. After running the gate command, read the output and continue or stop.

19. Stop — report: action completed, artifact produced, `next_action` from state update.

## Per-Item Iteration

Some actions have `iteration_mode: per_item` in `stage-actions.yaml`. The engine handles this:

- `next-step` returns `current_item` (e.g., `"E-001"`), `pending_items`, and `total_items`
- The engine sets `current_item` in `workflow-state.json`
- `collect-inputs` includes `current_item` in `prompt_placeholders`
- You generate output for ONLY that one item
- `update-state` marks that item as done and checks if all items are complete
- If items remain, `next-step` will return the same action with the next item

**You do NOT manage per-item state.** The engine tracks which items are done.
Your job: generate output for the one `current_item` the engine gives you.

## Prompt Loading Rule

- Load exactly one skill file from `.b2s/skills/...`
- Use `.b2s/artifact-templates/...` only as the output structure contract
- Treat `{resolved_policy_inputs}` as governing constraints
- Do not open or synthesize other skill prompts

## Gate Handling

- If `workflow-state.json` shows `awaiting_human: true`, do not generate artifacts
- Use CLI commands `approve-current-gate` or `reject-current-gate` to continue
- Do not self-approve a gate

## Source of Truth

Trust:
- `workflow-state.json` for state
- `stage-actions.yaml` for action definitions
- CLI-produced files in `.b2s/tmp/` and `.b2s/state/`

Do NOT trust:
- Your own summaries of what should happen next
- Guessed action statuses
- Manually written state files
