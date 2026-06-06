# Prompt — Create Detailed Test Plan

Recommended environment:
- VS Code Copilot Chat
- ChatGPT or another approved LLM if relevant artifacts are provided

Owner:
- QA Lead / QA Engineer

Repository access is useful for automation planning.

You are a senior QA engineer.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/bdd-scenarios.md`
- `features/<feature-name>/engineering-contracts/test-strategy.md`

Task:
Create a detailed test plan with test cases.

Rules:
- Every functional requirement must have at least one test case.
- Every business rule must have at least one test case.
- Every security requirement must have at least one security/authorization test.
- Every audit requirement must have one audit validation.
- Include positive and negative cases.
- Mark automation candidates.

Output:
Create `features/<feature-name>/engineering-contracts/test-plan.md`.

For each test case use:

```markdown
## TP-001 — <test title>

Related requirements:
- FR-xxx

Related user story:
- US-xxx

Related BDD scenario:
- BDD-xxx

Preconditions:
- ...

Test data:
- ...

Steps:
1. ...
2. ...

Expected result:
- ...

Test type:
- Functional / Security / Integration / Regression / Audit / Performance

Automation candidate:
- Yes / No / Partial

Priority:
- High / Medium / Low

Open questions:
- ...
```