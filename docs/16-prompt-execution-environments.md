# Prompt Execution Environments

Different prompt families are meant to run in different tools.

Do not assume every prompt should run in GitHub Copilot Coding Agent or in a business-facing Copilot surface.

## Summary

| Prompt group | Typical owner | Recommended environment | Repository / code access |
|---|---|---|---|
| `prompts/0-input-preparation` | Business analyst / product owner / architect | Microsoft 365 Copilot, ChatGPT, VS Code Copilot Chat | Not usually required |
| `prompts/1-routing` | Product owner / architect / tech lead | VS Code Copilot Chat or another repository-aware assistant | Helpful |
| `prompts/2-business-intake` | Product owner / business analyst | Microsoft 365 Copilot, ChatGPT, VS Code Copilot Chat | Not usually required |
| `prompts/3-planning-and-modular-delivery` | Architect / tech lead / senior engineer | VS Code Copilot Chat | Recommended |
| `prompts/4-engineering-readiness` | Tech lead / QA / architect / security lead | VS Code Copilot Chat | Recommended |
| `prompts/5-handoff` | Engineering lead / senior engineer | VS Code Copilot Chat | Recommended |
| `prompts/6-business-copilot` | Business user / business analyst | Microsoft 365 Copilot / Copilot Studio | No |
| `prompts/7-perspectives` | Delivery lead / scrum master / PM | VS Code Copilot Chat | Helpful |
| `prompts/8-copilot-implementation` | Developer | VS Code Copilot Agent mode / GitHub Copilot Coding Agent | Yes |
| `prompts/9-reviewers` | Senior developer / QA / architect / security reviewer | VS Code Copilot Chat / PR review surface | Yes |

## Operating Rule

Work inside one initiative workspace at a time.

All relative input and output paths are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Business-facing environments

Use Microsoft 365 Copilot, Copilot Studio, ChatGPT, or another approved business-facing assistant for:

```text
input preparation
business intake
business review outputs
business-facing gap analysis
business approval preparation
```

Do not use those surfaces to create implementation tasks or code changes.

## Repository-aware engineering environments

Use VS Code Copilot Chat or another repository-aware assistant for:

```text
routing
architecture review
delivery planning
engineering readiness
quality gates
OpenSpec handoff
standalone handoff
planning projection
```

These prompts benefit from repository context, existing artifact context, and feature-workspace awareness.

## Coding-agent environments

Use VS Code Copilot Agent mode or GitHub Copilot Coding Agent only after the feature has a clear implementation source of truth.

Typical prerequisites:

```text
engineering-readiness/readiness-check.md exists
required quality gates are complete or explicitly accepted as risk
openspec/changes/D1-.../tasks.md exists
or standalone-delivery/D1-.../tasks.md exists
```

If the repository uses the optional ready-for-Copilot gate, complete:

```text
quality-gates/ready-for-copilot-checklist.md
```

before implementation starts.

## Review environments

Use review prompts with:

```text
repository diff access
feature artifact context
task context
test context
```

These are best run in VS Code Copilot Chat, GitHub PR review, or another diff-aware review surface.

## Anti-patterns

Do not:

```text
ask a coding agent to implement directly from raw BRS inputs
ask a business-facing Copilot surface to create engineering tasks
run review prompts without the relevant diff or changed files
mix artifacts from multiple initiative workspaces in one run
```
