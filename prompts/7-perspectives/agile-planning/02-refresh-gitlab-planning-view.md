# Prompt - Refresh GitLab Planning View

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

This prompt creates a read-only planning projection for teams that work with epics, features, user stories, GitLab issues, milestones and labels.

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
- the existing `perspectives/agile-planning/gitlab-planning-view.md`

## Output path

```text
perspectives/agile-planning/gitlab-planning-view.md
```

## Template

Use:

```text
templates/perspectives/agile-planning/gitlab-planning-view.md
templates/perspectives/agile-planning/gitlab-refresh-report.md
```

Preserve the template headings and add detail only where the evidence demands it.

## Quality bar

A good output must:

- map source artifacts to GitLab planning items
- preserve source IDs and source paths
- clearly state that this is a projection, not the source of truth
- avoid redefining requirements, architecture constraints or acceptance criteria
- show how quality gate actions should be tracked
- make GitLab planning usable without creating a parallel framework
- clearly identify stale mappings and sync actions after source changes

## Anti-patterns to avoid

Do not produce outputs that:

- create new scope not present in the source artifacts
- redefine requirements independently from the traceability matrix
- duplicate OpenSpec or standalone tasks as a new authoritative task list
- create a second backlog source of truth
- generate many epics, features, or stories without source references
- hide the source artifact path

## Stop conditions

- If delivery increments or traceability matrix are missing, produce a draft view and mark missing inputs.
- If neither OpenSpec nor standalone handoff exists, do not invent implementation tasks.
- If readiness-check is missing, mark the planning view as Draft.
- Do not invent GitLab IDs.

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

## Self-review checklist

Before finalizing, verify:

- [ ] The refreshed view still states it is a projection, not source of truth.
- [ ] Every changed epic, feature, story, and task still points to source artifact path and source ID where possible.
- [ ] Classic Agile user story phrasing is used only for the projection layer.
- [ ] Acceptance sources still point back to source artifacts rather than duplicating them.
- [ ] Stale items and sync actions are visible.
