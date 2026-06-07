# Quality Gate Prompt — Create Architecture Review

## Purpose

Review the active deliverable against the initial architecture document and global architecture rules.

Use this only when an architecture review is needed before implementation or merge.

## Inputs

Use:
- `input/initial-architecture.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`
- `modules/software-modules.md` if available
- OpenSpec proposal/design/tasks.

## Output file

```text
quality-gates/architecture-review.md
```

## Output structure

```markdown
# Architecture Review

## Active Deliverable

## Review Decision
Approved / Approved with risks / Not approved

## Architecture Constraints Checked

| Constraint ID | Constraint | Compliant? | Notes |
|---|---|---|---|

## Findings

| Finding ID | Severity | Description | Recommendation |
|---|---|---|---|

## Module Boundary Review

## API / Data Contract Review

## Security / Auth Review

## Observability / Operations Review

## Open Architecture Decisions

## Required Actions
```

## Rules

- Do not invent new architecture.
- Check against the initial architecture and global rules.
- If the design conflicts with an architecture constraint, mark it clearly.
- Keep the review scoped to the active deliverable.
