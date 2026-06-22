# E-001 — Application Intake and Submission

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-001 |
| Initiative ID | I011-N2 |
| Wave | Wave 1 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-21 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Enable applicants to submit personal loan applications online, validate inputs, assign a unique Application Reference Number (ARN), and confirm submission via email so applicants can track progress and the business can begin downstream decisioning.

---

## Scope

**In scope:**
- Online application form, client- and server-side validation, ARN assignment, email confirmation with ARN.

**Out of scope:**
- Offer generation, AI scoring, AML/KYC flows (handled in other epics).

---

## High-Level Acceptance Criteria

- AC-E-001: Applicants can submit a completed application and immediately receive an ARN and confirmation.
- AC-E-002: Incomplete or invalid applications are prevented from submission with clear inline errors.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | § Application Intake | Online submission and ARN assignment |
| Requirement | REQ-001 | Online Application Submission |
| Requirement | REQ-002 | Client-side and Server-side Validation |
| Requirement | REQ-003 | Email Confirmation with ARN |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Applicant Portal (Frontend) | New / Changed | Add intake form, client validation, UX messages |
| Loan Origination API (Backend) | New / Changed | Submission endpoint, validation, ARN generation |
| Notification Service | Integration | Send email confirmations with ARN |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| Notification Service | External | Yes | Email delivery must be available for confirmations |
| Identity verification (KYC) | Epic E-003 | No | Not required for initial submission but may be used later |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Email delivery delays causing applicant confusion | Medium | Medium | Provide in-UI acknowledgement and retry via background job; surface expected timeline |

---

## Foundation / Setup

No foundation setup required beyond existing Applicant Portal and Notification Service connectivity. Ensure feature flag for intake form to allow dark-launch.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| F-001.1 | Application Form & Validation | Frontend / Backend | Must | D1 | Ready |
| F-002.1 | ARN Assignment & Confirmation | Backend / Integration | Must | D1 | Ready |

---
*Status: Draft — set to Accepted only after epic review gate.*
