# Business Intake Summary

> Produced by: product-owner
> Primary consumer: Product Owner, business analyst, delivery lead
> Purpose: confirm business scope, intent, gaps, and reviewable boundaries before architecture and planning
> Downstream use: architecture review, delivery planning, readiness

## Metadata

| Field | Value |
|---|---|
| Initiative | I021-NEXT21 |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-17T16:10:00+00:00 |
| Created by | product-owner |

## Executive Summary

| Field | Summary |
|---|---|
| Initiative | AI-Powered Loan Origination Platform |
| Business objective | Replace manual loan origination with an AI-assisted digital platform to reduce decision time and improve consistency (see OBJ-001..OBJ-005). |
| Why now | Competitive pressure from fintechs and regulatory need for auditable, consistent decisions. |
| Main outcome expected | Consistent, auditable loan decisions for eligible applicants within minutes and digital end-to-end for a majority of cases. |
| Primary risk or constraint | Regulatory compliance (AML/KYC/GDPR) and integration with Experian and Temenos core banking. |

## Source Document Inventory

| Source | Type | Coverage / purpose | Owner | Notes |
|---|---|---|---|---|
| input/brs.md | BRS | Full functional and non-functional requirements, objectives, scope, constraints | Head of Retail Lending | Primary source for intake |
| input/architecture.md | Architecture | Proposed cloud topology and component mapping | Architect | Provides proposed service boundaries and constraints |

## Objectives

| Objective ID | Objective | Success measure | Source reference |
|---|---|---|---|
| OBJ-001 | Reduce decision time to ≤30 minutes for straight-through cases | ≥70% decisions ≤30 minutes | input/brs.md |
| OBJ-002 | Improve underwriter consistency | Variance in approval rates reduced by ≥50% | input/brs.md |
| OBJ-003 | Full regulatory audit trail | 100% decisions have immutable audit trail within 24h | input/brs.md |
| OBJ-004 | Comply with AML/KYC/GDPR | Zero regulatory findings in first post-launch audit | input/brs.md |
| OBJ-005 | Enable digital end-to-end for eligible applicants | ≥60% approved loans disbursed without human intervention | input/brs.md |

## Scope

| Area | In scope | Out of scope | Source reference |
|---|---|---|---|
| Product | Personal loan origination (£1k–£50k): intake, AI pre-screening, AML/KYC, underwriter workflow, offer generation, disbursement | Mortgages, business loans, native mobile app (Phase 2) | input/brs.md |
| Integrations | Experian, HMRC, DocuSign, Temenos T24 | Additional bureau providers or payment systems | input/brs.md, input/architecture.md |

## Requirements (summary)

| Requirement ID | Summary | Business value | Source reference |
|---|---|---|---|
| FR-001 | Applicant submission form fields and validation | Ensures complete applications before submission | input/brs.md |
| FR-002 | Inline validation and error handling on intake form | Reduces incomplete submissions and rework | input/brs.md |
| FR-003 | Assign unique Application Reference Number (ARN) | Enables tracking and idempotent processing | input/brs.md |
| FR-004 | Email confirmation with ARN and timeline | Improves applicant experience and traceability | input/brs.md |
| FR-005 | Status retrieval by ARN and DOB without registration | Lowers friction for applicants to check status | input/brs.md |
| FR-006 | Trigger AI pre-screening within 60s of submission | Speeds decisioning for eligible cases | input/brs.md |
| FR-007 | Produce risk score (0–1000) and recommendation | Standardises decision inputs for automation | input/brs.md |
| FR-008 | AI model input requirements (bureau data, DTI, LTI, etc.) | Ensures scores use consistent signals | input/brs.md |
| FR-009 | Integrate Experian CreditExpert API with 30s SLA | Provides credit bureau data for scoring | input/brs.md |
| FR-010 | Auto-approve rules for amounts ≤£10,000 with AML/KYC clearance | Enables straight-through processing for low-risk cases | input/brs.md |
| FR-011 | Auto-decline notifications with cooling-off period | Maintains regulatory fairness and cooling-off policy | input/brs.md |
| FR-012 | AML screening against sanctions and PEP lists within 60s | Compliance requirement to prevent prohibited disbursements | input/brs.md |
| FR-013 | KYC identity verification via HMRC API | Ensures identity verification before offer generation | input/brs.md |
| FR-014 | Compliance hold routing for failed AML/KYC | Routes potential compliance issues to human review | input/brs.md |
| FR-015 | Underwriter queue, actions, and immutable decision logging | Enables human oversight and traceability | input/brs.md |
| FR-016 | Underwriter escalation after 4 business hours | Ensures SLAs for human review | input/brs.md |
| FR-017 | Underwriter actions: approve/decline/request info | Human decision granularity and traceability | input/brs.md |
| FR-018 | Record underwriter actions immutably | Audit and compliance evidence | input/brs.md |
| FR-019 | Underwriter dashboard with AI context | Improves decision efficiency and consistency | input/brs.md |
| FR-020 | Loan offer generation with key terms | Enables digital offer and acceptance | input/brs.md |
| FR-021 | Present offer via portal and email | Applicant visibility and acceptance channel | input/brs.md |
| FR-022 | Digital acceptance via DocuSign integration | Legally-binding e-signature capture | input/brs.md |
| FR-023 | Log acceptance with timestamp and IP | Auditability for acceptance events | input/brs.md |
| FR-024 | Trigger disbursement to Temenos T24 upon acceptance | Completes end-to-end flow to core banking | input/brs.md |
| FR-025 | Include disbursement payload details in instruction | Correctly route payment details | input/brs.md |
| FR-026 | Retry and alert on disbursement failures | Operational resilience for payments | input/brs.md |
| FR-027 | Applicant notifications for disbursement | Keeps applicants informed of status | input/brs.md |
| FR-028 | Emit structured observability events for key steps | Operational metrics and audit signals | input/brs.md |
| FR-029 | Admin dashboard with metrics and filters | Operational visibility for teams | input/brs.md |
| FR-030 | Audit log is append-only and tamper-evident | Regulatory requirement for traceability | input/brs.md |

## Capabilities

| Capability | Outcome | Related requirements |
|---|---|---|
| Digital intake & ARN | Applicants can submit and track applications | FR-001, FR-003 |
| AI scoring & recommendation | Risk scoring and auto-route decisions | FR-006..FR-011 |
| Compliance screening | AML/KYC checks with hold routing | FR-012..FR-014 |
| Underwriter oversight | Queue, decisions, immutable audit | FR-015..FR-019 |

## Existing-System Context

| Area | Current-state note | Why it matters | Source reference |
|---|---|---|---|
| Loan processing | Manual paper/email workflow with inconsistent decisions | High automation opportunity; requires careful change management | input/brs.md |

## Gaps and Questions

| ID | Question / gap | Impact if unresolved | Owner | Needed before | Answer |
|---|---|---|---|---|---|
| OQ-001 | Approved AI model vendor / approach? | Affects AI Scoring design and explainability approach | Head of AI | AI design and procurement | Azure Foundry |
| OQ-002 | Cooling-off waiver legal sign-off flow? | Affects UI and legal workflow | Legal | Offer flow design | Not required |
| OQ-003 | HMRC KYC fallback behaviour? | Impacts compliance workflow and queueing | Compliance | Compliance runbook | manual verification |
| OQ-004 | Which AML providers? | Affects integration count and SLA | Compliance | Compliance integration plan | HM Treasury only |
| OQ-005 | T24 payment gateway contract status? | Impacts disbursement integration scope | IT Architecture | Integration specification | We can define ours |

## Risks and Assumptions

All open questions from the source BRS are recorded above with answers where available; no unresolved questions remain that block proceeding to the next staged action.


| ID | Type | Description | Impact | Owner / follow-up |
|---|---|---|---|---|
| R-001 | Compliance | Regulatory controls (AML/KYC/GDPR) increase scope and must be validated early | Could delay delivery if unresolved | Compliance / Architecture |
| R-002 | Integration | Experian or T24 outages could force manual routing | Requires circuit breakers and fallback processes | Integration lead |
| A-001 | Data residency | All data will remain in UK regions | Assumed available cloud services in UK | Architecture team |

## Consolidation Notes

| Topic | Overlap / conflict / assumption | Resolution or current position |
|---|---|---|
| AI model vendor | OQ-001 indicates in-house vs third-party decision pending | Record as open question (OQ-001) |

## PO Review Checklist

- [x] Objectives are understandable and measurable
- [x] Scope boundaries are explicit
- [x] Requirements are traceable to source documents
- [x] Existing-system context is visible when relevant
- [x] Open questions have clear impact and owners
- [x] Risks and assumptions are reviewable without engineering detail
