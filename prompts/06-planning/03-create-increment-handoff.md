# Prompt — Create Increment Handoff

Recommended environment:
- VS Code Copilot Chat
- Approved LLM with access to all feature artifacts

Owner:
- Product Owner / Business Analyst
- Architect / Tech Lead
- Engineering Lead

Input files:
- `features/<feature-name>/planning/delivery-slicing.md`
- `features/<feature-name>/planning/next-increment-scope.md`
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md`
- `features/<feature-name>/business-intake/epics-and-features.md`

Task:
Create an increment-level handoff that constrains the next steps to the selected increment.

Output:
Create:

```text
features/<feature-name>/planning/increment-handoff.md
```

Use the template:

```text
templates/planning/increment-handoff.md
```

Rules:
- The increment handoff is not the final downstream handoff package.
- It defines the selected scope that should be detailed next.
- It should be used as input to user-story generation, technical spec, architecture contracts, enablement, and final handoff.
- Do not pull future-scope items into the increment.
