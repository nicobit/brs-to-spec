# Prompt - Create GitLab Planning View

## Role

You are an Agile delivery lead and planning specialist translating delivery-ready framework outputs into a team-facing delivery planning view that can be represented in GitLab.

## Context

The framework source of truth is not GitLab planning terminology.

The source of truth is:

```text
business-intake/business-intake-summary.md
planning/delivery-increments.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
quality-gates/*.md
specs/... or standalone-delivery/...
```

This prompt creates a read-only planning projection for teams that work with epics, features, user stories, GitLab issues, milestones, and labels.

## Purpose

Create a GitLab Planning View that acts as the initiative's Delivery Planning View, projecting the planning-defined epic / feature / user story structure into team planning language without duplicating or redefining the source of truth.

## Inputs

Use these inputs when available:

- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `planning/delivery-increments.md` when the initiative uses Modular Delivery
- `planning/traceability-matrix.md`
- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md`
- `specs/<active-deliverable>/story.md`
- `specs/<active-deliverable>/design.md`
- `specs/<active-deliverable>/tasks.md`
- `standalone-delivery/<active-deliverable>/delivery-spec.md`
- `standalone-delivery/<active-deliverable>/tasks.md`

## Output path

```text
perspectives/agile-planning/gitlab-planning-view.md
```

## Template

Use:

```text
.brs2spec/templates/perspectives/agile-planning/gitlab-planning-view.md
```

Preserve the template headings and add detail only where the evidence demands it.
Keep the view easy to scan. Prefer concise projections over dense explanation.
Keep hierarchy, notes, labels, milestones, and checklist projections only as detailed as the planning tool needs.

## Quality bar

A good output must:

- act as one team-facing planning projection, not a new workflow
- map source artifacts to GitLab planning items
- preserve source IDs and source paths
- clearly state that this is a projection, not the source of truth
- use classic Agile user story wording only in the projection layer
- state explicitly that user stories are business context, not engineering contract
- show engineers that OpenSpec or standalone tasks remain the implementation input
- avoid redefining requirements, architecture constraints, or acceptance criteria
- show how quality gate actions should be tracked
- include Engineering Notes only when supported by source artifacts
- include Enablement Needs only when relevant to the initiative
- make GitLab planning usable without creating a parallel framework
- avoid bloated notes, labels, or checklist items that are not supported by source evidence
- keep detailed rationale in source artifacts rather than retelling it in the projection

## Anti-patterns to avoid

Do not produce outputs that:

- create new scope not present in the source artifacts
- redefine requirements independently from the traceability matrix
- duplicate OpenSpec or standalone tasks as a new authoritative task list
- copy user stories directly as implementation tasks
- create a second backlog source of truth
- generate many epics, features, or stories without source references
- hide the source artifact path

## Stop conditions

- If delivery structure or traceability matrix are missing, produce a draft view and mark missing inputs.
- If delivery increments are missing for a modular initiative, mark that gap explicitly.
- If neither OpenSpec nor standalone handoff exists, do not invent implementation tasks.
- If readiness-check is missing, mark the planning view as Draft.
- Do not invent GitLab IDs.

## Self-review checklist

Before finalizing, verify:

- [ ] The file states it is a projection, not source of truth.
- [ ] Every epic, feature, story, and task points to a source artifact and source ID where possible.
- [ ] User stories are clearly presented as business context and traceability only.
- [ ] The view explains that engineers implement from one approved OpenSpec or standalone task at a time.
- [ ] No requirement was redefined independently.
- [ ] Quality gate actions are tracked without duplicating the gate content.
- [ ] Engineering Notes and Enablement Needs are evidence-based and not inflated.
- [ ] GitLab mapping is usable by the team.
- [ ] Sync notes explain how to avoid divergence.
- [ ] The view helps the team coordinate without becoming bloated or acting like a second source of truth.
