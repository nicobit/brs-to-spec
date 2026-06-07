# BDD Scenarios — Example

## Active Deliverable

D1 — Create onboarding request

### SCN-001 — Create onboarding request successfully

```gherkin
Given an authorized user
And all mandatory onboarding fields are provided
When the user submits the onboarding request
Then the request is created
And an audit event is emitted
```

### SCN-002 — Reject request with missing mandatory fields

```gherkin
Given an authorized user
And a mandatory onboarding field is missing
When the user submits the onboarding request
Then the request is rejected
And validation errors are shown
```
