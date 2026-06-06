# Prompt — Create Traceability Matrix

Recommended environment:
- VS Code Copilot Chat
- ChatGPT or another approved LLM if all artifacts are provided

Owner:
- QA Lead / Delivery Lead

Repository access is useful when mapping to tasks or code areas.

Input files:
- `features/<feature-name>/business-intake/epics-and-features.md`
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/bdd-scenarios.md`
- `features/<feature-name>/engineering-contracts/test-plan.md`
- `features/<feature-name>/openspec-change/tasks.md` if available

Task:
Create or update the traceability matrix.

Rules:
- Every business objective should map to at least one epic.
- Every epic should map to at least one feature/capability.
- Every feature/capability should map to requirements.
- Every requirement should map to at least one story or scenario.
- Every business rule should map to a test.
- Every security requirement should map to a security check.
- Every audit requirement should map to audit validation.
- Every OpenSpec task should map back to a feature and requirement.
- Mark gaps as Not Covered.

Output:
Create `features/<feature-name>/engineering-contracts/traceability-matrix.md`.

Table:

| Business Objective | Epic | Feature / Capability | Requirement ID | Requirement Title | User Story | Acceptance Criteria | BDD Scenario | Test Case | OpenSpec Task | Code Area | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
