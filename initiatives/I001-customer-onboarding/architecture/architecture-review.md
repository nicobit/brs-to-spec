# Architecture Review

> Primary consumer: Architect, tech lead, delivery lead
> Purpose of this artifact: confirm architecture constraints, alignment, conflicts, and decisions that shape delivery
> Downstream use: architecture rules, delivery structure, readiness, governed contract decisions

## Constraints Identified

- **PII protection required**: PII must be encrypted at rest and in transit (from BRS NFR-003). Owner: Security.
- **Use Identity Provider B**: BRS mandates using Identity Provider B; integration contract needed. Owner: Integration/Product.
- **Availability target**: Service must target >= 99.9% availability — affects deployment topology and redundancy. Owner: Architecture/Ops.
- **Data residency / GDPR**: Regional residency requirement implied; hosting and data partitioning decisions required. Owner: Architecture / Legal.

## Existing-System Impact Summary

- Identity Provider B and Payment Provider A are external dependencies. The initiative must confirm API contracts, SLA, retry semantics, and webhook semantics before implementation.
- If the onboarding service synchronously depends on IDP for happy-path completion, user-visible latency and frontend UX are impacted — product must accept potential 202/async UX or require blocking flows.
- CRM sync is optional per BRS; if later required it will introduce additional contract, data-mapping, and privacy review work.

## Optional Visual View

The draft `input/architecture.md` includes a focused C4 context and container diagram plus an integration sequence (mermaid). Use those diagrams as the authoritative initial view; no additional visual added here.

## BRS Alignment

- The draft architecture preserves traceability to BRS functional requirements FR-001..FR-005 and NFRs (performance, availability, observability). Key architecture elements (frontend, orchestration API, data store, queue, support UI) are directly derived from the BRS.

## Conflicts

- No direct conflicts discovered between the draft architecture and the BRS. Several open choices remain and must not be silently resolved (see Open Decisions). These choices materially affect delivery (sync vs async verification, data store choice, deployment topology).

## Decisions

The following decisions were recorded and have been resolved. Each entry includes owner and resolution date.

| Decision ID | Decision | Why it matters | Owner | Status | Resolved date |
|---|---|---|---|---|---|
| D-001 | Synchronous vs asynchronous identity verification | Impacts API semantics, UX (202 vs 200), retry/backoff design, and queueing | Architect / Integration owner | Resolved | 2026-06-09 |
| D-002 | Primary data store choice (relational vs document) | Affects schema design, consistency, queries, and migration | Data owner / Architect | Resolved | 2026-06-09 |
| D-003 | Deployment topology to meet 99.9% | Affects cost, redundancy, and operational runbooks | Ops / Architect | Resolved | 2026-06-09 |
| D-004 | CRM sync in initial scope or post-launch | Changes integration effort, data contracts, and privacy review | Product / Business owner | Resolved | 2026-06-09 |
| D-005 | Notification provider selection and template management | Affects SLA, deliverability, and compliance | Product / Ops | Resolved | 2026-06-09 |

## Missing Inputs and Impact

- `business-intake/business-intake-summary.md` has been populated with intake details and objectives; confirm owners and numeric targets. Impact: ensures acceptance and priority decisions are available for planning.
- `planning/delivery-structure.md` is present and provides an initial delivery breakdown; review stories to ensure acceptance criteria reflect resolved decisions (D-001..D-005).

## Recommended Next Actions (short)

- Architect to review `input/architecture.md`, mark `Architect review status` and populate `Architect Review Notes` with approved decisions or corrections.
- Product to complete `business-intake/business-intake-summary.md` with confirmed scope (CRM decision, rollout plan) and acceptance owners.
- Product/Delivery to add `planning/delivery-structure.md` so architecture implications can be mapped to delivery slices.
- Integration/Platform owners to validate IDP and Payment Provider contracts (endpoints, webhooks, SLAs).

---

Generated from `input/brs.md` and `input/architecture.md` on 2026-06-09.

## Architect Review Entry (2026-06-09)

The following decisions were recorded from the initiative input package (`input/input-package.md`) and have been applied to the draft architecture metadata and notes:

- D-001: Identity Provider B verification mode — **asynchronous** (webhook/callback). Owner: Architect / Integration. Resolved: 2026-06-09.
- D-002: Primary data store — **relational**. Owner: Data / Architect. Resolved: 2026-06-09.
- D-003: Deployment topology — **Azure (AKS across Availability Zones)**. Owner: Ops / Architecture. Resolved: 2026-06-09.
- D-004: CRM sync — **In scope** for initial delivery. Owner: Product. Resolved: 2026-06-09.
- D-005: Notification provider — **SendGrid**. Owner: Product / Ops. Resolved: 2026-06-09.

Notes:
- Integration contracts (endpoints, webhooks, error semantics, SLAs) for Identity Provider B and Payment Provider A are still required and must be delivered before handoff.
- GDPR residency region recorded as **Italy** and requires Legal validation.

