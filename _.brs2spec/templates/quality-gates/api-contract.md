# API Contract

> Optional visual view: add a compact request/response or interaction sequence only when it materially improves contract clarity for reviewers or implementers.
> Prefer one embedded markdown-friendly visual over a separate diagram artifact.

## Metadata

| Field | Value |
|---|---|
| **Status** | **In progress** — change to `Accepted` when all open questions are answered and owner signs off |
| Active deliverable |  |
| Governed boundary |  |
| API owner |  |
| Review date |  |
| Trigger reason from readiness |  |

## API Summary

## Endpoints

| Method | Path | Purpose | Auth required? | Consumer(s) | Compatibility impact |
|---|---|---|---|---|---|

## Request / Response Contract

| Endpoint | Request schema | Response schema | Validation rules |
|---|---|---|---|

## Optional Visual View

Add only when a compact interaction or request/response sequence makes the governed API boundary easier to review than tables alone.
Reference an existing authoritative diagram instead of duplicating it when one already exists.

## Error Handling

| Error case | Status / code | Message rule | Consumer action |
|---|---|---|---|

## Versioning and Compatibility

## Security Requirements

## Observability Requirements

## Open Questions

| Question ID | Question | Owner | Required before | Answer |
|---|---|---|---|---|

## Acceptance

Status: `In progress` → change to `Accepted` when all checklist items are ticked or explicitly recorded as accepted risk.

When accepted, update the `Status` field in Metadata to `Accepted`. The git commit records who accepted and when.

## CI Gate

> Add this section when the artifact reaches Status: Accepted.
> A gate with Status: Accepted but Gate status: Not wired is a delivery risk.

| Field | Value |
|---|---|
| Test runner / tool | (e.g. Pact, Schemathesis, Dredd) |
| CI command | (e.g. schemathesis run quality-gates/api-contract.yaml --checks all) |
| CI step name | (e.g. API contract gate) |
| Gate status | Not wired / Wired / Passing |

To generate the CI step configuration, run:

```text
.brs2spec/quality-gates/generate-ci-gate-config.md
```
