# Business Intake Summary

> Produced by: product-owner
> Primary consumer: Product Owner, business analyst, delivery lead
> Purpose: confirm business scope, intent, gaps, and reviewable boundaries before architecture and planning

## Metadata

| Field | Value |
|---|---|
| Initiative | I010-NEXT1 |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Executive Summary

| Field | Summary |
|---|---|
| Initiative | AI-Powered Loan Origination Platform |
| Business objective | Deliver an AI-assisted loan origination platform that reduces decision time, improves consistency, and provides full auditability |
| Why now | Competitive pressure from fintechs and regulatory need for auditable decisions |
| Main outcome expected | Faster, consistent, and auditable loan decisions for eligible applicants |
| Primary risk or constraint | Regulatory compliance (FCA, GDPR) and integration with core banking and credit/identity providers |

## Source Document Inventory

| Source | Type | Coverage / purpose | Owner | Notes |
|---|---|---|---|---|
| input/brs.md | BRS | Full functional and NFR scope | Head of Retail Lending | Primary source |
| routing/routing-decision.md | Routing | Delivery & execution recommendations | orchestrator | Generated |
| input/architecture.md | Architecture notes | Existing-system context | | Optional |

## Objectives

| Objective ID | Objective | Success measure | Source reference |
|---|---|---|---|
| OBJ-001 | Reduce average decision time to ≤30 minutes for straight-through cases | ≥70% of applications ≤30 minutes | input/brs.md |
| OBJ-002 | Improve underwriter consistency | Variance reduced by ≥50% | input/brs.md |
| OBJ-003 | Achieve full regulatory audit trail | 100% decisions have audit trail within 24h | input/brs.md |

## Scope

| Area | In scope | Out of scope | Source reference |
|---|---|---|---|
| Product | Personal loan intake, AI pre-screening, AML/KYC, underwriter workflow, offer generation, disbursement | Mortgages, business loans, mobile native app | input/brs.md |

## Requirements

| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
|---|---|---|---|---|
| FR-006 | Trigger AI pre-screening within 60s | Faster triage and routing | input/brs.md | System logs and timings |
| FR-009 | Integrate with Experian CreditExpert | Enable credit checks within 30s | input/brs.md | Integration test with Experian sandbox |

## Capabilities

| Capability | Outcome | Related requirements | Notes |
|---|---|---|---|
| Application intake | Capture applicant data and assign ARN | FR-001, FR-003 | Web form, validations |
| AI scoring pipeline | Risk score and recommendation | FR-006, FR-007 | Model must be explainable |

## Existing-System Context

| Area | Current-state note | Why it matters | Source reference |
|---|---|---|---|
| Core banking | Temenos T24 used for disbursement | Integration required for live disbursement | input/brs.md |
| Credit bureau | Experian contract exists | Use Experian API for credit reports | input/brs.md |

## Gaps and Questions

| ID | Question / gap | Impact if unresolved | Owner | Needed before |
|---|---|---|---|---|
| GAP-001 | Approved AI model vendor/approach? | Affects model procurement and explainability approach | Head of AI | Requirements and model design |
| GAP-002 | HMRC KYC fallback when unavailable? | Affects operational routing | Compliance | Intake acceptance |

## Risks and Assumptions

| ID | Type | Description | Impact | Owner / follow-up |
|---|---|---|---|---|
| R-001 | Compliance | Regulatory requirements may delay delivery | High | Compliance team |
| R-002 | Integration | Delays in Experian or T24 integrations | High | Architecture/Integration team |

## Consolidation Notes

| Topic | Overlap / conflict / assumption | Resolution or current position |
|---|---|---|
| AI model | Vendor vs in-house tradeoffs | Investigate Azure Foundry and vendor options |

## PO Review Checklist

- [ ] Objectives are understandable and measurable
- [ ] Scope boundaries are explicit
- [ ] Requirements are traceable to source documents
- [ ] Existing-system context is visible when relevant
- [ ] Open questions have clear impact and owners
- [ ] Risks and assumptions are reviewable without engineering detail
