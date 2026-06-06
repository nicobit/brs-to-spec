# Epics and Features

## 1. Business Objectives

### BO-001 — Improve onboarding control and auditability

Description:
Improve the control, traceability, and consistency of client onboarding requests.

Success measures:
- Onboarding requests are created with mandatory data.
- Only authorized users can create or approve requests.
- Status changes are auditable.

## 2. Epics

### EPIC-001 — Client Onboarding Workflow

Business objectives:
- BO-001

Description:
Support the creation, approval, rejection, and auditability of onboarding requests.

Business value:
Improves operational control and reduces manual follow-up.

In scope:
- Create onboarding requests
- Approve or reject requests
- Enforce role-based access
- Record audit events

Out of scope:
- Reporting dashboard
- External workflow integration

Related requirements:
- FR-001
- FR-002
- DATA-001
- SEC-001
- SEC-002
- AUD-001

## 3. Features / Capabilities

### FEAT-001 — Onboarding Request Creation

Parent epic:
- EPIC-001

Description:
Allow Relationship Managers to create onboarding requests with mandatory data.

Business value:
Starts the onboarding process in a controlled and validated way.

Related requirements:
- FR-001
- DATA-001
- SEC-001
- AUD-001

Candidate user stories:
- US-001 — Create onboarding request

### FEAT-002 — Compliance Approval

Parent epic:
- EPIC-001

Description:
Allow Compliance users to approve or reject onboarding requests.

Business value:
Ensures onboarding decisions are controlled by the right role.

Related requirements:
- FR-002
- SEC-002
- AUD-001

Candidate user stories:
- US-002 — Approve onboarding request
- US-003 — Reject onboarding request

## 4. Requirement-to-Feature Mapping

| Requirement ID | Requirement Title | Epic | Feature / Capability | Notes |
|---|---|---|---|---|
| FR-001 | Create onboarding request | EPIC-001 | FEAT-001 | Core creation flow |
| FR-002 | Approve or reject request | EPIC-001 | FEAT-002 | Compliance flow |
| DATA-001 | Mandatory onboarding fields | EPIC-001 | FEAT-001 | Required for creation |
| SEC-001 | Role-based creation | EPIC-001 | FEAT-001 | Authorization |
| SEC-002 | Role-based approval | EPIC-001 | FEAT-002 | Authorization |
| AUD-001 | Audit status changes | EPIC-001 | FEAT-001, FEAT-002 | Cross-cutting |

## 5. Delivery Slicing Recommendations

1. Implement request creation data model and validation.
2. Implement creation API and authorization.
3. Implement approval/rejection flow.
4. Add audit events.
5. Add UI and regression tests.

## 6. Open Questions

- Should new requests start as Draft or Submitted?
- Which exact fields must be present in audit events?
