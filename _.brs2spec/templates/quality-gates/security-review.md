# Security Review

## Metadata

| Field | Value |
|---|---|
| **Status** | **In progress** — change to `Accepted` when all checklist items are ticked or explicitly recorded as accepted risk |
| Active deliverable |  |
| Reviewer |  |
| Review date |  |
| Related readiness check |  |
| Related architecture review |  |

## Review Decision

| Decision | Value |
|---|---|
| Decision owner |  |
| Conditions / residual risks |  |

## Security Scope

## Controls Checked

| Control area | Required? | Status | Evidence | Gap / Risk | Required action | Owner | Required before |
|---|---|---|---|---|---|---|---|
| Authentication |  |  |  |  |  |  | Implementation |
| Authorization |  |  |  |  |  |  | Implementation |
| Role / permission model |  |  |  |  |  |  | Implementation |
| Data classification |  |  |  |  |  |  | Implementation |
| PII / sensitive data |  |  |  |  |  |  | Implementation |
| Input validation |  |  |  |  |  |  | Implementation |
| Secrets management |  |  |  |  |  |  | Implementation |
| Audit trail |  |  |  |  |  |  | Merge |
| Logging safety |  |  |  |  |  |  | Merge |
| External exposure |  |  |  |  |  |  | Implementation |
| Regulatory / compliance |  |  |  |  |  |  | Merge |

## Threat Scenarios

| Scenario ID | Threat scenario | Likelihood | Impact | Existing control | Required mitigation | Residual risk |
|---|---|---|---|---|---|---|

## Findings

| Finding ID | Severity | Area | Evidence | Risk | Recommendation | Owner | Required before |
|---|---|---|---|---|---|---|---|

## Residual Risks

| Risk ID | Risk | Impact | Mitigation | Accepted by | Review date |
|---|---|---|---|---|---|

## Required Actions Before Implementation / Merge

| Action ID | Action | Owner | Required before | Status |
|---|---|---|---|---|

## Acceptance

Status: `In progress` → change to `Accepted` when all checklist items are ticked or explicitly recorded as accepted risk.

When accepted, update the `Status` field in Metadata to `Accepted`. The git commit records who accepted and when.

## CI Gate

> Add this section when the artifact reaches Status: Accepted.
> A gate with Status: Accepted but Gate status: Not wired is a delivery risk.
> The security gate should be present from the first commit — it is not conditional on this artifact.

| Field | Value |
|---|---|
| Test runner / tool | (e.g. Semgrep, Trivy, Bandit, GitLeaks) |
| CI command | (e.g. semgrep --config=auto --error) |
| CI step name | (e.g. Security gate) |
| Gate status | Not wired / Wired / Passing |

To generate the CI step configuration, run:

```text
.brs2spec/quality-gates/generate-ci-gate-config.md
```

## Final Security Decision
