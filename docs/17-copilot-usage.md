# Copilot Usage

## Workflow-status rule

Before asking Copilot to create or update an artifact, ask it to state:

```text
current stage
completed artifacts
missing artifacts
next prompt
risk if skipped
```

This keeps the workflow explicit without adding a new orchestration artifact.

## Artifact-quality rule

Before accepting a generated artifact, ask Copilot:

```text
Is this artifact good enough for the next workflow step?
What decision does it support?
What concrete evidence is present?
What is still too generic, repetitive, or vague?
```

Use:

```text
docs/21-artifact-quality-review.md
```

when the artifact exists but still feels weak.

## Do Not Ask

```text
Implement this BRS.
Create all tasks for the whole feature.
Generate code directly from input/brs.md.
```

## Ask Instead

### Workflow status

```text
Use `.brs2spec/brs-to-spec-run-workflow.md` to identify the active initiative workspace, current stage, missing artifacts, and next prompt to run.
```

### Artifact generation

```text
Create engineering-readiness/readiness-check.md for the active initiative workspace using .brs2spec/4-engineering-readiness/01-check-engineering-readiness.md and the matching template.
```

### Task implementation

```text
Implement Task 001 from openspec/changes/F-XXX.X-<story-slug>/tasks.md for the active initiative workspace.

Before coding:
1. Read the feature inputs and planning artifacts.
2. Read the active handoff artifacts.
3. Inspect existing similar code and tests.
4. Provide a short implementation plan.

Then implement only Task 001, update tests, and summarize files changed, coverage, assumptions, and risks.
```

### Review

```text
Review the implementation for Task 001 using .brs2spec/9-reviewers/01-senior-code-review.md and the active initiative workspace artifacts.
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
