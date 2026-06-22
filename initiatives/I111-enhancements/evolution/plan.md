# Framework Evolution Plan

## Goal

Evolve `.b2s` from a strong staged prompt runner into a richer action-driven
framework where each action can explicitly declare:

- required and optional inputs
- context policies
- prompt family and skill
- output template
- validation rules
- human gate behavior

## Important constraint

Do not remove or rewrite the framework's identity.

- keep `.b2s/workflow/stage-actions.yaml` as the action registry
- keep existing prompts available as the default path
- keep current initiatives compatible
- add new behavior in an additive, opt-in way

## What already exists

The current engine already provides much of the orchestration spine:

- staged actions
- input collection
- selected skill execution
- template enforcement
- validation pass/fail flow
- stateful next-step resolution
- human gates

## What this enhancement adds

1. A richer action contract
2. Policy-aware input collection and prompt placeholders
3. Named validation rule catalogs
4. Prompt-family routing and fallback rules
5. A policy library structure
6. Additional enterprise coverage where gaps are proven after overlap analysis
7. Documentation, migration notes, and tests

## Ordered implementation prompts

| # | Prompt | Purpose |
|---|---|---|
| 01 | `01-action-contract-v2.md` | Extend the action schema without breaking old actions |
| 02 | `02-input-policies-and-placeholder-contract.md` | Resolve policies and expose them to prompts |
| 03 | `03-validator-rule-catalog.md` | Move from opaque validation to named reusable rules |
| 04 | `04-prompt-family-resolution.md` | Allow one framework to orchestrate multiple prompt families |
| 05 | `05-policy-library-and-phase-mapping.md` | Create the policy structure and map it to phases |
| 06 | `06-enterprise-coverage-actions.md` | Add missing NFR and AI handoff coverage as additive actions |
| 07 | `07-docs-migration-and-golden-example.md` | Update docs and provide a reference configuration |
| 08 | `08-tests-and-backward-compatibility.md` | Lock in non-breaking behavior with tests |

## Non-goals

- do not replace the staged workflow model
- do not delete native `.b2s` prompts
- do not force every action to use external prompt families
- do not require migration of all existing actions in one pass

## Success criteria

- existing workflows still run
- old actions remain valid
- new actions can declare policies and prompt families
- prompts receive resolved policy and input placeholders
- validators can report named rule failures
- docs show how to mix `.b2s`, `SpecKit`, `BMAD`, and `HVE` styles safely
