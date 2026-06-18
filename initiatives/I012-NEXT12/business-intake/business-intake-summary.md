# Business Intake Summary

> Produced by: product-owner
> Primary consumer: Product Owner, business analyst, delivery lead
> Purpose: confirm business scope, intent, gaps, and reviewable boundaries before architecture and planning
> Downstream use: architecture review, delivery planning, readiness
> Status: Draft

## Metadata

| Field | Value |
|---|---|
| Initiative | AI-Powered Loan Origination Platform (I012-NEXT12) |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Executive Summary

| Field | Summary |
|---|---|
| Initiative | Replace manual personal-loan origination with an AI-assisted digital platform to deliver consistent, auditable, regulatory-compliant decisions in minutes for eligible applicants. |
| Business objective | Reduce decision time, improve consistency, ensure full auditability, and enable digital end-to-end for eligible applicants (see OBJ-001..OBJ-005). |
| Why now | Competitive pressure from fintechs, regulatory obligations (FCA/GDPR/AML), and existing manual process limitations. |
| Main outcome expected | Straight-through processing for eligible applications (≥70% under 30 minutes), immutable audit trail, and integrated compliance checks. |
| Primary risk or constraint | Regulatory compliance (AML/KYC, explainability), vendor integrations (Experian, DocuSign, Temenos T24), and UK-only data residency. |

## Source Document Inventory

| Source | Type | Coverage / purpose | Owner | Notes |
|---|---|---|---|---|
| `input/brs.md` | BRS | Full functional and non-functional requirements, objectives, constraints, open questions | Head of Retail Lending | Primary source for requirements and constraints |
| `routing/routing-decision.md` | Routing decision | Delivery and execution mode selection (OpenSpec / Enterprise+Modular) | orchestrator | Informs artifact scope and required next actions |
| `input/architecture.md` | Architecture | High-level component topology and integration points | Architect (draft) | Provides integration and deployment constraints |

## Objectives

| Objective ID | Objective | Success measure | Source reference |
|---|---|---|---|
| OBJ-001 | Reduce average decision time for straight-through cases to ≤30 minutes | ≥70% of applications reach decision in ≤30 minutes | `input/brs.md` |
| OBJ-002 | Improve underwriter consistency | Variance in approval rate across underwriters reduced by ≥50% | `input/brs.md` |
| OBJ-003 | Achieve full regulatory audit trail for all loan decisions | 100% of decisions have immutable audit trail within 24h of go-live | `input/brs.md` |
| OBJ-004 | Comply with AML, KYC, and GDPR requirements | Zero regulatory findings in first post-launch compliance audit | `input/brs.md` |
| OBJ-005 | Enable digital end-to-end for eligible applicants | ≥60% of approved loans disbursed without human intervention | `input/brs.md` |

## Scope

| Area | In scope | Out of scope | Source reference |
|---|---|---|---|
| Product | Loan application intake, AI pre-screening, credit bureau integration, AML/KYC checks, underwriter review, offer generation, disbursement integration, applicant portal, admin dashboards, observability | Mortgages, business loans, direct debit setup, mobile native app (Phase 2) | `input/brs.md` |

## Requirements (selected highlights)

| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
|---|---|---|---|---|
| FR-001 | Online application intake capturing mandatory applicant fields and loan details | Enables digital intake and ARN assignment | `input/brs.md` | Form validation, ARN issued on submit |
| FR-006 | Trigger AI pre-screening within 60s of submission | Enables rapid decisioning and routing | `input/brs.md` | Scoring event within SLA |
| FR-009 | Integrate with Experian CreditExpert API; fallback to refer when unavailable | Necessary for credit decision inputs and regulatory completeness | `input/brs.md` | Experian response within 30s or auto-refer behavior proven |
| FR-012 | Perform AML screening against HM Treasury sanctions/PEP databases within 60s | Regulatory compliance requirement | `input/brs.md` | AML checks complete within SLA; compliance hold routing validated |
| FR-020 | Generate loan offer document with terms and digital acceptance via DocuSign | Enables digital acceptance and downstream disbursement | `input/brs.md` | Offer generation and DocuSign integration test |

## Capabilities

| Capability | Outcome | Related requirements | Notes |
|---|---|---|---|
| Rapid scoring pipeline | Score and recommend `AUTO_APPROVE`/`REFER_TO_UNDERWRITER`/`AUTO_DECLINE` | FR-006..FR-011 | AI model must be explainable (constraint) |
| Compliance screening | AML/KYC checks and routing to compliance team | FR-012..FR-014 | Circuit-breaker and fallback behavior required |
| Immutable audit trail | Tamper-evident log of state transitions | FR-028 | Stored in Cosmos DB append-only container |

## Existing-System Context

| Area | Current-state note | Why it matters | Source reference |
|---|---|---|---|
| Underwriting process | Currently manual, paper/email workflows with 5–10 day decision times | Drives need for digital automation and auditability | `input/brs.md` |
| Credit bureau integration | Experian contract exists | Integration latency and contract terms affect design | `input/architecture.md`, `input/brs.md` |
| Core banking | Temenos T24 via internal payment gateway | Disbursement integration and contract details required | `input/architecture.md` |

## Gaps and Questions

| ID | Question / gap | Impact if unresolved | Owner | Needed before |
|---|---|---|---|---|
| GAP-001 | OQ-001: Approved AI model vendor / approach (in-house vs third-party)? — Affects model design, explainability approach, and compliance posture | Affects model design, explainability approach, and compliance posture | Head of AI | Prior to detailed scoring pipeline design |
| GAP-002 | OQ-002: Does cooling-off waiver require legal sign-off flow? — Affects UX and legal acceptance flow design | Affects UX and legal acceptance flow design | Legal | Prior to offer/acceptance workflow finalization |
| GAP-003 | OQ-003: HMRC KYC API fallback when unavailable (manual verification or auto-refer)? — Affects compliance queue load and SLA expectations | Affects compliance queue load and SLA expectations | Compliance | Before finalizing Compliance Service state machine |
| GAP-004 | OQ-004: Exact AML database providers (HM Treasury only or additional vendors)? — Affects screening coverage and latency | Affects screening coverage and latency | Compliance | Before procurement and compliance sign-off |
| GAP-005 | OQ-005: T24 payment gateway contract details — existing or needs negotiation? — Affects Payment Gateway Adapter scope and integration timeline | Affects Payment Gateway Adapter scope and integration timeline | IT Architecture | Before disbursement increment planning |

## Risks and Assumptions

| ID | Type | Description | Impact | Owner / follow-up |
|---|---|---|---|---|
| RSK-001 | Compliance | Model explainability requirement may limit vendor choices or increase engineering effort | Delayed delivery of scoring pipeline | Head of AI / Compliance |
| RSK-002 | Integration | Experian/T24/DocuSign outages increase refer-to-underwriter rates | Increased manual workload and slower decisioning | Platform / Integrations team |
| RSK-003 | Data residency | All data must remain in UK data centres | Constraints on cloud region and vendor services | Architecture / Security |

## Consolidation Notes

| Topic | Overlap / conflict / assumption | Resolution or current position |
|---|---|---|
| AI vendor | OQ-001 lists multiple approaches; BRS notes Azure Foundry as preferred | Record preference but confirm Head of AI decision in GAP-001 |
| KYC fallback | OQ-003 answered as 'manual verification' in BRS but confirm operational process | Treat as current position pending Compliance confirmation |

## PO Review Checklist

- [ ] Objectives are understandable and measurable
- [ ] Scope boundaries are explicit
- [ ] Requirements are traceable to source documents
- [ ] Existing-system context is visible when relevant
- [ ] Open questions have clear impact and owners
- [ ] Risks and assumptions are reviewable without engineering detail
