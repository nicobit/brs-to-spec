# .b2s Evolution Prompt Set

This folder contains an ordered enhancement package for evolving the `.b2s`
workflow engine without replacing the current framework or deleting existing
prompts.

## Intent

The target model is:

```text
phase
  -> inputs
  -> context policies
  -> prompt
  -> template
  -> artifact
  -> validation
  -> gate
```

The implementation approach is additive:

- keep the staged engine
- keep existing actions and prompts working
- enrich the action contract
- add policy-aware input resolution
- add named validation rules
- add pluggable prompt families per artifact type

## Recommended order

1. `01-action-contract-v2.md`
2. `02-input-policies-and-placeholder-contract.md`
3. `03-validator-rule-catalog.md`
4. `04-prompt-family-resolution.md`
5. `05-policy-library-and-phase-mapping.md`
6. `06-enterprise-coverage-actions.md`
7. `07-docs-migration-and-golden-example.md`
8. `08-tests-and-backward-compatibility.md`

## Outcome

After completing this sequence, `.b2s` should still run current workflows, but
it should also support richer action definitions and selective use of different
prompt families such as native `.b2s`, `SpecKit`, `BMAD`, and `HVE`.
