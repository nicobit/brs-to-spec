# OpenSpec Handoff

OpenSpec is the default downstream execution layer.

## Handoff objective

Create one OpenSpec change for the active deliverable only.

## Output

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

## Inputs

Use:
- normalized BRS,
- normalized initial architecture,
- business intake summary,
- initial architecture review,
- global architecture rules,
- delivery increments,
- traceability matrix,
- engineering readiness check.

## Important rule

Do not create tasks for the whole BRS.

OpenSpec should receive only the active deliverable scope.
