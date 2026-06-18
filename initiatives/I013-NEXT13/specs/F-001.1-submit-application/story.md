# F-001.1 — Submit Online Application

## Metadata

| Field | Value |
|---|---|
| Story ID | F-001.1 |
| Epic | E-001 — Application Intake |
| Feature | F-001 — Online Application Submission |
| Priority | Must |
| Increment | D1 |
| AC references | AC-001 |
| FR references | FR-001, FR-004, FR-005 |

## 1. User Story

As an **Applicant**,
I want to submit an online personal loan application with all required personal, financial, and employment details,
so that my application is registered in the NEXT13 platform and I can progress to credit assessment.

### Business Goal

This story is the top-of-funnel intake step for the UK lending origination platform. Without it, no application enters the processing pipeline and no downstream scoring, compliance, or disbursement flows can execute.

### Scope

**In scope:**
- Submission of the application form with all required fields (name, DOB, NI number, UK address, income, requested amount and term)
- Server-side validation of all required fields
- Storage of a new application record with status `Submitted`
- Returning an Application Reference Number (ARN) to the applicant
- Confirmation screen shown to applicant after successful submission

**Out of scope:**
- Inline field validation (F-001.2)
- ARN generation service internals (F-001.3)
- AI scoring (F-002)
- AML/KYC checks (F-003)

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-001 | System shall accept online loan application submissions |
| Requirement | FR-004 | System shall capture all required applicant personal and financial data |
| Requirement | FR-005 | System shall store application with audit-ready status trail |
| Business Rule | BR-001 | Application must include a valid UK address (postcode format) |
| Business Rule | BR-002 | Applicant must be 18 or older at time of submission |
| Use Case | UC-001 | Submit Loan Application |
| Architecture Constraint | ARCH-C-001 | UK-only data residency for all PII and application data |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-001 | Application must include a valid UK address | UK postcode format must be validated server-side before acceptance |
| BR-002 | Applicant must be 18+ at time of submission | DOB must be validated; under-18 submissions must be rejected with clear error |
| BR-003 | Duplicate submissions within 30 minutes must be detected | Idempotency key required on POST; duplicate returns existing ARN |

## 4. Acceptance Criteria

### AC-001 — Successful submission returns ARN and Submitted status

**Given** an Applicant has completed all required fields (name, DOB, NI number, valid UK address, income, loan amount, term)
**When** the Applicant submits the application
**Then** the system accepts the application and returns HTTP 201
**And** the response body contains an Application Reference Number (ARN) in format `NEXT-YYYYMMDD-NNNNNN`
**And** the application is stored in the database with status `Submitted`
**And** the ARN is displayed to the Applicant on the confirmation screen

Traceability:
- Requirements: FR-001, FR-004
- Business Rules: BR-001, BR-002
- BDD Scenario: SCN-F001-001

### AC-002 — Missing required field is rejected before persistence

**Given** an Applicant has not provided the National Insurance Number
**When** the Applicant submits the application
**Then** the system returns HTTP 422
**And** the response body contains a field-level validation error for `national_insurance_number`
**And** no application record is created in the database

### AC-003 — Under-18 applicant is rejected

**Given** an Applicant has entered a date of birth that results in age less than 18
**When** the Applicant submits the application
**Then** the system returns HTTP 422
**And** the error message states the applicant does not meet the minimum age requirement
**And** no application record is created

## 5. BDD Scenarios

```gherkin
# F-001.1 — Submit Online Application
# AC-001 — Successful submission

Feature: Online loan application submission

  Scenario: Applicant submits valid application and receives ARN
    Given an Applicant has completed all required fields with valid UK data
    And the Applicant is 25 years old
    And the Applicant's UK postcode "SW1A 1AA" is valid
    When the Applicant submits the application
    Then the system returns HTTP 201
    And the response body contains an ARN matching the pattern "NEXT-\d{8}-\d{6}"
    And the application is stored with status "Submitted"
    And the confirmation screen displays the ARN to the Applicant

  Scenario: Submission rejected when National Insurance Number is missing
    Given an Applicant has completed all fields except National Insurance Number
    When the Applicant submits the application
    Then the system returns HTTP 422
    And the response body contains a field error for "national_insurance_number"
    And no application record is created in the database

  Scenario: Submission rejected when applicant is under 18
    Given an Applicant has entered a date of birth 16 years ago
    When the Applicant submits the application
    Then the system returns HTTP 422
    And the error message references the minimum age requirement
    And no application record is created in the database

  Scenario: Duplicate submission within 30 minutes returns existing ARN
    Given an Applicant has already submitted application "NEXT-20260617-000001" 10 minutes ago
    When the Applicant submits the same application again
    Then the system returns HTTP 200
    And the response body contains the existing ARN "NEXT-20260617-000001"
    And no duplicate application record is created
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Intake API | API Service | New `POST /v1/applications` endpoint |
| Application Database | PostgreSQL | New `applications` table with status enum |
| ARN Generator Service | Internal Service | Called by intake API; generates unique ARN (see F-001.3) |
| Applicant Portal | Frontend | Form submission flow and confirmation screen |
| Idempotency Store | Cache (Redis) | Stores submission hash → ARN for duplicate detection |

### Data Impact

New `applications` table:
- `id` (uuid, PK)
- `arn` (varchar, unique, immutable after creation)
- `applicant_id` (uuid, FK to applicants)
- `status` (enum: Draft, Submitted, Scoring, Compliant, Referred, Approved, Rejected, Disbursed)
- `payload_hash` (varchar, for idempotency)
- `submitted_at` (timestamptz)
- `created_at`, `updated_at` (timestamptz)

All data stored in UK Azure region only (ARCH-C-001).

### API Impact

`POST /v1/applications`
- Request: `ApplicationSubmitRequest` — name, dob, ni_number, address (UK postcode), income, requested_amount, term_months
- Response 201: `{ "arn": "NEXT-20260617-NNNNNN", "status": "Submitted" }`
- Response 422: `{ "errors": [{ "field": "national_insurance_number", "message": "..." }] }`
- Response 200 (duplicate): `{ "arn": "NEXT-20260617-000001", "status": "Submitted" }`

TLS 1.3 required (ARCH-C-002). OAuth2 token required in Authorization header.

## 7. Constraints

The coding agent must respect these constraints without exception:

- UK-only data residency: no PII (name, DOB, NI number, address) may leave UK Azure regions (ARCH-C-001)
- TLS 1.3 only on all transport; do not downgrade (ARCH-C-002)
- ARN must be globally unique and immutable once issued — no ARN field updates permitted
- Do not touch existing authentication or session management code
- Duplicate detection window is exactly 30 minutes — use Redis TTL
- Status enum must match exactly: `Draft`, `Submitted`, `Scoring`, `Compliant`, `Referred`, `Approved`, `Rejected`, `Disbursed`

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-001.3 — ARN Generation | Story | No | Intake API calls ARN generator; can be stubbed in parallel |
| Authentication service | Platform | Yes | OAuth2 token validation required before accepting submissions |
| UK Azure PostgreSQL instance | Infrastructure | Yes | Application DB must be provisioned in UK South region |
| Redis (idempotency store) | Infrastructure | No | Can be disabled in dev; required in staging/prod |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Create `applications` table migration with status enum | Database | infra: UK Postgres | Migration runs; table schema matches spec |
| T-002 | Implement `ApplicationSubmitRequest` schema with all required fields | API | none | Schema validates all required fields; rejects missing fields with 422 |
| T-003 | Implement `POST /v1/applications` endpoint: validate, call ARN generator, persist, return 201 | API | T-001, T-002, F-001.3 | API test: 201 on valid payload; 422 on missing NI |
| T-004 | Implement idempotency check: hash payload, check Redis, return existing ARN if found | API | T-003 | Test: duplicate submission within 30 min returns same ARN |
| T-005 | Implement age validation: reject if applicant is under 18 | API | T-002 | Test: DOB 16 years ago returns 422 with age error |
| T-006 | Add integration test: full submission flow — valid payload returns ARN with Submitted status | Test | T-003 | Integration test passes against test database |

## 10. Test Expectations

- [ ] Unit: NI number format validation accepts valid, rejects invalid formats
- [ ] Unit: UK postcode format validation (real postcode regex)
- [ ] Unit: Age validation — boundary cases (exactly 18, one day under 18)
- [ ] Unit: Idempotency hash generation is deterministic
- [ ] API: `POST /v1/applications` returns 201 with ARN for valid complete payload
- [ ] API: `POST /v1/applications` returns 422 with field error for missing NI number
- [ ] API: `POST /v1/applications` returns 422 for under-18 applicant
- [ ] API: Duplicate submission within 30 minutes returns 200 with existing ARN
- [ ] Integration: Full submission flow stores application in DB with status `Submitted`
- [ ] Security: Request without valid OAuth2 token returns 401
- [ ] Regression: Existing authentication endpoints must not be affected

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-001, AC-002, AC-003) are implemented and verifiable
- [ ] All BDD scenarios pass as automated tests
- [ ] No PII leaves UK Azure region (verified by architecture review sign-off)
- [ ] ARN uniqueness guaranteed under concurrent load
- [ ] Idempotency tested with Redis TTL expiry scenario
- [ ] Traceability matrix updated: FR-001, FR-004, FR-005 → F-001.1
- [ ] All architecture constraints (ARCH-C-001, ARCH-C-002) respected
- [ ] No blocking open questions remain
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-001.1 — Submit Online Application
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Implement the POST /v1/applications endpoint for the NEXT13 lending origination platform.
The endpoint accepts an online loan application, validates all required fields server-side,
checks for duplicate submissions (idempotency), generates a unique ARN via the ARN generator
service, stores the application with status "Submitted" in the UK-hosted PostgreSQL database,
and returns the ARN and status to the Applicant.

Files / components likely impacted:
- src/api/v1/applications/routes.py — new endpoint
- src/api/v1/applications/schemas.py — ApplicationSubmitRequest, ApplicationSubmitResponse
- src/api/v1/applications/validators.py — age, NI format, UK postcode validators
- src/services/arn_generator.py — call ARN generation service (see F-001.3)
- src/services/idempotency.py — Redis-backed duplicate detection (30-min TTL)
- src/db/migrations/YYYYMMDD_create_applications_table.py — new migration
- src/db/models/application.py — Application ORM model with status enum
- tests/api/test_submit_application.py — new test file

Constraints (must not be violated):
- All data (PII: name, DOB, NI number, address) must remain in UK Azure regions only.
  Do not add any external API calls that transmit PII outside UK (ARCH-C-001).
- TLS 1.3 only — do not add any configuration that permits lower TLS versions (ARCH-C-002).
- ARN is immutable once issued — do not allow any code path that updates the ARN field.
- Do not touch src/auth/ — authentication is out of scope for this story.
- Status enum values must match exactly: Draft, Submitted, Scoring, Compliant, Referred,
  Approved, Rejected, Disbursed — do not invent new status values.

Expected implementation steps:
1. Migration: applications table (id, arn, applicant_id, status, payload_hash, submitted_at,
   created_at, updated_at). Status enum must include all 8 values above.
2. Request schema: validate name, dob, ni_number (UK format), address (UK postcode),
   income (positive decimal), requested_amount (positive decimal), term_months (int 6–360).
3. Age check: compute age from dob; reject with 422 if under 18.
4. Idempotency: hash the request payload; check Redis for existing ARN with 30-min TTL.
   If found, return 200 with existing ARN. If not, continue.
5. Call ARN generator service — do not implement ARN generation inline (see F-001.3).
6. Persist application: status = Submitted, store payload_hash for idempotency.
7. Return 201 with ARN and status.
8. Return 422 with field-level errors for any validation failure.

Tests to add:
- Unit: ni_number validator accepts "AB 12 34 56 C", rejects "12345678", "not-a-ni"
- Unit: postcode validator accepts "SW1A 1AA", rejects "99999"
- Unit: age validator rejects DOB 16 years ago, accepts exactly 18
- Unit: idempotency hash is deterministic for same payload
- API: POST /v1/applications → 201 with ARN matching NEXT-\d{8}-\d{6}
- API: POST /v1/applications with missing ni_number → 422 with field error "national_insurance_number"
- API: POST /v1/applications with DOB 16 years ago → 422 with age error
- API: Duplicate submission within 30 min → 200 with same ARN
- Integration: full flow from submission to DB record with status "Submitted"

What NOT to change:
- src/auth/ — authentication is out of scope
- Existing applicant portal routes
- Any existing database migration files
- ARN generator internals (F-001.3 owns that)

Validation checklist before marking complete:
- [ ] POST /v1/applications returns 201 with ARN for valid payload
- [ ] POST /v1/applications returns 422 with field errors for missing NI
- [ ] POST /v1/applications returns 422 for under-18 applicant
- [ ] Duplicate submission within 30 min returns 200 with existing ARN
- [ ] Application record stored with status "Submitted"
- [ ] No PII logged or transmitted outside UK region
- [ ] All unit and integration tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
