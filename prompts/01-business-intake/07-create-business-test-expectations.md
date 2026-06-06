# Prompt 07 — Create Business Test Expectations

Recommended environment:
- Microsoft 365 Copilot, ChatGPT, or another approved LLM
- GitHub Copilot Chat if artifacts are already in the repository

Owner:
- Business PO / BA with QA support

This prompt does not require code access.

You are a QA-minded Business Analyst.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`

Task:
Create high-level business test expectations that Business PO and QA can understand.

Rules:
- Focus on business behavior, not technical implementation.
- Include UAT scenarios.
- Include positive and negative scenarios.
- Include expected business outcomes.
- Mark unclear expected behavior as open.

Output:
Create `features/<feature-name>/business-intake/business-test-expectations.md`.

Structure:

```markdown
# Business Test Expectations

## 1. UAT Scope
## 2. Key Business Scenarios
## 3. Negative / Exception Scenarios
## 4. Role-Based Scenarios
## 5. Audit / Evidence Expectations
## 6. Reporting Expectations
## 7. Test Data Needed
## 8. Open Questions
```

Also group business test expectations by epic and feature where possible.

For each test expectation, include:
- Parent epic
- Parent feature/capability
- Related user story
- Related acceptance criteria
