# Design — {{F-XXX.X}}: {{User Story Name}}

> Technical context for this user story only.
> This file is the primary context for an AI coding agent running `/opsx:apply`.
> Self-contained: an engineer implements from this file + tasks.md + specs/ without opening any other artifact.
> Omit any section that does not apply to this story.

## What this story touches

<!-- One short paragraph: which components are modified, which boundaries are crossed, which data stores are written. -->
<!-- Be specific — name the service, the table, the endpoint. -->

## API surface

<!-- Only endpoints created or modified by this story. Omit if this story has no API changes. -->

| Method | Path | Purpose | Auth | Request | Response | Full spec |
|---|---|---|---|---|---|---|

<!-- Full schemas in specs/api.md. -->

## Data model changes

<!-- Only tables created or modified by this story. Omit if this story has no schema changes. -->

| Table | Change | Key columns | PII? | Encryption | Full spec |
|---|---|---|---|---|---|

<!-- Full DDL, indexes, migration notes in specs/data.md. -->

## Integration points

<!-- Only integrations invoked by this story. Omit if no external calls. -->

| Integration | Protocol | Auth | Async? | Idempotency | Full spec |
|---|---|---|---|---|---|

## Architecture constraints applied

<!-- Only rules from architecture-rules.md that directly affect this story. -->

| Rule ID | Constraint | How applied |
|---|---|---|

## Security decisions

<!-- Only security concerns relevant to this story. Omit if none. -->

| Concern | Decision | Gate reference |
|---|---|---|

## Observability requirements

<!-- Signals this story must emit. Mark as mandatory — not optional. Omit if none. -->

| Signal | Type | Emitted when | Labels | Gate reference |
|---|---|---|---|---|

## Sequence view

<!-- Add a Mermaid diagram ONLY if an async flow or integration boundary is hard to follow from text. -->
<!-- Delete this section if not needed. -->

```mermaid
sequenceDiagram
```

## Open questions

<!-- Questions that must be resolved before coding starts. Remove when resolved. -->
<!-- Delete this section if none. -->

| # | Question | Owner | Needed before |
|---|---|---|---|
