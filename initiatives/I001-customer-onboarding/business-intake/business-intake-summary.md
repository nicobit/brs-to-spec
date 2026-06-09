# Business Intake Summary

> Primary consumer: Product Owner, business analyst, delivery lead
> Purpose: confirm business scope, intent, gaps, and reviewable boundaries before architecture and planning

## Executive Summary

| Field | Summary |
|---|---|
| Initiative | I001 — Customer Onboarding |
| Business objective | Reduce time-to-onboard and improve onboarding completion rate to increase conversion and operational efficiency (see measurable targets in `input/brs.md`). |
| Why now | High business value from improved conversion; existing manual effort and regulatory drivers (GDPR) create urgency. |
| Main outcome expected | A reliable, observable digital onboarding flow for retail customers integrating identity verification and payment validation with measurable improvement in onboarding metrics. |
| Primary risk or constraint | Dependency on Identity Provider B (availability and contract semantics) and PII/data residency compliance. |

## Source Document Inventory

| Source | Type | Coverage / purpose | Owner | Notes |
|---|---|---|---|---|
| input/brs.md | BRS | Full business requirements, objectives, NFRs, scope, integrations | Product | Primary source for this intake |
| input/architecture.md | Draft architecture | Architect-reviewed architecture derived from BRS | Architecture | Reviewed — architect-validated (2026-06-09); decisions D-001..D-005 recorded |
| input/input-package.md | Input package | Stub — needs consolidation notes and owners | Product | Stub — populate as part of intake |

## Objectives

| Objective ID | Objective | Success measure | Source reference |
|---|---|---|---|
| OBJ-001 | Reduce median time-to-onboard | From 5 days → 1 day (numeric target to confirm) | input/brs.md |
| OBJ-002 | Increase onboarding completion rate | Target: 90% within 90 days (confirm exact target) | input/brs.md |
| OBJ-003 | Reduce manual processing effort | Reduce by 2.0 FTEs within 6 months | input/brs.md |

## Scope

| Area | In scope | Out of scope | Source reference |
|---|---|---|---|
| Primary onboarding flow | New digital onboarding for retail customers: identity verification, profile capture, initial consent, notifications | Enterprise account provisioning; legacy manual backlog reprocessing | input/brs.md |
| Integrations | Identity Provider B, Payment Provider A, Email/SMS gateway | Custom biometric identity provider, enterprise provisioning | input/brs.md |

## Requirements

| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
|---|---|---|---|---|
| FR-001 | Create account via email or phone | Enables customer access | input/brs.md | BDD scenario AC-001 |
| FR-002 | Complete identity verification via Identity Provider B | Prevent fraud and comply with KYC requirements | input/brs.md | AC scenarios in input/brs.md |
| FR-003 | Persist customer profile and consent records | Legal and operational traceability | input/brs.md | Data model & tests |
| FR-004 | Send onboarding notifications via email/SMS | Customer engagement and completion signaling | input/brs.md | Notification templates & delivery checks |
| FR-005 | Support agent view and retry capabilities | Operational recovery and supportability | input/brs.md | Support UI validation |

## Capabilities

| Capability | Outcome | Related requirements | Notes |
|---|---|---|---|
| Fast verification flow | Reduced time-to-onboard and higher completion | FR-001, FR-002, NFR-001 | Requires IDP SLAs and UX decision (sync vs async) |
| Observable onboarding metrics | Measure time-to-onboard and failure rate | NFR-005 | Telemetry and tracing required |
| Support recovery tools | Reduce manual effort and FTEs | FR-005 | Support UI and retry APIs needed |

## Existing-System Context

| Area | Current-state note | Why it matters | Source reference |
|---|---|---|---|
| Identity Provider B | External vendor to be used for verification | Service availability and API semantics directly affect UX and implementation | input/brs.md, input/architecture.md |
| Payment Provider A | External payment validation | Required for payment-related validation flows; contract semantics needed | input/brs.md |
| CRM | Optional downstream system | If required, will add data contracts and privacy review | input/brs.md, input/architecture.md |

## Optional Visual View

See `input/architecture.md` for a compact C4 context, container, and integration sequence that supports business review.

## Gaps and Questions

| ID | Question / gap | Impact if unresolved | Owner | Needed before |
|---|---|---|---|---|
| Q-001 | Confirm numeric success targets (conversion %, latency threshold M) | Defaults applied (Conversion=25%; Latency 95th=30s); Product to confirm or update | Product | Release planning |
| Q-002 | Confirm whether IDP verification is synchronous or asynchronous (webhook) | Resolved — asynchronous (webhook/callback). Update delivery stories and UX to reflect async 202 Accepted flow. | Architect / Integration owner | Architecture review (complete) |
| Q-003 | Confirm whether CRM sync is in initial scope | Affects integration effort and privacy review | Product | Scope decision before planning |
| Q-004 | Provide owners for Product, Engineering, Security | Lacking named owners slows approvals and gating | Product / Program lead | PO review |

## Risks and Assumptions

| ID | Type | Description | Impact | Owner / follow-up |
|---|---|---|---|---|
| R-001 | Integration risk | IDP outages or unexpected API semantics | Delays and user-facing failures; mitigations: retries, fallbacks | Integration owner |
| R-002 | Compliance risk | Data residency and GDPR requirements | Could block rollout in regions; need legal/security signoff | Security / Legal |
| A-001 | Assumption | IDP and Payment Provider APIs support required interactions | If false, alternative vendor or design changes required | Product / Integration |

## Consolidation Notes

| Topic | Overlap / conflict / assumption | Resolution or current position |
|---|---|---|
| Measurable targets | BRS contains placeholders (X, Y, Z, M) | Product to populate numeric targets in `input/brs.md` or `input/input-package.md` |
| Input package | `input/input-package.md` is a stub | Populate with owners, inventory, and consolidation notes |

## PO Review Checklist

- Objectives are understandable and measurable (numeric targets missing). 
- Scope boundaries are explicit.
- Requirements are traceable to `input/brs.md`.
- Existing-system context is visible; integration owners must validate contracts.
- Open questions have owners assigned above; Product to confirm.

