# Skill: Acceptance Criteria

Use this skill to create clear, testable acceptance criteria.

## Format

Use Given/When/Then.

```gherkin
Given [precondition]
When [action/event]
Then [expected result]
```

## Include Positive, Negative, and Boundary Scenarios

For each story, consider:

- happy path
- validation errors
- authorization errors
- missing data
- invalid state transitions
- integration failure
- duplicate submission
- audit/logging expectation
- notification expectation
- performance expectation if relevant

## Good Acceptance Criteria

Good criteria are:

- observable
- testable
- specific
- linked to business rules
- not implementation-only

## Weak Acceptance Criteria

Avoid:

- "The system works correctly"
- "Data is handled"
- "Performance is good"
- "User can manage records"
- "API is implemented"

## Example

```gherkin
Given a client advisor has entered all mandatory onboarding data
When the advisor submits the onboarding request
Then the system creates the request with status "Submitted"
And the request is visible to the compliance reviewer
And an audit record is created for the submission event
```
