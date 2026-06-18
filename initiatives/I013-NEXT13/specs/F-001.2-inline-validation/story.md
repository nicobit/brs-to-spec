# F-001.2 — Inline Field Validation

## Metadata

| Field | Value |
|---|---|
| Story ID | F-001.2 |
| Epic | E-001 — Application Intake |
| Feature | F-001 — Online Application Submission |
| Priority | Must |
| Increment | D1 |
| AC references | AC-002 |
| FR references | FR-002 |

## 1. User Story

As an **Applicant**,
I want inline field validation as I fill in the loan application form,
so that I cannot submit an incomplete or incorrectly formatted application and I receive immediate feedback to correct my entries.

### Business Goal

Inline validation prevents malformed applications from reaching the server, reduces server-side rejection rates, and improves Applicant completion rates. It is also the first line of defence against obviously invalid data (non-UK postcodes, future DOBs, non-numeric income).

### Scope

**In scope:**
- Client-side field validation for all required application form fields
- Real-time error messages displayed adjacent to each field on blur
- Submission button disabled until all required fields pass client-side validation
- Client-side validation mirrors server-side rules (format only — not business eligibility)

**Out of scope:**
- Server-side validation (F-001.1)
- Age eligibility check (enforced server-side in F-001.1)
- Duplicate detection (F-001.1)
- Any network call during validation

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-002 | System shall validate all required fields before acceptance |
| Business Rule | BR-001 | Application must include a valid UK address (postcode format) |
| Use Case | UC-001 | Submit Loan Application — inline validation step |
| Architecture Constraint | ARCH-C-001 | No PII transmitted during validation; all checks are client-side |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-001 | Application must include a valid UK address | UK postcode regex validated client-side on blur |
| BR-004 | NI number must match UK format (e.g., AB123456C) | NI field must validate format client-side |

## 4. Acceptance Criteria

### AC-002 — Required field validation prevents submission

**Given** an Applicant is on the application form
**When** the Applicant leaves a required field blank and moves to the next field
**Then** an inline error message appears immediately below the blank field
**And** the Submit button remains disabled until all required fields are valid
**And** the error message is descriptive (not just "required")

Traceability:
- Requirements: FR-002
- Business Rules: BR-001, BR-004
- BDD Scenario: SCN-F001-002

### AC-003 — Invalid postcode format shows specific error

**Given** an Applicant has entered "99999" in the postcode field
**When** the Applicant moves focus away from the postcode field
**Then** an inline error message states "Please enter a valid UK postcode"
**And** the field is visually highlighted as invalid

### AC-004 — Invalid NI number format shows specific error

**Given** an Applicant has entered "12345678" in the NI number field
**When** the Applicant moves focus away from the NI field
**Then** an inline error message states "Please enter a valid National Insurance number (e.g., AB 12 34 56 C)"

## 5. BDD Scenarios

```gherkin
# F-001.2 — Inline Field Validation
# AC-002 — Required field prevents submission

Feature: Inline field validation on loan application form

  Scenario: Submit button disabled while required field is blank
    Given an Applicant is filling in the loan application form
    And the Applicant has completed all fields except the National Insurance Number
    When the Applicant views the form
    Then the Submit button is disabled
    And the National Insurance Number field displays no error yet

  Scenario: Inline error appears on blur for blank required field
    Given an Applicant has left the National Insurance Number field blank
    When the Applicant moves focus to the next field
    Then an error message "National Insurance Number is required" appears below the NI field
    And the Submit button remains disabled

  Scenario: Invalid UK postcode shows format error on blur
    Given an Applicant has entered "99999" in the postcode field
    When the Applicant moves focus away from the postcode field
    Then an error message "Please enter a valid UK postcode" appears below the postcode field
    And the field is visually highlighted with an error border

  Scenario: Invalid NI number format shows specific error on blur
    Given an Applicant has entered "12345678" in the NI number field
    When the Applicant moves focus away from the NI field
    Then an error message "Please enter a valid National Insurance number (e.g., AB 12 34 56 C)" appears
    And the field is visually highlighted with an error border

  Scenario: All fields valid enables Submit button
    Given an Applicant has correctly completed all required fields
    When the Applicant fills in the last field with a valid value
    Then the Submit button becomes enabled
    And no error messages are displayed
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Applicant Portal | Frontend (React/Vue) | Add field-level validation logic and error rendering |
| Validation Utilities | Frontend JS module | New `validators.js` with UK postcode and NI regex functions |
| Application Form Component | Frontend | Blur event handlers, error state per field, submit button state |

### Data Impact

No data is stored or transmitted during inline validation. All validation is purely client-side.

### API Impact

None — inline validation does not make any API calls.

## 7. Constraints

The coding agent must respect these constraints without exception:

- No API calls during inline validation — all checks must be client-side only
- Do not transmit NI number, DOB, or any PII during the validation phase (ARCH-C-001)
- Validation rules must mirror server-side rules exactly; no relaxed client-side rules
- Do not rewrite or replace existing form components — extend them with validation logic
- Error messages must be user-friendly and specific; do not use generic "Invalid" messages

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-001.1 — Submit Application | Story | No | Can be built in parallel; both use same validation rules |
| Applicant Portal UI framework | Frontend | Yes | Validation hooks depend on existing form framework |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Implement `validators.js` with UK postcode regex and NI format regex | Frontend | none | Unit test: 10 valid postcodes pass; 10 invalid fail |
| T-002 | Add blur event handlers to all required fields with error state management | Frontend | T-001 | Manual test: error appears on blur for blank field |
| T-003 | Implement submit button disabled logic: enabled only when all fields pass | Frontend | T-002 | Test: button disabled with one invalid field; enabled with all valid |
| T-004 | Add visual error styling (border highlight + error message below field) | Frontend | T-002 | Visual review: error state clearly distinguished from valid state |
| T-005 | Write unit tests for validators (postcode, NI, required, income range) | Test | T-001 | 100% branch coverage on validators.js |

## 10. Test Expectations

- [ ] Unit: UK postcode validator accepts "SW1A 1AA", "M1 1AE"; rejects "99999", "INVALID"
- [ ] Unit: NI validator accepts "AB 12 34 56 C", "AB123456C"; rejects "12345678", ""
- [ ] Unit: Required field validator rejects empty string and whitespace-only
- [ ] Unit: Income validator rejects negative and zero values
- [ ] UI: Submit button disabled when any required field is blank
- [ ] UI: Inline error appears on blur for blank required field
- [ ] UI: Inline error appears on blur for invalid postcode
- [ ] UI: Inline error appears on blur for invalid NI format
- [ ] UI: All errors clear when field is corrected
- [ ] Regression: Existing portal pages unaffected by new validators

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-002, AC-003, AC-004) are implemented and verifiable
- [ ] All BDD scenarios are covered by automated or documented manual tests
- [ ] No PII is transmitted during validation (confirmed by network inspection)
- [ ] Validation rules match server-side rules exactly (cross-checked with F-001.1)
- [ ] Submit button state is correct under all field combinations
- [ ] Traceability matrix updated: FR-002 → F-001.2
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-001.2 — Inline Field Validation
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Add inline client-side field validation to the NEXT13 loan application form. All validation
must be purely client-side (no API calls). Display field-level error messages on blur.
Disable the Submit button until all required fields pass validation. Validation rules
must exactly match the server-side rules implemented in F-001.1.

Files / components likely impacted:
- src/portal/validators.js — new validation utility module
- src/portal/components/ApplicationForm.vue (or .tsx) — add blur handlers and error state
- src/portal/components/FormField.vue (or .tsx) — add error display slot
- tests/portal/validators.test.js — unit tests for validators
- tests/portal/ApplicationForm.test.js — component tests for validation behaviour

Constraints (must not be violated):
- No API calls during validation — all checks must be purely client-side.
- Do not transmit NI number, DOB, or any PII in a network request during validation (ARCH-C-001).
- Do not rewrite or replace existing form components — add validation logic to them.
- Validation regex for UK postcode and NI number must match exactly what is implemented
  server-side in F-001.1 validators.py.
- Error messages must be specific and user-friendly (not generic "Invalid").

Expected implementation steps:
1. Create validators.js with:
   - isValidUKPostcode(value): regex-based UK postcode validator
   - isValidNINumber(value): accepts "AB 12 34 56 C" and "AB123456C" formats
   - isRequired(value): rejects empty string and whitespace
   - isPositiveDecimal(value): rejects zero, negative, and non-numeric
   - isValidTermMonths(value): accepts integer 6–360
2. Add blur event handlers to each required field in ApplicationForm.
3. Track per-field error state: errorMessages: { [fieldName]: string | null }
4. Display error message below each field when errorMessages[fieldName] is set.
5. Compute formIsValid: all required fields have no error and are non-empty.
6. Bind Submit button disabled attribute to !formIsValid.

Tests to add:
- Unit validators.test.js:
  - isValidUKPostcode: pass for "SW1A 1AA", "M1 1AE"; fail for "99999", "INVALID", ""
  - isValidNINumber: pass for "AB 12 34 56 C"; fail for "12345678", "", "not-a-ni"
  - isRequired: fail for "", "   "; pass for "a"
- Component ApplicationForm.test.js:
  - Submit button disabled when NI field is blank
  - Error message appears after blur on blank NI field
  - Error message clears after valid NI entered
  - Submit button enabled when all fields valid

What NOT to change:
- Existing portal routes and navigation
- Server-side validation in src/api/
- Authentication or session management
- Any existing form component not related to the application form

Validation checklist before marking complete:
- [ ] Inline error appears on blur for each required field when blank
- [ ] Inline error appears for invalid UK postcode format
- [ ] Inline error appears for invalid NI number format
- [ ] Submit button disabled when any required field is blank or invalid
- [ ] Submit button enabled when all required fields are valid
- [ ] No network requests made during validation
- [ ] All unit and component tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
