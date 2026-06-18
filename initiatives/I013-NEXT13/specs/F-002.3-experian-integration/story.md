# F-002.3 — Experian Credit Lookup with Underwriter Fallback

## Metadata

| Field | Value |
|---|---|
| Story ID | F-002.3 |
| Epic | E-002 — Decisioning and Scoring |
| Feature | F-002 — AI Scoring Pipeline |
| Priority | Must |
| Increment | D2 |
| AC references | AC-006 |
| FR references | FR-009 |

## 1. User Story

As the **System**,
I want to fetch Experian credit bureau data for each application and fall back to refer-to-underwriter if the lookup fails or times out,
so that scoring is enriched with authoritative credit data and no application is blocked by a transient Experian outage.

### Business Goal

AI scoring accuracy depends on Experian bureau data (credit history, existing debt, defaults). Without it, scores are less accurate and approval rates are less reliable. The fallback-to-underwriter path ensures regulatory continuity: no application is silently dropped or erroneously approved due to a bureau outage.

### Scope

**In scope:**
- Calling Experian API (enterprise contract, ARCH-C-003) for credit bureau data
- Passing bureau data to the AI Scoring Service as a scoring input
- Implementing timeout (5 seconds), retry (3 attempts), and fallback logic
- On fallback: setting application status to `Referred`, routing to underwriter queue with `EXPERIAN_UNAVAILABLE` reason
- Emitting `experian.lookup.completed` or `experian.lookup.failed` audit event

**Out of scope:**
- AI scoring logic itself (F-002.2)
- Underwriter dashboard (F-004)
- Experian contract setup (procurement — already contracted, ARCH-C-003)

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-009 | System shall use Experian credit bureau data as a scoring input |
| Architecture Constraint | ARCH-C-003 | Must use enterprise Experian contract — no alternative bureau |
| Architecture Constraint | ARCH-C-005 | Experian integration SLA: response within 5 seconds |
| Architecture Constraint | ARCH-C-001 | PII transmitted to Experian must be limited to minimum necessary; no UK data stored outside UK |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-012 | Experian SLA: 5-second timeout; 3 retries with exponential backoff | Timeout and retry must be implemented exactly as specified |
| BR-013 | If Experian unavailable after 3 retries: fallback to refer-to-underwriter | Fallback must not silently drop the application |
| BR-014 | Only minimum necessary PII may be transmitted to Experian (NI number, name, DOB) | Do not send financial details or address beyond what Experian requires |

## 4. Acceptance Criteria

### AC-006 — Experian lookup enriches scoring; fallback routes to underwriter

**Given** an application in `Scoring` status
**When** the Scoring Service requests Experian credit data
**Then** Experian returns bureau data within 5 seconds
**And** the bureau data is passed as input to the AI Scoring Service
**And** an `experian.lookup.completed` event is emitted to the audit log

**Given** Experian does not respond within 5 seconds after 3 retry attempts
**When** the fallback logic triggers
**Then** the application status is set to `Referred`
**And** the application is enqueued to the underwriter queue with reason `EXPERIAN_UNAVAILABLE`
**And** an `experian.lookup.failed` event is emitted to the audit log

Traceability:
- Requirements: FR-009
- Business Rules: BR-012, BR-013, BR-014
- BDD Scenario: SCN-F002-003

## 5. BDD Scenarios

```gherkin
# F-002.3 — Experian Credit Lookup with Underwriter Fallback
# AC-006 — Lookup and fallback

Feature: Experian credit bureau integration with fallback

  Scenario: Experian returns bureau data within SLA
    Given application "NEXT-20260617-000001" is in "Scoring" status
    And Experian API responds within 2 seconds
    When the Scoring Service calls Experian for credit bureau data
    Then Experian bureau data is returned and stored as a scoring input
    And an "experian.lookup.completed" event is emitted with ARN and lookup duration

  Scenario: Experian times out — 3 retries then refer-to-underwriter
    Given application "NEXT-20260617-000002" is in "Scoring" status
    And Experian API does not respond within 5 seconds on any of 3 attempts
    When the fallback logic triggers after the 3rd timeout
    Then the application status is set to "Referred"
    And the application is enqueued to the underwriter queue with reason "EXPERIAN_UNAVAILABLE"
    And an "experian.lookup.failed" event is emitted with ARN and failure reason

  Scenario: Experian returns error response — treat as failure
    Given application "NEXT-20260617-000003" is in "Scoring" status
    And Experian API returns HTTP 503
    When the Scoring Service processes the error response
    Then the retry logic is applied (up to 3 attempts)
    And if all 3 attempts return 503: application referred with "EXPERIAN_UNAVAILABLE"

  Scenario: Only minimum necessary PII transmitted to Experian
    Given an application with name, DOB, NI number, address, income, and loan details
    When the Scoring Service constructs the Experian request
    Then only name, DOB, and NI number are included in the Experian API call
    And income and loan amount are not transmitted to Experian
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Experian Integration Client | External Integration | New `experian_client.py` wrapping enterprise Experian API |
| Scoring Service | Worker | Extended to call Experian client before ML inference |
| Application Database | PostgreSQL | New column: `bureau_data_json` (JSONB, nullable) |
| Underwriter Queue | Message Queue | Receives fallback applications with `EXPERIAN_UNAVAILABLE` reason |
| Immutable Audit Store | Event log | Consumes `experian.lookup.completed` and `experian.lookup.failed` events |

### Data Impact

New column on `applications`: `bureau_data_json` (JSONB, nullable) — stores Experian response for audit.

PII minimisation: only `name`, `dob`, `ni_number` transmitted to Experian.

### API Impact

Experian API is external (enterprise contract). Use existing Experian enterprise endpoint as per ARCH-C-003. Do not use any alternative bureau.

## 7. Constraints

The coding agent must respect these constraints without exception:

- Use enterprise Experian API contract only — do not use Experian sandbox URL in production config (ARCH-C-003)
- PII minimisation: transmit only name, DOB, NI number to Experian — not income, loan amount, or address (BR-014)
- Timeout: 5 seconds per attempt, 3 retries with exponential backoff (BR-012)
- Fallback is mandatory — do not leave application in Scoring status after 3 failures (BR-013)
- Bureau data stored in UK Azure region only (ARCH-C-001)
- Audit events for both success and failure paths

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-002.2 — Scoring Result | Story | Yes | Experian data is a scoring input; F-002.2 must accept bureau data |
| Experian Enterprise API | External | Yes | Enterprise contract must be active and endpoint URL available |
| F-004 — Underwriter Queue | Story | No | Consumer of fallback referrals; can be stubbed |
| Immutable Audit Store | Platform | Yes | Must be available for audit events |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Implement `Experian Client` with timeout (5s), retry (3x exponential backoff), PII minimisation | Integration | Experian API | Unit test with mocked Experian: success, timeout, 503 error paths |
| T-002 | Integrate Experian client into Scoring Service: call before ML inference | Worker | T-001, F-002.2 | Integration test: bureau data passed as input to ML inference |
| T-003 | Implement fallback: after 3 failures set Referred status, enqueue with EXPERIAN_UNAVAILABLE | Worker | T-001 | Test: simulated 3 timeouts → Referred status + underwriter queue message |
| T-004 | Add `bureau_data_json` column; store Experian response (success path) | Database | none | Migration runs; column stores valid JSON |
| T-005 | Emit `experian.lookup.completed` and `experian.lookup.failed` audit events | Worker | T-001 | Both events appear in audit store with correct schema |

## 10. Test Expectations

- [ ] Unit: Experian client respects 5s timeout per attempt
- [ ] Unit: Experian client retries 3 times with exponential backoff before giving up
- [ ] Unit: PII minimisation — only name, DOB, NI in outbound request; no income or loan amount
- [ ] Unit: HTTP 503 from Experian treated as failure and retried
- [ ] Integration: successful Experian response → bureau data stored → passed to ML inference
- [ ] Integration: 3 Experian timeouts → application status Referred + underwriter queue message
- [ ] Audit: experian.lookup.completed event schema correct (ARN, duration, source)
- [ ] Audit: experian.lookup.failed event schema correct (ARN, failure reason, attempt count)
- [ ] Security: Experian API key not logged or exposed in error messages

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-006) are implemented and verifiable
- [ ] All BDD scenarios are covered by automated tests
- [ ] PII minimisation verified by reviewing outbound Experian request schema
- [ ] Fallback path tested with simulated Experian outage
- [ ] Traceability matrix updated: FR-009 → F-002.3
- [ ] All architecture constraints (ARCH-C-001, ARCH-C-003, ARCH-C-005) respected
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-002.3 — Experian Credit Lookup with Underwriter Fallback
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Implement Experian credit bureau integration for the NEXT13 scoring pipeline.
The Experian client is called before ML inference. It has a 5-second timeout per attempt,
3 retries with exponential backoff. On success: pass bureau data to ML inference.
On 3 failures: set application status to Referred, route to underwriter queue with
EXPERIAN_UNAVAILABLE reason, emit experian.lookup.failed audit event.

Files / components likely impacted:
- src/integrations/experian_client.py — new Experian API client
- src/workers/scoring_worker.py — extended to call Experian before ML inference
- src/db/migrations/YYYYMMDD_add_bureau_data_column.py — new bureau_data_json column
- src/events/schemas.py — ExperianLookupCompletedEvent, ExperianLookupFailedEvent
- tests/integrations/test_experian_client.py — new test file
- tests/workers/test_scoring_worker_experian.py — integration tests

Constraints (must not be violated):
- Use enterprise Experian API endpoint only — do not use sandbox URL in prod config (ARCH-C-003).
  Read endpoint from environment variable EXPERIAN_API_ENDPOINT.
- PII minimisation: only name, DOB, NI number in outbound Experian request.
  Do NOT include income, loan amount, address, or any other application fields (BR-014).
- Timeout: 5 seconds per attempt. Retry: 3 attempts with exponential backoff (1s, 2s, 4s).
- After 3 failures: set status = Referred, enqueue EXPERIAN_UNAVAILABLE, do NOT leave as Scoring.
- Store bureau response in bureau_data_json (JSONB) in UK Azure region only (ARCH-C-001).
- Experian API key must never appear in logs or error messages.

Expected implementation steps:
1. Experian Client: POST to EXPERIAN_API_ENDPOINT/credit-check with {name, dob, ni_number}.
   5s timeout, retry on timeout or 5xx with backoff: 1s, 2s, 4s.
2. On success: return bureau_data dict; emit experian.lookup.completed event.
3. On 3 failures: raise ExperianUnavailableError; emit experian.lookup.failed event.
4. In Scoring Worker, before ML inference:
   a. Call Experian Client.
   b. On success: store in bureau_data_json; pass to ML inference.
   c. On ExperianUnavailableError: set status = Referred; enqueue EXPERIAN_UNAVAILABLE; return.
5. Add bureau_data_json JSONB column (nullable).

Tests to add:
- Unit: Experian client retries 3 times on timeout; raises ExperianUnavailableError on 3rd
- Unit: Experian client retries on HTTP 503; passes on HTTP 200
- Unit: outbound request contains only name, dob, ni_number (assert no income/amount fields)
- Unit: Experian API key not in logged error messages
- Integration: Experian success → bureau data stored → passed to ML inference
- Integration: 3 Experian timeouts → application Referred + underwriter queue message

What NOT to change:
- ML Inference Service internals
- F-002.2 scoring thresholds
- Underwriter queue consumer (F-004 owns that)

Validation checklist before marking complete:
- [ ] 5-second timeout enforced per attempt
- [ ] 3 retries with exponential backoff before failure
- [ ] PII minimisation: no income or loan amount in Experian request
- [ ] Fallback: 3 failures → Referred status + EXPERIAN_UNAVAILABLE queue message
- [ ] bureau_data_json stored on success
- [ ] experian.lookup.completed and experian.lookup.failed events emitted
- [ ] API key not in logs
- [ ] All unit and integration tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
