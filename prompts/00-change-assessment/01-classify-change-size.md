# Prompt — Classify Change Size

Recommended environment:
- Microsoft 365 Copilot, ChatGPT, or another approved LLM
- VS Code Copilot Chat if the change is already in the repository

Owner:
- Business PO / BA initially
- Confirmed by Tech Lead / Architect for medium or large changes

Input:
- BRS or change description
- Draft architecture if available
- Any known constraints

Task:
Classify the change as Small, Medium, or Large/Risky and recommend which artifact flow to use.

Definitions:

## Small change — Minimal flow

Use for:
- simple validation
- minor UI change
- small bug fix
- small configuration change
- no significant architecture, security, audit, data, or integration impact

## Medium change — BDD + test strategy flow

Use for:
- new feature in existing module
- moderate frontend/backend change
- role-based behavior
- workflow step
- non-trivial validation
- QA planning needed

## Large / risky change — Full framework

Use for:
- regulated feature
- client-data-impacting change
- audit/compliance-heavy change
- security-sensitive change
- cross-system integration
- risky database migration
- major architecture change
- external contract change
- high business impact
- multi-team delivery

Output:
Create or update `features/<feature-name>/quality-gates/change-size-assessment.md`.

Use this structure:

```markdown
# Change Size Assessment

## Recommended classification
Small / Medium / Large-Risky

## Reasoning

## Risk signals found

## Recommended flow

## Required artifacts

## Optional artifacts

## Artifacts not needed

## Questions to confirm before proceeding

## Final recommendation
```

Rules:
- Do not over-classify every change as large.
- If unsure between Small and Medium, choose Medium.
- If there is client data, audit, authorization, regulatory, or integration impact, explain why Medium or Large is recommended.
