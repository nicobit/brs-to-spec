# Data Contract

> Optional visual view: add a compact logical ERD or data-ownership view only when it materially improves schema, ownership, or downstream-impact clarity.
> Prefer one embedded markdown-friendly visual over a separate diagram artifact.

## Metadata

| Field | Value |
|---|---|
| Active deliverable |  |
| Governed boundary |  |
| Data owner |  |
| Review date |  |
| Trigger reason from readiness |  |

## Data Entities

| Entity | Owner | Purpose | Sensitivity | Retention | Consumers |
|---|---|---|---|---|---|

## Schema Changes

| Entity | Change | Migration required? | Backward compatible? | Risk |
|---|---|---|---|---|

## Optional Visual View

Add only when a compact logical ERD or ownership view makes the governed data boundary easier to review than tables alone.
Reference an existing authoritative diagram instead of duplicating it when one already exists.

## Data Quality Rules

| Rule ID | Rule | Validation | Owner |
|---|---|---|---|

## Data Migration

## Reporting / Downstream Impact

## Privacy / Compliance Considerations

## Open Questions

| Question ID | Question | Owner | Required before |
|---|---|---|---|

## Acceptance

Status: `In progress` → change to `Accepted` when all checklist items are ticked or explicitly recorded as accepted risk.

When accepted, update the `Status` field in Metadata to `Accepted`. The git commit records who accepted and when.

## CI Gate

> Add this section when the artifact reaches Status: Accepted.
> A gate with Status: Accepted but Gate status: Not wired is a delivery risk.

| Field | Value |
|---|---|
| Test runner / tool | (e.g. Great Expectations, dbt tests, Pandera) |
| CI command | (e.g. great_expectations checkpoint run data_contract_checkpoint) |
| CI step name | (e.g. Data contract gate) |
| Gate status | Not wired / Wired / Passing |

To generate the CI step configuration, run:

```text
.brs2spec/quality-gates/generate-ci-gate-config.md
```
