# Prompt — Fix Review Comments

Recommended environment:
- VS Code Copilot Agent mode
- GitHub Copilot Coding Agent

Owner:
- Developer

Repository and code access are required.

You are fixing review comments for Task <number>.

Input:
- Review comments from the PR
- `features/<feature-name>/openspec-change/tasks.md`
- Relevant business intake and engineering contract artifacts

Rules:
- Fix only the review comments.
- Do not expand scope.
- Do not refactor unrelated code.
- Add tests if the fix changes behavior.
- Explain any comments you disagree with.

Output summary:
- Review comments addressed
- Files changed
- Tests added/updated
- Remaining risks