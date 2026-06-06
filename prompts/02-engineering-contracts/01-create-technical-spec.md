# Prompt — Create Technical Specification

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with repository context

Owner:
- Architect / Tech Lead

This prompt benefits from code and architecture access.

You are a senior solution architect and technical lead.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/business-intake/gaps-and-questions.md`
- `features/<feature-name>/input/architecture-draft.md`

Task:
Create a technical specification aligned with the approved business intake and draft architecture.

Rules:
- Do not invent new architecture unless required.
- Prefer existing system patterns.
- Identify unclear decisions as open.
- Explicitly map requirements to components.
- Cover security, audit, data, integration, error handling, observability, deployment, and tests.

Output:
Create `features/<feature-name>/engineering-contracts/technical-spec.md`.

Structure:

```markdown
# Technical Specification

## 1. Overview
## 2. Scope
## 3. Requirements Covered
## 4. Architecture Summary
## 5. Components Impacted
## 6. Component Responsibilities
## 7. Data Model Changes
## 8. API Changes
## 9. UI Changes
## 10. Integration Changes
## 11. Security and Authorization Design
## 12. Audit and Compliance Design
## 13. Error Handling
## 14. Logging and Observability
## 15. Configuration Changes
## 16. Deployment Considerations
## 17. Backward Compatibility
## 18. Testing Implications
## 19. Architecture Decisions
## 20. Risks and Open Decisions
```

Also include a Mermaid component or sequence diagram where useful.

Also use:
- `features/<feature-name>/business-intake/epics-and-features.md`

The technical specification should explicitly state which epics/features are affected and whether the technical design supports the proposed delivery slicing.
