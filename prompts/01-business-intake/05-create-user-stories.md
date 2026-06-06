# Prompt 05 — Create User Stories and Acceptance Criteria

Recommended environment:
- Microsoft 365 Copilot, ChatGPT, or another approved LLM
- GitHub Copilot Chat if artifacts are already in the repository

Owner:
- Business PO / BA

This prompt does not require code access.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/epics-and-features.md`

Task:
Create Agile user stories with acceptance criteria.

Rules:
- Do not invent business behavior.
- Every user story must map to one parent epic and one parent feature/capability where possible.
- Every user story must map to one or more requirement IDs.
- Acceptance criteria must use Given / When / Then.
- Include positive, negative, validation, authorization, and audit scenarios where relevant.
- If a story cannot be written because information is missing, add an open question.
- Keep stories small enough to be independently discussed and estimated.

Output:
Create `features/<feature-name>/business-intake/user-stories.md`.

Structure:

```markdown
# User Stories

## US-001 — <title>

Parent epic:
- EPIC-001 — <epic title>

Parent feature:
- FEAT-001 — <feature title>

As a <actor>,  
I want <capability>,  
so that <business outcome>.

### Requirements Covered
- FR-xxx
- BR-xxx
- SEC-xxx

### Acceptance Criteria

#### AC-001 — <title>
Given ...
When ...
Then ...

#### AC-002 — <title>
Given ...
When ...
Then ...

### Non-Functional Considerations

### Data Considerations

### Security / Authorization Considerations

### Audit / Compliance Considerations

### Notes

### Open Questions
```

## How to use this prompt

Run this only after:

```text
business-intake/epics-and-features.md
```

exists.

This prompt uses the epics/features structure to create user stories.

Each story must reference:

```text
Parent epic
Parent feature/capability
Related requirements
Acceptance criteria
```

Do not create stories for requirements that are still unclear. Add open questions instead.

## Mandatory use of architecture alignment

If this file exists, read it:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Use it to:
- avoid creating unrealistic or unsupported user stories
- avoid inventing acceptance criteria for unresolved architecture decisions
- add open questions to affected stories
- identify stories blocked by architecture decisions
- include relevant architecture constraints in notes

Do not hide alignment issues inside user stories.

## Large BRS / multi-quarter scope rule

If the feature has a planning folder, especially:

```text
features/<feature-name>/planning/next-increment-scope.md
features/<feature-name>/planning/increment-handoff.md
```

then create detailed user stories only for the selected increment.

Do not create detailed user stories for the entire multi-quarter BRS unless explicitly requested.

Use the planning artifacts to determine:
- which requirements are included,
- which features are included,
- which requirements are deferred,
- which architecture blockers affect stories,
- which stories are candidates for the next increment.
