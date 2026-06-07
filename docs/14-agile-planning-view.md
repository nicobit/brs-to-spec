# Agile / GitLab Planning View

## Purpose

The Agile / GitLab Planning View translates the framework output into the planning language used by delivery teams.

It helps teams answer:

```text
What do we create in GitLab?
What is the epic?
What are the issues / stories?
Which tasks/checklists come from OpenSpec or standalone delivery?
Which quality gate actions must be tracked?
```

## Important rule

The planning view is a **projection**, not a source of truth.

Do not maintain scope, requirements, architecture constraints, quality gates or implementation tasks independently in this view.

## Source of truth

The source of truth remains:

```text
initiatives/<initiative-id>-<slug>/
business-intake/business-intake-summary.md
planning/delivery-structure.md
planning/delivery-increments.md when the initiative uses Modular Delivery
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
quality-gates/*.md
openspec/changes/<change>/proposal.md
openspec/changes/<change>/design.md
openspec/changes/<change>/tasks.md
standalone-delivery/<deliverable>/*
```

All of the paths above are relative to the active initiative workspace.

## Generated view

```text
perspectives/agile-planning/gitlab-planning-view.md
```

## Recommended GitLab mapping

| Framework artifact | GitLab planning item |
|---|---|
| Business objective | Portfolio / roadmap theme |
| Business capability | Epic or parent epic |
| Delivery increment | Epic, feature issue, or milestone |
| User-story projection | GitLab issue |
| Engineering task | Issue task list, child issue, or MR checklist |
| Quality gate action | Issue task, child issue, or approval checklist |
| OpenSpec task | GitLab issue task or MR checklist |
| Standalone delivery task | GitLab issue task or child issue |

## Why this is a view, not a backlog

A classic Agile backlog can become a competing source of truth.

This framework avoids that by generating a planning view that references source artifact IDs and paths.

## User story rule

When the planning view includes user stories, use classic Agile phrasing:

```text
As a <persona>,
I want <capability>,
so that <business value>.
```

This is a projection convenience only.

Acceptance criteria remain in the source artifacts such as:

```text
BDD scenarios
delivery spec
OpenSpec tasks
standalone validation plan
traceability matrix
```
