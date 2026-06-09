# Input Package

## Initiative Workspace

| Field | Value |
|---|---|
| Initiative ID | I001 |
| Initiative slug | customer-onboarding |
| Workspace path | `initiatives/I001-customer-onboarding/` |

## Input Inventory

| Artifact | Source document | Available? | Version / date | Completeness | Notes |
|---|---|---|---|---|---|
| BRS | `input/brs.md` | Yes | 1.0 | Partial — owners and some targets blank | Requires PO to fill stakeholder names and confirm numeric targets |
| Architecture | `input/architecture.md` | Yes | 1.0 (2026-06-09) | Reviewed | Architect-validated; decisions D-001..D-005 recorded in `input/architecture.md` |

## Consolidation Notes

### Source Overlap

Single BRS source — no overlap.

### Source Conflicts

None identified at input stage.

### Authoritative Sections or Resolution Rule

BRS is the single source of truth for business requirements. Architecture draft is a proposal only — not authoritative until architect-reviewed.

## Known Limitations

- BRS stakeholder names are blank — owner fields must be populated before governance sign-off
- Measurable targets in BRS used placeholder values; defaults have been applied in the input package but PO should confirm or replace them in `input/brs.md`

## Missing Inputs

| Missing input | Impact | Owner | Required before |
|---|---|---|---|
| BRS stakeholder names | Ownership and sign-off cannot be assigned | PO | Readiness |

## Assumptions

| Assumption | Basis | Risk if wrong |
|---|---|---|
| Identity Provider B supports required verification flows | BRS states "assumed" explicitly | If IdP cannot support the flows, the integration design changes significantly |
| Required API keys and webhooks will be provisioned before implementation | BRS assumption | If not provisioned on time, implementation is blocked |

## Decisions and Clarifications Received

Use this section to record answers that came from human conversations — vendor calls, PO sessions, Legal review, architect decisions — that are not captured in any other document.

When you have a new answer, add a row here. The next time you trigger the workflow, the framework will pick it up automatically.

| Decision ID | Question / open decision | Answer received | Source (who / when) | Confidence | Impact on workflow |
|---|---|---|---|---|---|
| Decision ID | Question / open decision | Answer received | Source (who / when) | Confidence | Impact on workflow |
|---|---|---|---|---|---|
| D-001 | Identity Provider B: sync vs async verification? | Asynchronous (webhook/callback) | Integration (2026-06-09) | High | Enables async verification flow; API supports 202 Accepted + webhook processing |
| D-002 | Payment Provider A: mandatory for all onboarding paths or only some? | Mandatory for all onboarding paths | Integration (2026-06-09) | High | Ensures payment validation included in MVP flows |
| D-003 | GDPR data residency: which regions? | Italy | Product / Legal (2026-06-09) | High | Legal validation required; informs data partitioning and hosting |
| D-004 | Technology stack for containers? | AKS (Azure Kubernetes Service) | Ops (2026-06-09) | Medium | Guides deployment IaC (AKS) and ops readiness |
| D-005 | Profile Store: relational vs document? | Relational | Data / Architect (2026-06-09) | High | Influences schema, migrations, and consistency decisions |
| D-006 | Email/SMS gateway provider? | SendGrid | Product / Ops (2026-06-09) | High | Provider selection for notifications; template ownership assigned to Product/Ops |
| D-007 | CRM sync: in scope or post-launch? | In scope (initial delivery) | Product (2026-06-09) | High | CRM mapping and data contract must be included in delivery plan |
| D-008 | Numeric success targets: conversion %, latency threshold, FTE reduction | Conversion = 25%; Latency (95th pct) = 30s (30000 ms); FTE reduction = 0.5 | Product (applied default 2026-06-09) | Medium | Enables acceptance criteria and BDD numeric targets for testing and acceptance |
| D-009 | Named owners for Product, Engineering, Security roles | Product Owner = Product Owner (TBD); Engineering = Engineering Lead (TBD); Security = Security Lead (TBD) | Program (applied defaults 2026-06-09) | Low | Placeholder owners assigned; update with real names when available |

## Recommended Next Step

Run the workflow:

```text
#brs-to-spec-run-workflow
```

Or trigger it naturally by asking about the initiative status.
