# Prompt — Implement One Task with Copilot

Recommended environment:
- VS Code Copilot Agent mode
- GitHub Copilot Coding Agent

Owner:
- Developer

Repository and code access are required.

Implement Task <number> from:

```text
features/<feature-name>/openspec-change/tasks.md
```

Before coding, read:

```text
features/<feature-name>/business-intake/requirements.md
features/<feature-name>/business-intake/user-stories.md
features/<feature-name>/engineering-contracts/technical-spec.md
features/<feature-name>/engineering-contracts/bdd-scenarios.md
features/<feature-name>/openspec-change/proposal.md
features/<feature-name>/openspec-change/design.md
features/<feature-name>/openspec-change/tasks.md
```

Then:

1. Inspect existing similar code in the repository.
2. Provide a short implementation plan:
   - files to change
   - tests to add or update
   - assumptions
   - risks
3. Implement only Task <number>.
4. Do not implement future tasks.
5. Do not change unrelated files.
6. Do not introduce new dependencies.
7. Add or update tests.
8. Provide a final summary with:
   - files changed
   - requirements covered
   - user stories / acceptance criteria covered
   - tests added
   - risks
   - remaining open questions

## Architecture & Contract Extensions

Before implementing a task, read relevant files under `features/<feature-name>/architecture-contracts/` such as API contract, OpenAPI, domain model, data model, event contracts, threat model, quality scenarios, and ADRs.
