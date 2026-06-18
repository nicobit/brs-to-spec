# `.b2s` Run Workflow

## Purpose

This prompt orchestrates the staged `.b2s` workflow by delegating deterministic
mechanics to scripts and limiting prompt work to one selected artifact action at
a time.

## Runtime Rules

- `.b2s` is staged, not event-driven
- exactly one active action is allowed at a time
- script-written output files are authoritative
- stdout summaries are never gating truth
- load only the selected skill prompt for the selected action
- do not preload unrelated personas, prompts, or templates

## Execution Sequence

Use this sequence exactly:

1. Identify active initiative workspace — record its absolute path as WORKSPACE_ROOT.
2. Read `WORKSPACE_ROOT/.b2s/state/workflow-state.json` in full.
3. Run `next-step --workspace-root WORKSPACE_ROOT`.
4. Read `WORKSPACE_ROOT/.b2s/state/next-step.json` in full.
5. Branch on the result — **you must follow the correct branch, no exceptions**:

   **Branch A — `overall == pass` and `selected_action` is non-null → action is ready:**
   Go to step 7 (collect inputs and execute).

   **Branch B — `overall == pass` and `selected_action` is null → workflow is complete:**
   Stop. Report "Workflow complete — no further actions."

   **Branch C — `overall == fail` → workflow is blocked:**
   Do NOT stop. You MUST execute the Blocked Diagnosis Protocol below before reporting anything.
   After diagnosis, either recover and continue, or report the diagnosis result and stop.

6. [Branch C only] **Blocked Diagnosis Protocol** — execute all steps:
   a. Note `current_stage` and `blocked_reason` from `workflow-state.json`.
   b. Read `WORKSPACE_ROOT/.b2s/workflow/stage-actions.yaml` in full.
   c. The `blocked_reason` names a stage (e.g. "stage `6-review-package` is incomplete").
      That stage is the SYMPTOM. The CAUSE is a prerequisite stage that has not completed.
      Find which earlier stage is blocking it: look at `blocked_by_stage` for each action
      in the named stage — that earlier stage is where the real problem is.
      If no `blocked_by_stage`, the named stage itself is the cause.
   d. For each action in the CAUSE stage, read its `action_id`, `conditions`, `outputs.primary`,
      and check `action_status` from `workflow-state.json`.
   e. Classify each action in the CAUSE stage:
      - `skipped` — conditions do not pass for this initiative's delivery_mode/execution_mode; expected, not the cause
      - `already_done` — action_status is `ai_validated` or `accepted`; not the cause
      - `needs_execution` — action_status is `not_run`, conditions pass, output artifact does NOT exist on disk
      - `stale` — action_status is `not_run`, conditions pass, output artifact EXISTS on disk (was reset)
      - `failed` — action_status is `failed`
   f. Report which stage is the CAUSE and the classification for each action in it.
   g. Act on the first non-skipped, non-already_done action found in the CAUSE stage:
      - `needs_execution` → execute it: go to step 7 with this action_id
      - `stale` → run `validate-artifact --action-id <id>` then `update-state --action-id <id>`; then go to step 3
      - `failed` → stop and report: human intervention required to retry this action
   h. If all actions in the CAUSE stage are `skipped` or `already_done` → the stage is genuinely
      complete but the engine does not know it. Run `repair-state --workspace-root WORKSPACE_ROOT`
      to rebuild action statuses from disk, then go to step 3.
   i. Only stop with "blocked" if repair-state was tried and the workflow is still blocked.

7. Run `collect-inputs --workspace-root WORKSPACE_ROOT` (use `--action-id` if recovering a specific action).
8. Read `WORKSPACE_ROOT/.b2s/tmp/current-inputs.json` in full.
9. If `overall != pass`, stop and surface the missing required inputs.
9b. For every entry in `required_inputs` and `optional_inputs` where `exists == true`,
    read the file at `WORKSPACE_ROOT/{match}` in full before proceeding.
    Do not start generating until every input file has been read.
10. Load only the selected skill prompt from the `skill_ref` path in `stage-actions.yaml`.
11. Load the referenced artifact template only as the output shape contract.
12. Generate or update the target artifact(s), writing to `WORKSPACE_ROOT/{output_path}`.
13. Run `validate-artifact --workspace-root WORKSPACE_ROOT`.
14. Read `WORKSPACE_ROOT/.b2s/tmp/current-validation.yaml` in full.
15. If validation fails, stop and surface the failures — do not run `update-state`.
16. Run `update-state --workspace-root WORKSPACE_ROOT`.
17. Read `WORKSPACE_ROOT/.b2s/tmp/current-state-update.json` in full.
18. If a human gate was opened (`awaiting_human: true` in `current-state-update.json`):
    a. Read the primary output artifact in full.
    b. Present the artifact content to the user as a readable summary (not raw markdown dump).
    c. State the gate owner and gate ID from the state update.
    d. Ask the user explicitly:
       > **Review required** — [gate_owner] gate: [gate_id]
       > Please review the artifact above and reply with one of:
       > - **approve** — to accept and continue to the next action
       > - **reject: <justification>** — to mark it failed and stop
    e. Do not advance state further. Wait for the user's response.
19. Stop — report what action ran, what artifact was produced, and what `next_action` is.

## Prompt Loading Rule

When an action is selected:

- read `.b2s/workflow/stage-actions.yaml` only as needed to resolve that action
- load exactly one skill file from `.b2s/skills/...`
- use `.b2s/artifact-templates/...` only as the output structure contract
- do not open or synthesize other skill prompts for convenience

## Gate Handling

- if `workflow-state.json` shows `awaiting_human: true`, do not continue artifact generation
- use `approve-current-gate` or `reject-current-gate` to continue
- do not self-approve a gate inside this workflow prompt

## Failure Handling

- if any required machine-written file is missing, stop immediately
- if validation says `fail`, do not run `update-state`
- if state says the workflow is blocked, diagnose before stopping:
  1. read `workflow-state.json` — find `current_stage` and `blocked_reason`
  2. read `.b2s/workflow/stage-actions.yaml` — find which stage is blocking and list its actions
  3. for each action in that stage, check:
     - its `action_status` in `workflow-state.json` (not_run / ai_validated / accepted / failed)
     - whether its output artifact exists on disk at `WORKSPACE_ROOT/{output_path}`
     - whether its conditions pass given current state fields (`delivery_mode`, `execution_mode`, etc.)
  4. classify each action as one of:
     - `skipped` — conditions do not pass; this is expected and not the cause
     - `already_done` — status is ai_validated or accepted; not the cause
     - `needs_execution` — status is not_run but conditions pass and output missing; THIS is the cause
     - `stale` — status is not_run but output artifact already exists on disk; was reset, needs revalidation
     - `failed` — status is failed; needs retry
  5. report the diagnosis clearly: which action is the blocker and its classification
  6. if classification is `needs_execution`: execute that action now (load its skill, generate artifact, validate, update-state) instead of stopping
  7. if classification is `stale`: run `validate-artifact --action-id <id>` then `update-state --action-id <id>` to recover without regenerating
  8. if classification is `failed`: report and stop — human intervention required
  9. only stop with "blocked" if no action can be executed or recovered

## Required Machine Files

- `.b2s/state/next-step.json`
- `.b2s/tmp/current-inputs.json`
- `.b2s/tmp/current-validation.yaml`
- `.b2s/tmp/current-state-update.json`
- `.b2s/tmp/current-gate.json` when a gate decision command is used

## One Thin-Slice Example

Example staged path on paper:

1. `next-step` selects `route-initiative`
2. `collect-inputs` confirms `input/brs.md`
3. only `route-initiative.md` is loaded
4. `routing/routing-decision.md` is generated
5. `validate-artifact` verifies the routing artifact
6. `update-state` sets routing artifact status and next action
7. reassessment selects `create-business-intake-summary`

## Source Of Truth

The orchestrator trusts:

- `workflow-state.json` for staged state
- `stage-actions.yaml` for action definitions
- machine-written output files from the engine commands

It does not trust:

- freehand prompt summaries
- guessed next actions
- implied gate status
