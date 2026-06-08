# Codex Prompt - Improve `main` for Agile Delivery Without Adding Complexity

You are working on the `main` branch of `nicobit/brs-to-spec`.

Act as a senior software architect, Agile delivery coach, enterprise delivery governance expert, GitHub Copilot workflow designer, and technical writer.

## Goal

Improve the `main` branch so it is easier to understand and use in a real Agile delivery setup, without making the framework heavier or more complex.

Do **not** redesign the framework.

Do **not** add multiple new tracks.

Do **not** add mandatory artifacts unless they are already part of the existing workflow.

Do **not** replace the initiative workspace model.

Do **not** revert to branch `0.0.5`.

Instead, improve `main` by recovering the useful team-facing concepts from `0.0.5`:

```text
Epics
Features
User Stories
Acceptance source
Engineering notes
Enablement needs
GitLab / Agile mapping
```

Express them through one simple team-facing planning artifact, not through several new flows.

---

# Current situation

The current `main` branch is strong because it has:

```text
initiatives/<initiative-id>-<slug>/
```

as the operating model.

It also supports:

```text
one or more BRS inputs
optional architecture inputs
business intake
architecture review
delivery planning
engineering readiness
conditional quality gates
OpenSpec mode
Standalone mode
Business Copilot mode
GitHub Copilot / VS Code workflow guidance
GitLab Planning View
Copilot implementation prompts
reviewer prompts
```

This should remain the baseline.

However, the framework must be easier for Agile teams to understand.

A real Agile delivery team expects to see:

```text
Epic
Feature
User Story
Acceptance Criteria / Acceptance source
Engineering notes
Enablement needs
GitLab or planning-tool mapping
```

The solution is **not** to add many new tracks.

The solution is to improve the existing planning perspective into a single, simple, team-facing view.

---

# Main design decision

Create or improve one artifact:

```text
perspectives/delivery-planning/delivery-planning-view.md
```

or, if the repository already has:

```text
perspectives/agile-planning/gitlab-planning-view.md
```

then either:

1. extend it and rename the concept to **Delivery Planning View**, or
2. keep the GitLab file name but make the content clearly serve as the Delivery Planning View.

Choose the least disruptive option.

The important concept is:

```text
Delivery Planning View = team-facing planning projection
```

It is not the source of truth.

It is not a new workflow.

It is not a replacement for engineering readiness, quality gates, OpenSpec, or standalone delivery.

It is a readable projection that helps the team understand what to create in GitLab or another Agile planning tool.

Prefer extending the current planning-view assets unless there is a clear benefit to renaming them.

---

# Source-of-truth rule

The Delivery Planning View must clearly state:

```text
This is a planning projection.
It is not the source of truth.
```

The source of truth remains the initiative workspace artifacts:

```text
initiatives/<initiative-id>-<slug>/
  input/
  business-intake/
  architecture/
  planning/
  engineering-readiness/
  quality-gates/
  openspec/ or standalone-delivery/
```

The Delivery Planning View must reference source artifact paths and IDs whenever possible.

Do not duplicate source-of-truth content unnecessarily.

---

# Critical rule: User stories are not the engineering contract

Add this rule clearly to the relevant documentation, prompts, templates, and Copilot instructions.

The relationship must be explicit:

```text
User Story = business/user intent and traceability.
Acceptance source = expected behavior and validation reference.
OpenSpec / standalone package = engineering execution contract.
Tasks = what engineers and Copilot implement.
```

Engineers must **not** implement from user stories alone.

The correct flow is:

```text
Requirement
  -> User Story
  -> Acceptance source / BDD / validation reference
  -> OpenSpec or standalone proposal/design/tasks
  -> implementation task
  -> code
```

The wrong flow is:

```text
User Story
  -> direct implementation
```

When creating OpenSpec or standalone handoff artifacts, include traceability back to:

```text
Epic
Feature / Capability
User Story
Requirement ID
Acceptance source
Architecture constraint
Quality gate
```

OpenSpec or standalone tasks should reference the related user story, but the task itself must contain the engineering-ready behavior, constraints, validation expectations, and implementation scope.

Add this clarification wherever relevant, especially in:

```text
README.md
HOW_TO_USE.md
.github/copilot-instructions.md
docs/15-github-copilot-workflow.md
prompts/5-handoff/
prompts/7-perspectives/
templates/perspectives/
```

---

# Required content of the Delivery Planning View

The Delivery Planning View should contain these sections.

## 1. Planning Summary

Include:

```text
Initiative ID
Initiative name
Delivery mode
Execution mode
Active deliverable
Readiness status
Main source artifacts
Last generated / refreshed date
```

## 2. Agile Delivery Breakdown

Use team-friendly Agile language:

```text
Business Objective
Epic
Feature / Capability
User Story
Acceptance source
Source requirement
Quality gate reference
Suggested labels
```

User stories must use the classic format:

```text
As a <persona>,
I want <capability>,
so that <business value>.
```

Acceptance criteria should not be duplicated as the source of truth.

Instead, reference the acceptance source, for example:

```text
BDD scenarios
delivery spec
OpenSpec tasks
standalone validation plan
traceability matrix
business intake summary
```

Each user story must explain its downstream consumption:

```text
Used as business context and traceability for OpenSpec / standalone tasks.
Not sufficient for direct implementation.
```

## 3. Engineering Notes

Do not call this "Technical Planning".

Use the heading:

```text
Engineering Notes
```

This section should summarize practical implementation-relevant information without becoming a new technical-spec workflow.

Include only what exists or is clearly derived from source artifacts:

```text
components affected
architecture constraints
API impact
data impact
event impact
security considerations
observability considerations
dependencies
important assumptions
implementation risks
```

Every note should reference the source artifact.

Do not invent architecture.

Do not create a separate mandatory `technical-spec.md` unless the repository already has such a pattern and it is optional.

## 4. Enablement Needs

Use the heading:

```text
Enablement Needs
```

This section exists only to make visible work that Agile teams often forget.

Include enablement needs only when they are present or triggered by source artifacts:

```text
CI/CD
infrastructure
environment configuration
secrets
permissions
monitoring
alerting
logging
release / rollback
SRE or support handover
operational readiness
documentation
```

Do not turn this into a separate enablement track.

Do not make enablement mandatory for every initiative.

For each enablement need include:

```text
Need
Reason / trigger
Source artifact
Suggested GitLab item
Owner / role
Required before
```

## 5. GitLab / Agile Tool Mapping

Map the initiative to GitLab or another Agile planning tool.

Include:

```text
Suggested Epic
Suggested Features / Issues
Suggested User Stories
Suggested Tasks / Checklists
Suggested Milestones
Suggested Labels
Blocking dependencies
Quality gate actions
Enablement tasks
```

Do not invent real GitLab issue IDs.

Use placeholder IDs only, for example:

```text
GL-EPIC-TBD
GL-ISSUE-TBD
```

The mapping must show that GitLab user stories are planning items, while OpenSpec or standalone tasks are the engineering implementation contract.

## 6. Engineering Consumption Model

Add a dedicated section explaining how engineers use the planning view.

Include this model:

```text
Agile item:
Epic / Feature / User Story

Engineering input:
OpenSpec or standalone proposal, design, and tasks

Engineer implementation source:
One approved implementation task at a time

Traceability:
Task links back to requirement, user story, acceptance source, architecture constraint, and quality gates
```

State clearly:

```text
Engineers use user stories for business context.
Engineers use OpenSpec or standalone tasks for implementation.
```

## 7. Staleness and Refresh Rules

Clearly explain when the Delivery Planning View becomes stale.

It becomes stale if any source artifacts used by the current initiative path change, for example:

```text
BRS input
architecture input
business intake summary
delivery structure
delivery increments (when modular delivery is used)
traceability matrix
engineering readiness
quality gates
OpenSpec tasks (when OpenSpec mode is used)
standalone delivery tasks (when standalone mode is used)
execution mode
```

If stale, update the source artifacts first, then regenerate the Delivery Planning View.

---

# Prompt changes required

Review and update the relevant prompt files.

Most likely files:

```text
prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md
prompts/7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md
```

or create:

```text
prompts/7-perspectives/delivery-planning/01-create-delivery-planning-view.md
prompts/7-perspectives/delivery-planning/02-refresh-delivery-planning-view.md
```

Choose the least disruptive structure.

The prompts must follow the repository's standard quality pattern:

```text
Role
Context
Purpose
Inputs
Output path
Required output structure
Quality bar
Anti-patterns
Stop conditions
Self-review checklist
```

The prompt must enforce:

```text
one initiative workspace
source traceability
no duplicate source of truth
classic Agile user story format
Engineering Notes instead of Technical Planning
Enablement Needs only when relevant
Delivery Planning View as projection only
user stories are business context, not engineering contract
OpenSpec / standalone tasks are engineering execution input
```

---

# Handoff prompt changes required

Review the handoff prompts, especially:

```text
prompts/5-handoff/
```

Ensure OpenSpec and standalone handoff prompts explicitly consume:

```text
requirements
user stories
acceptance source
architecture constraints
readiness check
quality gates
```

but generate engineering-ready artifacts:

```text
proposal
design
tasks
validation expectations
implementation scope
```

Add a rule:

```text
Do not copy user stories as implementation tasks.
Convert user stories and acceptance sources into engineering-ready tasks with traceability.
```

Each generated task should reference:

```text
Requirement ID
User Story ID
Acceptance source
Architecture constraint
Quality gate reference
Validation expectation
```

---

# Template changes required

Review and update the relevant template files.

Most likely files:

```text
templates/perspectives/agile-planning/gitlab-planning-view.md
templates/perspectives/agile-planning/gitlab-refresh-report.md
```

or create:

```text
templates/perspectives/delivery-planning/delivery-planning-view.md
templates/perspectives/delivery-planning/delivery-planning-refresh-report.md
```

Choose the least disruptive structure.

The template must include:

```text
Planning Summary
Agile Delivery Breakdown
Engineering Notes
Enablement Needs
GitLab / Agile Tool Mapping
Engineering Consumption Model
Source Traceability
Staleness and Refresh Rules
Open Questions
```

---

# Documentation changes required

Update documentation so the framework remains simple.

Most likely files:

```text
README.md
HOW_TO_USE.md
docs/14-agile-planning-view.md
docs/15-github-copilot-workflow.md
.github/copilot-instructions.md
```

Add a clear explanation:

```text
The Delivery Planning View is the single team-facing planning projection.
It combines Agile breakdown, engineering notes, enablement needs, and GitLab mapping.
It is not a new workflow and not a source of truth.
```

Add another clear explanation:

```text
User stories provide business intent and traceability.
OpenSpec / standalone tasks provide the engineering implementation contract.
Engineers should not implement from user stories alone.
```

Make sure the docs do not imply that teams must run multiple new planning tracks.

Avoid language like:

```text
Technical Planning
Enablement Track
Agile Track
```

unless those already exist and are explicitly optional.

Prefer:

```text
Delivery Planning View
Engineering Notes
Enablement Needs
```

---

# Copilot instruction changes required

Update:

```text
.github/copilot-instructions.md
```

Make sure GitHub Copilot understands:

```text
work inside one initiative workspace
do not implement from raw BRS
do not implement from user stories alone
do not create tasks for the whole initiative at once
use OpenSpec / standalone package as implementation input
treat Delivery Planning View as a projection only
use classic Agile user story format when creating planning projections
use Engineering Notes, not Technical Planning
include Enablement Needs only when source artifacts justify them
```

Add this explicit rule:

```text
When implementing code, use one approved OpenSpec / standalone task as the implementation unit.
Use linked user stories only for business context and validation traceability.
```

---

# Validation changes required

Update validation scripts if needed.

Likely file:

```text
tools/scripts/check_program.py
```

Validation should check for:

```text
Delivery Planning View prompt or improved GitLab Planning View prompt
Delivery Planning View template or improved GitLab Planning View template
README mentions Delivery Planning View
HOW_TO_USE explains when to generate it
Copilot instructions mention projection-only planning view
classic Agile user story format is present
Engineering Notes heading is present
Enablement Needs heading is present
source-of-truth warning is present
user stories are not engineering contract
OpenSpec / standalone tasks are implementation input
```

Do not over-engineer validation.

---

# Example changes required

If an example exists under:

```text
examples/
```

or:

```text
initiatives/
```

update one compact example to show the Delivery Planning View.

The example should demonstrate:

```text
Epic
Feature
User Story
Acceptance source
Engineering Notes
Enablement Needs
GitLab mapping
Engineering consumption model
Source artifact references
```

Keep the example compact.

Do not create a huge artificial example.

---

# Important constraints

Do not make the framework harder to understand.

Do not add three separate flows for:

```text
Agile Planning
Technical Planning
Enablement Planning
```

Do not call the section "Technical Planning".

Use:

```text
Engineering Notes
```

Do not make enablement mandatory.

Use:

```text
Enablement Needs
```

Do not duplicate acceptance criteria as a second source of truth.

Do not create real GitLab IDs.

Do not allow direct implementation from user stories.

Do not remove:

```text
OpenSpec mode
Standalone mode
Business Copilot mode
Copilot instructions
quality gates
reviewer prompts
initiative workspace model
```

Do not replace initiative workspaces with feature workspaces unless the repository already consistently uses feature workspaces. `main` should keep its current initiative model.

---

# Expected output from you

After making changes, provide:

## A. Summary

Explain what you changed and why.

## B. Design decision

Explain why the solution uses one Delivery Planning View instead of multiple new tracks.

## C. Engineering consumption model

Explain how user stories, acceptance sources, OpenSpec / standalone tasks, and implementation relate to each other.

## D. Files changed

List the files changed.

## E. Validation

Run the available validation scripts and report results.

## F. Recommendation

State whether `main` is now better suited for an Agile delivery team without becoming more complex.

Proceed with the improvement.
