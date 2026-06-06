# Prompt Execution Environments

This project uses different prompts for different audiences.  
Not every prompt should be executed in the same tool.

## Summary

| Prompt Group | Owner | Recommended Tool | Alternative Tool | Needs Code Access? | Creates / Updates |
|---|---|---|---|---:|---|
| `01-business-intake` | Business PO / BA | Microsoft 365 Copilot or approved LLM | ChatGPT / Copilot Chat | No | `business-intake/*` |
| `02-engineering-contracts` | Architect / Tech Lead / QA | VS Code Copilot Chat | ChatGPT with repo context | Sometimes | `engineering-contracts/*` |
| `03-openspec-handoff` | Engineering Lead / Senior Developer | VS Code Copilot Chat | GitHub Copilot Chat | Yes, recommended | `openspec-change/*` |
| `04-copilot-implementation` | Developer | VS Code Copilot Agent / Coding Agent | GitHub Copilot Coding Agent | Yes | Code + tests |
| `05-reviewers` | Reviewer / QA / Architect / Security | PR review + Copilot Chat | ChatGPT with diff/context | Yes, for best results | Review findings |

## Business tools

Business users can use:

```text
Microsoft 365 Copilot
ChatGPT
An approved internal LLM
GitHub Copilot Chat if available
```

Business users should use these tools only for:

```text
BRS summarization
Requirement extraction
User stories
Acceptance criteria
Gaps and questions
Business test expectations
```

Business users should not run prompts that create implementation tasks or code.

## Engineering tools

Engineers should use:

```text
VS Code Copilot Chat
VS Code Copilot Agent mode
GitHub Copilot Coding Agent
Approved internal engineering LLMs
```

Engineers should run prompts that require repository awareness:

```text
technical specification
BDD scenarios
OpenSpec proposal
OpenSpec design
OpenSpec tasks
implementation
code review
architecture review
security review
```

## Recommended operating model

```text
Business PO / BA
  uses Microsoft 365 Copilot, ChatGPT, or another approved LLM
  creates business-intake artifacts

Architect / Tech Lead / QA
  uses VS Code Copilot Chat or another approved engineering LLM
  creates engineering-contract artifacts

Engineering Lead
  uses VS Code Copilot Chat
  creates OpenSpec proposal, design, and tasks

Developer
  uses VS Code Copilot Agent
  implements one OpenSpec task at a time

Reviewer / QA / Architect / Security
  uses PR review + Copilot reviewer prompts
  validates implementation
```

## Important boundaries

### Business users may create

```text
business-intake/brs-summary.md
business-intake/requirements.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
business-intake/business-test-expectations.md
```

### Business users should not create

```text
openspec-change/tasks.md
code changes
database migration scripts
API contracts without engineering review
architecture decisions without architect review
```

### Engineers may create

```text
engineering-contracts/technical-spec.md
engineering-contracts/bdd-scenarios.md
engineering-contracts/test-strategy.md
engineering-contracts/test-plan.md
openspec-change/proposal.md
openspec-change/design.md
openspec-change/tasks.md
code and tests
```

## If business uses Microsoft 365 Copilot

Use Microsoft 365 Copilot when the BRS is in:

```text
Word
SharePoint
Teams meeting transcript
Excel
PowerPoint
```

Recommended use:

1. Ask Copilot to summarize the BRS.
2. Ask Copilot to extract requirements.
3. Ask Copilot to create user stories and acceptance criteria.
4. Ask Copilot to identify gaps and open questions.
5. Copy the reviewed output into the repository under `business-intake/`.

Do not ask Microsoft 365 Copilot to implement code.

## If business uses ChatGPT or another approved LLM

Use it when:

```text
the BRS has been exported or pasted as text
the company allows this usage
the content is not restricted beyond the approved tool policy
```

Recommended use:

1. Paste the BRS or attach the converted Markdown.
2. Run the business intake prompts.
3. Review the output manually.
4. Save the approved output into the repository.

## If engineers use VS Code Copilot Chat

Use it when prompts need repository context:

```text
existing architecture
existing code structure
existing tests
existing naming conventions
existing API patterns
existing database migration patterns
```

This is the preferred environment for:

```text
engineering-contracts/*
openspec-change/*
review prompts
```

## If developers use Copilot Agent

Use it only after:

```text
business-ready-checklist.md is complete
engineering-ready-checklist.md is complete
openspec-change/proposal.md exists
openspec-change/design.md exists
openspec-change/tasks.md exists
ready-for-copilot-checklist.md is complete
```

## Bad usage

Do not do this:

```text
Business PO gives Word BRS directly to Copilot Agent and asks it to implement.
```

Do this instead:

```text
Business BRS
  → business intake
  → engineering contracts
  → OpenSpec proposal/design/tasks
  → Copilot implements one task at a time
```

## Word BRS extraction prompt

Prompt:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

Recommended tools:

```text
Microsoft 365 Copilot
ChatGPT
another approved LLM
GitHub Copilot Chat if the document is already in the repository
```

Owner:

```text
Business PO / BA
```

This prompt does not require repository or code access.

It creates:

```text
features/<feature-name>/input/brs-original.md
```
