# Prompt — Convert BRS Word to Markdown

## Purpose

Convert a raw BRS document into normalized Markdown.

## Input

Use the provided BRS source document, usually:
- Word `.docx`,
- SharePoint document,
- Confluence export,
- pasted text.

## Output file

```text
input/brs.md
```

## Output structure

```markdown
# BRS

## Source Metadata

| Field | Value |
|---|---|
| Source document |  |
| Version |  |
| Date |  |
| Owner |  |
| Conversion notes |  |

## Executive Summary

## Business Context

## Objectives

## Scope

### In Scope

### Out of Scope

## Requirements

Preserve original IDs if available.

| Requirement ID | Requirement | Source section | Notes |
|---|---|---|---|

## Business Rules

## Non-Functional Requirements

## Data / Reporting Requirements

## Operational / Audit / Compliance Requirements

## Assumptions

## Dependencies

## Risks

## Open Questions

## Original Structure / Section Index
```

## Rules

- Preserve the original meaning.
- Do not invent requirements.
- Preserve requirement IDs if present.
- Preserve tables as Markdown tables.
- Mark unclear or missing sections.
- If a diagram is present but cannot be rendered, describe it textually.
- Include conversion notes.
