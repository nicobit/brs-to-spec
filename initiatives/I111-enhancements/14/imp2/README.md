# Prompt Placeholder Support - Implementation Pack

This folder contains the final ordered plan and implementation prompts for
adding workflow-driven prompt placeholders to `.b2s`.

## Objective

Enable prompts and skills to consume engine-resolved workflow inputs and outputs
through a stable placeholder contract, instead of hardcoded path text.

## Final placeholder contract

The implementation in this pack is based on these prompt-facing placeholders:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

## Ordered prompts

1. `00-final-plan.md`
2. `01-add-prompt-placeholders-to-collect-inputs.md`
3. `02-add-output-placeholders-to-collect-inputs.md`
4. `03-wire-placeholder-rendering-into-workflow-execution.md`
5. `04-migrate-run-workflow-and-selected-skills.md`
6. `05-add-tests-for-placeholder-support.md`
7. `06-document-placeholder-usage.md`

## Scope boundary

- This pack does not redesign the full prompt system.
- This pack does not ingest file contents into engine state.
- This pack adds placeholder support for resolved paths and outputs.
- Prompt migration should start with a small set of representative prompts and
  then expand incrementally.
