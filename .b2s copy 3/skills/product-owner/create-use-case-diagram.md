# Skill - Create Use Case Diagram

## Identity

```text
skill_id:    product-owner.create-use-case-diagram
persona:     product-owner
action_id:   create-use-case-diagram
produces:    business-analysis/use-cases.puml, business-analysis/use-cases.md
```

## When this skill is used

Run this after the requirements catalog exists. This action co-produces two files in one pass: the PlantUML diagram and the markdown companion catalog.

## Role for this task

You are a senior business analyst producing the behavioral map of the initiative. This artifact assigns stable `UC-NNN` identifiers used by downstream use-case specs, actors, process flows, planning, BDD, and handoff content.

## Preconditions

Before starting, verify:
- `business-analysis/requirements.md` exists and has at least one `FR-NNN` row

Optional context:
- `business-intake/business-intake-summary.md`
- BRS source files under `input/`

If the required input is missing or empty, stop and report the blocker.

## Instructions

### Step 1 - Read inputs

Read `{workspace_root}/business-analysis/requirements.md` in full.
Optionally read `{workspace_root}/business-intake/business-intake-summary.md` and BRS files under `{workspace_root}/input/` for broader actor and lifecycle context.
Do not start writing until requirements are read completely.

### Step 2 - Identify actors

From the requirements, identify every human role and external system that:
- initiates a use case
- participates as a secondary actor
- receives an output from a use case

Use the most stable business-facing actor names supported by the source.

### Step 3 - Group requirements into use cases

Group requirements into distinct actor-visible goals.

Rules:
- Every use case must trace to at least one `FR-NNN`
- Do not create one use case per requirement unless the requirements truly represent separate goals
- Do not collapse the whole initiative into one generic use case
- Do not inject implementation detail into use case titles
- Preserve lifecycle breadth when the initiative spans multiple process stages

Coverage rules:
- First, scan `requirements.md` by capability, epic, or major requirement cluster and list the distinct actor-visible goals before drawing anything.
- Preserve initiative breadth: if the requirements span multiple lifecycle stages, the use cases must reflect that breadth rather than stopping at the first entry flow.
- A use case may cover multiple FRs only when they belong to the same observable actor goal or tightly coupled business outcome.
- System-only FR clusters still need representation when they create a distinct governed business outcome or state transition consumed by another actor or process.
- If the requirements clearly imply many distinct goals, a tiny 2-3 UC output is almost certainly under-modeled and should be corrected before finalizing.

Before assigning `UC-NNN` ids, create a scratch mapping for yourself:
- `Capability or cluster -> candidate goal(s) -> FR-NNN coverage`
- Use that mapping to confirm that no major requirement cluster is silently omitted.
- If `requirements.md` appears suspiciously tiny, generic, or domain-mismatched, cross-check against the BRS and stop rather than producing shallow use cases.

### Step 4 - Assign stable IDs

Assign sequential `UC-NNN` identifiers starting from `UC-001`. These IDs must remain identical in both output files.

### Step 5 - Write `business-analysis/use-cases.puml`

Write valid PlantUML using standard use-case syntax.

Required conventions:
- Include `@startuml` and `@enduml`
- Include `left to right direction`
- Declare actors outside the system boundary
- Put all use cases inside one system rectangle
- Ensure every actor connects to at least one use case
- **Always quote use case names that contain hyphens**: `usecase "UC-001" as UC001` — not `usecase UC-001 as UC001`. PlantUML parses an unquoted hyphen as a subtraction operator and raises a syntax error.

### Step 6 - Write `business-analysis/use-cases.md`

Write the markdown companion using `.b2s/artifact-templates/use-cases.md`.

Required conventions:
- Use a `graph LR` Mermaid block
- Actors use `ACT_ID([Actor Name])`
- Use cases use `UC001(UC-001 Goal Title)`
- Include a UC Catalog table with actor names and `FR-NNN` sources

### Step 7 - Verify consistency

Before finishing, verify:
- Every `UC-NNN` in the PUML exists in the markdown file
- Actor names are identical across both files
- Every use case traces to at least one `FR-NNN`
- Every major requirement cluster is covered or explicitly excluded with reason
- The UC set represents the whole initiative lifecycle, not just the first submission or entry flow, when the requirements describe a broader lifecycle

## Output requirements

Both files must be written:
- `business-analysis/use-cases.puml`
- `business-analysis/use-cases.md`

`UC-NNN` IDs must be identical across both files.

## Done criteria

- [ ] `use-cases.puml` exists and contains at least one `UC-NNN`
- [ ] `use-cases.md` exists and contains at least one `UC-NNN`
- [ ] `UC-NNN` IDs match across both files
- [ ] Actor names match across both files
- [ ] Every use case traces to at least one `FR-NNN`
- [ ] The UC set reflects the breadth of the initiative rather than only the first entry flow
- [ ] Status is `Draft` in the markdown file

## Stop conditions

- If `business-analysis/requirements.md` is missing or has no `FR-NNN` rows, stop and report the blocker.
- If the initiative is purely technical with no user-facing goals, produce the artifacts with an explanation rather than inventing business-facing use cases.
- Do not invent use cases that are not traceable to `FR-NNN` entries in `requirements.md`.

## Notes for the staged engine

- Do not mention event IDs, event result files, or dispatcher pass/fail metadata
- This action's official outputs are both the PUML and markdown files
