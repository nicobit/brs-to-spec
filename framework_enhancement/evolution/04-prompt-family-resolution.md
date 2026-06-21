# Prompt 04 - Add Pluggable Prompt Family Resolution

## Context

The framework should orchestrate multiple prompt families without losing its own
staged identity. The goal is not to replace native `.b2s` prompts. The goal is
to let an action declare which prompt family it draws from.

## Step 1 - Read current skill loading behavior

Read these files in full:

- `.b2s/scripts/b2s_engine/dispatch.py`
- `.b2s/module-index.md`
- `.b2s/prompts/run-workflow.md`

Inspect how `skill_ref` is currently resolved and loaded.

## Step 2 - Define the routing model

Implement a lightweight model where an action can declare:

```yaml
prompt_family: b2s
skill_ref: ".b2s/skills/product-owner/create-requirements.md"
```

Later-compatible family values should include:

- `b2s`
- `speckit`
- `bmad`
- `hve`

The engine does not need to understand external frameworks semantically. It only
needs to resolve prompt assets cleanly and predictably.

Important constraint for this enhancement pass:

- `prompt_family` is metadata first
- do not reorganize the existing skill tree in the first implementation
- keep current `skill_ref` paths valid
- family-aware physical folder restructuring, if still desired later, should be
  treated as a separate follow-on enhancement

## Step 3 - Preserve current paths and document future conventions

For this implementation:

- preserve the current persona-based skill layout
- do not move existing skill files
- do not rewrite all `skill_ref` values
- use `prompt_family` to describe the source style or strategy, not to force a
  filesystem migration

If you document a future folder convention for prompt families, mark it clearly
as a future option rather than a required implementation step.

## Step 4 - Add fallback behavior

If an action declares a non-`b2s` prompt family but the referenced skill file is
missing, fail clearly unless a compatibility fallback is declared.

If `compatibility.fallback_skill_ref` is present, use it and record that a
fallback occurred.

## Step 5 - Seed the phase mapping

Update representative actions so the intended family direction is explicit:

- requirements -> `speckit`
- epics or features -> `bmad`
- stories or handoff -> `hve`
- business intake -> `b2s`

If the corresponding actions do not exist yet, document the target mapping in
comments or docs and seed only the actions that already exist.

Do not fabricate new action types in this prompt just to demonstrate family
usage. Keep this prompt limited to routing metadata and compatibility behavior.

## Step 6 - Update documentation

Document that `.b2s` is an orchestration framework with pluggable prompt
families, not a single-prompt ideology.

## Done criteria

- [ ] actions can declare a prompt family
- [ ] existing `skill_ref` loading still works
- [ ] fallback behavior is explicit
- [ ] docs explain the mixed-family design clearly
