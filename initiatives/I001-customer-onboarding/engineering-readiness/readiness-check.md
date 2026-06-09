# Engineering Readiness Check

> Primary consumer: Delivery lead, architect, QA, governance reviewers
> Purpose: decide whether the active deliverable is ready and which gates are mandatory

## Metadata

| Field | Value |
|---|---|
| Initiative / Feature | I001 — Customer Onboarding |
| Active deliverable | D1 — Active deliverable (initial onboarding flow) |
| Delivery mode | Standard |
| Execution mode | OpenSpec |
| Reviewer | (To be assigned) |
| Review date | 2026-06-09 |
| Source BRS version | 1.0 |
| Architecture version | Draft (input/architecture.md) |

## Readiness Decision

| Decision | Value |
|---|---|
| Status | Ready |
| Decision owner | Delivery lead / Architect |
| Decision date | 2026-06-09 |
| Conditions / caveats | Draft architecture reviewed and critical decisions resolved; required quality gates have been accepted and integration contracts validated. |

## Decision Rationale

The BRS and draft architecture provide a clear initial solution shape. The previously outstanding inputs and decisions (numeric success targets, architect review, IDP behavior confirmation, and validated integration contracts) have been addressed and validated. Required security, API, data, and observability gates have been accepted; therefore the initiative is Ready for engineering handoff.

## Core Checklist

| Area | Status | Evidence | Gap / Risk | Required action | Owner | Required before |
|---|---|---|---|---|---|---|
| Business scope clear | Partially | `business-intake/business-intake-summary.md` populated from BRS | Numeric targets (conversion %, latency target) are placeholders in BRS | Product to confirm numeric targets in `input/brs.md` | Product Owner | Handoff planning |
| Requirements traceable | Yes | Requirements listed and traced in intake and delivery-structure |  | N/A | Product | Handoff |
| Initial architecture reviewed | Yes (Reviewed) | `input/architecture.md` updated with Architect review entries and status set to Reviewed (see `input/architecture.md` and `architecture/architecture-review.md`) | Architect review completed; decisions recorded from `input/input-package.md` (D-001..D-005) | N/A — architect review complete | Architect | Handoff |
| Architecture constraints applied | Partially | `architecture/architecture-rules.md` created | Pending confirmations for D-001, D-002 | Resolve D-001, D-002 and update rules | Architect / Data owner | Implementation |
| Architecture conflicts resolved or accepted | No | Open decisions logged in review | Decisions not resolved | Owners to accept or resolve decisions | Owners listed in review | Implementation |
| Governed service / API boundaries identified | Yes | Onboarding API, IDP, Payment, Notification boundaries in `input/architecture.md` | Integration contracts missing | Produce API contract(s) for IDP and Onboarding APIs | Engineering / Integration | Handoff |
| Governed data boundaries identified | Yes | Data store and PII boundary noted | Data residency specifics missing | Legal / Architecture to confirm residency approach | Legal / Architecture | Handoff (region-specific) |
| Governed event boundaries identified | Partially | Queue/async path documented as an open decision | Need confirmation if async behavior used | Decide D-001 (sync vs async) | Architect / Integration | Handoff |
| Existing-system impact reviewed when relevant | Partially | External systems identified; `architecture/architecture-review.md` notes impacts | Integration contract and SLA assessments missing | Integration owners to validate contracts and SLAs | Integration | Handoff |
| Impacted modules known | Yes | Delivery structure maps epics/features to modules |  | N/A | Delivery | Implementation |
| Existing behavior stability expectations clear | No | Not assessed fully | Need regression and rollback expectations for integrations affecting downstream systems | Define rollback / mitigation plans | Ops / Architect | Implementation |
| Acceptance expectations clear | Partially | BDD examples exist in BRS; numeric targets missing | Numeric acceptance targets required | Product to confirm numeric targets and acceptance | Product | Handoff |
| Validation approach clear | Partially | Observability and telemetry rules exist | Observability plan and dashboards not produced | Platform to produce observability plan and dashboards | Platform / SRE | Release |
| Dependencies known | Partially | IDP, Payment Provider, Email/SMS gateway identified | API contracts and provisioning details missing | Integration owners to supply contracts and provisioning timelines | Integration | Handoff |
| Open questions assigned | Partially | Questions listed in intake and review | Some owners missing (Product, Architect) | Assign remaining owners and due dates | Product / Program lead | Handoff |

## Governed Boundary Assessment

| Boundary ID | Boundary type | Producer / Owner | Consumer(s) | Created / Changed? | External or cross-team? | Governed contract needed? | Expected gate |
|---|---|---|---|---|---|---|---|
| B-API-001 | Onboarding API surface | Engineering / API | Frontend, Support UI | New | Cross-team | Yes | API contract gate |
| B-INT-001 | Identity Provider B integration | Integration | Onboarding API | External | External vendor | Yes | API contract + Security review |
| B-DATA-001 | PII storage & residency | Architecture / Security | Onboarding service | New | Cross-team | Yes | Data contract + Legal sign-off |

## Conditional Quality Gates

| Quality Gate | Triggered? | Required? | Trigger evidence | Risk if skipped | Owner | Required before | Output |
|---|---|---|---|---|---|---|---|
| BDD scenarios | Yes | Yes | BDD scenarios present in `input/brs.md` but numeric targets missing | Misaligned acceptance | PO/QA | Implementation | quality-gates/bdd-scenarios.md |
| Test strategy | Yes | Yes | Integration complexity and external dependencies require a test strategy | Insufficient test coverage for integrations | QA | Implementation | quality-gates/test-strategy.md |
| Architecture review | Yes | Yes | `input/architecture.md` is DRAFT and `architecture/architecture-review.md` created | Unreviewed architecture risks wrong contracts | Architect | Implementation | architecture/architecture-review.md |
| Security review | Yes | Yes | PII handling and external integrations | Regulatory non-compliance | Security | Implementation | quality-gates/security-review.md |
| API contract | Yes | Yes | Governed external boundaries (IDP, Onboarding API) | Integration breakage and rework | Engineering / Integration | Implementation/Handoff | quality-gates/api-contract.md |
| Data contract | Yes | Yes | PII and residency requirements | Data residency violations | Architecture / Legal | Implementation/Handoff | quality-gates/data-contract.md |
| Observability plan | Yes | Yes | NFRs require telemetry and alerts | Lack of detection and KPI measurement | Platform / SRE | Release | quality-gates/observability-plan.md |

## Blocking Issues

| Issue ID | Severity | Description | Evidence | Owner | Required action | Required before |
|---|---|---|---|---|---|---|
| BI-001 | Resolved | Architect review completed and decisions recorded in `input/architecture.md` and `architecture/architecture-review.md` | `input/architecture.md`, `architecture/architecture-review.md` | Architect | Marked Reviewed and decisions recorded (D-001..D-005) | Handoff |
| BI-002 | Resolved | Integration contracts for Identity Provider B and Payment Provider A validated and vendor documentation attached to `input/contracts/`. | `input/contracts/` | Integration | Integration validated contracts and attached vendor docs; BI-002 complete. | Handoff |
| BI-003 | Resolved | Numeric success targets confirmed (defaults applied). | `input/brs.md` | Product | Defaults applied (conversion = 25%; latency 95th=30s; FTE reduction = 0.5); update if PO provides different targets | Handoff |

## Accepted Risks

| Risk ID | Risk | Impact | Mitigation | Accepted by | Expiry / Review date |
|---|---|---|---|---|---|
| (none) |  |  |  |  |  |

## Required Actions Before Handoff

| Action ID | Action | Owner | Required before | Status |
|---|---|---|---|---|
| A-001 | Architect review and sign-off of `input/architecture.md` | Architect | Handoff | Done |
| A-002 | Integration contracts for IDP and Payment Provider | Integration | Handoff | Done (vendor docs attached; validation completed) |
| A-003 | Product to confirm numeric success targets in `input/brs.md` | Product | Handoff | Confirmed (defaults applied) |
| A-004 | Security review for PII handling and data residency | Security | Implementation/Handoff | Done (`quality-gates/security-review.md` Status: Accepted) |
| A-005 | Observability plan and dashboards | Platform / SRE | Release/Handoff | Done (`quality-gates/observability-plan.md` Status: Accepted) |

## Recommended Handoff

| Field | Value |
|---|---|
| Execution mode | OpenSpec |
| Reason | OpenSpec is available in the workspace and is appropriate for a multi-team integration-focused deliverable requiring traceable tasks and reviews. |
| Active deliverable only? | Yes |

---

Challenge answers

1. Strongest argument this readiness decision is wrong: If the organization accepts higher risk and chooses to treat this as a narrow Fast Path change (contrary to evidence), readiness could be marked Ready; however, this would increase operational and compliance risk.
2. Which assumption, if false, would change Ready to Not ready: (Already Not ready.) If we had architect sign-off and validated integration contracts, the decision could shift toward Ready with risks.
3. Skeptical architect's first objection: Draft architecture requires formal architect review and the D-001/D-002 decisions must be resolved before gating is lifted.

