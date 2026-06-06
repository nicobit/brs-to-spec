# Prompt — Create Test Strategy

Recommended environment:
- VS Code Copilot Chat
- ChatGPT or another approved LLM if relevant artifacts are provided

Owner:
- QA Lead

Repository access is useful for test framework alignment.

You are a senior QA manager.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md`
- `features/<feature-name>/engineering-contracts/bdd-scenarios.md`

Task:
Create a test strategy.

Rules:
- Cover functional and non-functional testing.
- Cover security, authorization, audit, integration, regression, and error handling.
- Identify automation candidates.
- Identify test data and environment needs.
- Identify risks and dependencies.

Output:
Create `features/<feature-name>/engineering-contracts/test-strategy.md`.

Structure:

```markdown
# Test Strategy

## 1. Objective
## 2. Scope
## 3. Out of Scope
## 4. Test Levels
## 5. Functional Test Areas
## 6. Non-Functional Test Areas
## 7. Security and Authorization Testing
## 8. Audit and Compliance Testing
## 9. Integration Testing
## 10. Regression Testing
## 11. Automation Strategy
## 12. Test Data Needs
## 13. Environment Needs
## 14. Risks and Dependencies
## 15. Entry Criteria
## 16. Exit Criteria
```