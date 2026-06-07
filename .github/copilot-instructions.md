# GitHub Copilot Instructions - BRS to Delivery Readiness Framework

## Purpose of this repository

This repository is not a normal application codebase.

It is an enterprise delivery-readiness framework that transforms:

```text
one or more BRS inputs + optional architecture inputs
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

## Initiative workspace rule

Operate inside one initiative workspace at a time.

The standard workspace shape is:

```text
initiatives/<initiative-id>-<slug>/
```

All workflow paths are relative to the active initiative workspace.

The canonical source set for a feature starts with:

```text
input/brs.md or input/brs/*.md
input/architecture.md or input/architecture/*.md
input/input-package.md
```

Start with `input/brs.md` and `input/architecture.md`. Expand to folders only when the same initiative genuinely has multiple source documents.

## Source of truth hierarchy

Respect this order within the active initiative workspace:

```text
1. input/brs.md or input/brs/*.md
2. input/architecture.md or input/architecture/*.md
3. input/input-package.md
4. business-intake/business-intake-summary.md
5. architecture/architecture-review.md
6. architecture/architecture-rules.md
7. planning/delivery-increments.md
8. planning/traceability-matrix.md
9. engineering-readiness/readiness-check.md
10. quality-gates/*.md
11. openspec/changes/... or standalone-delivery/...
12. perspectives/agile-planning/gitlab-planning-view.md
13. implementation and review helper outputs
```

The Agile / GitLab Planning View is a projection only. It is not the source of truth.

Implementation summaries, review comments, and reviewer prompt outputs are downstream helper artifacts only.

## Coding-agent boundary

Do not start coding from raw source inputs.

Code implementation should begin only when the active initiative workspace has:

```text
engineering-readiness/readiness-check.md
required quality gates completed or explicitly accepted as risk
openspec/changes/D1-.../tasks.md
or standalone-delivery/D1-.../tasks.md
```

If `quality-gates/ready-for-copilot-checklist.md` exists, use it as the final implementation gate.

## Consolidation rule for multiple source files

When multiple BRS or architecture files exist:

```text
analyze all files in the relevant input folder
preserve source document names and section references
record overlap, conflicts, and assumptions in input/input-package.md
do not silently merge conflicting statements without noting the conflict
```

## Architecture rule

If the architecture input defines a constraint, do not override it unless explicitly marked as:

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

## Implementation rule

When using a coding agent:

```text
implement one task at a time
read the active feature artifacts first
inspect existing similar code before changing files
update tests with behavior changes
return assumptions, risks, and open questions
```

Do not implement future tasks in the same pass.

## Review rule

After implementation, use the review prompts under:

```text
prompts/9-reviewers/
```

Treat review prompts as implementation review surfaces, not as replacements for artifact-generation quality gates.

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

Always include source artifact paths and source IDs or source file names.

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

- generate application code directly from raw BRS sources
- create tasks for the whole feature at once
- ignore the architecture input
- call triggered quality gates optional
- duplicate source-of-truth content in the planning view
- invent GitLab issue IDs
- invent missing requirements, architecture decisions, or acceptance criteria
- mix outputs from different initiative workspaces
- treat standalone mode as lower quality than OpenSpec mode

## Recommended behavior in Copilot Chat

When asked to help with this repository:

1. Identify the active initiative workspace.
2. Identify the user's current workflow step.
3. Ask which source artifacts exist only if that is unclear.
4. Recommend the next prompt to run.
5. Generate or update only the relevant artifact inside that initiative workspace.
6. Preserve source paths and traceability.
7. Include evidence, risk, owner, required-before, and traceability.
8. Do not create unrelated files.

