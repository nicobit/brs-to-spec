# Prompt — Convert Initial Architecture Document to Markdown

## Purpose

Convert the initial architecture document into normalized Markdown.

## Input

Use the provided architecture source document, usually:
- Word `.docx`,
- architecture draft,
- high-level design,
- C4 diagram export,
- SharePoint/Confluence page,
- pasted architecture text.

## Output file

```text
input/initial-architecture.md
```

## Output structure

```markdown
# Initial Architecture

## Source Metadata

| Field | Value |
|---|---|
| Source document |  |
| Version |  |
| Date |  |
| Owner |  |
| Conversion notes |  |

## Architecture Summary

## System Context

## Current State

## Target State

## Components / Containers

## Integrations

## Data Ownership

## API / Interface Constraints

## Authentication and Authorization

## Security Constraints

## Audit / Compliance Constraints

## Observability / Logging

## Deployment / Environment Constraints

## Technology Stack

## Architecture Decisions Already Taken

## Open Architecture Decisions

## Risks / Assumptions

## Diagram Descriptions
```

## Rules

- Preserve explicit constraints.
- Do not invent architecture.
- Mark assumptions clearly.
- If no initial architecture document is provided, create this file and write:
  `No initial architecture document provided.`
