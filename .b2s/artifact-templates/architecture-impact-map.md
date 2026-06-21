# Architecture Impact Map

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | architect |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Requirements assessed | N |
| Ready | N |
| Needs clarification | N |
| Blocked | N |
| ADRs required | N |
| High-risk items | N |

---

## Impact by Requirement

### REQ-001 — {{Requirement Title}}

| Area | Impact |
|---|---|
| Capability | CAP-NNN |
| Impacted System | {{system name}} |
| Impacted Component | {{component name}} |
| Impacted API | {{endpoint or API surface}} |
| Impacted Data / Entity | {{entity or table}} |
| Impacted Integration | {{external system or integration point}} |
| Security Impact | None / Auth change / PII exposure / Compliance |
| Deployment Impact | None / Config change / New service / Migration |
| Observability Impact | None / New metrics / New alerts / Logging change |
| Performance / Scalability Impact | None / Load increase / New bottleneck / SLA risk |
| Backward Compatibility Impact | None / Additive / Breaking |
| Required ADR | ADR-NNN / None |
| Architecture Risk | Low / Medium / High |
| Readiness | Ready / Needs Clarification / Blocked |

---

## Impact Summary by System

| System | Requirements Impacted | Risk Level | ADRs Required | Readiness |
|---|---|---|---|---|
| {{system}} | REQ-NNN, REQ-NNN | Low / Medium / High | N | Ready / Needs Clarification / Blocked |

---

## Impact Summary by Component

| Component | Type | Requirements | Change Type | Risk |
|---|---|---|---|---|
| {{component}} | API / Service / UI / Database / Event / Integration | REQ-NNN | New / Modified / Extended | Low / Medium / High |

---

## Blocked Requirements

| REQ-NNN | Blocking Reason | Required Action | Owner |
|---|---|---|---|
| | | | |

---
*Every requirement must have an architecture impact assessment. If impact is unclear, mark Needs Clarification. If an architecture decision is missing, mark Blocked. Set Status: Accepted only after architecture review. Never self-accept.*
