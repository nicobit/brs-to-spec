# Initial Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T18:10:00+00:00 |
| Created by | architect |
| Status | Draft |

## Summary

High-level architecture will use microservices for intake, scoring, underwriting, and disbursement. Integrations: Experian, KYC provider, DocuSign, Temenos T24.

## Risks and Assumptions

- Experian SLA and KYC provider selection are unresolved (see GAP-001, GAP-002).

## Recommendations

- Use event-driven integration for scoring and asynchronous disbursement.

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Intake & Validation | Frontend, existing API gateway | Intake API (new) | Add intake contract with validation schema | Medium |
| AI Scoring | None (new capability) | Scoring Service (async) | Event contract for scoring jobs | Medium |
| Underwriting Workflow | Underwriter UI (existing) | Underwriter Queue (new) | Queue contract, decision recording API | Medium |
| Disbursement | Temenos T24 (existing) | Disbursement Adapter | T24 mapping and retry semantics | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | Data residency in UK | Regulatory requirement | Legal non-compliance and fines; must restrict region | BRS: Data residency
| ARCH-C-002 | PII encrypted at rest and in transit | Security & compliance | Data breach exposure and regulatory action | BRS: Security requirements

## Brownfield Impact

Existing Temenos T24 integration will be adapted via a Disbursement Adapter. Migration surface: disbursement payload mapping and reconciliation. Rollback sensitivity: disbursement operations must be idempotent and support compensation.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 Adapter | New boundary / Adapter | Disbursement service, Ops | Yes (adapter) | Yes | Yes (compensation flows) |

**Regression surface:** Disbursement and reconciliation functionality is at risk due to mapping differences.
**Rollback sensitivity:** High - incorrect disbursements have financial impact requiring manual remediation.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | Intake loads <2s; scoring ≤90s | Achievable with CDN, async scoring, and autoscaling | Medium |
| Security | PII encrypted; secure integrations | Achievable with encryption and RBAC; external vendor security must be verified | High |
| Scalability | Support 500 concurrent submissions | Achievable with autoscaling and queueing architecture | Medium |
| Availability | 99.9% during business hours | Requires multi-AZ and resilient integrations with fallbacks | High |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Experian SLA and error modes | product-owner | Assume SLA M (TBD) | Integration design |
| DEC-002 | KYC provider selection | product-owner | Assume vendor X for POC | Vendor contract signing |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian provides sub-10s median latency | BRS / vendor expectation | Scoring pipeline must fallback to refer-to-underwriter and surface degraded SLA to users |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact KYC provider rate limits and API features | Affects latency, cost, and design | Vendor POC and contract evaluation |

## Analysis Signals

- Traffic model: expected bursty intake; monitor queue lengths and scoring latency as primary signals.
---

*This review captures the initial architecture fit and known risks. See GAP catalog for blocking items that must be resolved before full design.*
