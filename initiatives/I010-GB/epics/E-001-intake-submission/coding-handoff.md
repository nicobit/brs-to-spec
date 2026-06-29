# Coding Handoff - E-001 Intake & Submission

## 0 - Component and Repository Map
- Component: Intake API service — repo: platform/intake-service
- Audit store: platform/audit
- Mock adapters: test/mocks/scoring, test/mocks/email

## 1. Implementation Objective

Implement the Intake submission and status endpoints, persist applications, generate ARN, and publish `application.submitted` events so downstream scoring and audit consumers can operate.

## 2. Scope

In Scope:
- POST /api/intake/submit — validate, persist, return 201 with `arn`
- GET /api/intake/status — lookup application by `arn` and `dob`
- Publish `application.submitted` event on successful persist

Out of Scope:
- Email delivery implementation (mock adapter used in tests)

Constraints:
- PII handling per NFR-004; data residency UK-only

## 3. Data Model

See Implementation Contract below (inlined).

## 4. API Specification

```yaml
openapi: "3.0.3"
info:
  title: "Intake API"
  version: "1.0.0"
paths:
  /api/intake/submit:
    post:
      summary: "Submit application"
      operationId: "submitApplication"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - full_name
                - dob
                - ni_number
                - loan_amount
                - repayment_term_months
              properties:
                full_name:
                  type: string
                dob:
                  type: string
                  format: date
                ni_number:
                  type: string
                annual_income:
                  type: number
                loan_amount:
                  type: number
                repayment_term_months:
                  type: integer
      responses:
        "201":
          description: "Created"
          content:
            application/json:
              schema:
                type: object
                properties:
                  arn:
                    type: string
        "400":
          description: "Validation error"

  /api/intake/status:
    get:
      summary: "Lookup application status by ARN and DOB"
      operationId: "lookupStatus"
      parameters:
        - in: query
          name: arn
          required: true
          schema:
            type: string
        - in: query
          name: dob
          required: true
          schema:
            type: string
            format: date
      responses:
        "200":
          description: "Status returned"
          content:
            application/json:
              schema:
                type: object
                properties:
                  arn:
                    type: string
                  status:
                    type: string
                  last_update:
                    type: string
                    format: date-time
        "404":
          description: "Not found"
```

## 5. Inline Implementation Contract (from implementation-contract.md)

<!-- Implementation contract inlined -->

```
# Implementation Contract — E-001 Intake & Submission

## Data Entities

<!-- copied fields and API from existing implementation-contract.md -->

```
 (see implementation-contract.md content present in the repo)
```

## 6. Acceptance Criteria by Story

### S-001.2 - Intake API: submit application

```gherkin
Scenario: Valid submission returns ARN
  Given a valid application payload
  When POST /api/intake/submit is called
  Then respond 201 with JSON containing arn

Scenario: Invalid loan amount returns 400
  Given loan_amount = 500000 (above max)
  When POST /api/intake/submit is called
  Then respond 400 with validation error for loan_amount

Scenario: Event published after successful persist
  Given a successful persist
  When the handler completes
  Then an application.submitted event is published containing arn

Scenario: Missing required field returns 400
  Given a payload missing ni_number
  When POST /api/intake/submit is called
  Then respond 400 with validation error for ni_number
```

### S-001.0 - Intake end-to-end POC (spike)

```gherkin
Scenario: Successful application submission returns ARN
  Given the applicant completes the application form with valid values
  When they submit the form to POST /api/intake/submit
  Then the API responds 201 with JSON containing an "arn"
```

### S-001.1 - Confirmation email POC

```gherkin
Scenario: Confirmation email is queued and sent
  Given an application.submitted event with valid arn
  When the email worker processes the event
  Then an email is enqueued to the mock provider containing the arn and applicant email
```

## 7. Test Requirements

- Unit: validation, ARN generation
- Integration: persistence + event publication, mock consumer
- E2E: POC with mocks

## 8. Definition of Done

- All AC satisfied and automated tests implemented
- API contract implemented and contract tests pass
- Events produced match schema and are consumed by mocks

*This file is the self-contained coding handoff for E-001. Implement from this document alone.*
