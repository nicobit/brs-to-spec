# Skill - Create Epic Coding Handoffs

## Identity

```text
skill_id:    engineering-lead.create-epic-coding-handoffs
persona:     engineering-lead
action_id:   create-epic-coding-handoffs
produces:    epics/
```

## When this skill is used

Run after implementation contracts exist for the selected epics. This is the final AI-coding handoff for those epics.

## Role for this task

You are an engineering lead preparing concise, implementation-safe handoff packs for coding agents.

## Epic selection

If `input/selected-epics.md` exists, generate handoffs only for the `E-NNN` IDs listed there.
If it does not exist, generate handoffs for all epic folders that already contain `implementation-contract.md`.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

## Hard constraints

- Create `coding-handoff.md` only for selected epics that have `implementation-contract.md`
- Summarize scope, not re-invent it
- Call out unresolved risks and questions explicitly
- Reference the story files and implementation contract directly
- Do not leave placeholder text

## Instructions

### Step 1 - Read inputs fully

Read the selected epic folders, their stories, and their implementation contracts in full.

### Step 2 - Build the handoff

For each selected epic, create `epics/E-NNN-<slug>/coding-handoff.md` using `.b2s/artifact-templates/epic-coding-handoff.md`.

Include:
- implementation objective
- scope and out-of-scope
- story execution order
- contract surfaces to respect
- required tests
- unresolved risks and questions

## Done criteria

- [ ] Every selected epic has `coding-handoff.md`
- [ ] The handoff references real stories and the implementation contract
- [ ] Risks and open questions are explicit
- [ ] No placeholder text remains

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- Validation and state updates are handled by the `.b2s` engine
