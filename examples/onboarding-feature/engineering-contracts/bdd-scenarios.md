# BDD Scenarios

## Feature: Onboarding Approval

### Scenario BDD-001 — Successful request creation

Related requirements:
- FR-001
- DATA-001
- AUD-001

Related user stories:
- US-001

Given a user has the Relationship Manager role  
And the user enters client name, client type, booking location, and risk category  
When the user submits the onboarding request  
Then the system creates the request  
And the system records an audit event.

### Scenario BDD-002 — Unauthorized request creation

Related requirements:
- SEC-001

Given a user does not have the Relationship Manager role  
When the user tries to create an onboarding request  
Then access is denied.
