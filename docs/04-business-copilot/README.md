# Business Copilot

Business Copilot mode provides a business-facing intake and review surface for enterprise initiatives.
It is designed for use with Microsoft 365 Copilot, Word, SharePoint, Teams, and Copilot Studio.

!!! warning "Scope boundary"
    Business Copilot is **not** the engineering execution source of truth. It covers intake and review only. Engineering work continues in VS Code after business approval.

## What it covers

| Area | Yes | No |
|---|---|---|
| Business intake from BRS documents | ✓ | |
| Business-facing gap analysis and summary | ✓ | |
| Business approval preparation | ✓ | |
| Review outputs in Word / SharePoint format | ✓ | |
| Engineering task creation | | ✗ |
| Implementation planning | | ✗ |
| Code generation | | ✗ |
| Technical review | | ✗ |

## How it fits the framework

```text
Business Copilot (intake and review)
  -> business-approved outputs
    -> IT maps to OpenSpec or standalone execution mode
      -> engineering continues in VS Code
```

## When to use each page

| I want to… | Go to |
|---|---|
| Run an intake session using M365 Copilot | [Run Business Intake in M365](how-to-run-business-intake-in-m365-copilot.md) |
| Build the BRS Intake Agent in Copilot Studio | [Create the BRS Intake Agent](how-to-create-m365-copilot-agent.md) |
| Understand how Copilot Studio fits the full framework | [Extended Integration Architecture](copilot-studio-extended-integration.md) |
| Let stakeholders answer open decisions via Teams | [Create the Decision Capture Agent](how-to-create-decision-capture-agent.md) |
| Give PMs delivery status in Teams without VS Code | [Create the Status Query Agent](how-to-create-status-query-agent.md) |
| Alert reviewers when quality gates are ready | [Create the Gate Notification Agent](how-to-create-gate-notification-agent.md) |

## Prompts

Three prompts are available in `.brs2spec/skills/6-business-copilot/`, designed as a sequence:

| Prompt | Purpose | Required |
|---|---|---|
| `01-analyze-brs.md` | Analyze BRS and produce a structured business summary | Yes |
| `02-identify-gaps-and-questions.md` | Identify gaps, open questions, and unresolved dependencies | Yes |
| `03-draft-epics-and-features.md` | Draft prioritised epics and features — business perspective only | Optional |

Each prompt can be copied directly into Microsoft 365 Copilot — no repository access required.

See [Run Business Intake in M365](how-to-run-business-intake-in-m365-copilot.md) to view and run each prompt.
