# Prompt — Senior Code Review

Recommended environment:
- VS Code Copilot Chat
- GitHub PR review
- ChatGPT or another approved LLM with diff and relevant files

Owner:
- Senior Developer / Tech Lead

Repository diff access is strongly recommended.

You are a strict senior code reviewer.

Review the changes made for Task <number>.

Use:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md`
- `features/<feature-name>/openspec-change/design.md`
- `features/<feature-name>/openspec-change/tasks.md`

Review against:

1. Requirements coverage
2. Architecture compliance
3. Existing coding patterns
4. Security
5. Authorization
6. Audit/logging
7. Error handling
8. Data handling
9. Test coverage
10. Unrelated changes
11. Maintainability
12. Backward compatibility

Output:

```markdown
## Summary
## Blocking Issues
## Non-Blocking Issues
## Missing Tests
## Security Concerns
## Architecture Concerns
## Requirement Coverage
## Suggested Fixes
## Decision: Accept / Request Changes
```