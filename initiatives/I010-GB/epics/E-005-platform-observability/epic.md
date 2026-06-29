# E-005 — Platform & Observability

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-005 |
| Initiative ID | I010-GB |
| Wave | Wave 1 |
| Priority | Should |
| Increment | D1 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Provide platform capabilities—observability, metrics, audit store, and CI/CD scaffolding—to ensure safe delivery, regulatory auditability, and operational visibility for the initiative. This enables teams to validate integrations, monitor system health, and provide immutable audit trails required by regulators.

---

## Scope

**In scope:**
- Immutable audit store and append-only API (FR-028).
- Metrics pipeline and admin dashboards (FR-029, FR-030).
- CI/CD pipeline templates, environment provisioning, and deployment scaffolding.

**Out of scope:**
- Feature-specific UI pages and business logic (handled in respective epics).

---

## High-Level Acceptance Criteria

- AC-E-005-1: Audit store accepts append events and is tamper-evident.
- AC-E-005-2: Metrics pipeline ingests and displays admin dashboard metrics per FR-029.
- AC-E-005-3: CI/CD pipeline can deploy a sample Intake service to staging in UK region.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| Requirement | FR-028 | Immutable audit log of state transitions |
| Requirement | FR-029 | Admin dashboard metrics and refresh |
| Requirement | FR-030 | Emit structured observability events |
| Non-functional | NFR-005 | Audit log write-once, tamper-evident |
| Constraint | ARCH-C-001 | UK data residency for logs |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Audit Store | New | Immutable append-only audit storage with retention policy. |
| Metrics Pipeline | New | Ingest, aggregate, and expose admin metrics. |
| CI/CD | New/Changed | Pipeline templates, environment provisioning, infra as code. |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| Cloud provider UK region | External | Yes | Must provision UK-region resources for data residency. |
| Logging provider / storage | External | No | Choose compliant storage supporting append-only semantics. |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Audit store performance under load | Medium | High | Prototype with expected event rate; scale with partitioning and retention policies. |

---

## Foundation / Setup

Provide Terraform/ARM/Bicep modules (team preference) for audit store, metrics pipeline, and a templated CI/CD pipeline. Ensure test harness for synthetic event generation.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-005.0 | Platform e2e POC | frontend / backend / infrastructure / integration | Must | D1 | Not Ready |
| S-005.1 | Audit store: append API | Infrastructure / Backend | Must | D1 | Not Ready |
| S-005.2 | Metrics pipeline & dashboard | Infrastructure / Backend | Should | D2 | Not Ready |
| S-005.3 | CI/CD: pipeline template and deploy sample service | Infrastructure | Must | D1 | Not Ready |

---

## Advisory Reviews

*Status: Draft — set to Accepted only after epic review gate.*
