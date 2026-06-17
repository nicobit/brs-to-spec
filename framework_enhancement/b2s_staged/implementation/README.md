# `.b2s` Implementation Prompts

## Purpose

This folder converts the staged-framework analysis into an implementation-ready
prompt set for building a new `.b2s/` framework.

The target is:

- staged orchestration like `_.brs2spec`
- artifact quality and output shape like `.brs2spec2`
- script-owned deterministic mechanics

## What this folder contains

- `00-implementation-plan.md` - overall build strategy
- `01-target-structure.md` - target `.b2s/` file and folder layout
- `02-stage-action-model.md` - how stage actions replace event templates
- `03-script-command-surface.md` - required script commands
- `04-prompt-adaptation-strategy.md` - how to adapt `.brs2spec2` prompts
- `04a-output-file-contracts.md` - required schemas for script outputs
- `04b-state-and-gate-model.md` - workflow-state and gate-state contract
- `05-prompt-scaffold-b2s-core.md`
- `06-prompt-define-stage-actions-and-state.md`
- `07-prompt-port-artifact-templates.md`
- `08-prompt-port-and-adapt-skill-prompts.md`
- `09-prompt-implement-next-step-and-inputs.md`
- `10-prompt-implement-validation-and-state-update.md`
- `11-prompt-implement-run-workflow-orchestrator.md`
- `12-prompt-implement-repair-reset-and-gates.md`
- `13-prompt-verify-b2s-with-fixtures.md`
- `14-prompt-strengthen-upstream-skill-prompts.md`
- `15-prompt-deepen-artifact-validation.md`
- `16-prompt-add-single-action-retry.md`
- `17-prompt-clean-workflow-model-and-reset-semantics.md`

## Recommended starting point

Start with `05-prompt-scaffold-b2s-core.md`.

That prompt creates the `.b2s/` foundation that all later prompts assume
already exists.

## Precondition

Before executing `05`, review and keep aligned:

- `02-stage-action-model.md`
- `03-script-command-surface.md`
- `04a-output-file-contracts.md`
- `04b-state-and-gate-model.md`

These files define the contracts that later prompts must not improvise.
