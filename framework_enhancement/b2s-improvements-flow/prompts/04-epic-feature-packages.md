# Prompt 4 — Improve Epics and Features

You are improving the `.b2s` delivery decomposition model.

Current problem:

The framework can generate a delivery structure, but Epics and Features are not strong enough as reusable, reviewable artifacts.

Create or improve two templates:

1. `epic-package.md`
2. `feature-package.md`

The goal is to make Epics and Features useful for enterprise planning and AI-assisted implementation.

## Epic Package Requirements

Each Epic must include:

- Epic ID
- Epic title
- business objective
- business capabilities delivered
- scope
- out of scope
- linked BRS references
- linked business rules
- impacted business processes
- impacted systems/modules
- risks
- dependencies
- features included
- release/increment recommendation
- success metrics
- readiness status

Epic template:

```markdown
# {{Epic ID}} {{Epic Title}}

## Business Objective

## Business Capabilities Delivered

## Scope

## Out of Scope

## Source Traceability

| Source | Reference | Notes |
|---|---|---|

## Impacted Processes

## Impacted Systems / Modules

## Features

| Feature ID | Feature Name | Priority | Increment | Notes |
|---|---|---|---|---|

## Dependencies

## Risks

## Success Metrics

## Readiness Status
```

## Feature Package Requirements

Each Feature must include:

- Feature ID
- Feature title
- parent Epic
- feature goal
- user/business value
- scope
- out of scope
- linked requirements
- linked business rules
- impacted components
- stories included
- acceptance criteria summary
- BDD coverage expectations
- dependencies
- implementation notes
- test strategy summary

Feature template:

```markdown
# {{Feature ID}} {{Feature Title}}

## Parent Epic

## Feature Goal

## Business Value

## Scope

## Out of Scope

## Source Traceability

| Source | Reference | Notes |
|---|---|---|

## Business Rules

| Rule ID | Rule | Impact |
|---|---|---|

## Impacted Components

| Component | Change |
|---|---|

## Stories

| Story ID | Story Title | Priority | Increment | Status |
|---|---|---|---|---|

## Acceptance Criteria Summary

## BDD Coverage Expectations

## Dependencies

## Implementation Notes

## Test Strategy Summary
```

Update the workflow so that:

1. Epics are generated from business objectives, capabilities, process flows, and major requirement groups.
2. Features are generated from coherent functional slices inside each Epic.
3. Stories are generated from Features, not directly from the raw BRS.
4. Every Story must link back to its Feature and Epic.
5. The traceability matrix must include Epic, Feature, and Story IDs.

Avoid generic decomposition. If a Feature contains unrelated stories, split it.
