# Requirements

## 1. Business Objective

Allow Relationship Managers to create onboarding requests and Compliance users to approve or reject them.

## 2. Functional Requirements

### FR-001 — Create onboarding request
The system shall allow an authorized Relationship Manager to create an onboarding request.

Priority: Must

Acceptance criteria:
- Given a Relationship Manager enters all mandatory fields
  When the request is submitted
  Then the system creates a new onboarding request.

### FR-002 — Approve or reject onboarding request
The system shall allow a Compliance user to approve or reject an onboarding request.

Priority: Must

## 3. Data Requirements

### DATA-001 — Mandatory onboarding fields
The request must include client name, client type, booking location, and risk category.

## 4. Security Requirements

### SEC-001 — Role-based creation
Only users with Relationship Manager role can create onboarding requests.

### SEC-002 — Role-based approval
Only Compliance users can approve or reject onboarding requests.

## 5. Audit Requirements

### AUD-001 — Audit status changes
Every status change must be auditable.
