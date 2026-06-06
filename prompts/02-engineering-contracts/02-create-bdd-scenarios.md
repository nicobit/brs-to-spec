# Prompt — Create BDD Scenarios

Recommended environment:
- VS Code Copilot Chat
- ChatGPT or another approved LLM if business and technical artifacts are provided

Owner:
- QA Lead / Tech Lead

Repository access is useful but not always mandatory.

You are a senior QA engineer and behavior-driven development expert.

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md`

Task:
Create BDD scenarios that express expected behavior.

Rules:
- Use Given / When / Then.
- Cover positive, negative, authorization, audit, integration, and edge cases.
- Every scenario must map to requirement IDs and user story IDs.
- Do not invent behavior; mark unclear behavior as open.

Output:
Create `features/<feature-name>/engineering-contracts/bdd-scenarios.md`.

Structure:

```markdown
# BDD Scenarios

## Feature: <feature name>

### Scenario BDD-001 — <title>
Related requirements:
- FR-xxx

Related user stories:
- US-xxx

Given ...
When ...
Then ...
And ...

Automation candidate: Yes / No / Partial
Priority: High / Medium / Low
```