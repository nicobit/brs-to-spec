# How to Use This Framework

## Workspace rule

Work inside one initiative workspace at a time.

The standard workspace shape is:

```text
initiatives/<initiative-id>-<slug>/
```

Create a new workspace with:

```bash
python tools/scripts/new_initiative.py onboarding-request --initiative-id I001 --mode enterprise --execution-mode openspec
```

## Default input mode

Start simple unless the same initiative clearly has multiple source documents:

```text
input/brs.md
input/architecture.md
input/input-package.md
```

## Expanded input mode

If the same initiative is described by more than one BRS or more than one architecture source, expand only that input family:

```bash
python tools/scripts/add_brs.py initiatives/I001-onboarding-request compliance
python tools/scripts/add_architecture.py initiatives/I001-onboarding-request security-constraints
```

After expansion, the workspace can look like:

```text
input/brs/
  main.md
  compliance.md
input/architecture/
  main.md
  security-constraints.md
input/input-package.md
```

All prompt input and output paths are relative to the current initiative workspace, not the repository root.

## Step 0 - Prepare inputs

Inside the initiative workspace, maintain either:

```text
input/brs.md
input/architecture.md
input/input-package.md
```

or, when needed:

```text
input/brs/*.md
input/architecture/*.md
input/input-package.md
```

Run:

```text
prompts/0-input-preparation/01-convert-brs-word-to-markdown.md
prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md
prompts/0-input-preparation/03-normalize-input-package.md
```

Use `input/input-package.md` to record:

```text
source inventory
completeness
overlap
conflicts
assumptions
consolidation notes
```

## Step 1 - Select delivery and execution mode

Run:

```text
prompts/1-routing/01-select-delivery-and-execution-mode.md
```

Output:

```text
routing/routing-decision.md
```

## Step 2 - Create business intake summary

Run:

```text
prompts/2-business-intake/01-create-business-intake-summary.md
```

Output:

```text
business-intake/business-intake-summary.md
```

This is the main Product Owner review artifact for the current initiative workspace.

## Step 3 - Review architecture

Run:

```text
prompts/3-planning-and-modular-delivery/01-review-initial-architecture.md
prompts/3-planning-and-modular-delivery/02-create-global-architecture-rules.md
```

Outputs:

```text
architecture/architecture-review.md
architecture/architecture-rules.md
```

## Step 4 - Plan delivery

For Enterprise Path, run:

```text
prompts/3-planning-and-modular-delivery/03-create-delivery-structure.md
prompts/3-planning-and-modular-delivery/07-create-traceability-matrix.md
```

For Enterprise + Modular Delivery, also run:

```text
prompts/3-planning-and-modular-delivery/04-identify-software-modules.md
prompts/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md
prompts/3-planning-and-modular-delivery/06-define-delivery-increments.md
```

## Step 5 - Check engineering readiness

Run:

```text
prompts/4-engineering-readiness/01-check-engineering-readiness.md
```

Output:

```text
engineering-readiness/readiness-check.md
```

The readiness check decides whether the active deliverable is ready and which quality gates are triggered.

## Step 6 - Run required Conditional Quality Gates

Run only gates where:

```text
Triggered = Yes
Required = Yes
```

Quality gates are not optional. They are conditional.

These gate artifacts are pre-implementation or pre-release governance artifacts.

They are not the same as downstream implementation review prompts.

If the initiative creates or changes a governed boundary, the corresponding contract gate should normally be triggered:

- governed service or API boundary -> `API contract`
- governed data ownership or schema boundary -> `Data contract`
- governed asynchronous event boundary -> `Event contract`

## Step 7A - OpenSpec handoff

Run:

```text
prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md
```

Output:

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

The generated tasks are the engineering implementation contract for OpenSpec mode.

They should preserve traceability back to requirements, user stories when available, acceptance sources, architecture constraints, and quality gates.

## Step 7B - Standalone handoff

Run:

```text
prompts/5-handoff/02-create-standalone-delivery-package.md
```

Output:

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

The generated tasks are the engineering implementation contract for Standalone mode.

They should preserve traceability back to requirements, user stories when available, acceptance sources, architecture constraints, and quality gates.

## Step 8 - Optional ready-for-Copilot gate

Before asking a coding agent to implement, you may complete:

```text
templates/quality-gates/ready-for-copilot-checklist.md
```

Use it to confirm the active deliverable, implementation source, readiness state, and required quality gates.

## Step 9 - Implement one task

Use a coding-agent environment such as VS Code Copilot Agent mode only after the handoff artifacts exist.

Run:

```text
prompts/8-copilot-implementation/01-implement-one-task.md
```

If review findings come back, use:

```text
prompts/8-copilot-implementation/02-fix-review-comments.md
```

Do not implement from user stories alone.

Use user stories for business context and traceability.

Use one approved OpenSpec or standalone task as the implementation unit.

## Step 10 - Review implemented work

Run the review prompts that match the change:

```text
prompts/9-reviewers/01-senior-code-review.md
prompts/9-reviewers/02-qa-review.md
prompts/9-reviewers/03-architecture-review.md
prompts/9-reviewers/04-security-review.md
```

These prompts review actual code and tests after implementation.

They do not replace the quality-gate artifacts created earlier in the workflow.

## Step 11 - Review template quality

For every generated artifact, check:

```text
Decision clear?
Evidence included?
Risk stated?
Owner assigned?
Required-before stage clear?
Traceability preserved?
```

If an artifact does not answer these questions, regenerate it using the same prompt and the template as a stricter quality bar.

## Important rules

Do not generate tasks for the whole initiative at once.

Do not skip architecture constraints.

Do not call triggered quality gates optional.

Do not force Product Owners to review low-level engineering details.

Do not use standalone mode as a lower-quality version of OpenSpec.

Do not mix outputs from different initiatives in the same workspace.

## Step 12 - Create GitLab Planning View

Use this only when the delivery team plans and tracks work in GitLab, Jira, Azure DevOps or a similar planning tool.

Run after delivery increments and preferably after readiness check:

```text
prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md
```

Output:

```text
perspectives/agile-planning/gitlab-planning-view.md
```

This file is a planning projection, not the source of truth.

It is also not the engineering contract.

Do not edit the planning view to change scope, requirements, architecture constraints, quality gates, or implementation tasks.

Use the planning view to show Agile breakdown, Engineering Notes, Enablement Needs, and GitLab mapping in one place.

User stories in this view provide business context and traceability.

Implementation still happens from approved OpenSpec or standalone tasks.

If something changes, update the source artifacts and regenerate the view.

To refresh the view after readiness or quality gates change, run:

```text
prompts/7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md
```

## Using GitHub Copilot / VS Code

This repository includes repository-level Copilot instructions:

```text
.github/copilot-instructions.md
```

Useful prompt files:

```text
.github/prompts/brs-to-spec-run-workflow.prompt.md
.github/prompts/create-engineering-readiness.prompt.md
.github/prompts/create-openspec-handoff.prompt.md
.github/prompts/create-standalone-handoff.prompt.md
.github/prompts/create-gitlab-planning-view.prompt.md
```

Recommended first Copilot request:

```text
Based on .github/copilot-instructions.md, identify the active initiative workspace, the current workflow stage, and the next artifact to create.
```

Do not ask Copilot to implement directly from raw BRS sources.
