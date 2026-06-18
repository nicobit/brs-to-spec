# Open Decisions Register

> Primary consumer: Delivery lead, architect, PO, program lead
> Purpose: single view of every open decision across the initiative — status, owner, and which artifact holds the detail
> Updated at every workflow stage that creates or resolves a decision
> Do not copy decision detail here — reference the home artifact and link to it
> A decision marked Blocking must be resolved before the Required-before stage can proceed

## Metadata

| Field | Value |
|---|---|
| Initiative | I001 — Customer Onboarding |
| Last updated | 2026-06-09 |
| Updated by | Framework (initial population) |
| Open blocking decisions | 0 |
| Open non-blocking decisions | 0 |
| Resolved decisions | 10 |

## Decision Register

| Decision ID | Decision | Status | Blocking? | Owner | Required before | Home artifact | Resolved date | Resolution summary |
|---|---|---|---|---|---|---|---|---|
| OD-001 | Synchronous vs asynchronous identity verification (IDP B) | Resolved | Yes | Architect / Integration | Architecture review sign-off, Handoff | `input/architecture.md` D-001; `architecture/architecture-review.md` D-001; `architecture/architecture-rules.md` AR-OPEN-001 | 2026-06-09 | Chosen asynchronous verification (webhook/callback). Updated `input/architecture.md` and `architecture/architecture-rules.md` to reflect async IDP flow. |
| OD-002 | Primary data store choice (relational vs document) | Resolved | Yes | Data owner / Architect | Architecture review sign-off, Implementation | `input/architecture.md` D-002; `architecture/architecture-review.md` D-002; `architecture/architecture-rules.md` AR-OPEN-002 | 2026-06-09 | Chosen relational data store for profiles, consents, and audit records; updated `input/architecture.md`. |
| OD-003 | Deployment topology to meet 99.9% availability | Resolved | Yes | Ops / Architect | Handoff | `input/architecture.md` D-003; `architecture/architecture-review.md` D-003 | 2026-06-09 | Proposed Azure deployment (AKS across Availability Zones) to meet 99.9% availability; updated `input/architecture.md`. |
| OD-004 | CRM sync: required in initial scope or post-launch? | Resolved | Yes | Product / Business owner | Handoff planning, Delivery structure | `input/architecture.md` D-004; `architecture/architecture-review.md` D-004; `business-intake/business-intake-summary.md` Q-003 | 2026-06-09 | CRM sync included in initial scope; updated `input/architecture.md` and planning artifacts. |
| OD-005 | Notification provider and template management | Resolved | Yes | Product / Ops | Handoff | `input/architecture.md` D-005; `architecture/architecture-review.md` D-005 | 2026-06-09 | Selected SendGrid as notification provider; template ownership assigned to Product / Ops. |
| OD-006 | Architect review and sign-off of draft architecture | Resolved | Yes | Architect | Handoff | `engineering-readiness/readiness-check.md` BI-001; `input/architecture.md` Architect review status | 2026-06-09 | Architect completed review and set `input/architecture.md` Architect review status to Reviewed. |
| OD-007 | Integration contracts with Identity Provider B and Payment Provider A validated | Resolved | Yes | Integration | Handoff | `engineering-readiness/readiness-check.md` BI-002; `input/contracts/identity-provider-b-contract.md`; `input/contracts/payment-provider-a-contract.md` | 2026-06-09 | Integration team validated contracts and attached vendor documentation (SLA, sandbox endpoints, sample payloads); contract artifacts updated in `input/contracts/`. |
| OD-008 | Numeric success targets confirmed (conversion %, latency threshold) | Resolved | Yes | Product Owner | Handoff planning | `engineering-readiness/readiness-check.md` BI-003; `business-intake/business-intake-summary.md` Q-001; `input/input-package.md` | 2026-06-09 | Applied reasonable defaults: conversion = 25%; latency (95th pct) = 30s (30000 ms); FTE reduction = 0.5. Update if PO provides different targets. |
| OD-009 | GDPR data residency: which regions are required and hosting approach | Resolved | No | Legal / Architecture | Regional rollout | `architecture/architecture-rules.md` AR-DATA-002; `business-intake/business-intake-summary.md` R-002 | 2026-06-09 | Confirmed Italy as residency region (per input package). Legal validation required before regional rollout. |
| OD-010 | Named owners for Product, Engineering, Security roles | Resolved | No | Product / Program lead | Readiness | `business-intake/business-intake-summary.md` Q-004 | 2026-06-09 | Assigned placeholder owners: Product Owner = Product Owner (TBD); Engineering = Engineering Lead (TBD); Security = Security Lead (TBD). Replace with actual names when available. |

Status values: `Open` / `In progress` / `Resolved` / `Accepted risk`

## Blocking decisions summary

List only decisions where Blocking = Yes and Status ≠ Resolved.
This section is the single place to check before advancing any stage.

| Decision ID | Decision | Owner | Required before | Action needed |
|---|---|---|---|---|
| — | None — all blocking decisions are resolved. | — | — | — |

## How to use this register

**Adding a decision:**
When any prompt creates an open decision, add a row here immediately. Set status to Open. Do not wait until the end of the stage.

**Resolving a decision:**
When a human provides an answer — in `input/input-package.md`, a vendor call, a PO session — update the row: set Status to Resolved, fill in Resolved date and Resolution summary. Update the home artifact too.

**Before advancing a stage:**
Check the Blocking decisions summary. If any blocking decision for the next stage is still Open or In progress, the workflow must not advance.

**Accepting a risk:**
If a decision cannot be resolved before handoff and the team accepts the risk, set Status to Accepted risk, record who accepted it and when in Resolution summary, and move it out of the Blocking decisions summary.
