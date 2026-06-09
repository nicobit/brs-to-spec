# Business Intake Summary

## Executive Summary

| Field | Summary |
|---|---|
| Initiative | I001 Client Onboarding |
| Business objective | Reduce onboarding lead time while preserving compliance checks and auditability |
| Why now | Manual onboarding review is too slow and incomplete submissions create rework |
| Main outcome expected | A guided onboarding submission flow that improves completeness and reviewability |
| Primary risk or constraint | Identity, document retention, and auditability obligations must remain intact |

## Source Document Inventory

| Source | Type | Coverage / purpose | Owner | Notes |
|---|---|---|---|---|
| `input/brs.md` | BRS | onboarding objectives and business requirements | Product / Compliance | main business source |
| `input/architecture.md` | Architecture note | approved service constraints and audit expectations | Architecture | constrains delivery design |

## Objectives

| Objective ID | Objective | Success measure | Source reference |
|---|---|---|---|
| OBJ-01 | Reduce onboarding lead time | submission-to-review lead time reduced | `input/brs.md` |
| OBJ-02 | Improve submission completeness | fewer incomplete onboarding requests | `input/brs.md` |
| OBJ-03 | Preserve auditability | auditable submission and review trail | `input/architecture.md` |

## Scope

| Area | In scope | Out of scope | Source reference |
|---|---|---|---|
| Onboarding submission | guided submission with identity and document capture | full reviewer workflow automation | `input/brs.md` |
| Auditability | capture audit event and traceable submission outcome | long-term retention policy redesign | `input/architecture.md` |

## Requirements

| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
|---|---|---|---|---|
| BRS-01 | collect required identity and document evidence during submission | improves reviewer completeness and reduces rework | `input/brs.md` | `quality-gates/bdd-scenarios.md` |
| BRS-02 | emit an auditable onboarding submission event | supports downstream traceability and compliance | `input/brs.md` | `standalone-delivery/D1-guided-onboarding/validation-plan.md` |

## Capabilities

| Capability | Outcome | Related requirements | Notes |
|---|---|---|---|
| identity verification | submission contains verified identity context | BRS-01 | must use approved validation service |
| document submission | required files arrive with the request | BRS-01 | file access and authorization matter |
| audit event publishing | successful submission is traceable downstream | BRS-02 | impacts event and observability expectations |

## Existing-System Context

| Area | Current-state note | Why it matters | Source reference |
|---|---|---|---|
| onboarding workflow | onboarding currently depends on manual completeness checks | guided submission should reduce manual triage | `input/brs.md` |
| operational controls | document handling and audit services already exist | the change must fit approved controls rather than replace them | `input/architecture.md` |

## Gaps and Questions

| ID | Question / gap | Impact if unresolved | Owner | Needed before |
|---|---|---|---|---|
| Q-01 | What exact retention rule applies to uploaded onboarding documents? | release and operational controls may be incomplete | Compliance | Release |
| Q-02 | Which downstream consumers depend on the audit event schema? | event and data contract scope may be incomplete | Architecture / Operations | Handoff |

## Risks and Assumptions

| ID | Type | Description | Impact | Owner / follow-up |
|---|---|---|---|---|
| R-01 | Risk | privacy obligations may require stricter document handling than currently assumed | security and release risk | Security / Compliance |
| A-01 | Assumption | existing identity validation service remains the approved mechanism | architecture and task scope depend on it | Architecture |

## Consolidation Notes

| Topic | Overlap / conflict / assumption | Resolution or current position |
|---|---|---|
| auditability | both business and architecture inputs require audit traceability | treated as non-negotiable delivery constraint |
| retention detail | business inputs imply retention sensitivity but policy detail is incomplete | keep as open question and risk until confirmed |

## PO Review Checklist

- Objectives are understandable and measurable.
- Scope boundaries are explicit.
- Requirements are traceable to source documents.
- Existing-system context is visible when relevant.
- Open questions have clear impact and owners.
- Risks and assumptions are reviewable without engineering detail.
