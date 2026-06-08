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
how initiative workspaces are organized
how single-file inputs expand into multi-file inputs only when needed
how the workflow should run
when OpenSpec is used
when standalone mode is used
when quality gates are mandatory
how the GitLab Planning View should behave
```

That guidance must preserve this boundary:

```text
User stories = business context and traceability
OpenSpec / standalone tasks = engineering implementation contract
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

The repository also includes implementation and review prompt groups:

```text
prompts/8-copilot-implementation/
prompts/9-reviewers/
```

Additional guidance:

```text
docs/16-prompt-execution-environments.md
docs/17-copilot-usage.md
templates/quality-gates/ready-for-copilot-checklist.md
```

## Recommended VS Code flow

### 1. Open the repository in VS Code

Make sure Copilot has access to repository context.

### 2. Select the active initiative workspace

Use an initiative-scoped workspace such as:

```text
initiatives/I001-onboarding-request/
```

All workflow paths are relative to that initiative workspace.

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
Based on the repository instructions, identify the active initiative workspace, the current BRS-to-delivery workflow stage, and the next prompt to run.
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

### 6. Implement one task at a time

After handoff artifacts exist, use:

```text
prompts/8-copilot-implementation/01-implement-one-task.md
```

If review findings come back, use:

```text
prompts/8-copilot-implementation/02-fix-review-comments.md
```

Optional pre-implementation gate:

```text
templates/quality-gates/ready-for-copilot-checklist.md
```

### 7. Review implemented tasks

Use:

```text
prompts/9-reviewers/01-senior-code-review.md
prompts/9-reviewers/02-qa-review.md
prompts/9-reviewers/03-architecture-review.md
prompts/9-reviewers/04-security-review.md
```

### 8. Use GitLab Planning View only as projection

The planning view exists to help the team create GitLab epics, issues, stories and tasks.

It is not the source of truth.

It is also not the engineering contract.

User stories in that view provide planning context and traceability only.

Copilot should implement from one approved OpenSpec or standalone task at a time.

Copilot implementation summaries and reviewer findings are also downstream helpers, not source-of-truth artifacts.

## Copilot anti-patterns

Do not ask Copilot:

```text
Implement this BRS directly.
Create all tasks for the entire feature at once.
Create GitLab issues without source traceability.
Ignore the architecture document.
Skip quality gates.
Mix artifacts from different initiative workspaces.
```

Ask instead:

```text
Create the readiness check for active deliverable D1 in initiatives/I001-onboarding-request using the framework instructions.
Create the security review because it is triggered by readiness-check.md.
Create the standalone delivery package for D1 using the completed quality gates.
Implement Task 001 from the active deliverable using prompts/8-copilot-implementation/01-implement-one-task.md.
Review the implementation using prompts/9-reviewers/01-senior-code-review.md.
Create the GitLab Planning View as a projection from the source artifacts.
```
