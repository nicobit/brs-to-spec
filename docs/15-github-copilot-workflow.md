# GitHub Copilot / VS Code Workflow

## Purpose

This repository includes GitHub Copilot instructions so that VS Code and GitHub Copilot understand the intended workflow.

The most important file is:

```text
.github/copilot-instructions.md
```

It tells Copilot:

```text
what this repository is
what the source of truth is
how the workflow should run
when OpenSpec is used
when standalone mode is used
when quality gates are mandatory
how the GitLab Planning View should behave
```

## Prompt files

Additional prompt files are provided under:

```text
.github/prompts/
```

Available prompts:

```text
brs-to-spec-run-workflow.prompt.md
create-engineering-readiness.prompt.md
create-openspec-handoff.prompt.md
create-standalone-handoff.prompt.md
create-gitlab-planning-view.prompt.md
```

## Recommended VS Code flow

### 1. Open the repository in VS Code

Make sure Copilot has access to repository context.

### 2. Add or create normalized input files

```text
input/brs.md
input/initial-architecture.md
input/input-package.md
```

### 3. Ask Copilot to identify workflow status

Use:

```text
.github/prompts/brs-to-spec-run-workflow.prompt.md
```

or ask:

```text
Based on the repository instructions, identify the current BRS-to-delivery workflow stage and recommend the next prompt to run.
```

### 4. Generate only the next artifact

Do not ask Copilot to generate the full project output in one step.

Recommended sequence:

```text
business intake
architecture review
delivery planning
readiness check
required quality gates
OpenSpec or standalone handoff
GitLab Planning View if needed
```

### 5. Use GitLab Planning View only as projection

The planning view exists to help the team create GitLab epics, issues, stories and tasks.

It is not the source of truth.

## Copilot anti-patterns

Do not ask Copilot:

```text
Implement this BRS.
Create all tasks for this BRS.
Create GitLab issues without source traceability.
Ignore the architecture document.
Skip quality gates.
```

Ask instead:

```text
Create the readiness check for active deliverable D1 using the framework instructions.
Create the security review because it is triggered by readiness-check.md.
Create the standalone delivery package for D1 using the completed quality gates.
Create the GitLab Planning View as a projection from the source artifacts.
```
