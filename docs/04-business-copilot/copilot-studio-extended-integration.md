# Copilot Studio — Extended Integration Architecture

This page covers how Copilot Studio can participate in the brs-to-spec framework **beyond BRS intake** — specifically for decision capture, status reporting, and gate notifications during active delivery.

The existing BRS Intake Assistant (see [how-to-create-m365-copilot-agent.md](how-to-create-m365-copilot-agent.md)) covers the upstream capture use case. This page covers the parallel tracks that run alongside the engineering workflow.

---

## Architecture overview

```
Teams / SharePoint
      ↑↓
Copilot Studio agents          ← business stakeholders live here
  - BRS Intake Assistant       (existing — upstream capture)
  - Decision Capture Agent     (new — decisions during delivery)
  - Status Query Agent         (new — progress visibility in Teams)
  - Gate Notification Agent    (new — reviewer alerts)
      ↓
SharePoint document library    ← shared file store
      ↓
GitHub Copilot / Claude Code   ← engineering agents live here
  Full framework runs here
  Reads BRS from SharePoint
  Writes all artifacts
  Gate enforcement, sequencing, handoff
      ↓
ADO / GitHub
  Handoff consumed by dev team
```

**The split is clean:** Copilot Studio never generates framework artifacts or enforces gates. It only reads existing artifacts and captures human input. The engineering agent owns all writes inside the initiative workspace.

---

## Track 1 — Decision Capture Agent

### Problem it solves

During delivery, open decisions pile up in `planning/open-decisions.md`. The answers require input from business stakeholders (PO decisions, vendor answers, legal sign-off, compliance input) — but those people are in Teams, not in VS Code. Currently the engineer must chase them manually.

### What this agent does

- Presents an open decision to a stakeholder in Teams in plain business language
- Captures their answer in a structured format
- Saves the answer to `input/input-package.md` in the SharePoint library under "Decisions and Clarifications Received"
- The engineering agent reads that file on next invocation and advances

### Agent instructions (system prompt)

```text
## Who you are

You are the Delivery Decision Assistant. Your job is to help business stakeholders
answer open questions that are blocking engineering progress — quickly and clearly,
without requiring them to use any engineering tools.

## What you do

You will be given one open decision at a time. You present it in plain business
language, ask for the answer, and record it in a structured format.

You do not explain technical details. You do not make decisions on behalf of the
stakeholder. You do not proceed until the stakeholder has given a clear answer.

## Format for each decision

Present the decision like this:

---
**Open decision for your input**

**Question:** [Plain language version of the decision]
**Why it matters:** [Business impact if left unresolved]
**Options (if applicable):** [List options if the decision has discrete choices]
**Needed before:** [Stage or date]
---

Wait for the stakeholder's answer. Then confirm:

"Thank you. I'll record your answer as:
**Decision:** [restate what they said in one sentence]
**Decided by:** [their name]
**Date:** [today's date]

Is this correct before I save it?"

Wait for confirmation. Then save to input-package.md using the format below.

## Output format — append to input/input-package.md under "Decisions and Clarifications Received"

| Decision ID | Question | Answer | Decided by | Date |
|---|---|---|---|---|
| [ID from open-decisions.md] | [question] | [answer] | [name] | [date] |

## Rules

- One decision at a time. Do not present multiple decisions at once.
- Never invent an answer. If the stakeholder is unsure, record "Pending — [reason]".
- Use business language. Do not reference technical artifacts by filename.
- Always confirm before saving.
```

### Power Automate wiring

1. Engineering agent detects a blocking decision → writes a trigger record to a SharePoint list (`/BRS-Decisions/pending-decisions`)
2. Power Automate flow fires → sends an Adaptive Card in Teams to the decision owner
3. Stakeholder answers via the Adaptive Card or opens the Copilot Studio agent
4. Agent saves answer to `input/input-package.md` in SharePoint
5. Engineering agent reads the updated file on next invocation → resolves the decision → advances

---

## Track 2 — Status Query Agent

### Problem it solves

PMs and business stakeholders want to know delivery status without opening VS Code or reading markdown files. Currently they must ask the engineer.

### What this agent does

- Reads `planning/workflow-state.json` from SharePoint
- Reads `planning/open-decisions.md` for blocking items
- Translates both into plain business language in Teams

### Agent instructions (system prompt)

```text
## Who you are

You are the Delivery Status Assistant. You give business stakeholders a plain-language
summary of where the initiative is, what is blocking it, and what decisions are needed.

You do not modify any files. You do not create artifacts. You only read and report.

## What you report

When asked for a status update, provide:

1. **Current stage** — where the initiative is in the delivery process (business language, not stage numbers)
2. **What was completed last** — one sentence
3. **What is happening next** — one sentence
4. **Blocking items** — any open decisions or quality gates waiting for human input
5. **What the business needs to do** — concrete actions, if any

## Tone

Plain business language. No engineering jargon. No filenames. No technical terms.
If something is blocked, be direct about what is needed and who needs to do it.

## Rules

- Never say "I don't know" — if the state file is missing or unreadable, say
  "The initiative workspace has not been set up yet. Engineering needs to run the
  framework first."
- Never invent status. Only report what is in the state file.
- If blocking decisions exist, list them by question — not by decision ID.
- Keep the response to one short paragraph plus a bullet list of actions if needed.
```

### SharePoint wiring

- Agent reads `planning/workflow-state.json` and `planning/open-decisions.md` via SharePoint connector
- No write access needed — read-only
- Can be triggered from Teams by typing "status" or "what is the status of [initiative name]"

---

## Track 3 — Gate Notification Agent

### Problem it solves

Quality gates (security review, data contract, test strategy, etc.) require a human to review the artifact and change `Status` from `In progress` to `Accepted`. Currently there is no mechanism to alert the right reviewer — the engineer must chase them.

### What this agent does

- Detects when a gate artifact appears or changes in SharePoint
- Sends a Teams notification to the gate reviewer with a summary of what needs review
- Records acknowledgement

### Power Automate wiring

1. Power Automate monitors the `quality-gates/` folder in SharePoint for new or modified files
2. When a gate artifact appears with `Status: In progress`, the flow extracts the gate type and reviewer field
3. Flow sends an Adaptive Card in Teams to the reviewer:

```
🔔 Quality gate ready for review

Initiative: [name]
Gate: [Security Review / Data Contract / Test Strategy / ...]
Summary: [one-line description of what was assessed]
Location: [SharePoint link]

Please review and update Status to Accepted when ready.
[Open in SharePoint] [Mark as Accepted]
```

4. If "Mark as Accepted" is clicked, the flow updates the `Status` field in the artifact directly
5. Engineering agent detects the status change on next invocation and advances

---

## What Copilot Studio does NOT do in this architecture

| Task | Owner | Why |
|---|---|---|
| Generate framework artifacts | Engineering agent only | Requires file system access, gate enforcement, content validation |
| Run the orchestrator or stage sequence | Engineering agent only | Auto-sequencing logic is too complex for Copilot Studio topics |
| Enforce gate chain | Engineering agent only | Content checks require reading markdown file content deeply |
| Create initiative workspace structure | Engineering agent only | Framework violation if done outside the workflow |
| Replace or duplicate the engineering workflow | Never | Would drift immediately from the file-based ground truth |

---

## Summary — what each track adds

| Track | Users served | Value |
|---|---|---|
| BRS Intake Assistant (existing) | Business stakeholders | Captures structured BRS before engineering starts |
| Decision Capture Agent (new) | PO, legal, compliance, vendors | Unblocks engineering without requiring them in VS Code |
| Status Query Agent (new) | PM, business lead | Delivery visibility in Teams without reading markdown |
| Gate Notification Agent (new) | Security, QA, architecture reviewers | Alerts reviewers when gates are ready, captures acceptance |

---

## See also

- [How to Create the M365 Copilot Agent](how-to-create-m365-copilot-agent.md)
- [How to Run Business Intake in M365 Copilot](how-to-run-business-intake-in-m365-copilot.md)
- [Delivery & Execution Modes](../02-delivery-and-execution-modes.md)
