# How to Create the Decision Capture Agent

!!! note
    These steps reflect the Copilot Studio experience as of mid-2025. The UI may differ slightly depending on your Microsoft 365 tenant configuration and region.

## Design goals

The agent — named **Delivery Decision Assistant** — lets business stakeholders (PO, legal, compliance, vendors) answer open decisions that are blocking engineering progress, directly from Microsoft Teams. It should:

- present one open decision at a time in plain business language
- capture the stakeholder's answer in a structured format
- save the answer to `input/input-package.md` in SharePoint so the engineering agent can read it on next invocation
- never make decisions on behalf of the stakeholder, never generate artifacts, never touch the initiative workspace directly

It is **not** an engineering assistant. It must not generate code, create framework artifacts, or advance the delivery workflow itself.

## Prerequisites

- Microsoft 365 licence with Copilot Studio access
- SharePoint document library containing the initiative workspace (the `initiatives/<id>-<slug>/` folder structure)
- Power Automate premium connectors (for automatic read/write to SharePoint)
- Permission to create agents in your tenant
- The initiative's `planning/open-decisions.md` file must already exist in SharePoint

---

## Steps

### 1. Open Copilot Studio

Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) and sign in with your Microsoft 365 account.

### 2. Create a new agent

- Click **Create** in the left sidebar
- Select **New agent**
- Choose **Skip to configure** to set it up manually

### 3. Set the agent name and description

- **Name:** `Delivery Decision Assistant`
- **Description:** Captures open decisions from business stakeholders during active delivery initiatives
- **Instructions:** Copy the system prompt below and paste it into the Instructions field.

??? note "System prompt — Delivery Decision Assistant"

    ```text
    ## Who you are

    You are the Delivery Decision Assistant. Your job is to help business stakeholders
    answer open questions that are blocking engineering progress — quickly and clearly,
    without requiring them to use any engineering tools.

    You do not modify initiative files directly. You do not create artifacts. You do not
    make decisions on behalf of the stakeholder. You capture their answer and save it so
    engineering can proceed.

    ## How to open the conversation

    When a user starts a conversation, greet them and explain what you do:

    "I have an open decision that needs your input before the engineering team can
    continue. I'll present it to you in plain language, capture your answer, and make
    sure it reaches the right people. This should take less than two minutes."

    Then present the open decision using the format below.

    ## How to present an open decision

    Present each decision like this:

    ---
    **Decision needed from you**

    **Question:** [Plain language version of the decision — no engineering jargon]
    **Why it matters:** [Business impact if left unresolved — one sentence]
    **Options:** [List options if the decision has discrete choices — omit if open-ended]
    **Needed before:** [Stage or date — in business terms]
    ---

    Wait for the stakeholder's answer.

    ## How to confirm and save

    Once the stakeholder answers, confirm before saving:

    "Thank you. I'll record your answer as:

    **Decision:** [restate what they said in one clear sentence]
    **Decided by:** [their name]
    **Date:** [today's date]

    Is this correct?"

    Wait for confirmation. If they say yes, save the answer using the output format below.
    If they want to change something, update and confirm again before saving.

    ## Output format

    Append the following row to the "Decisions and Clarifications Received" section of
    `input/input-package.md` in SharePoint:

    | Decision ID | Question | Answer | Decided by | Date |
    |---|---|---|---|---|
    | [ID] | [question in plain language] | [answer] | [name] | [date] |

    ## Rules that apply at all times

    - One decision at a time. Do not present multiple decisions in one conversation.
    - Never invent an answer. If the stakeholder is unsure, record:
      "Pending — [reason stakeholder gave]" and note that engineering will follow up.
    - Use business language. Do not reference technical artifacts, filenames, or stage numbers.
    - Never create files, folders, or framework artifacts.
    - Never advance the delivery workflow. Your only output is the answer row in input-package.md.
    - If the stakeholder asks about engineering details, say:
      "That is a question for the engineering team. I am here only to capture your decision."

    ## Re-entry and continuation

    If a user returns to answer a different decision:
    - Greet them and present the next open decision directly.
    - Do not repeat decisions already answered in a previous session.
    ```

### 4. Add knowledge sources

In the **Knowledge** tab:

- Click **Add knowledge**
- Select **SharePoint** and point to the initiative workspace folder in your SharePoint library
- Add `planning/open-decisions.md` as a knowledge source so the agent can read current open decisions

Do not add engineering artifacts, code repositories, or technical design documents.

### 5. Add the SharePoint write action (Power Automate)

The agent needs to append the decision answer to `input/input-package.md` in SharePoint. This requires a Power Automate flow.

#### Step A — Create the Power Automate flow

1. Go to [make.powerautomate.com](https://make.powerautomate.com) and sign in
2. Click **Create** → **Instant cloud flow**
3. Choose **When Copilot Studio calls a flow** as the trigger
4. Add the following input parameters to the trigger:
   - `decisionId` (string) — the decision ID from open-decisions.md (e.g. `D-005`)
   - `question` (string) — the question in plain language
   - `answer` (string) — the stakeholder's answer
   - `decidedBy` (string) — the stakeholder's name
   - `decisionDate` (string) — today's date
   - `filePath` (string) — full path to `input/input-package.md` in SharePoint
5. Add a **SharePoint — Get file content** action to read the current content of `input/input-package.md`
6. Add a **Compose** action to append the new row to the "Decisions and Clarifications Received" table
7. Add a **SharePoint — Update file** action to write the updated content back
8. Save and name the flow: `BRS Decision Capture — Append to Input Package`

#### Step B — Connect the flow to the agent

1. In Copilot Studio, open the **Delivery Decision Assistant** agent
2. Go to **Topics** and open (or create) the topic for decision confirmation
3. After the confirmation step, add an **Action** node
4. Select **Call an action** → **Power Automate flows**
5. Choose the flow created in Step A
6. Map the agent's captured values to the flow input parameters
7. Add a message node: "Your answer has been saved. The engineering team will be notified."

#### Step C — Test the flow

1. Use the **Test** panel in Copilot Studio to run through a sample decision conversation
2. After confirmation, verify that the row appears in `input/input-package.md` in SharePoint
3. Check that the decision ID, answer, name, and date are correct

### 6. Configure the Teams channel

- Click **Publish** in the top right
- Select **Microsoft Teams** as the channel
- Follow the wizard to add the agent to the relevant Teams team or channel
- Restrict access to business stakeholders — this agent is not for engineering team members

### 7. Wire the trigger (optional — Power Automate)

To automatically notify the decision owner in Teams when a new blocking decision is added to `planning/open-decisions.md`:

1. Create a Power Automate flow triggered by **SharePoint — When a file is modified**
2. Point it at `planning/open-decisions.md` in your initiative workspace
3. Parse the file for new rows where `Blocking = Yes` and `Status = Open`
4. For each new blocking decision, send an Adaptive Card in Teams to the owner listed in the decision row:

```
🔔 Decision needed — [Initiative name]

[Question in plain language]
Why it matters: [impact]
Needed before: [stage or date]

[Open Decision Assistant]
```

5. The Adaptive Card button opens the Delivery Decision Assistant in Teams

### 8. Test before rollout

1. Add a test blocking decision to `planning/open-decisions.md`
2. Verify the Teams notification fires and links to the agent
3. Run through the full conversation in the Test panel
4. Confirm the answer appears correctly in `input/input-package.md`
5. Verify the engineering agent reads the answer on next invocation

---

## See also

- [Extended Integration Architecture](copilot-studio-extended-integration.md)
- [How to Create the BRS Intake Assistant](how-to-create-m365-copilot-agent.md)
- [How to Create the Status Query Agent](how-to-create-status-query-agent.md)
- [How to Create the Gate Notification Agent](how-to-create-gate-notification-agent.md)
