# Business Intake Summary

> Produced by: product-owner
> Status: Draft
> Initiative: I111-NEXT11

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Source BRS | input/brs.md |
| Routing decision | routing/routing-decision.md |
| Created at | 2026-06-18 |

## Executive Summary

This initiative implements an AI-assisted Loan Origination Platform to replace a manual underwriting process. Key goals are faster decisions for eligible applications, consistent underwriting, and full regulatory auditability. Multiple external integrations and compliance requirements mean this initiative requires an engineering-ready handoff.

## Source Document Inventory

| File | Type | Coverage |
|---|---|---|
| input/brs.md | BRS | Full business requirements, objectives, scope, FRs (FR-001..FR-030), NFRs, constraints, open questions |
| routing/routing-decision.md | Routing decision | Delivery: enterprise-modular, execution: Enterprise+Modular |

## Objectives

| ID | Objective | Success measure | Source |
|---|---|---|---|
| OBJ-001 | Reduce average decision time for straight-through cases | ≥70% decisions ≤30 minutes | input/brs.md |
| OBJ-002 | Improve underwriter consistency | Underwriter approval variance reduced by ≥50% | input/brs.md |
| OBJ-003 | Full regulatory audit trail for all loan decisions | 100% decisions have immutable audit trail within 24h | input/brs.md |
| OBJ-004 | Comply with AML, KYC, GDPR | Zero regulatory findings in first post-launch audit | input/brs.md |
| OBJ-005 | Enable digital end-to-end for eligible applicants | ≥60% of approved loans disbursed without human intervention | input/brs.md |

## Scope

### In scope

- Personal loan intake (£1,000–£50,000)
- AI pre-screening and scoring
- Credit bureau integration (Experian)
- AML/KYC checks
- Underwriter review workflow
- Offer generation and e-signature (DocuSign)
- Core banking disbursement (Temenos T24)
- Applicant portal, admin dashboards, observability and audit trail

### Out of scope

- Mortgages, business loans, mobile native app, direct debit setup (Phase 2)

## Requirements (Functional)

| ID | Requirement | Business value | Source |
|---|---|---|---|
| FR-001 | Applicant can submit online application with required fields | Enables digital intake and downstream automation | input/brs.md |
| FR-006 | Trigger AI pre-screening within 60s of submission | Enables fast automated decisions | input/brs.md |
| FR-007 | AI produces risk score and recommendation | Drives routing and underwriter decisions | input/brs.md |
| FR-009 | Integrate Experian CreditExpert API within 30s | Required for scoring inputs; fallback to refer | input/brs.md |
| FR-012 | Perform AML screening against sanctions and PEP lists | Regulatory compliance requirement | input/brs.md |
| FR-015 | Present refer/large approvals to underwriter queue within 2 minutes | Ensures timely human review | input/brs.md |
| FR-020 | Generate loan offer document for approvals | Customer-facing contract and acceptance flow | input/brs.md |

## Requirements (Non-functional)

| ID | Requirement | Target | Source |
|---|---|---|---|
| NFR-001 | Form load time | ≤2s | input/brs.md |
| NFR-002 | AI scoring pipeline latency | ≤90s end-to-end | input/brs.md |
| NFR-004 | PII encryption | AES-256 at rest, TLS1.3 in transit | input/brs.md |
| NFR-006 | Availability | 99.9% business-hours uptime | input/brs.md |

## Capabilities

| Capability | Description |
|---|---|
| Digital intake | Online application capture, ARN generation, email confirmation |
| AI scoring | Risk scoring with explainability and decision recommendation |
| Compliance workflows | AML/KYC screening, compliance hold routing |
| Underwriter tooling | Dashboard, decision recording, escalation |

## Existing-System Context

| System | Role / Interaction |
|---|---|
| Experian CreditExpert | External credit report source for scoring |
| HMRC identity verification | KYC verification source |
| DocuSign | E-signature provider for offer acceptance |
| Temenos T24 (core) | Disbursement execution via internal payment gateway |

## Gaps and Questions

| ID | Question | Owner | Priority | Impact |
|---|---|---|---|---|
| GAP-001 | Approved AI model vendor/approach (in-house vs third-party)? | Head of AI | High | Affects model procurement and explainability approach (BRS notes Azure Foundry) |
| GAP-002 | Fallback for HMRC KYC API when unavailable — manual verify or auto-refer? | Compliance | High | Affects routing and SLA for decisions |
| GAP-003 | Exact AML database providers beyond HM Treasury? | Compliance | High | Affects vendor integration scope |

## Risks and Assumptions

| ID | Risk / Assumption | Mitigation |
|---|---|---|
| RSK-001 | Experian API availability could delay scoring | Implement circuit breaker and refer-to-underwriter fallback |
| RSK-002 | Regulatory audit findings if audit trail incomplete | Design immutable audit log and compliance review gate early |
| RSK-003 | Explainability requirements constrain ML model choices | Prefer explainable models or feature-level explanations |

## Consolidation Notes

- Source BRS is comprehensive; a few high-priority open questions remain (see Gaps).
- Routing recommends `enterprise-modular` which matches this workspace's workflow type.

## PO Review Checklist

| Item | Status |
|---|---|
| Objectives captured and measurable | Yes |
| Functional requirements atomised and traceable | Yes (sampled; full extraction required) |
| NFRs captured | Yes |
| Open questions surfaced as GAPs | Yes |
| Existing-system context documented | Yes |
| Status | Draft |
