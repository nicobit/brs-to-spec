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

It must also preserve this operating rule:

```text
every major artifact should have an obvious consumer
every major artifact should have an obvious downstream use
Copilot should avoid duplicating source-of-truth content into projection or handoff artifacts
```

## Prompt files

Prompt wrappers for Copilot are provided under:

```text
.github/prompts/
```

Available prompts:

```text
brs-to-spec-run-workflow.prompt.md
create-brs.prompt.md
draft-architecture-from-brs.prompt.md
create-engineering-readiness.prompt.md
generate-initiative-context.prompt.md
create-openspec-handoff.prompt.md
create-standalone-handoff.prompt.md
create-gitlab-planning-view.prompt.md
implement-one-task.prompt.md
spec-correction.prompt.md
describe-repository.prompt.md
```

These files are thin wrappers only. All logic lives in `.brs2spec/`. Do not edit the wrapper files; edit the corresponding `.brs2spec/` prompt instead.

The repository also includes implementation and review prompt groups:

```text
.brs2spec/8-copilot-implementation/
.brs2spec/9-reviewers/
```

Additional guidance:

```text
docs/16-prompt-execution-environments.md
docs/17-copilot-usage.md
.brs2spec/templates/quality-gates/ready-for-copilot-checklist.md
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

At the start of an initiative, architecture input is often high-level solution architecture context, not fully initiative-specific delivery architecture.

### 4. Ask Copilot to identify entry mode and workflow status

Use:

```text
.github/prompts/brs-to-spec-run-workflow.prompt.md
```

or ask:

```text
Based on the repository instructions, identify the active initiative workspace, the best entry mode, the current BRS-to-delivery workflow stage, and the next prompt to run.
```

### 5. Generate only the next artifact

Do not ask Copilot to generate the full project output in one step.

Recommended sequence:

```text
business intake
delivery planning
architecture review and refinement
readiness check
required quality gates
OpenSpec or standalone handoff
GitLab Planning View if needed
```

When generating an artifact, also ask Copilot to state:

```text
primary consumer
primary purpose or decision
next artifact or workflow that depends on it
what should be referenced instead of duplicated
```

Before moving on, also ask:

```text
Is this artifact good enough to support the next step?
What evidence of usefulness is present?
What is still too generic or too weak?
```

During delivery planning, define Epic / Feature / User Story structure before architecture refinement goes deep and before handoff.

Then ask Copilot to review the architecture against that initiative shape, rather than assuming the early architecture input already answers every delivery question.

Before readiness, ask Copilot to confirm that delivery shape is approved enough and architecture refinement is initiative-specific enough to support a real proceed / do not proceed decision.

Readiness should consume:

- approved delivery shape
- initiative-specific architecture review
- initiative-specific architecture rules
- traceability evidence when available

It should not compensate for vague planning or unresolved architecture by guessing.

If the entry mode is `existing-system enhancement`, surface brownfield impact early and create `architecture/existing-system-impact.md` when the change touches existing contracts, modules, or operational behavior.

At each step, ask Copilot to state:

```text
current stage
completed artifacts
missing artifacts
next prompt
risk if the next step is skipped
```

If the change is narrow, also ask whether the small-change path is appropriate and what minimum artifacts are still required.

### 6. Implement one task at a time

After handoff artifacts exist, use:

```text
.brs2spec/8-copilot-implementation/01-implement-one-task.md
```

If review findings come back, use:

```text
.brs2spec/8-copilot-implementation/02-fix-review-comments.md
```

Optional pre-implementation gate:

```text
.brs2spec/templates/quality-gates/ready-for-copilot-checklist.md
```

Only proceed when Copilot can point to the exact approved implementation task and its source artifacts.

The handoff package should clearly derive from:

- approved delivery shape
- initiative-specific architecture refinement
- readiness decisions
- triggered quality gates

If those upstream artifacts are weak, ask Copilot to improve them before handoff rather than letting it reconstruct them implicitly.

### 7. Review implemented tasks

Use:

```text
.brs2spec/9-reviewers/01-senior-code-review.md
.brs2spec/9-reviewers/02-qa-review.md
.brs2spec/9-reviewers/03-architecture-review.md
.brs2spec/9-reviewers/04-security-review.md
```

### 8. Use GitLab Planning View only as projection

The planning view exists to help the team create GitLab epics, issues, stories and tasks.

It is not the source of truth.

It is also not the engineering contract.

User stories in that view provide planning context and traceability only.

Copilot should implement from one approved OpenSpec or standalone task at a time.

Those tasks should already be derived from the planned stories plus engineering constraints.

Copilot implementation summaries and reviewer findings are also downstream helpers, not source-of-truth artifacts.

Treat `gitlab-planning-view.md` as coordination output for the delivery team, not as a place to restate requirements, architecture truth, or implementation contract details.

For a lightweight review model, use:

```text
docs/21-artifact-quality-review.md
```

## Stage-transition summary

Use this compact model:

```text
input preparation -> intake
intake -> early delivery shape
early delivery shape -> architecture refinement
architecture refinement -> readiness
readiness -> quality gates
quality gates -> handoff
handoff -> implementation
implementation -> review
```

If Copilot cannot explain the current stage and the required next artifact, stop and re-establish workflow status first.

For small changes, prefer the lightest safe path rather than the full path by default, but do not skip readiness or triggered gates when risk is real.

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
Implement Task 001 from the active deliverable using .brs2spec/8-copilot-implementation/01-implement-one-task.md.
Review the implementation using .brs2spec/9-reviewers/01-senior-code-review.md.
Create the GitLab Planning View as a projection from the source artifacts.
```
