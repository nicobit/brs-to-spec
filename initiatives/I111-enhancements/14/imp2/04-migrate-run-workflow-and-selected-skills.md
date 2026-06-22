# Prompt 04 - Migrate run-workflow and Selected Skills

## Context

The engine support is only useful if prompts begin consuming the new contract.
Migration should start with a small representative set rather than trying to
rewrite all prompts at once.

Before making changes, read these files in full:

- `.b2s/prompts/run-workflow.md`
- `.b2s/skills/product-owner/create-business-intake-summary.md`
- `.b2s/skills/delivery-lead/create-delivery-structure.md`
- `framework_enhancement/14/imp2/placeholder-contract-example-create-business-intake-summary.md`
- `framework_enhancement/14/imp2/placeholder-contract-example-create-delivery-structure.md`

## Goal

Update the orchestration prompt and a small set of representative skills to use
the new placeholder contract.

## Required work

1. Update `.b2s/prompts/run-workflow.md` so the reading and writing instructions
   are compatible with the placeholder model.
2. Update `create-business-intake-summary` to use:
   - `{resolved_required_inputs}`
   - `{resolved_optional_inputs}`
   - `{primary_output}`
3. Update `create-delivery-structure` to use:
   - `{resolved_required_inputs}`
   - `{resolved_optional_inputs}`
   - `{primary_output}`
   - `{secondary_outputs}`

## Rules

- Preserve the action-specific behavioral guidance in each skill
- Replace hardcoded path-reading instructions where the placeholder contract now
  covers them
- Do not over-generalize the skill content beyond what the placeholder contract
  supports

## Migration principle

This prompt is for initial migration only. Do not attempt a repo-wide rewrite of
all skills in one pass.

## Done criteria

- [ ] `run-workflow.md` is compatible with placeholder-driven input/output guidance
- [ ] `create-business-intake-summary` consumes placeholder-driven paths
- [ ] `create-delivery-structure` consumes placeholder-driven paths
- [ ] Action-specific generation instructions remain intact
