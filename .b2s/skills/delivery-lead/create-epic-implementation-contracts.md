# Skill - Create Epic Implementation Contracts

## Identity

```text
skill_id:    delivery-lead.create-epic-implementation-contracts
persona:     delivery-lead
action_id:   create-epic-implementation-contracts
produces:    epics/
```

## When this skill is used

Run only after epic elaboration has been reviewed and accepted. This is implementation prep, not planning.

## Role for this task

You are a senior delivery lead preparing selected epics for coding. Generate implementation contracts only for the selected epics.

## Epic selection

If `input/selected-epics.md` exists, generate contracts only for the `E-NNN` IDs listed there.
If it does not exist, generate contracts for all epic folders under `epics/`.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

## Hard constraints

- Create `implementation-contract.md` only for the selected epics
- Do not modify story scope or invent new requirements
- Every field, API, event, rule, and constraint must come from the selected epic's requirements and architecture inputs
- Include only sections relevant to the selected epic
- Do not leave placeholder text

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
Read `{resolved_optional_inputs}` when present.
Read the selected epic folders and their stories in full before writing any contract.

### Step 2 - Extract implementation evidence

For each selected epic:
- list linked requirements and canonical titles
- list data fields, state values, APIs, events, business rules, and non-functional constraints
- collect unresolved design questions that still block coding

### Step 3 - Write the contract

Create `epics/E-NNN-<slug>/implementation-contract.md` using `.b2s/artifact-templates/implementation-contract.md`.

Include only relevant sections:
- `## Data Entities`
- `## API Surface`
- `## Events`
- `## Business Rules`
- `## Non-Functional Constraints`
- `## Open Design Questions`

## Done criteria

- [ ] Every selected epic has `implementation-contract.md`
- [ ] Contract sections are evidence-based and relevant
- [ ] Canonical requirement traceability is preserved
- [ ] Open design questions are explicit
- [ ] No placeholder text remains

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- Validation and state updates are handled by the `.b2s` engine
