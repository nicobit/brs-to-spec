# Adapter Prompt — Create gstack Brief from Handoff

Use this when gstack will be used as a downstream execution/review layer or as a reviewer around another downstream framework.

Recommended environment:
- VS Code Copilot Chat
- Claude Code / gstack context if available
- Approved LLM with repository context

Owner:
- Tech Lead / Architect / Engineering Lead

Input files:
- `features/<feature-name>/handoff/spec-driven-handoff.md`
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md`
- `features/<feature-name>/architecture-contracts/*` if present
- `features/<feature-name>/enablement/*` if present
- `features/<feature-name>/openspec-change/*` if present

Task:
Create a concise gstack-ready brief.

Output:
Create:

```text
features/<feature-name>/handoff/gstack-brief.md
```

Use this structure:

```markdown
# gstack Brief

## 1. Purpose

## 2. Recommended gstack Usage Mode

Choose one:
- gstack as downstream execution/review layer
- gstack as reviewer around OpenSpec / Spec Kit / Kiro / standalone mode

## 3. Context Files to Provide

| File | Why gstack needs it |
|---|---|

## 4. Business Context Summary

## 5. Engineering Context Summary

## 6. Architecture / Contract Context

## 7. Enablement Context

## 8. Risks and Open Questions

## 9. Suggested gstack Skill Sequence

| Step | Suggested gstack skill | Purpose | Input context | Expected output |
|---|---|---|---|---|

## 10. Blocking Review Questions

## 11. Shipping / Release Concerns

## 12. Do Not Lose These Constraints
```

Rules:
- Do not copy all source documents in full.
- Summarize and point to files.
- Make blockers and constraints explicit.
- Make clear whether gstack is the execution owner or only a reviewer.
- If exact gstack skill names are not available in the target environment, describe the role to run instead.
