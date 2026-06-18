# Skill - Create Use Case Specs

## Identity

```text
skill_id:    product-owner.create-use-case-specs
persona:     product-owner
action_id:   create-use-case-specs
produces:    business-analysis/use-cases/UC-NNN.md
```

## When this skill is used

Run this after the use-case diagram and markdown catalog exist. It writes one use-case detail file per `UC-NNN`.

## Role for this task

You are a senior business analyst writing structured use-case specifications that capture main success scenarios, alternative flows, exception paths, and business-level postconditions.

## Preconditions

Before starting, verify:
- `business-analysis/requirements.md` exists
- `business-analysis/use-cases.puml` exists and contains `UC-NNN` IDs
- `business-analysis/use-cases.md` exists

Optional context:
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`
- `architecture/architecture-review.md`

If required inputs are missing, stop and report the blocker.

## Instructions

### Step 1 - Read the use-case inventory

Read `{workspace_root}/business-analysis/use-cases.puml` and extract the authoritative `UC-NNN` list.
Read `{workspace_root}/business-analysis/requirements.md` and build a private coverage map:
- `UC-NNN -> covered FR-NNNs`
- `FR-NNN -> owning UC-NNNs`

Do not write files until every `FR-NNN` is either covered by a use case or explicitly excluded with justification.

### Step 2 - Write one file per use case

For each `UC-NNN`, create `business-analysis/use-cases/UC-NNN.md` using `.b2s/artifact-templates/use-case-detail.md`.

Each file must include:
- overview
- preconditions
- main success scenario
- at least one meaningful alternative flow
- exception paths
- postconditions
- business rules referenced
- FR sources

### Step 3 - Validate completeness

After all files are written, verify:
- every `UC-NNN` from the diagram has exactly one file
- no file contains more than one use case
- every `FR-NNN` is covered by at least one UC or explicitly excluded
- actor references are consistent
- no file is a shallow stub

## Output requirements

- One file per use case under `business-analysis/use-cases/`
- Every file uses the standard template
- Every file has `Status: Draft`

## Done criteria

- [ ] The folder contains one file per `UC-NNN`
- [ ] No `UC-NNN` from the diagram is missing
- [ ] No file contains more than one use case
- [ ] Every file has preconditions, main scenario, alternative flow, and postconditions
- [ ] Every file traces to at least one `FR-NNN`
- [ ] Across the folder, all `FR-NNN` entries are covered or explicitly excluded
- [ ] Main scenario steps use business language only
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event IDs or result files
- This prompt writes artifact files only
