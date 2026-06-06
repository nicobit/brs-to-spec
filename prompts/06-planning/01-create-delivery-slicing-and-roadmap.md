# Prompt — Create Delivery Slicing and Roadmap

Recommended environment:
- VS Code Copilot Chat
- Approved LLM with access to all feature artifacts

Owner:
- Product Owner / Business Analyst
- Architect / Tech Lead
- Engineering Lead
- QA Lead
- Platform/SRE Lead where relevant

Use when:
- The BRS is large
- Delivery spans more than one quarter
- Multiple epics/features/capabilities are expected
- Not everything should become detailed user stories immediately

Input files:
- `features/<feature-name>/input/brs-original.md`
- `features/<feature-name>/input/architecture-draft.md`
- `features/<feature-name>/business-intake/brs-summary.md`
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md`
- `features/<feature-name>/business-intake/epics-and-features.md`
- `features/<feature-name>/business-intake/gaps-and-questions.md` if available

Task:
Create a delivery slicing and roadmap for the full BRS.

Output:
Create:

```text
features/<feature-name>/planning/delivery-slicing.md
```

Use the template:

```text
templates/planning/delivery-slicing.md
```

Rules:
- Do not create detailed user stories for the entire BRS.
- Create MVP / first valuable increment.
- Create quarter/increment slicing.
- Identify dependencies, architecture blockers, enablement blockers, and risks.
- Mark what is future scope.
- Mark which increment is recommended next.
- If priority is unclear, say so.
