# Prompt - Refresh GitLab Planning View

## Role

You are an Agile delivery lead and planning specialist translating delivery-ready framework outputs into a refreshed team-facing delivery planning view that can be represented in GitLab.

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

This prompt refreshes a read-only planning projection for teams that work with epics, features, user stories, GitLab issues, milestones, and labels.

## Purpose

Refresh the existing GitLab Planning View so it continues to serve as the initiative's Delivery Planning View after source artifacts change.

## Inputs

Use these inputs when available:

- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `planning/delivery-increments.md` when the initiative uses Modular Delivery
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
Keep the refreshed view concise. Update only the planning projection that changed because source artifacts changed.

## Quality bar

A good output must:

- keep the planning view as one projection, not a second workflow
- map source artifacts to GitLab planning items
- preserve source IDs and source paths
- clearly state that this is a projection, not the source of truth
- avoid redefining requirements, architecture constraints, or acceptance criteria
- preserve the rule that user stories are business context, not the engineering contract
- keep OpenSpec or standalone tasks as the implementation input
- show how quality gate actions should be tracked
- make GitLab planning usable without creating a parallel framework
- clearly identify stale mappings and sync actions after source changes
- keep stale-item notes and sync actions brief and action-oriented

## Anti-patterns to avoid

Do not produce outputs that:

- create new scope not present in the source artifacts
- redefine requirements independently from the traceability matrix
- duplicate OpenSpec or standalone tasks as a new authoritative task list
- copy user stories directly as implementation tasks
- create a second backlog source of truth
- generate many epics, features, or stories without source references
- hide the source artifact path
- re-expand unchanged sections into dense narrative

## Stop conditions

- If delivery structure or traceability matrix are missing, produce a draft view and mark missing inputs.
- If delivery increments are missing for a modular initiative, mark that gap explicitly.
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
- [ ] The engineering consumption model still makes clear that engineers implement from approved OpenSpec or standalone tasks, not user stories.
- [ ] Stale items and sync actions are visible.
