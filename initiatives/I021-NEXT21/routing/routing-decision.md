# Routing Decision

> Produced by: orchestrator
> Primary consumer: all downstream personas
> Purpose: select the minimum safe staged path for this initiative
> This artifact is immutable after acceptance. Changes require a routing reset or rerun.

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T15:55:14.241763+00:00 |
| Created by | orchestrator |
| Status | Draft |

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | OpenSpec | Multi-feature initiative (30+ FRs), multiple services and integrations, regulatory requirements — OpenSpec supports handoff to engineering teams and packaging for implementation. | High |
| Execution mode | Enterprise+Modular | Cross-service boundaries and multiple teams; modular delivery reduces coupling and enables parallel workstreams. | High |
| Small-change path applicable? | No | Not single-team / not under 5 FRs / regulatory and integration scope present. | High |

## Delivery Mode Assessment

| Criterion | Score | Evidence from inputs | Impact on decision |
|---|---|---|---|
| Requirement ambiguity | Medium | BRS contains detailed FRs (FR-001..FR-030) but several open questions (OQ-001..OQ-005). | Medium — enough detail to proceed but some clarifications required. |
| Architecture impact | High | Architecture file lists multiple services (API, AI Scoring, Compliance, Notification, Audit Store, Payment Adapter). | High — cross-service design and interfaces require design artifacts. |
| Compliance / audit relevance | High | BRS mandates AML/KYC, GDPR, audit trail, and regulatory reporting requirements. | High — compliance must be designed and validated early. |
| Business criticality | High | Production financial flow (loan origination, disbursement) with revenue and regulatory impact. | High — conservative delivery required. |
| Number of teams | High | Separate services indicate multiple teams/owners (AI, compliance, core banking, frontend). | High — coordination and modular boundaries needed. |
| Delivery size | High | 30+ functional requirements across multiple epics. | High — significant scope warrants OpenSpec. |
| AI context saturation risk | Medium | Several AI-specific FRs (AI scoring, explainability) but BRS centralises inputs. | Medium — requires dedicated AI scoping and dataset readiness. |
| Small-change path applicable? | No | Does not meet small-change criteria (multi-service, compliance, >5 FRs). | N/A |
| Regression / contract sensitivity | High | Integrations with Experian, HMRC, DocuSign, Temenos imply contract and API sensitivity. | High — API contracts and regression testing required. |

## Execution Mode Assessment

| Mode | Available? | Recommended? | Reason |
|---|---|---|---|
| OpenSpec | Yes | Yes | Initiative spans multiple features and will be consumed by engineering teams; OpenSpec supports story decomposition and handoff. |
| Standalone | Yes | No | Not a single-team, small change — not appropriate. |
| BusinessCopilot | Yes | No | Outputs are for engineering consumption, not purely business-facing. |

## Required Next Actions

| Order | Action ID | Reason required |
|---|---|---|
| 1 | create-business-intake-summary | Consolidate BRS into a concise intake artifact for downstream analysis and to drive requirements and scope decisions. |

## Actions Not Needed

| Action ID | Reason not needed |
|---|---|
| create-process-flows | Detailed process flows can be deferred until use-cases and requirements are validated to avoid premature locking of workflow details. |

## Risks of Under-Processing

- Missing or incomplete compliance controls could lead to regulatory breaches and costly remediation.
- Insufficient interface/API specification may cause downstream integration failures with Experian, HMRC, DocuSign, or Temenos.

## Risks of Over-Processing

- Producing an excessive set of low-value artifacts will delay delivery and increase cost without improving regulatory or technical guarantees.
- Over-engineering architecture before requirement clarifications may cause rework.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No — multi-service, compliance, and >5 FRs. |
| Minimum required artifacts | business-intake-summary, requirements catalog, entity model, use-case specs. |
| Readiness still required? | Yes — readiness checks for AI datasets, compliance sign-offs, and API contracts. |
| Gates that still may trigger | `business-intake-review` human gate; compliance and architecture review gates. |

## Workflow Type

| Field | Value |
|---|---|
| Recommended workflow type | enterprise-modular |
| Rationale | Multi-feature, multi-team initiative with regulatory constraints — modular enterprise workflow fits best. |
| Current workflow type | enterprise-modular |
| Match | yes |

### Workflow Type Mismatch Warning

If `Match` is `no`, include this block. (Not applicable — match = yes.)

## Constraints

_Key constraints identified in inputs:_

| Constraint | Source | Impact |
|---|---|---|
| Data residency in UK | BRS / Architecture | All storage and compute must remain in UK regions; affects cloud region selection and data replication. |
| Regulatory compliance (FCA, AML/KYC) | BRS | Requires design for auditability, explainability, and compliance gates. |
