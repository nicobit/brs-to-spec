# Routing Decision

> Produced by: orchestrator
> Primary consumer: all downstream personas
> Purpose: select the minimum safe staged path for this initiative
> This artifact is immutable after acceptance. Changes require a routing reset or rerun.

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Created at | 2026-06-18 |
| Created by | orchestrator |
| Status | Draft |

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | OpenSpec | Many functional requirements, multiple integrations, and regulatory controls require a full engineer-ready spec | High |
| Execution mode | Enterprise+Modular | Cross-team integrations and modular boundaries (credit, AML, core banking, e-sign) | High |
| Small-change path applicable? | No | Scope, compliance, and number of FRs exceed small-change thresholds | High |

## Delivery Mode Assessment

| Criterion | Score | Evidence from inputs | Impact on decision |
|---|---|---|---|
| Requirement ambiguity | High | Numerous detailed FRs and multiple open questions in the BRS; complexity across domains | Drives conservative routing |
| Architecture impact | High | Integrations with Experian, HMRC, DocuSign, Temenos T24 and multiple subsystems | Requires cross-team design and contracts |
| Compliance / audit relevance | High | AML/KYC, GDPR and regulatory audit trail requirements stated explicitly | Necessitates rigorous handoff and review |
| Business criticality | High | Customer-facing loan origination with direct revenue and regulatory exposure | High impact for failure |
| Number of teams | High | Multiple service boundaries implied (credit, compliance, underwriting, payments) | Enables modular execution |
| Delivery size | High | >15 functional requirements (FR-001..FR-030) | Not suitable for FastPath |
| AI context saturation risk | High | AI scoring, external data sources and explainability requirements increase context needs | Prefers OpenSpec packaging |
| Small-change path applicable? | No | Does not meet small-change criteria (multi-team, compliance, >5 FRs) | N/A |
| Regression / contract sensitivity | High | Core banking and external API contracts (T24, Experian) mean regression risk | Requires contract-first approach |

## Execution Mode Assessment

| Mode | Available? | Recommended? | Reason |
|---|---|---|---|
| OpenSpec | Yes | Yes | Provides engineering-ready artifacts for multi-team delivery |
| Standalone | No | No | Not suitable for cross-boundary, regulated work |
| BusinessCopilot | No | No | Outputs need engineering handoff, not business-only summaries |

## Required Next Actions

| Order | Action ID | Reason required |
|---|---|---|
| 1 | create-business-intake-summary | Summarise BRS into a concise intake for downstream analysis and gating |

## Actions Not Needed

| Action ID | Reason not needed |
|---|---|
| create-use-case-diagram | Not required as an immediate gate to begin business intake; can be produced later by analysis team |

## Risks of Under-Processing

If routing selects a smaller path (e.g., FastPath) the following could happen:

- Regulatory gaps: AML/KYC and audit trail gaps leading to non-compliance findings.
- Integration surprises: missing API contract work with Experian/T24 causing rework and schedule slips.
- Insufficient traceability for AI explainability requirements.

## Risks of Over-Processing

- Longer lead time and wasted effort on low-value artifacts.
- Delaying delivery of critical customer-facing increments.
- Higher up-front cost with minimal incremental risk reduction beyond the recommended path.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No |
| Minimum required artifacts | business-intake-summary, requirements catalog, routing decision |
| Readiness still required? | Yes — AML/KYC, Experian integration readiness, and API contract definitions |
| Gates that still may trigger | business-intake-review (human gate), compliance review |

## Workflow Type

| Field | Value |
|---|---|
| Recommended workflow type | enterprise-modular |
| Rationale | Delivery size, multi-team integration, and compliance needs demand the enterprise-modular pattern |
| Current workflow type | enterprise-modular |
| Match | yes |

## Constraints

| Constraint | Source | Impact |
|---|---|---|
| UK data residency | BRS (GDPR) | All data and processing must remain in UK datacenters |
| Use Experian, DocuSign, Temenos T24 | BRS integrations | Requires contract and connector work before implementation |
