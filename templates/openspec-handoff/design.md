# Design — {{Deliverable ID}}: {{Deliverable Name}}

> Technical decisions and constraints for this increment only.
> This file is the primary context for an AI coding agent running `/opsx:apply`.
> Keep it self-contained: an engineer should be able to implement from this file + tasks.md without opening any other artifact.

## System context

<!-- One paragraph: where this deliverable fits in the overall system. -->
<!-- Name the components touched, the boundaries crossed, the data stores written. -->

## API surface

| Method | Path | Purpose | Auth | Request body | Response | Contract artifact |
|---|---|---|---|---|---|---|

<!-- Fill every column. If contract artifact is in specs/, link it. -->
<!-- Example: POST | /onboarding | Create onboarding record | API key | {email, phone} | 202 {id} | specs/api.md#post-onboarding -->

## Data model changes

| Table / entity | Change | Key columns | PII? | Encryption | Contract artifact |
|---|---|---|---|---|---|

<!-- Reference specs/data.md for full DDL. Only show the columns relevant to this increment here. -->

## Integration points

| Integration | Protocol | Auth method | Async? | Idempotency | Contract artifact |
|---|---|---|---|---|---|

## Architecture constraints applied

| Rule ID | Constraint | How applied in this increment |
|---|---|---|

<!-- Pull binding rules from architecture/architecture-rules.md. Only list rules that affect this increment. -->

## Security decisions

| Concern | Decision | Accepted risk? | Gate reference |
|---|---|---|---|

## Observability requirements

| Signal | Type | Emitted by | Purpose | Gate reference |
|---|---|---|---|---|

<!-- Distilled from observability-plan.md. Only signals relevant to this increment. -->
<!-- An engineer must emit these — do not leave them as optional. -->

## Sequence / interaction view

<!-- Add a Mermaid diagram ONLY if the async flow or integration boundary is hard to follow from text alone. -->
<!-- If a diagram already exists in input/architecture.md, reference it instead of duplicating. -->
<!-- Delete this section if not needed. -->

```mermaid
sequenceDiagram
```

## Open questions

| # | Question | Owner | Needed before |
|---|---|---|---|

<!-- Questions that must be resolved before or during implementation. -->
<!-- Remove resolved questions before handing to an agent. -->
