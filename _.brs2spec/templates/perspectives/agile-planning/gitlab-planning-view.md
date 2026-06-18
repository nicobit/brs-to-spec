# GitLab Planning View

> This file is a planning projection.
> It is not the source of truth.
> If scope, requirements, architecture constraints, quality gates or implementation tasks change,
> update the source artifacts first and regenerate this view.
> User stories provide business context and traceability.
> Engineers implement from approved OpenSpec or standalone tasks, not from user stories alone.
> Primary consumer: delivery team, Product Owner, scrum master / PM
> Purpose of this artifact: project approved source artifacts into Agile-tool language for coordination and tracking
> Downstream use: GitLab / Jira / Azure DevOps planning and delivery coordination
> Do not duplicate: requirements truth, architecture truth, acceptance truth, or implementation task truth
> Keep this view easy to scan and useful for coordination.
> Prefer concise projections over dense explanation.
> Include only engineering notes, enablement needs, and tracking items that are supported by source artifacts.
> Keep hierarchy, task projection, and gate-tracking detail only to the level needed for planning-tool coordination.
> Keep narrative notes brief. If a section becomes long, the source artifact probably carries the real detail.

## Metadata

| Field | Value |
|---|---|
| Initiative |  |
| Active deliverable |  |
| Delivery mode |  |
| Execution mode | OpenSpec / Standalone |
| Readiness status |  |
| Source of truth |  |
| Generated from |  |
| Generated date |  |
| View status | Draft / Updated / Stale |

## Planning Summary

Stories in this view should come from `planning/delivery-structure.md` and remain traceable to requirements and downstream implementation tasks.
Keep the summary brief. Do not restate the whole initiative.

## Agile Delivery Breakdown

Keep this section concise and projection-focused.

## Source Artifact Map

| Source artifact | Path | Purpose | Used in this view? |
|---|---|---|---|

## Suggested GitLab Hierarchy

Only include the hierarchy needed for the active initiative shape.

| GitLab level | Suggested title | Source artifact | Source ID | Notes |
|---|---|---|---|---|
| Epic / Parent epic |  |  |  |  |
| Feature / Epic / Issue |  |  |  |  |
| User story / Issue |  |  |  |  |
| Task / Checklist item |  |  |  |  |

## Epic Projection

Keep entries concise. Reference source detail rather than retelling it.

| Field | Value | Source |
|---|---|---|
| Epic title |  |  |
| Epic goal |  |  |
| Business value |  |  |
| Scope |  |  |
| Out of scope |  |  |
| Related requirements |  |  |
| Related architecture constraints |  |  |
| Related quality gates |  |  |

## Feature / Issue Projection

Keep descriptions short and coordination-oriented.

| Initiative ID | Suggested GitLab title | Description | Business value | Source deliverable | Related requirements | Dependencies | Labels |
|---|---|---|---|---|---|---|---|

## User Story Projection

Keep user stories readable and traceable. Do not attach duplicated acceptance detail here.

| Story ID | Suggested GitLab title | User story in format `As a <persona>, I want <capability>, so that <business value>.` | Source artifact path | Source requirement ID | Acceptance source | Quality gate references | Labels |
|---|---|---|---|---|---|---|---|

## Engineering Notes

List only notes that change implementation, validation, sequencing, or coordination.

| Note area | Summary | Source artifact | Source ID / reference |
|---|---|---|---|
| Components affected |  |  |  |
| Architecture constraints |  |  |  |
| API impact |  |  |  |
| Data impact |  |  |  |
| Event impact |  |  |  |
| Security considerations |  |  |  |
| Observability considerations |  |  |  |
| Dependencies |  |  |  |
| Assumptions and risks |  |  |  |

## Enablement Needs

Only include needs that are real prerequisites or clear delivery accelerators.

| Need | Reason / trigger | Source artifact | Suggested GitLab item | Owner / role | Required before |
|---|---|---|---|---|---|

## GitLab / Agile Tool Mapping

## Task / Checklist Projection

Project only task detail needed for planning-tool tracking. Engineers still implement from source tasks.

| Task ID | Suggested task / checklist item | Source artifact | Source ID | Validation / evidence expected | Required before | Owner / Team |
|---|---|---|---|---|---|---|

## Quality Gate Actions to Track

| Gate | Action | Source artifact | Required before | Suggested GitLab representation | Owner |
|---|---|---|---|---|---|

## Suggested Labels

Keep labels minimal and useful. Do not generate label clutter.

| Label | Reason |
|---|---|

## Suggested Milestone / Iteration

Keep this section brief and source-linked.

| Field | Value | Source / Notes |
|---|---|---|

## Engineering Consumption Model

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

Engineers use user stories for business context.

Engineers use OpenSpec or standalone tasks for implementation.

## Sync Notes

| Item | Source of truth | What to do if this changes |
|---|---|---|

## Acceptance Source Notes

Do not duplicate full acceptance criteria here.

Reference the acceptance source instead, for example:

```text
BDD scenarios
delivery spec
OpenSpec tasks
standalone validation plan
traceability matrix
```

## Source Traceability

| Planning item | Source artifact | Source ID / reference | Notes |
|---|---|---|---|

## Stale View Handling

If any source artifact used by the active initiative path changes, mark the view status as `Stale`, update the source artifact map, and regenerate this projection rather than editing planning items independently.

Examples:

- `planning/delivery-increments.md` when the initiative uses Modular Delivery
- `specs/.../tasks.md` when OpenSpec mode is used
- `standalone-delivery/.../tasks.md` when standalone mode is used

## Do Not Duplicate

List any content that should not be copied as independent truth into GitLab.
Keep this list short and specific.

## Open Questions
