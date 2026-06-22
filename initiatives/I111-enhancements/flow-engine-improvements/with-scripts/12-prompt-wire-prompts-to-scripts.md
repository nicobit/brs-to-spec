# Prompt 12 — Wire Prompt Layer to the Scripts

## Goal

Update the prompt layer so deterministic engine mechanics call scripts instead of
being described only in prose.

## Files to modify

At minimum review and update:

- `.brs2spec2/prompts/dispatch-next.md`
- `.brs2spec2/prompts/dispatch-all.md`
- `.brs2spec2/prompts/new-initiative.md`
- `.brs2spec2/prompts/restart.md`

## What to change

### Replace prompt-only mechanics with explicit script calls

Examples:

- runtime event creation → `instantiate-event`
- Step 10 input preparation → `collect-inputs`
- queue transitions → `move-event`
- result contract checks → `validate-result`
- state updates → `update-state`

### Keep prompt-owned tasks

Do not move artifact authoring into scripts in this step.

Prompts should still own:

- semantic artifact generation
- business interpretation
- natural-language judgment

## Desired outcome

Prompts become shorter and higher-level:

- ask the engine script for authoritative mechanics
- use the outputs
- focus the AI on content production

## Verification

After implementation, verify:

1. prompts no longer instruct the model to hand-copy runtime event fields
2. prompts refer to script commands for deterministic mechanics
3. artifact-generation instructions remain intact
