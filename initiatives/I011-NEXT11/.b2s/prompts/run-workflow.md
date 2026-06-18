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
- load only the selected skill prompt from `.b2s/skills/...`
- do not preload unrelated personas, prompts, or templates

## Execution Sequence

Use this sequence exactly:

1. identify active initiative workspace — record its absolute path as WORKSPACE_ROOT
   (e.g. `C:/Users/nicol/source/brs-to-spec/initiatives/I0101-NEW`)
2. read staged state
3. run `next-step`
4. read `.b2s/state/next-step.json`
5. if `overall != pass`, stop and surface `blocking_reason`
6. if `selected_action` is null, stop because the workflow is complete
7. run `collect-inputs`
8. read `.b2s/tmp/current-inputs.json`
9. if `overall != pass`, stop and surface missing required inputs
9b. for every entry in `required_inputs` and `optional_inputs` where `exists == true`,
    read the file at `WORKSPACE_ROOT/{match}` in full before proceeding —
    e.g. if WORKSPACE_ROOT is `C:/Users/nicol/source/brs-to-spec/initiatives/I0101-NEW`
    and match is `business-analysis/requirements.md`, read
    `C:/Users/nicol/sourcers-to-spec/initiatives/I0101-NEW/business-analysis/requirements.md`.
    Do not start generating until every input file has been read and its content is in context.
    Record each file read in `read_evidence`.
10. load only the selected skill prompt from `.b2s/skills/...`
11. load the referenced artifact template only as the output shape contract
12. generate or update the target artifact(s) writing to WORKSPACE_ROOT/{output_path}
13. run `validate-artifact`
14. read `.b2s/tmp/current-validation.yaml`
15. if validation fails, stop and surface the failures
16. run `update-state`
17. read `.b2s/tmp/current-state-update.json`
18. if a human gate was opened, stop and wait for gate approval or rejection
19. reassess from step 2 or stop

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
- if state says the workflow is blocked, stop and surface the blocking reason

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
