# Prompt — Select Next Increment Scope

Recommended environment:
- VS Code Copilot Chat
- Approved LLM with access to all feature artifacts

Owner:
- Product Owner / Business Analyst
- Architect / Tech Lead
- Engineering Lead

Input files:
- `features/<feature-name>/planning/delivery-slicing.md`
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/epics-and-features.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md`
- `features/<feature-name>/business-intake/gaps-and-questions.md` if available

Task:
Select the scope that should be detailed for the next increment.

Output:
Create:

```text
features/<feature-name>/planning/next-increment-scope.md
```

Use the template:

```text
templates/planning/next-increment-scope.md
```

Rules:
- Select a coherent, valuable increment.
- Do not include features blocked by unresolved architecture decisions unless the increment goal is to resolve those decisions.
- Make excluded/deferred requirements explicit.
- Identify which stories should be created next.
- Identify architecture, enablement, and QA prerequisites.
- Mark whether the increment is ready for detailed user stories.
