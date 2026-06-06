# Prompt — Create Spec-Driven Handoff Package

Recommended environment:
- VS Code Copilot Chat
- Approved LLM with repository context

Owner:
- Business Analyst / Product Owner
- Architect / Tech Lead
- Engineering Lead

Input files:
- `features/<feature-name>/input/brs-original.md`
- `features/<feature-name>/input/architecture-draft.md`
- `features/<feature-name>/business-intake/*`
- `features/<feature-name>/engineering-contracts/technical-spec.md`
- `features/<feature-name>/architecture-contracts/*` if present
- `features/<feature-name>/enablement/*` if present

Task:
Create a single handoff package that can be given to OpenSpec, GitHub Spec Kit, Kiro, gstack, or used in standalone mode.

Output:

```text
features/<feature-name>/handoff/spec-driven-handoff.md
```

Use:

```text
templates/handoff/spec-driven-handoff.md
```

Rules:
- Do not rewrite all source artifacts in full.
- Summarize and link to source artifacts.
- Highlight blockers clearly.
- Include unresolved decisions and risks.
- Identify whether handoff is ready.
- Recommend one downstream mode.

## Large BRS / increment handoff rule

If the BRS is multi-quarter and these files exist:

```text
features/<feature-name>/planning/delivery-slicing.md
features/<feature-name>/planning/next-increment-scope.md
features/<feature-name>/planning/increment-handoff.md
```

then the handoff package should clearly state whether it is for:
- the full initiative,
- or the selected next increment.

For downstream implementation, prefer handoff for the selected next increment.
