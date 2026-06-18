# F-002.2 — AI Scoring Result with Explainability

## Metadata

| Field | Value |
|---|---|
| Story ID | F-002.2 |
| Epic | E-002 — Decisioning and Scoring |
| Feature | F-002 — AI Scoring Pipeline |
| Priority | Must |
| Increment | D1 |
| AC references | AC-005 |
| FR references | FR-007, FR-008 |

## 1. User Story

As the **Scoring Service**,
I want to produce a 0–1000 risk score and recommendation (Approve / Refer / Decline) with explainability outputs,
so that every credit decision is auditable and compliant with FCA explainability requirements.

### Business Goal

FCA regulations and ARCH-C-002 mandate that no black-box-only AI models may be used. Every score must have a human-interpretable explanation: a set of feature contributions (e.g., "Income reduced score by 45 points due to low income-to-loan ratio"). Without this, the platform cannot go live.

### Scope

**In scope:**
- Consuming the `scoring-requests` queue enqueued by F-002.1
- Running the ML inference service to produce a 0–1000 risk score
- Attaching explainability adapter outputs (feature contributions)
- Producing a recommendation: Approve (≥ 700), Refer (400–699), Decline (< 400)
- Storing score, recommendation, and explanation in the application record
- Emitting `scoring.completed` audit event
- Updating application status to `Scored`

**Out of scope:**
- Experian credit data lookup (F-002.3)
- AML/KYC checks (F-003)
- Underwriter review (F-004)

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-007 | System shall produce a 0–1000 risk score for each application |
| Requirement | FR-008 | System shall provide explainability outputs for every score |
| Architecture Constraint | ARCH-C-002 | Explainable AI only — no black-box-only models |
| Architecture Constraint | ARCH-C-004 | Immutable audit log must capture scoring.completed with score and explanation |
| Architecture Constraint | ARCH-C-001 | All ML inference in UK Azure region |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-009 | Score ≥ 700 → Approve; 400–699 → Refer; < 400 → Decline | Recommendation logic must use these exact thresholds |
| BR-010 | Explainability output must include at least 3 feature contributions | Scoring service must validate explanation output before storing |
| BR-011 | Score and explanation must be stored immutably — no post-hoc modification | Audit store write must be idempotent; no update path for score |

## 4. Acceptance Criteria

### AC-005 — Score produced with recommendation and explainability

**Given** an application with status `Scoring` is in the scoring-requests queue
**When** the Scoring Service processes the application
**Then** a 0–1000 risk score is produced
**And** a recommendation is set: Approve (≥ 700), Refer (400–699), or Decline (< 400)
**And** at least 3 feature contributions are attached as explainability outputs
**And** the score, recommendation, and explanation are stored on the application record
**And** the application status changes to `Scored`
**And** a `scoring.completed` audit event is emitted with ARN, score, recommendation, and timestamp

Traceability:
- Requirements: FR-007, FR-008
- Business Rules: BR-009, BR-010, BR-011
- BDD Scenario: SCN-F002-002

### AC-006 — Recommendation thresholds are enforced correctly

**Given** a risk score of exactly 700
**When** the recommendation logic runs
**Then** the recommendation is `Approve`

**Given** a risk score of exactly 399
**When** the recommendation logic runs
**Then** the recommendation is `Decline`

## 5. BDD Scenarios

```gherkin
# F-002.2 — AI Scoring Result with Explainability
# AC-005 — Score, recommendation, and explanation

Feature: AI scoring pipeline — score and explainability output

  Scenario: Application scored with Approve recommendation and explainability
    Given application "NEXT-20260617-000001" is in "Scoring" status in the scoring queue
    When the Scoring Service processes the application
    Then the risk score is between 700 and 1000
    And the recommendation is "Approve"
    And at least 3 feature contributions are included in the explanation
    And the application status changes to "Scored"
    And a "scoring.completed" event is emitted to the audit log with ARN, score, and recommendation

  Scenario: Application scored with Refer recommendation
    Given application "NEXT-20260617-000002" produces a risk score of 550
    When the Scoring Service produces the recommendation
    Then the recommendation is "Refer"
    And the application is enqueued for underwriter review (F-004)

  Scenario: Application scored with Decline recommendation
    Given application "NEXT-20260617-000003" produces a risk score of 300
    When the Scoring Service produces the recommendation
    Then the recommendation is "Decline"
    And the applicant is notified of the decline decision

  Scenario: Scoring service rejects output with fewer than 3 feature contributions
    Given the ML inference service returns only 1 feature contribution
    When the Scoring Service validates the explainability output
    Then the result is rejected as non-compliant
    And a "scoring.explainability_insufficient" alert event is emitted
    And the application status is set to "Refer" (conservative fallback)

  Scenario: Score boundary — exactly 700 maps to Approve
    Given the ML inference service returns a risk score of 700
    When the recommendation logic runs
    Then the recommendation is "Approve"

  Scenario: Score boundary — exactly 399 maps to Decline
    Given the ML inference service returns a risk score of 399
    When the recommendation logic runs
    Then the recommendation is "Decline"
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Scoring Service | Worker | New scoring worker consuming `scoring-requests` queue |
| ML Inference Service | ML Platform | Existing service; called via internal API |
| Explainability Adapter | Internal Service | New adapter wrapping ML output with feature contributions |
| Application Database | PostgreSQL | New columns: `risk_score`, `recommendation`, `explanation_json` |
| Immutable Audit Store | Event log | Consumes `scoring.completed` structured event |
| Underwriter Queue | Message Queue | Receives referred applications (feeds F-004) |

### Data Impact

New columns on `applications` table:
- `risk_score` (INTEGER, 0–1000, nullable)
- `recommendation` (ENUM: Approve, Refer, Decline, nullable)
- `explanation_json` (JSONB, nullable) — stores feature contributions array

`explanation_json` schema:
```json
{
  "model_version": "1.2.3",
  "feature_contributions": [
    { "feature": "income_to_loan_ratio", "contribution": -45, "direction": "negative" },
    { "feature": "credit_history_months", "contribution": +120, "direction": "positive" },
    { "feature": "existing_debt_ratio", "contribution": -30, "direction": "negative" }
  ]
}
```

### API Impact

No public API surface change. Scoring Service is an internal worker.

## 7. Constraints

The coding agent must respect these constraints without exception:

- No black-box-only models — explainability adapter must always produce ≥ 3 feature contributions; reject and alert if not (ARCH-C-002)
- Score and explanation are immutable once stored — no UPDATE path on `risk_score`, `recommendation`, or `explanation_json`
- Recommendation thresholds are exact: ≥ 700 Approve, 400–699 Refer, < 400 Decline — do not make configurable
- All ML inference in UK Azure region (ARCH-C-001)
- Audit event must be written before worker acks the queue message
- Refer recommendation must trigger underwriter queue enqueue atomically with status update

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-002.1 — AI Pre-Screening Trigger | Story | Yes | Produces scoring-requests queue messages |
| ML Inference Service | Platform | Yes | Must have a test endpoint available for integration tests |
| Explainability Adapter | Internal | Yes | Must be deployed; produces feature contributions |
| F-004 — Underwriter Queue | Story | No | Consumer of Refer routing; can be stubbed |
| Immutable Audit Store | Platform | Yes | Must be available for scoring.completed event |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Add `risk_score`, `recommendation`, `explanation_json` columns to applications table | Database | none | Migration runs; columns exist with correct types |
| T-002 | Implement Scoring Worker: consume scoring-requests queue, call ML inference service | Worker | T-001, ML Inference | Worker processes message; score stored on application |
| T-003 | Implement Explainability Adapter: wrap ML output with feature contributions | Adapter | T-002 | Unit test: adapter produces ≥ 3 contributions; rejects < 3 |
| T-004 | Implement recommendation logic: apply thresholds (≥700/400-699/<400) | Worker | T-002 | Unit test: boundary cases 700 → Approve, 399 → Decline, 400 → Refer |
| T-005 | Emit `scoring.completed` audit event with ARN, score, recommendation, timestamp | Worker | T-002, T-004 | Test: audit event schema correct; emitted before ack |
| T-006 | Atomic Refer routing: update status to Scored and enqueue to underwriter queue | Worker | T-004 | Test: underwriter queue receives message on Refer recommendation |
| T-007 | Fallback: insufficient explainability → set Refer, emit alert, do not store bad explanation | Worker | T-003 | Test: 1 feature contribution → Refer fallback + alert event |

## 10. Test Expectations

- [ ] Unit: recommendation thresholds — 700 → Approve, 699 → Refer, 400 → Refer, 399 → Decline
- [ ] Unit: explainability adapter rejects output with < 3 feature contributions
- [ ] Unit: fallback to Refer on insufficient explainability + alert event emitted
- [ ] Unit: `scoring.completed` event schema validation
- [ ] Integration: full scoring flow — queue message → score → status `Scored` → audit event
- [ ] Integration: Refer recommendation → underwriter queue receives message
- [ ] Integration: score immutability — no UPDATE path on risk_score
- [ ] Performance: scoring worker processes 100 applications in < 5 minutes

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-005, AC-006) are implemented and verifiable
- [ ] All BDD scenarios are covered by automated tests
- [ ] Explainability adapter produces ≥ 3 feature contributions in all test cases
- [ ] Score immutability enforced (no update path)
- [ ] Recommendation thresholds verified with boundary tests
- [ ] Traceability matrix updated: FR-007, FR-008 → F-002.2
- [ ] All architecture constraints (ARCH-C-001, ARCH-C-002, ARCH-C-004) respected
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-002.2 — AI Scoring Result with Explainability
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Implement the Scoring Service worker for NEXT13. It consumes the scoring-requests queue,
calls the ML inference service, attaches explainability outputs via the Explainability
Adapter (≥ 3 feature contributions required), applies recommendation thresholds, stores
score/recommendation/explanation on the application record immutably, routes Refer cases
to the underwriter queue, and emits scoring.completed to the audit store.

Files / components likely impacted:
- src/workers/scoring_worker.py — new worker
- src/services/explainability_adapter.py — wraps ML output with feature contributions
- src/services/recommendation_engine.py — threshold logic: ≥700 Approve, 400-699 Refer, <400 Decline
- src/db/migrations/YYYYMMDD_add_scoring_columns.py — risk_score, recommendation, explanation_json
- src/events/schemas.py — ScoringCompletedEvent schema
- tests/workers/test_scoring_worker.py — new test file
- tests/services/test_explainability_adapter.py — new test file
- tests/services/test_recommendation_engine.py — new test file

Constraints (must not be violated):
- Explainability is mandatory: if ML output has < 3 feature contributions, do NOT store the
  result, set recommendation to Refer (conservative fallback), emit scoring.explainability_insufficient
  alert event (ARCH-C-002).
- Score, recommendation, and explanation_json are immutable once stored — no UPDATE path.
- Recommendation thresholds are exact: ≥700 Approve, 400-699 Refer, <400 Decline.
  Do NOT make these configurable — they are regulatory thresholds.
- Refer recommendation must atomically update status to Scored AND enqueue to underwriter queue.
- Audit event (scoring.completed) must be durably written before worker acks the queue message.
- All ML inference and data processing in UK Azure region (ARCH-C-001).

Expected implementation steps:
1. Scoring Worker consumes scoring-requests queue messages.
2. Call ML Inference Service (internal) with application payload.
3. Pass ML output to Explainability Adapter:
   a. If < 3 feature contributions: emit scoring.explainability_insufficient; set Refer; do not store raw ML output.
   b. If ≥ 3 contributions: proceed.
4. Apply recommendation thresholds.
5. Begin transaction:
   a. Update application: risk_score, recommendation, explanation_json, status = Scored.
   b. If Refer: enqueue to underwriter queue.
   c. Emit scoring.completed event.
   d. Commit.
6. Ack queue message after successful commit.

Tests to add:
- Unit recommendation_engine: score=700 → Approve; score=699 → Refer; score=400 → Refer; score=399 → Decline
- Unit explainability_adapter: 3 contributions → pass; 2 contributions → reject; 0 contributions → reject
- Unit: insufficient explainability → Refer fallback + alert event emitted
- Unit: scoring.completed event schema (ARN, score, recommendation, timestamp, model_version)
- Integration: queue message → score stored → status Scored → audit event emitted
- Integration: Refer → underwriter queue receives message
- Integration: risk_score column has no UPDATE path (constraint violation on attempted update)

What NOT to change:
- ML Inference Service — call it; do not modify it
- F-002.1 trigger logic
- Underwriter queue consumer (F-004 owns that)

Validation checklist before marking complete:
- [ ] Score produced and stored for all applications
- [ ] Explainability adapter produces ≥ 3 contributions; rejects < 3
- [ ] Recommendation thresholds correct for boundary cases
- [ ] scoring.completed event emitted before queue ack
- [ ] Refer → underwriter queue message sent atomically
- [ ] Score immutability: no UPDATE path on risk_score
- [ ] All unit and integration tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
