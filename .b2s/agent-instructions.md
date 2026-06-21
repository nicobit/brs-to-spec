# `.b2s` Agent Instructions

## Purpose

These instructions govern the staged `.b2s` framework.

## Core rules

- `.b2s` is a staged framework, not an event-queue framework.
- Determine work through stage actions and compact state.
- Scripts own deterministic orchestration mechanics.
- Prompts own artifact generation and business judgment.
- Load only the active skill prompt for the selected action.
- Gate progression on script-written output files, not stdout summaries.

## Runtime artifacts

Framework state for each initiative lives under:

```text
initiatives/<id>-<slug>/.b2s/
  state/
  tmp/
```

## Initial execution model

The first implementation supports exactly one active action at a time.

## Prompt loading rule

Do not load unrelated prompts or personas during execution.

## Prompt placeholder rule

When a skill prompt uses workflow-driven placeholders, prefer the engine-resolved
prompt placeholder contract over hardcoded path text.

Supported prompt-facing placeholders include:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{resolved_policy_inputs}`
- `{primary_output}`
- `{secondary_outputs}`
- `{prompt_family}`
- `{template_mode}`

Use resolved placeholders for actual read and write instructions. Do not expose
engine-internal terms like `matches` in prompt-facing placeholder names.
Policy files listed in `{resolved_policy_inputs}` are first-class generation
inputs and must be read in full before writing the artifact.

## Action contract rule

Every action is declared in `.b2s/workflow/stage-actions.yaml` and normalized by
the engine before execution.

Core action fields include:

- identity and routing: `action_id`, `stage_id`, `persona`, `skill_ref`
- output contract: `artifact_template_ref`, `outputs.primary`, `outputs.secondary`
- input contract: `inputs.required`, `inputs.optional`
- policy contract: `policy_refs`
- prompt strategy metadata: `prompt_family`
- validation contract: `validation_profile`, `validation_rules`
- progression contract: `blocked_by_stage`, `blocked_by_action`, `conditions`
- gate contract: `human_gate`

Older actions remain valid. Missing additive v2 metadata is defaulted by the
engine at load time.

## State rule

`workflow-state.json` is the source of staged orchestration truth, but only
after `state_validated` is true.

## Orchestrator rule

`run-workflow.md` defines the staged execution loop. Follow that loop exactly
and stop whenever a required engine output file is missing or reports failure.

## Gate rule

When `awaiting_human` is true, do not continue artifact generation. The only
valid next operations are gate approval, gate rejection, repair, or reset.

## Machine-file contract

The engine owns all files under `.b2s/state/` and `.b2s/tmp/`. AI agents must
never write to these paths directly.

1. **Never write to `workflow-state.json` directly.** All state changes must go
   through CLI commands (`update-state`, `approve-current-gate`,
   `reject-current-gate`, `repair-state`, `reset-to-phase`).
2. **Never write to `execution-log.jsonl` directly.** The engine owns the log
   and fingerprints every entry. Fabricated entries will be detected.
3. **Never fabricate CLI output files.** Files in `.b2s/state/` and `.b2s/tmp/`
   (`next-step.json`, `current-inputs.json`, `current-validation.yaml`,
   `current-state-update.json`, `current-gate.json`) are engine-written only.
4. **Gate approval requires the CLI.** Run `approve-current-gate` or
   `reject-current-gate`. Do not modify `awaiting_human` or `current_gate` by
   editing `workflow-state.json`.
5. **State integrity is verified.** The engine fingerprints execution log entries
   and audits them on every `dispatch-next` call. Entries written outside the
   engine are flagged as fabricated, and actions without verified engine evidence
   are flagged as ghost or unlogged.
