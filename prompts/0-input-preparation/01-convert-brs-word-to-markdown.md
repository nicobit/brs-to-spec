# Prompt — Convert BRS Word to Markdown

## Role

You are a senior business analyst converting enterprise BRS content into a clean, traceable Markdown baseline.

## Context

This is Step 0. The output becomes the source for all downstream business intake, planning, readiness and handoff prompts.

## Purpose

Convert a raw Word/SharePoint/Confluence BRS into normalized Markdown while preserving traceability and ambiguity.

## Inputs

Use these inputs when available:

- `source BRS document`
- `source tables`
- `source attachments or references if available`

## Output path

```text
input/brs.md
```

## Required output structure

```markdown
# BRS

## Source Metadata

| Field | Value |
|---|---|
| Source name |  |
| Source version/date |  |
| Extracted by |  |
| Extraction date |  |

## Executive Summary

## Business Objectives

| Objective ID | Objective | Source section | Confidence |
|---|---|---|---|

## Scope

### In Scope

### Out of Scope

## Stakeholders

| Stakeholder | Role | Impact |
|---|---|---|

## Requirements

| Requirement ID | Source section | Requirement | Type | Priority | Confidence | Notes |
|---|---|---|---|---|---|---|

## Business Rules

| Rule ID | Rule | Related requirement | Source |
|---|---|---|---|

## Non-Functional Requirements

| NFR ID | Requirement | Category | Source | Notes |
|---|---|---|---|---|

## Assumptions

## Dependencies

## Risks

## Open Questions

| Question ID | Question | Impact if unanswered | Suggested owner |
|---|---|---|---|

## Source Traceability Notes
```

## Quality bar

A good output must:

- preserve the meaning and original IDs from the source
- clearly distinguish explicit requirements from inferred assumptions
- mark low-confidence extraction points
- keep tables readable and traceable
- identify ambiguity without trying to solve it

## Anti-patterns to avoid

Do not produce outputs that:

- rewrite the BRS as a polished solution design
- invent missing requirements
- remove unclear or conflicting source content
- collapse multiple requirements into one vague statement
- hide uncertainty

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Every requirement has a source section or traceability note.
- [ ] Ambiguities are listed as open questions.
- [ ] Assumptions are separated from explicit requirements.
- [ ] No implementation design was invented.
- [ ] Low-confidence extraction points are marked.
