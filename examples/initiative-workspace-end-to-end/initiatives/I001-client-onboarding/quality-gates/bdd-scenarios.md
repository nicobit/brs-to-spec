# BDD Scenarios

## D1 Submission

### Scenario BDD-01 - Successful guided onboarding submission

Given a verified customer
And the required identity and document fields are available
When the onboarding submission is sent
Then the onboarding request is created
And the submission is routed for review
And an auditable submission event is emitted

### Scenario BDD-02 - Unauthorized document upload rejected

Given a user without the required upload permission
When a protected onboarding document upload is attempted
Then the upload is rejected
And no onboarding submission is completed
And the rejection is logged through approved controls
