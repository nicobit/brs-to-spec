# Prompt 06 - Document Placeholder Usage

## Context

Once placeholder support exists, maintainers need clear guidance so future
prompts use the contract consistently.

Before making changes, read these files in full:

- `framework_enhancement/14/imp2/prompt-placeholder-contract.md`
- `framework_enhancement/14/imp2/recommended-engine-changes-for-placeholder-support.md`
- the implementation changes produced by prompts 01-05

## Goal

Document how placeholder support should be used in future `.b2s` prompts and
skills.

## Required work

1. Add or update framework documentation describing:
   - the supported placeholder names
   - what each placeholder means
   - how list placeholders are rendered
   - when prompts should use resolved placeholders instead of hardcoded paths
2. Add a short migration note for older prompts that still use hardcoded path
   instructions.
3. Document the distinction between:
   - diagnostic input structures
   - prompt-facing placeholder structures

## Important rules to document

- do not use `matches` in prompt-facing placeholder names
- do not flatten list placeholders into comma-separated strings
- prefer resolved placeholders for actual reading instructions
- keep action-specific generation guidance separate from placeholder path wiring

## Done criteria

- [ ] Placeholder contract is documented in a maintainable location
- [ ] Future prompt authors have clear usage rules
- [ ] Migration boundary between old prompts and new placeholder-driven prompts is explained
