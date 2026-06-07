# Prompt — Convert Initial Architecture Document to Markdown

## Role

You are a senior solution architect normalizing an initial architecture document for downstream delivery analysis.

## Context

This is Step 0. The output becomes the architecture baseline and must not be silently overwritten later.

## Purpose

Convert the initial architecture document into normalized Markdown and extract constraints, decisions, assumptions, and open architecture questions.

## Inputs

Use these inputs when available:

- `source architecture document`
- `architecture diagrams`
- `architecture decision records`
- `system context notes`

## Output path

```text
input/initial-architecture.md
```

## Required output structure

```markdown
# Initial Architecture

## Source Metadata

| Field | Value |
|---|---|
| Source name |  |
| Source version/date |  |
| Extracted by |  |
| Extraction date |  |

## Architecture Summary

## System Context

## Main Components

| Component | Responsibility | Notes |
|---|---|---|

## Integration Points

| Integration | Producer | Consumer | Protocol / Pattern | Notes |
|---|---|---|---|---|

## Data Ownership and Persistence

## Security and Identity

## Deployment / Infrastructure

## Observability / Operations

## Architecture Constraints

| Constraint ID | Area | Constraint | Source | Mandatory? | Risk if violated |
|---|---|---|---|---|---|

## Architecture Decisions Already Taken

| Decision ID | Decision | Rationale | Source |
|---|---|---|---|

## Assumptions

## Open Architecture Decisions

| Decision ID | Question | Impact | Suggested owner |
|---|---|---|---|

## Conflicts / Ambiguities
```

## Quality bar

A good output must:

- extract explicit constraints and identify their source
- separate constraints from assumptions and open decisions
- preserve diagram references when available
- identify risks if a constraint is violated
- state when no architecture document is available

## Anti-patterns to avoid

Do not produce outputs that:

- invent new architecture
- treat assumptions as approved decisions
- ignore diagrams or non-text architecture content
- hide conflicts between architecture statements
- remove constraints because they are inconvenient

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Every architecture constraint has an ID.
- [ ] Decisions, assumptions and open decisions are separated.
- [ ] Any missing architecture input is explicitly stated.
- [ ] Conflicts and ambiguities are visible.
- [ ] No new architecture was invented.
