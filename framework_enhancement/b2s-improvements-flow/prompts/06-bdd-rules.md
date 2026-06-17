# Prompt 6 — Make BDD Mandatory Where It Matters

Improve the `.b2s` BDD generation rules.

Current problem:

BDD exists in the framework, but it is currently too conditional. For enterprise delivery, BDD should be a default output for business-facing stories in Standard and Full Governance mode.

Update the framework as follows:

## BDD Rules

Compact mode:

- BDD is optional.
- BDD is required only when the readiness check identifies complex behavior.

Standard mode:

- BDD is mandatory for every business-facing story.
- Each story must have at least:
  - one happy path scenario
  - one negative or validation scenario

Full Governance mode:

- BDD is mandatory and traceable.
- Each story must include applicable scenarios from:
  - happy path
  - negative path
  - validation
  - authorization/permission
  - business rule
  - state transition
  - integration failure
  - audit/compliance
  - edge case

## BDD Quality Rules

Each BDD scenario must:

- be written in valid Gherkin
- describe observable behavior
- avoid implementation details
- link to acceptance criteria
- link to business rules where applicable
- link to story ID
- avoid generic statements

Bad scenario example:

```gherkin
Scenario: Implement feature
  Given the developer writes code
  When the code is complete
  Then the feature works
```

Good scenario example:

```gherkin
Scenario: Reject submission for ineligible customer
  Given an operations user has completed a subscription request
  And the selected customer is marked as ineligible
  When the user submits the request
  Then the submission is rejected
  And the request remains in Draft status
  And the user sees the reason "Customer is not eligible"
  And no approval workflow is started
```

Update the readiness check so BDD is not only a gate but part of the standard story package generation.
