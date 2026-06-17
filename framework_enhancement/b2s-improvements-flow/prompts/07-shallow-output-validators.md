# Prompt 7 — Improve Validators Against Shallow Output

Improve `.b2s` validation so that it detects shallow delivery output.

Current problem:

The framework may validate that sections, IDs, and tables exist, but content can still be generic or too shallow.

Add semantic quality checks for Epic, Feature, Story, Acceptance Criteria, BDD, Tasks, and Coding Prompt artifacts.

## Story Quality Validation

Fail or warn if:

- story title is generic, such as "Story 1" or "Implement feature"
- actor is missing or generic
- business outcome is missing
- story has no linked requirement
- story has no linked business rule when business rules exist
- story has no acceptance criteria
- acceptance criteria are not testable
- implementation context is empty
- impacted components are missing
- constraints are missing
- definition of done is generic
- coding prompt does not mention tests
- coding prompt does not mention what not to change

## Acceptance Criteria Validation

Fail or warn if:

- AC is written as a vague statement
- AC cannot be tested
- AC has no link to story
- AC has no link to BDD scenario in Standard or Full Governance mode
- AC says only "system works", "user can use feature", or similar generic content

## BDD Validation

Fail or warn if:

- scenario is not valid Given/When/Then
- scenario describes developer activity instead of business behavior
- scenario has no observable outcome
- scenario has no negative path when required
- scenario has no authorization scenario when roles/permissions are present
- scenario has no audit scenario when audit/compliance is present
- scenario is duplicated across stories

## Task Validation

Fail or warn if:

- task says only "implement backend", "update UI", "write tests"
- task has no target area
- task has no validation expectation
- task has no dependency information
- task is too large and should be split

## Coding Prompt Validation

Fail or warn if:

- prompt is generic
- prompt does not include story goal
- prompt does not include constraints
- prompt does not include files/components likely impacted
- prompt does not include tests to add/update
- prompt does not include validation checklist
- prompt does not include out-of-scope instructions

Add test fixtures that intentionally contain shallow output and verify the validator catches them.
