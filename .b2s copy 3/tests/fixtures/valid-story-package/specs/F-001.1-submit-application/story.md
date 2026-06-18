# F-001.1 — Submit Application

## Metadata

| Field | Value |
| Story ID | F-001.1 |
| Feature | F-001 — Application Intake |
| Priority | Must |
| Increment | D1 |

## 1. User Story

As an **Applicant**,
I want to submit a loan application with all required personal and financial details,
so that my application is registered in the system and I receive an Application Reference Number.

### Business Goal

This story delivers the primary intake capability for the lending platform. Without it, no
application can enter the processing pipeline. Failure to implement this correctly means
applicants cannot start the origination journey.

### Scope

**In scope:**
- Submission of application form with required fields
- Server-side validation and ARN generation

**Out of scope:**
- Credit scoring — handled in F-002
- AML/KYC checks — handled in F-003

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-001 | System shall accept loan application submissions |
| Requirement | FR-002 | System shall validate all required fields before acceptance |
| Business Rule | BR-001 | Application must include valid UK address |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-001 | Application must include a valid UK address | Address field must be validated against UK postcode format |

## 4. Acceptance Criteria

### AC-001 — Successful submission generates ARN

**Given** an applicant has completed all required fields correctly
**When** the applicant submits the application
**Then** the system accepts the submission and returns an Application Reference Number
**And** the application is stored with status "Submitted"
**And** a confirmation message is displayed to the applicant

Traceability:
- Requirement: FR-001
- Business Rule: BR-001
- BDD Scenario: SCN-001

### AC-002 — Missing required field returns validation error

**Given** an applicant has not completed a required field
**When** the applicant attempts to submit
**Then** the submission is rejected with HTTP 422
**And** the response includes field-level validation messages

## 5. BDD Scenarios

# F-001.1
# AC-001
```gherkin
Scenario: Applicant submits valid application and receives ARN
  Given an applicant has completed all required fields with valid data
  And the applicant's UK address passes postcode validation
  When the applicant submits the application
  Then the system returns HTTP 201 with an Application Reference Number
  And the application is stored with status "Submitted"
  And a confirmation message is displayed to the applicant

Scenario: Applicant submission rejected for missing required field
  Given an applicant has left the National Insurance Number field empty
  When the applicant submits the application
  Then the system returns HTTP 422
  And the response body contains a field error for "national_insurance_number"
  And the application is not created in the system
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Intake API | API | New POST /applications endpoint |
| Application database | Database | New applications table with status field |
| ARN generator | Service | New service to generate unique reference numbers |
| Applicant portal | UI | Form submission and validation feedback |

### Data Impact

New `applications` table: id, arn, applicant_id, status (Submitted/Draft), created_at, updated_at.
ARN format: NEXT-YYYYMMDD-NNNNNN.

### API Impact

POST /applications — accepts application payload, returns 201 with ARN on success, 422 with
field errors on validation failure. Idempotency key required to prevent duplicate submissions.

## 7. Constraints

The coding agent must respect these constraints without exception:

- UK-only data residency: no PII may leave UK Azure regions (AR-001)
- All API endpoints must use TLS 1.3 (AR-002)
- ARN must be globally unique and immutable once issued
- Do not touch existing applicant authentication flow

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-001.2 Inline Validation | Story | No | Can be built in parallel |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Create applications table migration with status enum | Database | none | Migration runs without error; table exists with correct schema |
| T-002 | Implement ARN generator service returning NEXT-YYYYMMDD-NNNNNN | Service | T-001 | Unit test: 1000 generated ARNs are unique |
| T-003 | Implement POST /applications endpoint with payload validation | API | T-001, T-002 | API test: 201 on valid payload, 422 with field errors on invalid |
| T-004 | Add integration test: full submission flow returns ARN | Test | T-003 | Integration test passes against test database |

## 10. Test Expectations

- [ ] Unit tests — ARN uniqueness, postcode format validation
- [ ] Integration tests — full submission flow against test database
- [ ] API tests — 201 happy path, 422 with field errors, duplicate prevention
- [ ] Negative tests — missing required fields, invalid postcode, oversized payload
- [ ] Regression scope — existing applicant auth endpoints must not be affected

## 11. Definition of Done

This story is complete only when:
- [ ] all acceptance criteria are implemented and verifiable
- [ ] all BDD scenarios are covered by automated or documented manual tests
- [ ] traceability matrix is updated
- [ ] all architecture constraints are respected
- [ ] no blocking open questions remain
- [ ] regression risks are addressed
- [ ] coding prompt has been executed and reviewed

## 12. Coding-Agent Prompt

```
Story: F-001.1 — Submit Application

Goal:
Implement the POST /applications endpoint for the NEXT13 lending origination platform.
The endpoint accepts a loan application payload, validates all required fields, generates
a unique Application Reference Number (ARN), stores the application with status "Submitted",
and returns the ARN to the applicant.

Files / components likely impacted:
- src/api/applications/routes.py (new endpoint)
- src/api/applications/schemas.py (request/response schema)
- src/services/arn_generator.py (new service)
- src/db/migrations/ (new migration for applications table)
- tests/api/test_applications.py (new test file)

Constraints (must not be violated):
- All data must remain in UK Azure regions — do not add any external API calls that send PII outside UK
- TLS 1.3 only — do not downgrade transport security
- ARN must be globally unique and immutable once issued — do not allow updates to ARN field
- Do not touch src/auth/ — authentication is out of scope for this story

Expected implementation steps:
1. Create migration: applications table (id, arn, applicant_id, status, created_at, updated_at)
2. Implement ARN generator: format NEXT-YYYYMMDD-NNNNNN with collision check
3. Implement POST /applications: validate payload, call ARN generator, persist, return 201
4. Return 422 with field-level errors on validation failure
5. Add idempotency key support to prevent duplicate submissions

Tests to add or update:
- Unit: test ARN uniqueness (1000 generated ARNs must all be unique)
- Unit: test postcode validator rejects non-UK formats
- API: POST /applications returns 201 with ARN for valid payload
- API: POST /applications returns 422 with field errors for missing NI number
- Integration: full flow from submission to ARN retrieval

What NOT to change:
- src/auth/ — authentication is out of scope
- Existing applicant portal routes
- Any existing database migration files

Validation checklist before marking complete:
- [ ] POST /applications returns 201 with ARN for valid payload
- [ ] POST /applications returns 422 with field-level error messages for invalid payload
- [ ] ARN format matches NEXT-YYYYMMDD-NNNNNN
- [ ] All unit and integration tests pass
- [ ] No PII logged or transmitted outside UK region
```

---
*Status: Draft — set to Accepted only after human review.*
