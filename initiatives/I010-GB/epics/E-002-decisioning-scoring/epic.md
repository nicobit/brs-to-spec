# E-002 — Decisioning & Scoring

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-002 |
| Initiative ID | I010-GB |
| Title | Decisioning & Scoring |
| Priority | Must |
| Risk | High |
| Dependencies | E-001, E-005 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Run automated scoring to produce a risk score and recommendation that enables automated approvals and informed referrals to underwriters. Capture explainability artifacts to satisfy regulatory requirements.

---

## Scope

In scope:
- Scoring pipeline ingestion API and model inference (FR-006, FR-007).
- Explainability artifact capture and storage (FR-007, AR-005).

Out of scope:
- Underwriter UI flows (handled in E-003).

---

## Acceptance Criteria

- AC-E-002-1: On submission, the system triggers scoring within 60s (FR-006).
- AC-E-002-2: Scoring result includes numeric score and recommendation (FR-007).
- AC-E-002-3: Explainability artifacts stored and retrievable per AR-005.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| Functional | FR-006 | Trigger AI pre-screening within 60s |
| Functional | FR-007 | Produce risk score and recommendation |
| Functional | FR-008 | Model inputs for scoring |

---

## Impacted Systems

| System | Change Type | Notes |
|---|---|---|
| Scoring pipeline | New | Ingest scoring jobs, host models, emit results |
| Explainability service | New | Persist feature contributions and rationale |
| Intake API | Change | Publish scoring jobs on submit |

---

## Stories

| Story ID | Title | Layers | Priority |
|---|---|---|---|
| S-002.0 | Scoring e2e POC | frontend / backend / infrastructure / integration | Must |
| S-002.1 | Scoring ingestion API | backend / infrastructure | Must |
| S-002.2 | Store explainability artifacts | backend / infrastructure | Must |

---

## Advisory Reviews

*Status: Draft — proceed to review after technical validation.*
