# Event Contract

> Optional visual view: add a compact producer-consumer or event-flow view only when it materially improves event-boundary clarity for reviewers or implementers.
> Prefer one embedded markdown-friendly visual over a separate diagram artifact.

## Metadata

| Field | Value |
|---|---|
| Active deliverable |  |
| Event owner |  |
| Review date |  |

## Events

| Event name | Producer | Consumers | Purpose | Criticality |
|---|---|---|---|---|

## Payload Contract

| Event | Field | Type | Required? | Description |
|---|---|---|---|---|

## Delivery Semantics

| Concern | Decision | Evidence / Notes |
|---|---|---|
| Idempotency |  |  |
| Ordering |  |  |
| Retry |  |  |
| Dead-letter handling |  |  |
| Versioning |  |  |

## Optional Visual View

Add only when a compact producer-consumer or event-flow view makes the governed asynchronous boundary easier to review than tables alone.
Reference an existing authoritative diagram instead of duplicating it when one already exists.

## Consumer Impact

| Consumer | Impact | Required action | Owner |
|---|---|---|---|

## Observability

## Open Questions

## Acceptance

Status: `In progress` → change to `Accepted` when all checklist items are ticked or explicitly recorded as accepted risk.

When accepted, update the `Status` field in Metadata to `Accepted`. The git commit records who accepted and when.

## CI Gate

> Add this section when the artifact reaches Status: Accepted.
> A gate with Status: Accepted but Gate status: Not wired is a delivery risk.

| Field | Value |
|---|---|
| Test runner / tool | (e.g. AsyncAPI validator, Confluent Schema Registry check) |
| CI command | (e.g. asyncapi validate quality-gates/event-contract.yaml) |
| CI step name | (e.g. Event contract gate) |
| Gate status | Not wired / Wired / Passing |

To generate the CI step configuration, run:

```text
.brs2spec/quality-gates/generate-ci-gate-config.md
```
