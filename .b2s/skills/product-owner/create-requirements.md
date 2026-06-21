# Skill - Create Requirements Catalog

## Identity

```text
skill_id:    product-owner.create-requirements
persona:     product-owner
action_id:   create-requirements
produces:    business-analysis/requirements.md
```

## When this skill is used

Run this after the business intake summary is accepted. It produces the canonical requirements catalog used by downstream business analysis, planning, and traceability artifacts.

## Role for this task

You are a senior business analyst producing the single source of truth for functional requirements, non-functional requirements, and constraints. Every downstream artifact derives from this catalog.

## Preconditions

Before starting, verify:
- `business-intake/business-intake-summary.md` exists
- At least one BRS source file in `input/brs.md` or `input/brs/*.md` is readable

If either required input is missing, stop and report the blocker. Do not fabricate requirements from memory or stale output.

## Hard constraints

- Always replace the full target file rather than appending to prior content
- Treat the BRS as the primary source of truth; the intake summary is a normalization aid
- Never pass a generic or domain-mismatched stub as complete
- Do not stop after the first epic, section, or requirement cluster
- If the intake summary and the BRS differ, preserve the BRS-backed requirement and record the conflict in the Source column or notes

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Read every policy file listed in `{resolved_policy_inputs}` in full before writing.
Do not start writing until all required inputs and policy inputs are read completely.

Mentally discard any existing content of `business-analysis/requirements.md` and rebuild the artifact from the current inputs only.

### Step 2 - Inventory all requirements

Build a complete inventory across three types:

- Functional requirements (`FR-NNN`): what the system must do. One atomic requirement per row, written as a user story.
- Non-functional requirements (`NFR-NNN`): measurable quality attributes with specific thresholds or objectively testable conditions.
- Constraints (`C-NNN`): regulatory, platform, schedule, integration, or business boundaries imposed on the solution.

Do not stop after the first obvious cluster. Inventory the entire BRS before assigning any `FR-NNN`, `NFR-NNN`, or `C-NNN` identifiers.

### Step 3 - Normalize

For each requirement found:
1. Assign a sequential ID in the correct series
2. Write a short title
3. Write the requirement statement in the proper format
4. Assign priority: `High`, `Medium`, or `Low`
5. Set status to `Open`
6. Record the source reference to the BRS, intake summary, or both

### Step 4 - Quality check

Before finalizing, verify every row is:
- Measurable where applicable
- Singular rather than bundled
- Unambiguous
- Testable
- Traceable
- Uniquely identified

Apply the requirement writing standard from `{resolved_policy_inputs}`:
- keep requirements atomic
- avoid implementation leakage unless the source states a hard constraint
- prefer measurable wording over generic capability language

## Output requirements

Write `business-analysis/requirements.md` using `.b2s/artifact-templates/requirements.md`.

The artifact must contain:
- Metadata table with `Status: Draft`
- Functional Requirements table
- Non-Functional Requirements table
- Constraints table
- Every row populated with priority, status, and source

## Done criteria

- [ ] All functional requirements from the source are represented as individual rows
- [ ] All non-functional requirements and quality attributes are represented explicitly
- [ ] All constraints are represented explicitly
- [ ] No duplicate IDs exist across the three tables
- [ ] Every NFR contains a measurable threshold or objectively testable condition
- [ ] Every row has `Status: Open`
- [ ] Every row has a source reference
- [ ] The file was fully rewritten as one artifact document
- [ ] Status is `Draft`

## Stop conditions

- If `business-intake/business-intake-summary.md` is missing, stop and report the blocker. Do not proceed.
- If the BRS and the intake summary conflict on a requirement, preserve the BRS-backed requirement and record the conflict rather than silently merging it away.
- If stakeholder roles are unclear, use the best-supported role wording from the source material and note the ambiguity.
- Do not invent requirements that are not derivable from the BRS or intake summary.

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
