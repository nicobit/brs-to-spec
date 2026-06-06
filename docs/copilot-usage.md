# Copilot Usage Guide

## Do not ask

```text
Implement the BRS.
```

## Ask

```text
Implement Task 001 from features/<feature-name>/openspec-change/tasks.md.

Before coding:
1. Read the business intake package.
2. Read the engineering contracts.
3. Read the OpenSpec proposal and design.
4. Inspect existing similar code.
5. Provide a short plan.

Then implement only Task 001.
Add or update tests.
Do not change unrelated files.
```

## Expected Copilot output

After implementation, Copilot should summarize:

- Files changed
- Requirements covered
- User stories covered
- Tests added
- Assumptions
- Risks
- Remaining open questions

## Review after every task

Use:

```text
prompts/05-reviewers/01-senior-code-review.md
```
