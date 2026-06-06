# Copilot Studio Agent Design for BRS Intake

This is the long-term design for turning the Microsoft 365 Copilot Phase 1 process into a controlled Copilot Studio agent.

## Agent name

```text
BRS Intake Agent
```

## Purpose

Guide business users through BRS intake and produce approved SharePoint and/or repository-ready artifacts.

## Recommended channels

- Microsoft Teams
- Microsoft 365 Copilot
- SharePoint site

## Knowledge sources

Add:
- SharePoint BRS Intake site
- BRS templates
- business-intake prompt library
- approved examples
- governance guidance

Copilot Studio can use SharePoint sites and lists as knowledge sources.

## Topics

### Topic 1 — Start BRS intake

Questions:
- Which BRS document should be analyzed?
- Is there an architecture draft?
- Who is the business owner?
- What is the target quarter?
- Is this regulatory, client-driven, platform-driven, or internal?

### Topic 2 — Create BRS summary

Uses:

```text
prompts/12-business-copilot-intake/01-create-brs-business-summary.md
```

### Topic 3 — Extract requirements

Uses:

```text
prompts/12-business-copilot-intake/03-extract-business-requirements-for-review.md
```

### Topic 4 — Review gaps and questions

Uses:

```text
prompts/12-business-copilot-intake/04-identify-business-gaps-and-questions.md
```

### Topic 5 — Create delivery slicing

Uses:

```text
prompts/12-business-copilot-intake/05-create-business-delivery-slicing.md
```

### Topic 6 — Select next increment

Uses:

```text
prompts/12-business-copilot-intake/06-select-next-increment-for-business-review.md
```

### Topic 7 — Approval checklist

Uses:

```text
prompts/12-business-copilot-intake/08-create-business-approval-checklist.md
```

## Long-term actions

Phase 1:
- Manual save/copy into SharePoint outputs.

Phase 2:
- Create SharePoint pages/documents automatically.
- Update SharePoint lists.
- Notify IT in Teams.

Phase 3:
- Create repository branch.
- Commit Markdown artifacts.
- Open PR/MR.
- Notify engineering.

## Repository write-back rule

Never write directly to `main`.

Use:

```text
create branch
commit generated artifacts
open PR/MR
human review
merge after approval
```
