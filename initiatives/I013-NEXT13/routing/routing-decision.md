# Routing Decision

> Produced by: orchestrator
> Primary consumer: all downstream personas
> Purpose: select the minimum safe staged path for this initiative
> This artifact is immutable after acceptance. Changes require a routing reset or rerun.

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | orchestrator |
| Status | Draft |

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | OpenSpec | The initiative spans many functional requirements, multiple integrations, compliance obligations, and several delivery surfaces. | High |
| Execution mode | Enterprise+Modular | The scope covers multiple services, data stores, async flows, compliance processing, and downstream contracts that benefit from modular decomposition. | High |
| Small-change path applicable? | No | This is not a single-team, under-5-FR change and it has significant compliance and integration risk. | High |

## Delivery Mode Assessment

| Criterion | Score | Evidence from inputs | Impact on decision |
|---|---|---|---|
| Requirement ambiguity | Medium | Most requirements are clear, but several open questions affect AI vendor choice and payment/API contract details. | Supports a fuller staged path with explicit analysis and planning. |
| Architecture impact | High | The architecture includes portals, APIs, scoring, compliance, notifications, audit storage, SQL, Cosmos DB, Service Bus, and several external integrations. | Favors a deeper delivery mode and modular planning. |
| Compliance / audit relevance | High | FCA, AML, KYC, GDPR, immutable audit trails, UK residency, and explainability are all explicit constraints. | Rules out lightweight processing. |
| Business criticality | High | This is a customer-facing lending platform intended to reduce decision time from days to minutes and improve regulatory outcomes. | Increases the need for traceable staged outputs. |
| Number of teams | High | The solution implies coordination across product, architecture, compliance, integration, platform, and engineering concerns. | Points toward enterprise-style execution. |
| Delivery size | High | The BRS includes 30 functional requirements across intake, AI scoring, compliance, underwriting, offers, disbursement, and observability. | Pushes the initiative into Enterprise+Modular territory. |
| AI context saturation risk | High | The source material is large and cross-cutting, with many distinct domains and contracts to preserve across downstream artifacts. | Supports using OpenSpec with decomposed artifacts. |
| Small-change path applicable? | No | The initiative exceeds fast-path thresholds on size, compliance, and cross-boundary impact. | Confirms FastPath is not safe. |
| Regression / contract sensitivity | High | The initiative depends on Experian, HMRC, DocuSign, Temenos T24, Service Bus flows, and immutable audit behavior. | Requires careful contract and readiness treatment. |

## Execution Mode Assessment

| Mode | Available? | Recommended? | Reason |
|---|---|---|---|
| OpenSpec | Yes | Yes | The initiative has many user-facing capabilities that can be decomposed into implementable stories and engineering handoff packages. |
| Standalone | Yes | No | Standalone would underspec a multi-feature, multi-service platform with significant compliance and integration complexity. |
| BusinessCopilot | No | No | The outputs are clearly intended for engineering and delivery execution rather than business-only consumption. |

## Required Next Actions

| Order | Action ID | Reason required |
|---|---|---|
| 1 | create-business-intake-summary | Summarize objectives, requirements, and routing intent before gated progression. |
| 2 | gate-business-intake-review | Human review is required to accept the intake summary and complete the intake stage. |
| 3 | create-requirements | Build a normalized requirements catalog from the BRS and intake summary. |
| 4 | create-use-case-diagram | Map the end-to-end user and system interactions across applicant, underwriter, admin, and services. |
| 5 | create-entity-model | Define the business entities and data relationships for applications, decisions, offers, and audit records. |
| 6 | create-business-rules | Capture decisioning, compliance, cooling-off, and disbursement rules explicitly. |
| 7 | find-gaps-and-questions | Surface unresolved items that can affect architecture and delivery planning. |
| 8 | create-actors-and-personas | Establish primary actors across applicants, underwriters, admins, compliance, and operations. |
| 9 | create-use-case-specs | Decompose the use cases into detailed implementation-ready behavior. |
| 10 | create-process-flows | Model operational flows across straight-through, referred, compliance-hold, and disbursement scenarios. |
| 11 | review-initial-architecture | Review the provided architecture against business analysis outputs and resolved gaps. |
| 12 | create-architecture-rules | Establish implementation constraints and architectural guardrails for downstream work. |
| 13 | create-delivery-structure | Break the initiative into coherent delivery increments and implementation slices. |
| 14 | create-traceability-matrix | Preserve linkage from business objectives and requirements into delivery scope. |
| 15 | identify-software-modules | Define module boundaries suitable for enterprise-scale execution. |
| 16 | map-capabilities-to-modules | Align business capabilities with software responsibilities. |
| 17 | define-delivery-increments | Sequence delivery across platform, compliance, decisioning, and customer-facing scope. |
| 18 | check-engineering-readiness | Assess whether the initiative is ready for engineering handoff and quality gates. |
| 19 | generate-initiative-context | Package concise implementation context for downstream engineering work. |
| 20 | create-openspec-handoff | Produce the final OpenSpec handoff because OpenSpec is the selected delivery mode. |

## Actions Not Needed

| Action ID | Reason not needed |
|---|---|
| draft-architecture-from-brs | An explicit architecture input already exists, so the workflow should review rather than draft from scratch. |
| create-standalone-handoff | Standalone is not the selected delivery mode. |
| create-compact-handoff | FastPath is not selected and the initiative is too large for compact-only handoff. |

## Risks of Under-Processing

If this initiative is treated as a small or lightweight change, the team could miss compliance-critical rules, integration failure modes, and audit obligations. That would increase the chance of unsafe lending decisions, incomplete traceability, or downstream contract mismatches across Experian, HMRC, DocuSign, and Temenos T24.

## Risks of Over-Processing

Running more artifacts than needed could add delivery overhead and slow time-to-handoff. The main risk is spending effort on optional outputs that do not materially reduce implementation risk once the required enterprise planning and readiness artifacts are complete.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No |
| Minimum required artifacts | Routing, intake summary with gate, business analysis set, architecture review and rules, planning artifacts, readiness outputs, and OpenSpec handoff. |
| Readiness still required? | Yes |
| Gates that still may trigger | Business intake review and engineering readiness review; additional quality gates may trigger based on readiness outcomes. |

## Constraints

_Any routing constraints that apply: team tooling, regulation, timeline, or delivery model limits._

| Constraint | Source | Impact |
|---|---|---|
| UK-only data residency | BRS constraints and architecture topology | Limits deployment and storage choices to UK regions and affects architecture validation. |
| Explainable AI only | BRS constraints | Requires explicit treatment in architecture, rules, and readiness outputs. |
| Existing enterprise integrations must be used | BRS constraints and architecture input | Increases contract sensitivity and supports enterprise modular planning. |
| Open questions remain on vendor and contract details | BRS open questions | Requires gaps analysis and careful downstream planning rather than fast-path execution. |
