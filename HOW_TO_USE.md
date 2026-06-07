# How to Use This Framework

## Workspace rule

Work inside one feature workspace at a time.

The standard workspace shape is:

```text
features/<feature-id>-<slug>/
```

Create a new workspace with:

```bash
python tools/scripts/new_feature.py onboarding-request --feature-id F001 --mode enterprise --execution-mode openspec
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
python tools/scripts/add_brs.py features/F001-onboarding-request compliance
python tools/scripts/add_architecture.py features/F001-onboarding-request security-constraints
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

All prompt input and output paths are relative to the current feature workspace, not the repository root.

## Step 0 - Prepare inputs

Inside the feature workspace, maintain either:

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

This is the main Product Owner review artifact for the current feature workspace.

## Step 3 - Review architecture

Run:

```text
prompts/3-planning-and-modular-delivery/02-review-initial-architecture.md
prompts/3-planning-and-modular-delivery/03-create-global-architecture-rules.md
```

Outputs:

```text
architecture/architecture-review.md
architecture/architecture-rules.md
```

## Step 4 - Plan delivery

For Enterprise Path, run:

```text
prompts/3-planning-and-modular-delivery/01-create-delivery-structure.md
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

## Step 8 - Review template quality

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

Do not generate tasks for the whole feature at once.

Do not skip architecture constraints.

Do not call triggered quality gates optional.

Do not force Product Owners to review low-level engineering details.

Do not use standalone mode as a lower-quality version of OpenSpec.

Do not mix outputs from different features in the same workspace.

## Step 9 - Create GitLab Planning View

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

Do not edit the planning view to change scope, requirements, architecture constraints, quality gates, or implementation tasks.

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
Based on .github/copilot-instructions.md, identify the active feature workspace, the current workflow stage, and the next artifact to create.
```

Do not ask Copilot to implement directly from raw BRS sources.
