# Prompt 06 — Find Gaps and Questions

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

Also read if available:

```text
features/<feature-name>/input/architecture-draft.md
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Additional architecture-related checks:
- BRS and architecture contradictions
- architecture decisions missing for business requirements
- unclear integration boundaries
- unclear data ownership
- unclear authorization boundaries
- missing audit/logging support
- deployment/environment assumptions
- NFRs implied by architecture but missing from requirements

## Mandatory use of architecture alignment

If this file exists, read it:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Merge its findings into `gaps-and-questions.md`.

The final gaps file should include:
- business gaps
- requirement extraction gaps
- BRS/architecture contradictions
- missing architecture decisions
- data/integration gaps
- security/authorization gaps
- audit/logging gaps
- deployment/environment gaps
- enablement-related gaps
