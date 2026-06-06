# Copilot Instructions

## Project Context

This repository uses a spec-driven delivery process.

Do not implement directly from a raw BRS. Implement only from approved OpenSpec tasks, using the business intake and engineering contracts as context.

## Mandatory Rules

- Follow existing architecture and coding patterns.
- Inspect existing similar code before creating new patterns.
- Implement only the requested task.
- Do not perform unrelated refactoring.
- Do not introduce new frameworks or dependencies without approval.
- Do not hardcode environment-specific values.
- Add or update tests for every behavior change.
- Do not invent business rules.
- If a business or architecture decision is unclear, stop and report it.

## Before Coding

Read:

```text
features/<feature-name>/business-intake/requirements.md
features/<feature-name>/business-intake/user-stories.md
features/<feature-name>/engineering-contracts/technical-spec.md
features/<feature-name>/openspec-change/proposal.md
features/<feature-name>/openspec-change/design.md
features/<feature-name>/openspec-change/tasks.md
```

Then:

1. Identify the specific task.
2. Identify impacted files.
3. Inspect existing similar implementation.
4. Explain the intended approach.
5. Implement only that task.

## Security Rules

- Do not weaken authorization.
- Do not expose sensitive data in logs.
- Validate external inputs.
- Use existing authentication and authorization patterns.
- Security-sensitive behavior must have tests or explicit review notes.

## Audit and Logging Rules

- Use existing logging abstractions.
- Use existing audit mechanisms.
- Business-significant state changes must be auditable.
- Do not log secrets, tokens, personal data, or confidential business data.

## Database Rules

- Use the repository's existing migration approach.
- Do not drop or rename columns without explicit approval.
- Include backward compatibility considerations where relevant.
- Add rollback notes if project standard requires them.

## Pull Request Summary Rules

Every implementation summary must include:

- Task implemented
- Requirements covered
- User stories / acceptance criteria covered
- Files changed
- Tests added or updated
- Assumptions
- Risks
- Remaining open questions

## Forbidden Actions

- No implementation from raw BRS.
- No broad rewrites.
- No unrelated cleanup.
- No architecture invention.
- No new dependency without approval.
- No bypassing tests.
