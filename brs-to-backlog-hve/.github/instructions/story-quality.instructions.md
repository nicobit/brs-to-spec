# Story Quality Instructions

A good user story must be:

- business-value oriented
- small enough to implement and test
- traceable to the BRS
- clear for developer and QA
- explicit about business rules and data
- explicit about UI/API/integration scope where relevant

## Required Story Format

Each story must include:

- Story ID
- Parent Epic ID
- Title
- User story statement
- Business context
- Preconditions
- Main flow
- Alternative flows
- Exception flows
- Business rules
- Data requirements
- UI requirements
- API/integration requirements
- Non-functional requirements
- Acceptance criteria in Given/When/Then format
- Dependencies
- Out of scope
- Source traceability
- Test notes

## Split Stories When

Split a story if it contains:

- multiple personas
- multiple independent business outcomes
- multiple systems with separate delivery paths
- unrelated UI and backend changes
- several complex business rules
- reporting plus transactional behavior
- too many acceptance criteria

## Avoid

Avoid vague stories such as:

- "Implement dashboard"
- "Manage customer data"
- "Create backend API"
- "Handle integration"
- "Improve performance"

Rewrite them around observable business outcomes.
