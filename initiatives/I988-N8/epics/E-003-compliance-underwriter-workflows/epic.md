# E-003 — Compliance & Underwriter Workflows

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-003 |
| Initiative ID | I988-N8 |
| Wave | from elaboration plan |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-21 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Enable automated AML/KYC screening and efficient underwriter review so that high-risk applications are identified early, compliance evidence is recorded, and underwriters can triage and decide on referred applications with clear audit trails. Failure to deliver increases regulatory and financial risk.

---

## Scope

**In scope:**
- AML/KYC screening orchestration for submitted applications
- Underwriter task queue, task assignment, actions (approve, refer, escalate), and audit logging
- Emission of observability and audit events for regulatory retention

**Out of scope:**
- Full document-based KYC extraction (handled by a separate integration epic)
- Long-term reporting dashboards (E-005)

---

## High-Level Acceptance Criteria

- AC-E-001: AML screening is invoked for every submitted application and produces a deterministic screening result recorded in the audit log.
- AC-E-002: Underwriter actions (approve, refer, escalate) persist a task state transition and emit audit events within 2s of action completion.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | §Compliance | See requirements REQ-006, REQ-009..011, REQ-013, REQ-022 |
| Requirements | FR / REQ mapping | F-005, F-006, F-007 |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Scoring & Decisioning | Integration | Receive screening results and influence routing |
| Underwriter Service | New | Task queue and action APIs |
| Audit Service / Event Bus | Integration | Emit audit and observability events |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-002 — AI Scoring | Epic | Yes | Screening may consume scoring outputs for risk signals |
| Experian adapter | External | No | Used by screening where required (F-007 addresses observability only)

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Regulatory evidence not retained | Medium | High | Ensure event payloads include proof and retention policy; test retention flows |
| Underwriter queue bottleneck | Medium | Medium | Design idempotent tasks and scalable consumer group processing |

---

## Foundation / Setup

No foundation setup required — existing event bus, Key Vault, and CI/CD pipelines apply. Ensure the `underwriter-queue` topic and `audit-events` topic are provisioned in the environment prior to deployment.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| F-005.1 | AML/KYC screening orchestration | Backend / Integration | Must | D1 | Ready |
| F-006.1 | Underwriter queue and task actions | Backend / Frontend / Integration | Must | D1 | Ready |
| F-007.1 | Observability and audit event emission | Backend / Infrastructure | Should | D1 | Ready |

---
*Status: Draft — set to Accepted only after epic review gate. Never self-accept.*
