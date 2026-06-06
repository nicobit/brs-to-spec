# User Stories

## US-001 — Create onboarding request

Parent epic:
- EPIC-001 — Client Onboarding Workflow

Parent feature:
- FEAT-001 — Onboarding Request Creation

As a Relationship Manager,  
I want to create an onboarding request,  
so that the client onboarding process can start.

### Requirements Covered
- FR-001
- DATA-001
- SEC-001
- AUD-001

### Acceptance Criteria

#### AC-001 — Successful creation
Given I am a Relationship Manager  
And I enter all mandatory fields  
When I submit the request  
Then a new onboarding request is created  
And an audit event is recorded.

#### AC-002 — Missing mandatory fields
Given I am a Relationship Manager  
When I submit a request with missing mandatory fields  
Then validation errors are shown  
And the request is not created.

#### AC-003 — Unauthorized user
Given I am not a Relationship Manager  
When I try to create an onboarding request  
Then access is denied.
