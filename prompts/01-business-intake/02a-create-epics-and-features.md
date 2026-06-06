# Prompt — Create Epics and Features

Recommended environment:
- Microsoft 365 Copilot, ChatGPT, or another approved LLM
- GitHub Copilot Chat if artifacts are already in the repository

Owner:
- Business PO / BA
- Optional review by Scrum Master, Tech Lead, or Product Manager

This prompt does not require code access.

Input files:
- `features/<feature-name>/business-intake/brs-summary.md`
- `features/<feature-name>/business-intake/requirements.md`

Task:
Create a business delivery structure that groups the requirements into business objectives, epics, and features/capabilities.

Rules:
- Do not invent business scope.
- Do not treat requirements as epics automatically.
- Requirements describe obligations; epics/features organize delivery.
- Each epic must support one or more business objectives.
- Each feature/capability must belong to an epic.
- Each feature/capability must map to one or more requirement IDs.
- A requirement can map to multiple features if needed.
- Mark uncertain grouping decisions as assumptions.
- Identify candidate user stories, but do not fully write the stories here.

Output:
Create `features/<feature-name>/business-intake/epics-and-features.md`.

Use this structure:

```markdown
# Epics and Features

## 1. Business Objectives

### BO-001 — <business objective title>

Description:

Success measures:

Related BRS sections:

## 2. Epics

### EPIC-001 — <epic title>

Business objectives:
- BO-001

Description:

Business value:

In scope:

Out of scope:

Success measures:

Related requirements:
- FR-xxx
- NFR-xxx
- SEC-xxx

## 3. Features / Capabilities

### FEAT-001 — <feature title>

Parent epic:
- EPIC-001

Description:

Business value:

Related requirements:
- FR-xxx
- DATA-xxx
- SEC-xxx
- AUD-xxx

Candidate user stories:
- US-xxx — <candidate title>

Dependencies:

Assumptions:

Open questions:

## 4. Requirement-to-Feature Mapping

| Requirement ID | Requirement Title | Epic | Feature / Capability | Notes |
|---|---|---|---|---|

## 5. Delivery Slicing Recommendations

Suggest a sensible delivery order, for example:
1. Foundation / data model
2. Core backend behavior
3. User-facing UI
4. Audit / reporting
5. Hardening / regression

## 6. Open Questions
```

## How to use this prompt

Run this after:

```text
01-extract-business-requirements.md
```

and before:

```text
02-create-user-stories.md
```

This prompt creates the delivery structure. It should not create full user stories.

Remember:

```text
Requirements are not epics.
Requirements describe obligations.
Epics and features organize delivery.
User stories describe user-centered increments.
```

For a small change, the output may contain only one epic and one feature.

For medium and large/risky changes, use this step to identify multiple features/capabilities and a sensible delivery slicing.
