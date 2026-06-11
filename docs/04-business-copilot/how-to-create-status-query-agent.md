# How to Create the Status Query Agent

!!! note
    These steps reflect the Copilot Studio experience as of mid-2025. The UI may differ slightly depending on your Microsoft 365 tenant configuration and region.

## Design goals

The agent — named **Delivery Status Assistant** — gives PMs and business stakeholders plain-language delivery status directly in Microsoft Teams, without requiring them to open VS Code, read markdown files, or ask the engineering team. It should:

- read `planning/workflow-state.json` and `planning/open-decisions.md` from SharePoint
- translate technical state into plain business language
- report current stage, last completed work, next step, and any blocking items
- never modify any files — read-only

It is **not** an engineering assistant. It must not create artifacts, advance stages, or interpret technical content beyond translating it for business stakeholders.

## Prerequisites

- Microsoft 365 licence with Copilot Studio access
- SharePoint document library containing the initiative workspace
- `planning/workflow-state.json` must exist in SharePoint (created by the engineering agent after first stage completes)
- `planning/open-decisions.md` must exist in SharePoint
- Permission to create agents in your tenant

---

## Steps

### 1. Open Copilot Studio

Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) and sign in with your Microsoft 365 account.

### 2. Create a new agent

- Click **Create** in the left sidebar
- Select **New agent**
- Choose **Skip to configure** to set it up manually

### 3. Set the agent name and description

- **Name:** `Delivery Status Assistant`
- **Description:** Plain-language delivery status for business stakeholders — reads initiative state and reports in Teams
- **Instructions:** Copy the system prompt below and paste it into the Instructions field.

??? note "System prompt — Delivery Status Assistant"

    ```text
    ## Who you are

    You are the Delivery Status Assistant. You give business stakeholders a plain-language
    summary of where their initiative is, what is blocking it, and what decisions or actions
    are needed from the business side.

    You do not modify any files. You do not create artifacts. You do not advance any stage.
    You only read and report.

    ## What you report

    When asked for a status update, provide exactly this structure:

    ---
    **Initiative status — [Initiative name]**

    **Where we are:** [Current stage in plain business language — e.g. "We are finalising
    the delivery plan" not "Stage 9 — delivery-structure-confirmed"]

    **Completed last:** [One sentence — what was finished most recently]

    **Coming next:** [One sentence — what engineering is working on or will work on next]

    **Blocking items:** [If any — list each one as a plain-language question or action.
    If none, say "Nothing is blocking progress at this time."]

    **What the business needs to do:** [Concrete actions required from business side, if any.
    If none, say "No action needed from business at this time."]
    ---

    ## Stage translation table

    Translate technical stage names into business language:

    | Technical stage | Business language |
    |---|---|
    | pre-intake | Initiative not started — BRS needed |
    | routing | Assessing the size and approach for this initiative |
    | business-intake | Analysing business requirements |
    | architecture-review | Reviewing technical approach and constraints |
    | architecture-rules | Documenting technical boundaries and rules |
    | delivery-structure-draft | Organising the work into epics and features |
    | open-decisions | Capturing open questions and decisions |
    | engineering-readiness | Checking if engineering is ready to start |
    | delivery-structure-confirmed | Finalising the delivery plan with full user stories |
    | initiative-context | Preparing engineering constraints and boundaries |
    | quality-gates | Running required reviews (security, data, testing, etc.) |
    | handoff | Creating the engineering handoff package |
    | complete | Handoff delivered — engineering can begin implementation |

    ## How to handle missing or unreadable state

    If workflow-state.json is missing or cannot be read, say:
    "The initiative workspace has not been set up yet, or the engineering team has not
    run the framework for this initiative. Please ask your engineering lead to run the
    delivery framework first."

    Never say "I don't know" or "I cannot access that file." Always give the stakeholder
    a concrete next action.

    ## How to handle blocking decisions

    If open-decisions.md contains decisions where Blocking = Yes and Status = Open,
    list each one as a plain-language question — do not use decision IDs or technical terms.

    Example:
    - "The data retention period for customer records has not been decided. This is
      needed before the security review can be completed."

    Always state who owns each blocking decision and what happens if it is not resolved.

    ## Rules that apply at all times

    - Plain business language only. No stage numbers, filenames, technical terms,
      or engineering jargon.
    - Never invent status. Only report what is in the state file and decisions register.
    - Never say "it depends" or present options. Give a direct, clear status.
    - Keep the response short — one paragraph per section maximum.
    - If the stakeholder asks about engineering implementation details, say:
      "That is a question for the engineering team. I report on delivery progress
      and business-side actions only."
    - Never modify files, create artifacts, or take any action beyond reading and reporting.
    ```

### 4. Add knowledge sources

In the **Knowledge** tab:

- Click **Add knowledge**
- Select **SharePoint** and point to the initiative workspace folder
- Add the following files as knowledge sources:
  - `planning/workflow-state.json` — current stage and next action
  - `planning/open-decisions.md` — blocking decisions and owners

Do not add engineering artifacts, quality gate files, or technical design documents — the agent should report status, not interpret technical content.

### 5. Configure the Teams channel

- Click **Publish** in the top right
- Select **Microsoft Teams** as the channel
- Follow the wizard to add the agent to the relevant Teams team or channel
- The agent can be added to a dedicated **#delivery-status** channel or used as a personal app

### 6. Create a Teams trigger topic (optional)

To let stakeholders ask for status using natural language in Teams:

1. In Copilot Studio, go to **Topics** → **Add a topic** → **From blank**
2. Name the topic: **Status update**
3. Add trigger phrases:
   - "what is the status"
   - "where are we"
   - "what is blocking us"
   - "what decisions are open"
   - "what is the next step"
   - "are we on track"
4. Add a **Message** node that runs the status report format from the system prompt
5. Save and publish

### 7. Create a scheduled status report (optional — Power Automate)

To push a weekly status update automatically to a Teams channel:

1. Go to [make.powerautomate.com](https://make.powerautomate.com)
2. Click **Create** → **Scheduled cloud flow**
3. Set the schedule (e.g. every Monday at 9:00 AM)
4. Add a **SharePoint — Get file content** action for `planning/workflow-state.json`
5. Add a **SharePoint — Get file content** action for `planning/open-decisions.md`
6. Add a **Compose** action to format the status message in plain language (using the stage translation table from the system prompt)
7. Add a **Microsoft Teams — Post a message in a chat or channel** action
8. Point it at the relevant channel (e.g. `#delivery-status`)
9. Save and name the flow: `BRS Status — Weekly Report to Teams`

### 8. Test before rollout

1. Use the **Test** panel in Copilot Studio with a sample `workflow-state.json` that has a known stage
2. Verify the stage is translated correctly into business language
3. Add a test blocking decision to `planning/open-decisions.md` and verify it appears in the report
4. Test the "missing state file" scenario — verify the agent gives a clear action rather than an error

---

## See also

- [Extended Integration Architecture](copilot-studio-extended-integration.md)
- [How to Create the BRS Intake Assistant](how-to-create-m365-copilot-agent.md)
- [How to Create the Decision Capture Agent](how-to-create-decision-capture-agent.md)
- [How to Create the Gate Notification Agent](how-to-create-gate-notification-agent.md)
