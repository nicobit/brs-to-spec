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
how feature workspaces are organized
how single-file inputs expand into multi-file inputs only when needed
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

### 2. Select the active feature workspace

Use a feature-scoped workspace such as:

```text
features/F001-onboarding-request/
```

All workflow paths are relative to that feature workspace.

### 3. Start with simple normalized input files

```text
input/brs.md
input/architecture.md
input/input-package.md
```

Only expand to `input/brs/` or `input/architecture/` if the same initiative really has multiple source documents.

### 4. Ask Copilot to identify workflow status

Use:

```text
.github/prompts/brs-to-spec-run-workflow.prompt.md
```

or ask:

```text
Based on the repository instructions, identify the active feature workspace, the current BRS-to-delivery workflow stage, and the next prompt to run.
```

### 5. Generate only the next artifact

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

### 6. Use GitLab Planning View only as projection

The planning view exists to help the team create GitLab epics, issues, stories and tasks.

It is not the source of truth.

## Copilot anti-patterns

Do not ask Copilot:

```text
Implement this BRS directly.
Create all tasks for the entire feature at once.
Create GitLab issues without source traceability.
Ignore the architecture document.
Skip quality gates.
Mix artifacts from different feature workspaces.
```

Ask instead:

```text
Create the readiness check for active deliverable D1 in features/F001-onboarding-request using the framework instructions.
Create the security review because it is triggered by readiness-check.md.
Create the standalone delivery package for D1 using the completed quality gates.
Create the GitLab Planning View as a projection from the source artifacts.
```
