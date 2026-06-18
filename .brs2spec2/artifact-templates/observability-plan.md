# Observability Plan

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |

## Observability Scope

| Flow / Feature | SLI/SLO | Alert need | Trigger source |
|---|---|---|---|
| | | Yes / No | BRS §N |

## Logs

| Event | Level | Fields | PII-safe? | Format |
|---|---|---|---|---|
| | INFO / WARN / ERROR / CRITICAL | correlation_id, actor, action, outcome | Yes / No | JSON |

**PII safety rule:** The following fields from data-contract.md must NEVER appear in log lines: {{field list}}

## Metrics

| Name | Type | Labels | SLO Target | Collection interval |
|---|---|---|---|---|
| | counter / gauge / histogram | endpoint, status_code | | 15s |

## Traces

| Flow | Spans | Required attributes | Sampling | Cross-boundary? |
|---|---|---|---|---|
| | | correlation_id, actor_id | 10% / 100% for errors | Yes / No |

## Alerts

| Alert name | Condition | Severity | Threshold | Window | Auto-resolve | Owner |
|---|---|---|---|---|---|---|
| | metric > N | P1 / P2 / P3 | | 5m | Yes / No | on-call |

## Dashboards

| Panel | Metric / Query | Purpose |
|---|---|---|

## Runbook Notes

### Alert: {{Alert name}}

**When it fires:** {{condition that triggers the alert}}  
**First check:** {{diagnostic command or query}}  
**Common cause:** {{most likely root cause}}  
**Resolution steps:** {{numbered steps}}

## Support Diagnostics

| Scenario | Query / Command |
|---|---|

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

---
*Status: In progress — set to Accepted by SRE/engineering gate owner. Never self-accept.*
