# Domain Model

## 1. Ubiquitous Language

| Term | Definition | Source |
|---|---|---|
| Onboarding Request | Request to onboard a client | BRS |
| Approval Decision | Compliance decision to approve or reject | BRS |
| Onboarding Status | Current lifecycle status of the request | Architecture alignment |

## 2. Bounded Context

Client Onboarding

## 3. Entities

- OnboardingRequest

## 7. Domain Events

- OnboardingRequestCreated
- OnboardingRequestApproved
- OnboardingRequestRejected

## 9. Business Invariants

- Only valid roles can approve or reject.
- Status changes must be audited.
