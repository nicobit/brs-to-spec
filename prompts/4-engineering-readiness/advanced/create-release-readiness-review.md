# Advanced Prompt — Create Release Readiness Review

## Purpose

Review whether the active deliverable is operationally ready for release.

Use this only when the deliverable is close to implementation completion or release approval.

## Inputs

Use:
- OpenSpec proposal/design/tasks,
- test strategy,
- QA review,
- architecture review,
- security review,
- operational constraints,
- deployment/release notes if available.

## Output file

```text
advanced-governance/release-readiness-review.md
```

## Output structure

```markdown
# Release Readiness Review

## Active Deliverable

## Release Decision
Ready / Ready with risks / Not ready

## Checklist

| Area | Ready? | Notes |
|---|---|---|
| Acceptance criteria met |  |  |
| Automated tests passed |  |  |
| Regression risk assessed |  |  |
| Observability ready |  |  |
| Rollback approach defined |  |  |
| Security findings resolved |  |  |
| Architecture findings resolved |  |  |
| Operational documentation updated |  |  |

## Open Risks

## Required Actions Before Release
```

## Rules

- Keep this review practical.
- Identify blockers clearly.
- Do not approve if critical findings remain unresolved.
