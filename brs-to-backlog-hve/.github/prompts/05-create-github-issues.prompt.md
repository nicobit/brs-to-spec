# 05 — Create GitHub-Ready Issues

You are a GitHub backlog manager.

## Input

Read:

- `/output/02-candidate-epics.md`
- `/output/03-candidate-stories.md`
- `/output/04-backlog-review.md`
- `.github/instructions/output-format.instructions.md`

## Goal

Prepare GitHub-ready issues for epics, stories, and clarifications.

## Important Rules

- Do not lose traceability.
- Each GitHub issue must have a clear title and body.
- Use labels consistently.
- Use parent/child references where possible.
- Do not create delivery issues for unclear or blocked items unless they are marked as clarification issues.
- If the backlog review says "Needs major fixes" or "Not ready", still generate issues, but clearly mark them as draft and blocked.

## Output

Create:

```text
/output/05-github-issues.md
```

Use this structure:

# GitHub Backlog Issues

## 1. Recommended Labels

List recommended GitHub labels.

Examples:

- epic
- story
- clarification
- frontend
- backend
- integration
- security
- compliance
- reporting
- nfr
- blocked
- draft

## 2. Epic Issues

For each epic create:

```markdown
### GitHub Issue: [EPIC-ID] Epic title

Labels:
epic, [domain label]

## Business Objective

## Scope

## Out of Scope

## Related Capabilities

## Main Scenarios

## Dependencies

## Definition of Done

## Source Traceability

## Child Stories
```

---

## 3. Story Issues

For each story create:

```markdown
### GitHub Issue: [STORY-ID] Story title

Labels:
story, [domain label], [technical label if relevant]

## User Story

## Business Context

## Preconditions

## Main Flow

## Alternative / Exception Flows

## Business Rules

## Data Requirements

## UI Requirements

## API / Integration Requirements

## Acceptance Criteria

## Dependencies

## Source Traceability

## Test Notes

## Parent Epic
```

---

## 4. Clarification Issues

Create one clarification issue for each unresolved question that blocks backlog finalization.

For each clarification issue include:

- title
- question
- context
- affected epic/story
- decision needed
- impact if unresolved

## Quality Bar

The output should be directly usable to manually create GitHub issues or to automate issue creation.
