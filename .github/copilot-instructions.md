# GitHub Copilot Instructions — BRS to Delivery Readiness Framework

## Purpose of this repository

This repository is not a normal application codebase.

It is an enterprise delivery-readiness framework that transforms:

```text
BRS + initial architecture
```

into:

```text
business-approved, architecture-aligned, delivery-ready increments
```

using either:

```text
OpenSpec mode
Standalone mode
Business Copilot mode
```

## Core positioning

Do not treat this repository as a coding project where the goal is to generate application code directly.

The purpose is to guide business analysis, architecture-aware planning, engineering readiness, quality gates, and handoff to OpenSpec or standalone delivery.

## Source of truth hierarchy

Respect this order:

```text
1. input/brs.md
2. input/initial-architecture.md
3. input/input-package.md
4. business-intake/business-intake-summary.md
5. architecture/initial-architecture-review.md
6. architecture/global-architecture-rules.md
7. planning/delivery-increments.md
8. planning/traceability-matrix.md
9. engineering-readiness/readiness-check.md
10. quality-gates/*.md
11. openspec/changes/... or standalone-delivery/...
12. perspectives/agile-planning/gitlab-planning-view.md
```

The Agile / GitLab Planning View is a projection only. It is not the source of truth.

## Architecture rule

If `input/initial-architecture.md` defines a constraint, do not override it unless explicitly marked as:

```text
conflict
open decision
accepted deviation
```

Do not invent architecture.

## Workflow rule

Before creating implementation tasks, verify that the workflow has passed through:

```text
input preparation
routing
business intake
architecture review
delivery planning
engineering readiness
required Conditional Quality Gates
```

For small changes, Fast Path may go directly to OpenSpec or standalone handoff, but only if the change is already clear.

## Delivery modes

Use the smallest safe delivery mode:

```text
Fast Path
Standard Path
Enterprise Path
Enterprise + Modular Delivery
```

Do not automatically choose Enterprise + Modular for every request.

## Execution modes

OpenSpec is the default downstream, but it is not mandatory.

Choose one:

```text
OpenSpec
Standalone
Business Copilot
```

Use Standalone mode when the team does not use OpenSpec.

## Conditional Quality Gates

Quality gates are not optional.

They are conditional:

```text
not always required
but mandatory when triggered
```

If `engineering-readiness/readiness-check.md` marks a gate as:

```text
Triggered = Yes
Required = Yes
```

then the corresponding gate artifact must be created before the required-before stage.

Common gates:

```text
BDD scenarios
test strategy
QA review
architecture review
security review
release readiness review
API contract
data contract
event contract
threat model
observability plan
```

## Agile / GitLab Planning View rule

The GitLab Planning View maps delivery artifacts to:

```text
Epic
Feature / Issue
User Story
Task / Checklist
Milestone
Labels
```

but must not redefine:

```text
requirements
architecture constraints
acceptance criteria
quality gates
implementation tasks
```

Always include source artifact paths and IDs.

## User story format

When creating user story projections, use the classic format:

```text
As a <persona>,
I want <capability>,
so that <business value>.
```

But do not duplicate full acceptance criteria as the source of truth. Reference the acceptance source instead:

```text
BDD scenarios
delivery spec
OpenSpec tasks
standalone validation plan
traceability matrix
```

## Output quality

All outputs must be:

```text
evidence-based
traceable
decision-oriented
risk-aware
actionable
reviewable
```

Avoid generic statements like:

```text
Looks good.
Add tests.
Security should be considered.
Architecture is aligned.
```

Prefer:

```text
Control area | Status | Evidence | Gap / Risk | Required action | Owner | Required before
```

## Do not

Do not:

- generate application code directly from a raw BRS
- create tasks for the whole BRS at once
- ignore the initial architecture document
- call triggered quality gates optional
- duplicate source-of-truth content in the planning view
- invent GitLab issue IDs
- invent missing requirements, architecture decisions, or acceptance criteria
- treat standalone mode as lower quality than OpenSpec mode

## Recommended behavior in Copilot Chat

When asked to help with this repository:

1. Identify the user’s current workflow step.
2. Ask which source artifacts exist only if that is unclear.
3. Recommend the next prompt to run.
4. Generate or update only the relevant artifact.
5. Preserve source IDs and paths.
6. Include evidence, risk, owner, required-before, and traceability.
7. Do not create unrelated files.
