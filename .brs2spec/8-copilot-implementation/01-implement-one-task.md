# Prompt - Implement One Task

## Recommended environment

- VS Code Copilot Agent mode
- GitHub Copilot Coding Agent
- Another approved coding agent with repository and test access

## Role

You are implementing one approved engineering task for the active initiative workspace.

## Context

This is a downstream implementation helper.

It is not a source-of-truth creation prompt.

The source of truth remains the active initiative workspace artifacts, especially:

```text
engineering-readiness/readiness-check.md
quality-gates/*.md
openspec/changes/D1-<deliverable-name>/...
or standalone-delivery/D1-<deliverable-name>/...
```

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths below are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Purpose

Implement exactly one task from the active downstream source of truth.

## Source of truth

Use one of:

```text
openspec/changes/D1-<deliverable-name>/tasks.md
standalone-delivery/D1-<deliverable-name>/tasks.md
```

Do not implement directly from raw BRS inputs.

## Inputs

Load first — before reading any other artifact:

```text
engineering-readiness/initiative-context.md
```

This file contains the technology constraints, architecture rules, governed boundaries, active gates, and rollback sensitivity for this deliverable. It is the single source of constraint truth for implementation. If it is missing, run `.brs2spec/4-engineering-readiness/02-generate-initiative-context.md` before continuing.

Then use:

- the active downstream task artifact
- the related design or delivery specification artifact
- the relevant code, tests, and repository patterns

## Output path

There is no mandatory new framework artifact.

Primary output is:

```text
code changes
test changes
implementation summary in the coding session or PR / MR description
```

Optional saved review trail:

```text
reviews/implementation/task-<task-id>-implementation-summary.md
```

## Read before coding

Load `engineering-readiness/initiative-context.md` first (see Inputs above).

Then read the relevant artifacts that exist for the active initiative workspace:

```text
engineering-readiness/readiness-check.md
quality-gates/*.md that apply to the task
openspec/changes/D1-<deliverable-name>/proposal.md
openspec/changes/D1-<deliverable-name>/design.md
openspec/changes/D1-<deliverable-name>/tasks.md
standalone-delivery/D1-<deliverable-name>/delivery-spec.md
standalone-delivery/D1-<deliverable-name>/implementation-plan.md
standalone-delivery/D1-<deliverable-name>/tasks.md
standalone-delivery/D1-<deliverable-name>/validation-plan.md
```

Read only the artifacts that are relevant to the selected execution mode and active task.

Do not re-derive technology constraints or architecture rules from raw inputs — trust `initiative-context.md` for those.

## Required output structure

Return a final implementation summary using:

```markdown
## Task Implemented
## Files Changed
## Requirements / Artifacts Covered
## Validation Evidence
## Tests Added or Updated
## Assumptions
## Risks
## Remaining Open Questions
```

## Quality bar

A good implementation pass must:

- implement one task only
- preserve traceability to the active task and source artifacts
- show validation evidence, not only code changes
- update tests for behavior changes
- respect architecture constraints and required quality gate actions
- make any assumptions or remaining risks visible

## Anti-patterns to avoid

Do not:

- implement directly from raw BRS
- implement tasks for the whole BRS
- ignore architecture constraints
- skip required quality gate actions
- invent missing requirements
- silently change scope
- treat the planning view as the execution source of truth

## Stop conditions

- If there is no approved active task artifact, stop.
- If readiness-check is missing, stop.
- If a required quality gate is missing for the task, stop and report it.
- If architecture constraints are unclear and materially affect implementation, stop and report it.

## Self-review checklist

Before finalizing, verify:

- [ ] Exactly one task was implemented.
- [ ] The implementation traces back to the active task artifact.
- [ ] Required tests were added or updated.
- [ ] Validation evidence is visible.
- [ ] Scope was not silently expanded.
- [ ] Assumptions and risks are explicit.

## Required process

1. Identify the exact task ID and scope.
2. Identify the files likely to change.
3. Inspect existing similar implementation patterns before editing.
4. Provide a short implementation plan:
   - files to change
   - tests to add or update
   - assumptions
   - risks
5. Implement only that task.
6. Add or update tests for the behavior change.
7. Summarize what was changed and any remaining questions.

## Mandatory rules

- Do not implement future tasks.
- Do not perform unrelated refactoring.
- Do not invent business rules.
- Do not introduce new dependencies without approval.
- Do not weaken security, authorization, auditability, or validation.
- Do not ignore architecture constraints recorded in the initiative workspace.
