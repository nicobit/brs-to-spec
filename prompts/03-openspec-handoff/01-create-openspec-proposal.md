# Prompt — Create OpenSpec Proposal

Recommended environment:
- VS Code Copilot Chat
- GitHub Copilot Chat

Owner:
- Engineering Lead / Senior Developer

Repository access is recommended.

You are an engineering lead creating an OpenSpec-style change proposal.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/business-intake/gaps-and-questions.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md`

Task:
Create an implementation-oriented proposal from the approved business intake.

Rules:
- Keep it concise.
- Do not duplicate all business intake content.
- Reference upstream artifacts.
- Make the business problem, scope, and impact clear.
- List assumptions and unresolved decisions.
- Do not include low-level implementation tasks yet.

Output:
Create `features/<feature-name>/openspec-change/proposal.md`.

Structure:

```markdown
# Proposal — <feature name>

## Why
## What Changes
## Business Outcomes
## In Scope
## Out of Scope
## Impacted Users / Roles
## Impacted Systems
## Requirements Summary
## Risks
## Assumptions
## Open Questions
## Upstream References
```

Also use:
- `features/<feature-name>/business-intake/epics-and-features.md`

The proposal must identify:
- Business objectives
- Epics
- Features/capabilities included in this change

Also read if available:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Include relevant architecture constraints, risks, and unresolved decisions in the proposal.

## Mandatory use of architecture alignment

If this file exists, read it:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Include major constraints, contradictions, risks, and unresolved decisions in the proposal.
