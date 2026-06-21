# Prompt 07 - Document the Evolution and Add a Golden Example

## Context

Once the engine supports richer action definitions, the framework needs a clear
reference example. This prompt updates the docs and provides a concrete action
set showing how mixed prompt families and policy-aware actions should look.

## Step 1 - Update the core docs

Review and update the most relevant framework documentation, likely including:

- `.b2s/agent-instructions.md`
- `.b2s/module-index.md`
- `.b2s/prompts/run-workflow.md`
- repository docs that explain how `.b2s` works

The docs should explain:

- what an action definition contains now
- how policies are resolved
- how prompt families work
- how validation rules are declared
- how old actions remain compatible

## Step 2 - Create a golden action example

Create a compact example document under a suitable framework doc path showing a
fully enriched action definition, for example:

- business intake
- requirements
- architecture review
- AI coding handoff

Each example should show:

- inputs
- policy refs
- prompt family
- template ref
- validation rules
- gate behavior

## Step 3 - Add a migration guide

Write a short migration guide for maintainers that explains:

1. how to leave an old action unchanged
2. how to upgrade an action to v2 metadata
3. how to add policies
4. how to add a named validation rule
5. how to opt into a non-native prompt family

Keep it short and concrete.

## Step 4 - Add a phase-to-family map

Create one simple reference table showing the intended default family direction:

- business intake -> `b2s`
- requirements -> `speckit`
- architecture -> `b2s` plus `arc42`/`ADR` influence
- epics/features -> `bmad`
- stories/handoff -> `hve`

Treat this as guidance, not a hardcoded restriction.

## Done criteria

- [ ] core docs describe the richer action model
- [ ] a golden example exists
- [ ] maintainers have a migration guide
- [ ] the phase-to-family strategy is documented clearly
