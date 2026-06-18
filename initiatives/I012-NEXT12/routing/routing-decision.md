# Routing Decision

> Produced by: orchestrator
> Primary consumer: all downstream personas
> Purpose: select the minimum safe staged path for this initiative
> This artifact is immutable after acceptance. Changes require a routing reset or rerun.

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Created at | 2026-06-16 |
| Created by | orchestrator |
| Status | Draft |

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | OpenSpec | Multi-feature delivery with many cross-service integrations and engineering consumers; outputs must be engineer-friendly | High |
| Execution mode | Enterprise+Modular | Delivery size, multiple service boundaries, and distinct module responsibilities justify a modular enterprise approach | High |
| Small-change path applicable? | No | More than a handful of features, compliance scope, and multiple integrations — not appropriate for FastPath | High |

## Delivery Mode Assessment

| Criterion | Score | Evidence from inputs | Impact on decision |
|---|---|---|---|
| Requirement ambiguity | Medium | BRS is detailed but contains open questions (OQ-001..OQ-005) that affect design choices | Contributes to OpenSpec to capture clearer engineering requirements |
| Architecture impact | High | High-level architecture shows multiple services, external integrations (Experian, HMRC, DocuSign, T24) and separate data stores | Requires cross-team design and modular decomposition |
| Compliance / audit relevance | High | GDPR, AML/KYC, FCA Consumer Duty, explainability requirements are explicit | Drives higher assurance and traceability in the spec |
| Business criticality | High | Revenue-impacting customer-facing loan decisions and SLAs for decision latency | Increases risk of under-processing; need thorough handoff |
| Number of teams | Medium | Multiple logical services and stakeholders (AI, Compliance, Core Banking, Underwriter UI) | Favors modular enterprise delivery |
| Delivery size | High | BRS contains many FRs across intake, scoring, compliance, underwriter workflows, offer lifecycle | Supports OpenSpec and modular execution |
| AI context saturation risk | Medium | AI scoring and external data introduce model+data sensitivity; inputs are substantial but structured | Requires explicit modeling and test artifacts |
| Small-change path applicable? | No | The combination of compliance, integrations, and feature count prevents safe FastPath | |
| Regression / contract sensitivity | High | Shared APIs and external contracts (Experian, T24, DocuSign) create contract sensitivity | Enforces careful interface and contract design |

## Execution Mode Assessment

| Mode | Available? | Recommended? | Reason |
|---|---|---|---|
| OpenSpec | Yes | Yes | Required to produce engineer-ready artifacts, API/data contracts, and test expectations |
| Standalone | Yes | No | Single-team Standalone would not address cross-service integration and compliance needs |
| BusinessCopilot | Yes | No | Outputs are intended for engineering delivery, not purely business stakeholder consumption |

## Required Next Actions

| Order | Action ID | Reason required |
|---|---|---|
| 1 | create-business-intake-summary | Produce a concise intake for engineering and stakeholders summarizing scope and critical constraints |
| 2 | create-actors-and-personas | Identify actors and personas to inform use-cases and security boundaries |
| 3 | create-requirements | Convert BRS detail to prioritized engineer-ready requirements (stories/FRs) |
| 4 | create-use-case-diagram | Visualize user flows and integration touchpoints |
| 5 | create-entity-model | Define core data entities and persistence boundaries (audit vs. mutable state) |
| 6 | create-api-contract | Produce API and integration contracts (Experian, HMRC, DocuSign, T24) |
| 7 | create-observability-plan | Define audit, telemetry, and compliance monitoring requirements |

## Actions Not Needed

| Action ID | Reason not needed |
|---|---|
| create-brs | Source BRS already provided in `input/brs.md` — no new BRS generation required |

## Risks of Under-Processing

If the initiative is under-processed (e.g., by choosing FastPath or omitting API contracts):

- Regulatory non-compliance or audit failures due to incomplete AML/KYC traceability.
- Production incidents from incompatible integration contracts (Experian, T24) causing loan processing outages.
- Unclear responsibility for model explainability leading to rejection by compliance or regulators.

## Risks of Over-Processing

- Delays to business value and increased cost if every peripheral artifact is produced before delivering core flows.
- Stakeholder fatigue from excessive documentation; slower feedback cycles.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No — multiple integrations, compliance, and >15 FRs make FastPath unsafe |
| Minimum required artifacts | Intake summary, prioritized requirements, API contracts, entity model, observability plan |
| Readiness still required? | Yes — compliance sign-off, vendor integration availability, and model explainability evidence |
| Gates that still may trigger | Compliance gate, Architecture review, Engineering readiness gate |

## Constraints

| Constraint | Source | Impact |
|---|---|---|
| Data residency: UK-only | BRS / Architecture | Limits cloud region choices and storage locations |
| Use Experian CreditExpert | BRS | Integration contract and latency constraints; fallback behavior required |
| E-signature must use DocuSign | BRS | Vendor contract and integration design required |
| Core banking integration with Temenos T24 | BRS | Payment gateway adapter required; external contract negotiation may be needed |
| AI decisions must be explainable | BRS / Compliance | Prohibits black-box-only models; affects model design and testing |
