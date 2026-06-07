# Prompt — Refresh GitLab Planning View

## Role

You are an Agile delivery lead and GitLab planning specialist translating delivery-ready framework outputs into a GitLab-friendly planning view.

## Context

The framework source of truth is not GitLab planning terminology.

The source of truth is:

```text
business-intake/business-intake-summary.md
planning/delivery-increments.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
quality-gates/*.md
openspec/changes/... or standalone-delivery/...
```

This prompt creates a **read-only planning projection** for teams that work with epics, features, user stories, GitLab issues, milestones and labels.

## Purpose

Refresh the existing GitLab Planning View after source artifacts changed and identify stale, new, changed or removed mappings.

## Inputs

Use these inputs when available:

- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `planning/delivery-increments.md`
- `planning/traceability-matrix.md`
- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md`
- `openspec/changes/<active-deliverable>/proposal.md`
- `openspec/changes/<active-deliverable>/design.md`
- `openspec/changes/<active-deliverable>/tasks.md`
- `standalone-delivery/<active-deliverable>/delivery-spec.md`
- `standalone-delivery/<active-deliverable>/tasks.md`

## Output path

```text
perspectives/agile-planning/gitlab-planning-view.md
```

## Required output structure

```markdown
# GitLab Planning View

> This file is a planning projection.
> It is not the source of truth.
> If scope, requirements, architecture constraints, quality gates or implementation tasks change,
> update the source artifacts first and regenerate this view.

## Metadata

| Field | Value |
|---|---|
| Initiative / Feature |  |
| Active deliverable |  |
| Delivery mode |  |
| Execution mode | OpenSpec / Standalone |
| Source of truth |  |
| Generated from |  |
| Generated date |  |
| View status | Draft / Updated / Stale |

## Planning Summary

## Source Artifact Map

| Source artifact | Path | Purpose | Used in this view? |
|---|---|---|---|

## Suggested GitLab Hierarchy

| GitLab level | Suggested title | Source artifact | Source ID | Notes |
|---|---|---|---|---|
| Epic / Parent epic |  |  |  |  |
| Feature / Epic / Issue |  |  |  |  |
| User story / Issue |  |  |  |  |
| Task / Checklist item |  |  |  |  |

## Epic Projection

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

| Feature ID | Suggested GitLab title | Description | Business value | Source deliverable | Related requirements | Dependencies | Labels |
|---|---|---|---|---|---|---|---|

## User Story Projection

| Story ID | Suggested GitLab title | User story | Source requirement | Acceptance source | Quality gate references | Labels |
|---|---|---|---|---|---|---|

## Task / Checklist Projection

| Task ID | Suggested task / checklist item | Source artifact | Source ID | Validation / evidence expected | Required before | Owner / Team |
|---|---|---|---|---|---|---|

## Quality Gate Actions to Track

| Gate | Action | Source artifact | Required before | Suggested GitLab representation | Owner |
|---|---|---|---|---|---|

## Suggested Labels

| Label | Reason |
|---|---|

## Suggested Milestone / Iteration

| Field | Value | Source / Notes |
|---|---|---|

## Sync Notes

| Item | Source of truth | What to do if this changes |
|---|---|---|

## Do Not Duplicate

List any content that should not be copied as independent truth into GitLab.
```

## Quality bar

A good output must:

- map source artifacts to GitLab planning items
- preserve source IDs and source paths
- clearly state that this is a projection, not the source of truth
- avoid redefining requirements, architecture constraints or acceptance criteria
- show how quality gate actions should be tracked
- make GitLab planning usable without creating a parallel framework

## Anti-patterns to avoid

Do not produce outputs that:

- create new scope not present in the source artifacts
- redefine requirements independently from the traceability matrix
- duplicate OpenSpec or standalone tasks as a new authoritative task list
- create a second backlog source of truth
- generate many epics/features/stories without source references
- hide the source artifact path

## Stop conditions

- If delivery increments or traceability matrix are missing, produce a draft view and mark missing inputs.
- If neither OpenSpec nor standalone handoff exists, do not invent implementation tasks.
- If readiness-check is missing, mark the planning view as Draft.
- Do not invent GitLab IDs.

## Self-review checklist

Before finalizing, verify:

- [ ] The file states it is a projection, not source of truth.
- [ ] Every epic/feature/story/task points to a source artifact and source ID where possible.
- [ ] No requirement was redefined independently.
- [ ] Quality gate actions are tracked without duplicating the gate content.
- [ ] GitLab mapping is usable by the team.
- [ ] Sync notes explain how to avoid divergence.


## Refresh-specific requirements

Include these sections when refreshing:

```markdown
## Change Summary Since Previous View

| Area | Change detected | Source artifact | Impact on GitLab view |
|---|---|---|---|

## Stale Items to Review

| Planning item | Reason stale | Source of truth | Recommended action |
|---|---|---|---|

## New Items to Add

| Planning item | Source artifact | Source ID | Suggested GitLab representation |
|---|---|---|---|

## Items to Remove or Close

| Planning item | Reason | Source evidence |
|---|---|---|
```
