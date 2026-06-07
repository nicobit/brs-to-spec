# Copilot Usage

## Do Not Ask

```text
Implement this BRS.
Create all tasks for the whole feature.
Generate code directly from input/brs.md.
```

## Ask Instead

### Workflow status

```text
Use .github/prompts/brs-to-spec-run-workflow.prompt.md to identify the active initiative workspace, current stage, missing artifacts, and next prompt to run.
```

### Artifact generation

```text
Create engineering-readiness/readiness-check.md for the active initiative workspace using prompts/4-engineering-readiness/01-check-engineering-readiness.md and the matching template.
```

### Task implementation

```text
Implement Task 001 from openspec/changes/D1-<deliverable-name>/tasks.md for the active initiative workspace.

Before coding:
1. Read the feature inputs and planning artifacts.
2. Read the active handoff artifacts.
3. Inspect existing similar code and tests.
4. Provide a short implementation plan.

Then implement only Task 001, update tests, and summarize files changed, coverage, assumptions, and risks.
```

### Review

```text
Review the implementation for Task 001 using prompts/9-reviewers/01-senior-code-review.md and the active initiative workspace artifacts.
```

## Good Operating Pattern

```text
source inputs
  -> business intake
  -> architecture / planning
  -> readiness check
  -> required quality gates
  -> handoff artifacts
  -> implement one task
  -> review the task
  -> fix review findings
```

## Copilot Boundaries

Copilot should:

```text
implement one task at a time
read the active initiative workspace first
respect existing architecture and coding patterns
update tests with behavior changes
report assumptions and open questions
```

Copilot should not:

```text
invent business rules
skip required quality gates
implement future tasks
perform unrelated cleanup
rewrite architecture without an explicit decision
```
