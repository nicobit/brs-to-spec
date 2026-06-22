# Skill - Create Delivery Skeleton

## Identity

```text
skill_id:    delivery-lead.create-delivery-skeleton
persona:     delivery-lead
action_id:   create-delivery-skeleton
produces:    planning/delivery-skeleton.md
```

## When this skill is used

Run after architecture impact assessment is complete. This skill produces a lightweight hierarchy — epic IDs, feature IDs, story IDs, and one-line summaries only. Full story detail is generated later in per-feature files.

## Role for this task

You are a senior delivery lead decomposing the approved scope into a structured delivery hierarchy. At this stage you define the **shape** of the delivery — how many epics, features, and stories — without writing full story detail.

## Preconditions

Before starting, verify:

- `requirements/atomic-requirements.md` exists and is readable
- `domain/capability-map.md` exists and is readable
- `architecture/architecture-review.md` exists and is readable
- `architecture/architecture-impact-map.md` exists and is readable
- `governance/delivery-constitution.md` exists and is readable
- `input/brs.md` exists and is readable

Optional context:

- `domain/business-rules.md`
- `domain/domain-model.md`
- `architecture/architecture-rules.md`
- `architecture/required-adrs.md`
- `architecture/architecture-risks.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Do NOT write full story detail — only IDs, titles, and one-line summaries
- Every requirement (FR/REQ) from `atomic-requirements.md` must appear in the Requirement Coverage Summary
- Every capability (CAP-NNN) from `capability-map.md` must map to at least one epic
- Story IDs use the format S-NNN.N (feature.story)
- This file must be small enough to never truncate — keep it compact

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Count requirements and capabilities

Count total requirements in `atomic-requirements.md`. Count total capabilities in `capability-map.md`. These counts determine the minimum scope of the skeleton.

### Step 3 - Define epics from capabilities

Map capabilities to epics. Each epic should represent a major business capability or a logical grouping of related capabilities. Assign IDs E-001, E-002, etc.

Rules:
- An initiative with 7 capabilities should have approximately 3–5 epics (some capabilities group naturally)
- Every capability must be assigned to an epic
- Epics must be meaningful business outcomes, not technical layers

### Step 4 - Define features per epic

Each feature is a coherent deliverable sub-capability. Assign IDs F-001, F-002, etc., sequential across the whole artifact.

### Step 5 - Define story IDs per feature

For each feature, list story IDs (S-NNN.N) with one-line titles. Each story must be:
- Independently implementable
- Small enough for one focused session
- Traceable to at least one requirement

### Step 6 - Build coverage tables

Create the Capability Coverage table (every CAP-NNN must appear).
Create the Requirement Coverage Summary (every FR/REQ from atomic-requirements must appear).

Mark any uncovered requirements as **Not Covered** with a note.

### Step 7 - Story count assertion

Count all stories and populate the Story Count Assertion with Must/Should/Could breakdown and increment assignments.

## Output requirements

Write `planning/delivery-skeleton.md` using `.b2s/artifact-templates/delivery-skeleton.md`.

## Done criteria

- [ ] Every capability from capability-map.md maps to at least one epic
- [ ] Every requirement from atomic-requirements.md appears in the coverage summary
- [ ] Story count assertion matches the actual story count in the Story Index
- [ ] No full story detail is included — only IDs and one-line titles
- [ ] File is compact (no multi-paragraph descriptions per story)
- [ ] No placeholder text remains

## Stop conditions

- If any required input is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
