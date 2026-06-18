# F-002.1 — AI Pre-Screening Trigger

## Metadata

| Field | Value |
|---|---|
| Story ID | F-002.1 |
| Epic | E-002 — Decisioning and Scoring |
| Feature | F-002 — AI Scoring Pipeline |
| Priority | Must |
| Increment | D1 |
| AC references | AC-004 |
| FR references | FR-006 |

## 1. User Story

As the **System**,
I want to trigger AI pre-screening within 60 seconds of a successful application submission,
so that scoring starts promptly and applicants are not left waiting for a decision.

### Business Goal

Regulatory and competitive requirements demand rapid decisioning. Triggering AI pre-screening within 60 seconds of submission minimises time-to-decision and satisfies FCA expectations for transparent, timely credit assessment. Late scoring triggers would degrade Applicant experience and increase manual referral rates.

### Scope

**In scope:**
- Detecting a new `Submitted` application via event (or polling fallback)
- Updating application status from `Submitted` to `Scoring`
- Enqueuing the application for the AI Scoring Service (F-002.2)
- Emitting a structured `scoring.triggered` event to the audit log
- SLA: trigger must occur within 60 seconds of submission

**Out of scope:**
- Producing the actual score (F-002.2)
- Experian credit lookup (F-002.3)
- AML/KYC screening (F-003)

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-006 | System shall trigger AI pre-screening within 60s of application submission |
| Architecture Constraint | ARCH-C-002 | Scoring must tolerate external-latency spikes via staging queue with time-bounded retries |
| Architecture Constraint | ARCH-C-004 | Immutable audit log must capture scoring.triggered event with ARN and timestamp |
| Architecture Constraint | ARCH-C-001 | All processing in UK Azure region |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-007 | AI pre-screening must be triggered within 60 seconds of submission | SLA enforcement: monitor trigger latency; alert if > 60s |
| BR-008 | Application status must transition atomically from Submitted to Scoring | Status update must be transactional with queue enqueue |

## 4. Acceptance Criteria

### AC-004 — Pre-screening triggered within 60 seconds of submission

**Given** an application has been submitted and stored with status `Submitted`
**When** 60 seconds have elapsed since submission
**Then** the application status has changed to `Scoring`
**And** a `scoring.triggered` event has been emitted to the audit log with ARN and timestamp
**And** the application has been enqueued in the AI Scoring Service queue

Traceability:
- Requirements: FR-006
- Business Rules: BR-007, BR-008
- BDD Scenario: SCN-F002-001

### AC-005 — Status transition is atomic with queue enqueue

**Given** the pre-screening trigger updates application status to `Scoring`
**When** the queue enqueue fails
**Then** the status update is rolled back (application remains `Submitted`)
**And** the failure is logged and the trigger is retried

## 5. BDD Scenarios

```gherkin
# F-002.1 — AI Pre-Screening Trigger
# AC-004 — Trigger within 60s

Feature: AI pre-screening trigger on application submission

  Scenario: Pre-screening triggered within 60 seconds of submission
    Given an application "NEXT-20260617-000001" was submitted 30 seconds ago with status "Submitted"
    When the pre-screening trigger service processes the application
    Then the application status changes to "Scoring"
    And a "scoring.triggered" event is emitted to the audit log containing the ARN and timestamp
    And the application is enqueued in the AI Scoring Service queue

  Scenario: Pre-screening SLA breach is logged as alert
    Given an application "NEXT-20260617-000002" has been in "Submitted" status for 90 seconds
    When the pre-screening trigger service checks the queue
    Then an alert event "scoring.trigger.sla_breach" is emitted
    And the application is still enqueued for processing

  Scenario: Queue enqueue failure rolls back status change
    Given an application "NEXT-20260617-000003" is in "Submitted" status
    And the AI Scoring Service queue is unavailable
    When the pre-screening trigger attempts to enqueue the application
    Then the application status remains "Submitted"
    And an error event "scoring.trigger.enqueue_failed" is emitted
    And the trigger is scheduled for retry

  Scenario: Authorization check — only System role can trigger pre-screening
    Given a request to trigger pre-screening arrives with an Applicant token
    When the trigger service checks the caller's role
    Then the request is rejected with HTTP 403
    And no status change occurs
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Pre-Screening Trigger Service | Worker / Event Consumer | New worker that listens for `application.submitted` events |
| AI Scoring Service Queue | Message Queue (Azure Service Bus) | New queue: `scoring-requests` |
| Application Database | PostgreSQL | Status transition: Submitted → Scoring (with transaction) |
| Immutable Audit Store | Event log | Consumes `scoring.triggered` structured event |
| Observability / Alerting | Metrics | New metric: `scoring_trigger_latency_seconds` |

### Data Impact

`applications.status` transitions: `Submitted` → `Scoring` (atomic with queue enqueue).

New structured event schema:
```json
{
  "event": "scoring.triggered",
  "arn": "NEXT-20260617-000001",
  "timestamp": "2026-06-17T10:00:30Z",
  "trigger_latency_seconds": 30,
  "actor": "system"
}
```

### API Impact

No public API surface change. Pre-screening trigger is an internal worker.

## 7. Constraints

The coding agent must respect these constraints without exception:

- Status transition `Submitted → Scoring` must be atomic with queue enqueue — use a transaction that wraps both operations
- SLA is 60 seconds — instrument `scoring_trigger_latency_seconds` metric; alert threshold at 60s
- Do not call Experian or any external scoring service in this story (that is F-002.3)
- All processing in UK Azure region (ARCH-C-001)
- Audit event must be emitted before function returns — do not fire-and-forget the audit log write
- Do not accept non-System role callers

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-001.1 — Submit Application | Story | Yes | Relies on `application.submitted` event or Submitted status in DB |
| Azure Service Bus (scoring-requests queue) | Infrastructure | Yes | Must be provisioned before this story can be tested end-to-end |
| F-002.2 — Scoring Result | Story | No | Consumer of the queue; can be stubbed |
| Immutable Audit Store | Platform | Yes | Must be available for event emission |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Implement pre-screening trigger worker that listens for `application.submitted` events | Worker | F-001.1 | Worker picks up submitted applications within test harness |
| T-002 | Implement atomic status transition Submitted → Scoring with queue enqueue in single transaction | Worker | T-001, Azure SB | Test: queue failure rolls back status change |
| T-003 | Emit `scoring.triggered` structured event to immutable audit store | Worker | T-002 | Test: audit event contains ARN, timestamp, trigger_latency_seconds |
| T-004 | Instrument `scoring_trigger_latency_seconds` metric; alert when > 60s | Observability | T-001 | Metric appears in observability dashboard; test alert fires at 90s |
| T-005 | Add integration test: submit application → verify status = Scoring within 60s | Test | T-001, T-002 | Integration test passes under normal conditions |

## 10. Test Expectations

- [ ] Unit: status transition is rolled back when queue enqueue throws
- [ ] Unit: `scoring.triggered` event schema is valid (contains ARN, timestamp, latency)
- [ ] Unit: SLA breach event fires when latency > 60s
- [ ] Unit: non-System caller is rejected with 403
- [ ] Integration: submit application → status = Scoring within 60s
- [ ] Integration: queue unavailable → status remains Submitted; retry scheduled
- [ ] Observability: `scoring_trigger_latency_seconds` metric recorded on each trigger

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-004, AC-005) are implemented and verifiable
- [ ] All BDD scenarios are covered by automated tests
- [ ] Status transition atomicity proven by failure injection test
- [ ] SLA metric instrumented and alert configured
- [ ] Audit event schema validated against immutable audit store contract
- [ ] Traceability matrix updated: FR-006 → F-002.1
- [ ] All architecture constraints (ARCH-C-001, ARCH-C-002, ARCH-C-004) respected
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-002.1 — AI Pre-Screening Trigger
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Implement the pre-screening trigger worker for the NEXT13 lending origination platform.
The worker listens for application.submitted events (or polls for Submitted applications),
atomically updates status to Scoring while enqueuing the application to the AI Scoring
Service queue, emits a scoring.triggered audit event, and instruments SLA latency.

Files / components likely impacted:
- src/workers/prescreening_trigger.py — new worker class
- src/services/scoring_queue.py — Azure Service Bus client wrapper for scoring-requests queue
- src/db/models/application.py — status transition helper
- src/events/schemas.py — ScoringTriggeredEvent schema
- src/observability/metrics.py — scoring_trigger_latency_seconds metric
- tests/workers/test_prescreening_trigger.py — new test file

Constraints (must not be violated):
- Status transition Submitted → Scoring must be atomic with queue enqueue.
  Wrap both operations in a single database transaction; roll back if queue enqueue fails.
- SLA is 60 seconds — emit scoring.trigger.sla_breach event if latency > 60s.
- Do not call Experian, HMRC, or any external service in this story.
- All processing in UK Azure region (ARCH-C-001).
- Audit event must be durably written before the worker ack's the message.
- Reject non-System role callers with 403 if a direct API trigger path exists.

Expected implementation steps:
1. Worker listens on Azure Service Bus topic "application.submitted" (or polls DB for
   Submitted applications older than 5 seconds and younger than 60 seconds).
2. For each application:
   a. Compute trigger_latency = now() - submitted_at.
   b. If latency > 60s: emit scoring.trigger.sla_breach event; continue processing.
   c. Begin transaction: UPDATE applications SET status='Scoring'; enqueue to scoring-requests.
   d. If enqueue fails: rollback; emit scoring.trigger.enqueue_failed; schedule retry.
   e. Emit scoring.triggered event: {event, arn, timestamp, trigger_latency_seconds, actor: "system"}.
   f. Commit transaction.
3. Record scoring_trigger_latency_seconds metric on each successful trigger.

Tests to add:
- Unit: enqueue failure → status rollback → status remains Submitted
- Unit: scoring.triggered event contains correct ARN, timestamp, latency
- Unit: SLA breach event fires when latency > 60s
- Unit: non-System token rejected with 403
- Integration: application submitted → status = Scoring within 60s
- Integration: queue unavailable → status unchanged; retry scheduled

What NOT to change:
- F-002.2 scoring logic — this story only triggers, does not score
- Application model fields other than status
- Existing event schemas

Validation checklist before marking complete:
- [ ] Status transition atomic: queue failure rolls back status
- [ ] scoring.triggered event emitted with correct schema
- [ ] SLA metric recorded on each trigger
- [ ] SLA breach event fires at > 60s
- [ ] Integration test: submission → Scoring status within 60s
- [ ] All unit and integration tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
