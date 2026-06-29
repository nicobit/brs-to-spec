# E-004 — Underwriter Decisioning

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-004 |
| Initiative ID | I011-MB |
| Wave | Wave 3 |
| Priority | Must |
| Increment | D2 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Provide underwriters with a queue, detailed application view, and actions with immutable audit trail to enable compliant manual decisioning where models refer or require overrides.

---

## Scope

**In scope:**
- Underwriter Queue and Application Detail pages
- Actions: Approve / Decline / Request more info with audit entries
- Integration with `ExplainabilityStore` and `AuditStore`

**Out of scope:**
- Automated offer generation (E-005)

---

## High-Level Acceptance Criteria

- AC-E-001: Underwriter can view application details, score, credit report, and take actions; actions are audited immutably (FR-016, FR-018, FR-028).

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| FR-015 | Underwriter queue | FR-015 |
| FR-016 | Underwriter dashboard contents | FR-016 |
| FR-017 | Underwriter actions | FR-017 |
| FR-018 | Underwriter audit record | FR-018 |
| FR-028 | Immutable audit log | FR-028 |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Underwriter UI | Frontend | Queue, detail, actions |
| AuditStore | Change | Immutable audit entries |
| Underwriter APIs | Backend API | Action endpoints and audit writes |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-002 Scoring | Epic | Yes | Underwriter UI consumes /scores and explainability |

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-004.1 | Implement Underwriter Queue UI | Frontend | Must | D2 | Not Ready |
| S-004.2 | Application Detail UI & bindings | Frontend / Backend API | Must | D2 | Not Ready |
| S-004.3 | Underwriter action endpoints & audit | Backend API | Must | D2 | Not Ready |
| S-004.4 | Immutable audit schema | Backend API / Infrastructure | Must | D2 | Not Ready |

---

*Status: Draft.*
