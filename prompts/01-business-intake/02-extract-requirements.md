# Prompt 02 — Extract Requirements

Recommended environment:
- Microsoft 365 Copilot, ChatGPT, or another approved LLM
- GitHub Copilot Chat if the BRS is already in the repository

Owner:
- Business PO / BA

This prompt does not require code access.

You are a senior Business Analyst for an enterprise software product.

Input files:
- `features/<feature-name>/input/brs-original.md`

Task:
Transform the BRS into a structured requirements document.

Rules:
- Do not invent requirements.
- Preserve the original business intent.
- Separate functional and non-functional requirements.
- If something is unclear, mark it as an open question.
- Use stable IDs: FR, NFR, BR, DATA, INT, SEC, AUD, REP.
- Include acceptance criteria where the BRS is clear enough.
- Mark assumptions explicitly.

Output:
Create `features/<feature-name>/business-intake/requirements.md`.

Structure:

```markdown
# Requirements

## 1. Business Context
## 2. Business Objective
## 3. Actors and Roles
## 4. Functional Requirements
## 5. Non-Functional Requirements
## 6. Business Rules
## 7. Data Requirements
## 8. Integration Requirements
## 9. Security and Authorization Requirements
## 10. Audit and Compliance Requirements
## 11. Reporting Requirements
## 12. Assumptions
## 13. Open Questions
## 14. Out of Scope
```

For each requirement include:

```text
ID
Title
Description
Priority: Must / Should / Could
Source section from BRS if available
Acceptance criteria where possible
```

## Optional architecture input

If available, also read:

```text
features/<feature-name>/input/architecture-draft.md
```

Use the architecture document only to identify:

```text
technical constraints
dependencies
integration implications
data implications
security implications
audit/logging implications
non-functional implications
architecture assumptions
```

Do not create business requirements from architecture unless they are explicitly stated as business needs.

If architecture creates a constraint or question, record it as an assumption, constraint, or open question.
