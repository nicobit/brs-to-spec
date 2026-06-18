# Routing Decision

> Produced by: orchestrator
> Primary consumer: all downstream personas
> Purpose: select the minimum safe staged path for this initiative
> This artifact is immutable after acceptance. Changes require a routing reset or rerun.

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-NEXT1 |
| Created at | 2026-06-16 |
| Created by | orchestrator |
| Status | Draft |

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | BusinessCopilot | Initiative requires AI-assisted intake, rapid iteration, and stakeholder collaboration; BusinessCopilot accelerates business-facing artifact generation while integrating compliance checks. | High |
| Execution mode | Enterprise+Modular | Multiple integrations (Experian, HMRC, DocuSign, Temenos) and regulatory constraints require enterprise controls with modular delivery per capability. | High |
| Small-change path applicable? | No | Requirements are broad (many integrations, regulatory needs), not a safe small-change candidate. | Medium |

## Delivery Mode Assessment

| Criterion | Score | Evidence from inputs | Impact on decision |
|---|---|---|---|
| Requirement ambiguity | Low | BRs are detailed with clear scope and success measures | Favors standard staged delivery |
| Architecture impact | High | Multiple external integrations (Experian, HMRC, T24) and core banking coupling | Requires enterprise-level coordination and modular design |
| Compliance / audit relevance | High | FCA, GDPR, and audit trail requirements stated | Necessitates compliance gating and formal reviews |
| Business criticality | High | Customer-facing loan decisions and regulatory risk | Requires careful rollout and monitoring |
| Number of teams | High | Product, AI, Compliance, Architecture, Operations, Integrations | Larger coordination overhead; modular releases recommended |
| Delivery size | Large | Multiple epics and integrations in scope | Multi-stage delivery recommended |
| AI context saturation risk | Medium | AI model requirements and explainability constraints | Requires model governance and explainability artifacts |
| Small-change path applicable? | No | Many moving parts and integrations increase risk | Avoid small-change path |
| Regression / contract sensitivity | High | Core banking and compliance integrations imply high risk | Strong testing and contracts required |

## Execution Mode Assessment

| Mode | Available? | Recommended? | Reason |
|---|---|---|---|
| OpenSpec | Yes | No | Too lightweight for regulatory, integration needs |
| Standalone | Yes | No | Lacks enterprise controls required for core banking integration |
| BusinessCopilot | Yes | Yes | Supports business-driven artifact generation and stakeholder collaboration while enabling governance |

## Required Next Actions

| Order | Action ID | Reason required |
|---|---|---|
| 1 | create-business-intake-summary | Build a focused business intake to confirm scope and acceptance criteria for downstream analysis |
| 2 | create-requirements | Produce a requirements catalog from the intake and BRs for engineering planning |
| 3 | create-entity-model | Capture data model assumptions tied to integrations and audit requirements |

## Actions Not Needed

| Action ID | Reason not needed |
|---|---|
| create-business-test-expectations | Can be produced later once requirements are stable |

## Risks of Under-Processing

If routing selects a smaller path, the project risks missing regulatory requirements, integration contracts, and model governance, leading to production rework and compliance findings.

## Risks of Over-Processing

Over-processing will add unnecessary delay and cost; aim to modularize to deliver the highest-risk integrations first.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No |
| Minimum required artifacts | business-intake, requirements, entity-model |
| Readiness still required? | Yes — tests, compliance checks, and model governance |
| Gates that still may trigger | Business intake review, compliance gate, architecture review |

## Constraints

- Must comply with FCA Consumer Duty regulations
- Must comply with UK GDPR (data residency: UK only)
- Integrations with Experian, HMRC, DocuSign, and Temenos T24 will need contracts and API agreements
- AI explainability requirements constrain acceptable model approaches
