# Prompt — Find Gaps and Questions

Recommended environment:
- Microsoft 365 Copilot, ChatGPT, or another approved LLM
- GitHub Copilot Chat if artifacts are already in the repository

Owner:
- Business PO / BA, with review by QA or Tech Lead if needed

This prompt does not require code access.

You are a critical requirements reviewer for an enterprise banking-grade software product.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`

Task:
Identify gaps, contradictions, ambiguities, missing roles, missing business rules, missing data definitions, missing authorization rules, missing audit rules, and missing acceptance criteria.

Rules:
- Do not solve gaps by inventing behavior.
- Create clear questions for Business PO / Architect / QA.
- Separate critical blockers from assumptions.

Output:
Create `features/<feature-name>/business-intake/gaps-and-questions.md`.

Use this table:

| ID | Area | Issue | Why it matters | Affected artifact | Proposed question | Severity | Owner | Status |
|---|---|---|---|---|---|---|---|---|

Severity:
- Critical
- High
- Medium
- Low

Additional check:
- Verify that business objectives, epics, features, requirements, and user stories are aligned.
- Identify orphan requirements that do not map to any feature.
- Identify features that do not map to requirements.
- Identify user stories that do not map to a feature or epic.
