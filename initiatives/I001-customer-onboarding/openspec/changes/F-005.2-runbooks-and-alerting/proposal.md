# Proposal — F-005.2: Runbooks and Alerting

**As an** SRE,
**I want** runbooks and alerting for high-failure-rate and IDP webhook issues,
**so that** on-call can respond and restore service quickly.

**Requirement:** NFR-005
**Acceptance criteria:** Runbooks present and alert rules tested in staging; pager drill completed

## Why now

Telemetry signals are live (F-005.1). This story hardens operations — tuning alert thresholds to real traffic, testing runbooks, and ensuring on-call is ready before production launch.

## What changes

- Alert thresholds tuned against staging traffic baseline
- Pager drill completed for all P1 alert rules
- Runbooks reviewed by SRE and Engineering
- Dashboard links attached to `quality-gates/observability-plan.md`

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-005.1 | Telemetry signals must exist to tune thresholds against |
| Can run in parallel with | F-004.2, F-002.2, F-003.2 | No shared schema or API |
| Blocks | none | Terminal for observability track |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | All P1 runbooks exercised in staging | SRE runbook drill | Drill result documented |
| AC-002 | Alert thresholds tuned to staging traffic | Compare alert firing rate vs false positives | Threshold values documented |
| AC-003 | Pager drill completed | On-call notification test | Pager received by on-call |
| AC-004 | Dashboard links attached | Check observability-plan.md | Links filled in for all 3 dashboards |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Observability plan | `quality-gates/observability-plan.md` | Runbook content, alert expressions, dashboard list |
