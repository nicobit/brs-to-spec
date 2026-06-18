# F-001.3 — ARN Generation Service

## Metadata

| Field | Value |
|---|---|
| Story ID | F-001.3 |
| Epic | E-001 — Application Intake |
| Feature | F-001 — Online Application Submission |
| Priority | Must |
| Increment | D1 |
| AC references | AC-003 |
| FR references | FR-003 |

## 1. User Story

As the **System**,
I want to generate a unique Application Reference Number (ARN) on every accepted submission,
so that every application is traceable through scoring, compliance, underwriter, and disbursement stages.

### Business Goal

The ARN is the cross-system correlation key for the entire NEXT13 lending origination lifecycle. It appears in audit logs, underwriter dashboards, Temenos T24 disbursement records, and Applicant correspondence. Collision or predictability in ARN generation would break traceability and create regulatory audit risk.

### Scope

**In scope:**
- ARN Generator Service: generates unique ARN in format `NEXT-YYYYMMDD-NNNNNN`
- Collision detection: check for existing ARN before returning
- ARN stored immutably on the application record (no update path)
- Service is called by the Intake API (F-001.1) synchronously

**Out of scope:**
- Application form submission (F-001.1)
- ARN display to Applicant (F-001.1 confirmation screen)
- ARN format changes — format is fixed for this increment

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-003 | System shall generate a unique Application Reference Number for each accepted submission |
| Business Rule | BR-005 | ARN must be globally unique and immutable once issued |
| Architecture Constraint | ARCH-C-004 | ARN must be included in all immutable audit log entries |
| Architecture Constraint | ARCH-C-001 | ARN generation must execute within UK Azure region |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-005 | ARN must be globally unique and immutable once issued | Collision check required; no ARN update path permitted |
| BR-006 | ARN format: NEXT-YYYYMMDD-NNNNNN (zero-padded 6-digit sequential per day) | ARN generator must implement this exact format |

## 4. Acceptance Criteria

### AC-003 — ARN generation produces unique, correctly formatted ARN

**Given** the Intake API calls the ARN Generator Service for an accepted application
**When** the ARN Generator creates a new ARN
**Then** the ARN matches format `NEXT-YYYYMMDD-NNNNNN` (e.g., `NEXT-20260617-000001`)
**And** the ARN is unique across all applications in the database
**And** the ARN is returned to the Intake API within 200ms

Traceability:
- Requirements: FR-003
- Business Rules: BR-005, BR-006
- BDD Scenario: SCN-F001-003

### AC-004 — Collision detection retries on conflict

**Given** an ARN collision occurs (duplicate in database)
**When** the ARN Generator detects the collision
**Then** the generator retries with the next sequence number
**And** the retry succeeds within 3 attempts
**And** the collision event is logged for monitoring

### AC-005 — ARN is immutable after issuance

**Given** an ARN has been issued and stored on an application record
**When** any code path attempts to update the ARN field
**Then** the update is rejected by the database constraint
**And** an error is logged

## 5. BDD Scenarios

```gherkin
# F-001.3 — ARN Generation Service
# AC-003 — ARN uniqueness and format

Feature: Application Reference Number generation

  Scenario: ARN generated in correct format
    Given the ARN Generator Service is called for a new application on date 2026-06-17
    When the service generates an ARN
    Then the ARN matches the pattern "NEXT-20260617-\d{6}"
    And the ARN is stored on the application record

  Scenario: 1000 concurrent ARN requests produce no duplicates
    Given the ARN Generator Service is running
    When 1000 simultaneous ARN generation requests are made
    Then all 1000 generated ARNs are unique
    And all ARNs match the pattern "NEXT-\d{8}-\d{6}"

  Scenario: ARN collision triggers retry with next sequence number
    Given a sequence collision occurs for "NEXT-20260617-000001"
    When the ARN Generator detects the collision
    Then the generator retries with "NEXT-20260617-000002"
    And the collision event is recorded in the application log

  Scenario: ARN field update is rejected by database constraint
    Given an application exists with ARN "NEXT-20260617-000001"
    When code attempts to update the ARN field to "NEXT-20260617-999999"
    Then the database rejects the update with a constraint violation
    And the original ARN "NEXT-20260617-000001" remains unchanged
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| ARN Generator Service | Internal Service | New `arn_generator.py` with format logic and collision check |
| Application Database | PostgreSQL | ARN column: unique constraint + immutability trigger |
| Application Audit Log | Immutable store | ARN included in every audit event (ARCH-C-004) |
| Daily Sequence Counter | Redis | Atomic counter per calendar day for NNNNNN part |

### Data Impact

`applications.arn` column:
- `VARCHAR(24)`, unique constraint, NOT NULL
- Database-level immutability: trigger rejects UPDATE on `arn` field after first INSERT
- Format: `NEXT-YYYYMMDD-NNNNNN` — 24 characters total

Daily sequence: Redis key `arn:seq:YYYYMMDD` — atomic INCR, 6-digit zero-padded, TTL = 48h.

### API Impact

ARN Generator is an internal service called synchronously by the Intake API. It has no public API surface.

## 7. Constraints

The coding agent must respect these constraints without exception:

- ARN is immutable once issued — implement database trigger or application-level guard to prevent updates
- ARN format is fixed: `NEXT-YYYYMMDD-NNNNNN` — do not change the format or add flexibility
- Daily sequence counter must be atomic — use Redis INCR (not a read-then-write pattern) to prevent races
- Service must return within 200ms — no external API calls in the generation path
- All generation must execute in UK Azure region (ARCH-C-001)
- Maximum 3 collision retries before raising a fatal error

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-001.1 — Submit Application | Story | No | Intake API calls this service; can be stubbed in F-001.1 development |
| Redis (daily sequence store) | Infrastructure | Yes | Must be provisioned in UK Azure region |
| UK Azure PostgreSQL | Infrastructure | Yes | ARN unique constraint added in F-001.1 migration |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Implement `ARNGenerator` class with format `NEXT-YYYYMMDD-NNNNNN` using Redis atomic INCR | Service | Redis | Unit test: format matches regex; 1000 calls produce unique ARNs |
| T-002 | Add collision detection: query DB for existing ARN; retry up to 3 times with incremented sequence | Service | T-001, DB | Test: simulated collision results in retry and different ARN |
| T-003 | Add immutability constraint to `applications.arn`: DB trigger or CHECK constraint | Database | F-001.1 T-001 | Test: attempted UPDATE on ARN field raises constraint violation |
| T-004 | Log collision events to application monitoring | Service | T-002 | Verify log entry appears on simulated collision |
| T-005 | Write performance test: 1000 concurrent ARN generations, assert all unique and p99 < 200ms | Test | T-001 | Performance test passes |

## 10. Test Expectations

- [ ] Unit: ARN format matches `NEXT-\d{8}-\d{6}` for today's date
- [ ] Unit: 1000 sequential ARN calls produce 1000 unique values
- [ ] Unit: ARN generation uses correct calendar date (not hardcoded)
- [ ] Unit: Collision detection retries and returns different ARN on conflict
- [ ] Unit: After 3 failed retries, service raises `ARNGenerationError`
- [ ] Database: UPDATE on `arn` column raises constraint violation
- [ ] Performance: 1000 concurrent requests → no duplicates, p99 < 200ms
- [ ] Integration: ARN generator called from Intake API returns valid ARN in response

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-003, AC-004, AC-005) are implemented and verifiable
- [ ] All BDD scenarios are covered by automated tests
- [ ] ARN uniqueness guaranteed under concurrent load (performance test passes)
- [ ] ARN immutability enforced at database level
- [ ] Traceability matrix updated: FR-003 → F-001.3
- [ ] All architecture constraints (ARCH-C-001, ARCH-C-004) respected
- [ ] No blocking open questions remain
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-001.3 — ARN Generation Service
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Implement the ARN Generator Service for the NEXT13 lending origination platform.
The service generates a globally unique Application Reference Number in the format
NEXT-YYYYMMDD-NNNNNN, enforces immutability at the database level, and handles
collisions gracefully. It is called synchronously by the Intake API (F-001.1).

Files / components likely impacted:
- src/services/arn_generator.py — new ARNGenerator class
- src/db/migrations/YYYYMMDD_add_arn_immutability_trigger.py — DB trigger/constraint
- src/db/models/application.py — ensure arn column has unique constraint
- tests/services/test_arn_generator.py — new test file
- tests/performance/test_arn_concurrent.py — concurrent load test

Constraints (must not be violated):
- ARN is immutable once issued — implement at database level (trigger or generated column).
  Do not rely solely on application-level guards.
- ARN format is exactly NEXT-YYYYMMDD-NNNNNN — do not generalise or make it configurable.
- Daily sequence counter must use Redis INCR (atomic) — do not use read-then-write pattern.
- Maximum 3 collision retries; raise ARNGenerationError on 4th failure.
- Service must return within 200ms — no external API calls allowed in generation path.
- All execution within UK Azure region (ARCH-C-001).

Expected implementation steps:
1. ARNGenerator.__init__: inject Redis client and DB session.
2. Implement _get_daily_sequence(date): Redis INCR on key "arn:seq:YYYYMMDD"; TTL = 48h.
3. Implement _format_arn(date, seq): return f"NEXT-{date:%Y%m%d}-{seq:06d}".
4. Implement generate(db_session): loop up to 3 retries:
   a. Get sequence from Redis.
   b. Format ARN.
   c. Check uniqueness in DB.
   d. If unique, return ARN. If not, retry.
   e. After 3 failures, raise ARNGenerationError and log.
5. Add DB trigger: BEFORE UPDATE ON applications FOR EACH ROW IF OLD.arn IS NOT NULL THEN RAISE EXCEPTION.
6. Log collision events to structured log with ARN candidate and retry count.

Tests to add:
- Unit: format produces "NEXT-20260617-000001" for date=2026-06-17, seq=1
- Unit: format uses zero-padded 6 digits (seq=1 → "000001", seq=999999 → "999999")
- Unit: 1000 sequential calls produce 1000 unique ARNs
- Unit: collision on 1st and 2nd try → success on 3rd
- Unit: 3 consecutive collisions → ARNGenerationError raised
- Database: UPDATE applications SET arn='NEW' WHERE id=X → constraint violation
- Performance: 1000 concurrent calls → 0 duplicates; p99 < 200ms

What NOT to change:
- Existing application model fields (except adding arn unique constraint if missing)
- Intake API routes (F-001.1 owns that)
- Redis configuration — use existing Redis client

Validation checklist before marking complete:
- [ ] ARN format matches NEXT-\d{8}-\d{6}
- [ ] 1000 concurrent ARN requests produce 0 duplicates
- [ ] p99 latency < 200ms under concurrent load
- [ ] ARN UPDATE rejected at database level
- [ ] Collision retry logs appear on simulated collision
- [ ] All unit and performance tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
