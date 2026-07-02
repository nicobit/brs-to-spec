# 03 — Create Candidate User Stories

You are an agile product owner and solution analyst.

## Input

Read:

- `/output/02-candidate-epics.md`
- `/output/01-extracted-capabilities.md`
- `/input/brs.md` for source traceability
- `/input/architecture.md` if available
- `.github/instructions/story-quality.instructions.md`
- `.github/instructions/brs-traceability.instructions.md`
- `.github/skills/backlog-splitting/SKILL.md`
- `.github/skills/acceptance-criteria/SKILL.md`

## Goal

Create candidate user stories for each epic.

## Important Rules

- Stories must be small enough to implement and test.
- Stories must be business-value oriented.
- Do not create vague stories such as "implement dashboard" or "manage data".
- Split stories when different personas, workflows, business rules, systems, or test scenarios are involved.
- Include acceptance criteria in Given/When/Then format.
- Preserve traceability to the BRS.
- Include implementation notes only if supported by the BRS or architecture.

## Output

Create:

```text
/output/03-candidate-stories.md
```

Use this structure:

# Candidate User Stories

## 1. Story Summary Table

| Story ID | Epic ID | Title | Persona | Priority | Complexity | Dependencies | Confidence |
|---|---|---|---|---|---|---|---|

## 2. Stories by Epic

For each story include:

### Story ID

Example: STORY-001

### Parent Epic

### Title

### User Story

Use this format:

```text
As a [persona], I want [capability/action], so that [business value].
```

### Business Context

### Preconditions

### Main Flow

### Alternative Flows

### Exception Flows

### Business Rules

### Data Requirements

### UI Requirements

If no UI is involved, say "Not applicable".

### API / Integration Requirements

If no integration is involved, say "Not applicable".

### Non-Functional Requirements

### Security / Audit / Compliance Requirements

### Acceptance Criteria

Use Given/When/Then format.

### Dependencies

### Out of Scope

### Source Traceability

Reference BRS sections or quotes.

### Test Notes

### Implementation Notes

Only include implementation notes if clearly supported by the BRS or architecture.

## 3. Missing Clarifications

List questions that block story finalization.

## Quality Bar

Each story must be testable, traceable, and understandable by a developer and QA engineer.
