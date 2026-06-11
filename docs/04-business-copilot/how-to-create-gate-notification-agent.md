# How to Create the Gate Notification Agent

!!! note
    These steps reflect the Copilot Studio experience as of mid-2025. The UI may differ slightly depending on your Microsoft 365 tenant configuration and region.

## Design goals

The Gate Notification Agent alerts the right reviewer in Microsoft Teams when a quality gate artifact is ready for review, and captures their acceptance back into the artifact — without requiring the reviewer to open VS Code or edit markdown files. It should:

- detect when a quality gate artifact appears or changes in SharePoint with `Status: In progress`
- send a plain-language Teams notification to the reviewer named in the gate artifact
- capture the reviewer's acceptance and write `Status: Accepted` back to the artifact
- never generate gate content, never evaluate gate criteria, never advance the workflow itself

Quality gates that this agent handles:

| Gate | Artifact |
|---|---|
| BDD scenarios | `quality-gates/bdd-scenarios.md` |
| Test strategy | `quality-gates/test-strategy.md` |
| Security review | `quality-gates/security-review.md` |
| Threat model | `quality-gates/threat-model.md` |
| Data contract | `quality-gates/data-contract.md` |
| API contract | `quality-gates/api-contract.md` |
| Event contract | `quality-gates/event-contract.md` |
| Observability plan | `quality-gates/observability-plan.md` |
| QA review | `quality-gates/qa-review.md` |
| Release readiness review | `quality-gates/release-readiness-review.md` |

## Prerequisites

- Microsoft 365 licence with Copilot Studio access and Power Automate premium connectors
- SharePoint document library containing the initiative workspace
- Quality gate artifacts must exist in `quality-gates/` in SharePoint
- Permission to create agents and flows in your tenant
- Reviewers must have Microsoft Teams accounts

---

## Steps

### 1. Open Copilot Studio

Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) and sign in with your Microsoft 365 account.

### 2. Create a new agent

- Click **Create** in the left sidebar
- Select **New agent**
- Choose **Skip to configure** to set it up manually

### 3. Set the agent name and description

- **Name:** `Gate Review Assistant`
- **Description:** Notifies reviewers when quality gates are ready and captures acceptance
- **Instructions:** Copy the system prompt below and paste it into the Instructions field.

??? note "System prompt — Gate Review Assistant"

    ```text
    ## Who you are

    You are the Gate Review Assistant. You notify reviewers when a quality gate is ready
    for their review and capture their acceptance decision.

    You do not evaluate the quality gate content. You do not generate gate artifacts.
    You do not decide whether a gate passes or fails. You only present the gate summary
    to the reviewer and record their decision.

    ## How to present a gate for review

    When notifying a reviewer, present the gate like this:

    ---
    **Quality gate ready for your review**

    **Initiative:** [Initiative name]
    **Gate:** [Gate name in plain language — e.g. "Security Review", "Test Strategy"]
    **What it covers:** [One sentence summary of what was assessed]
    **Prepared by:** [Engineering team or engineer name]
    **Location:** [SharePoint link to the gate artifact]

    Please review the document at the link above. When you are satisfied it is complete
    and accurate, reply "Accept" or click the Accept button below.

    If you have concerns, reply with your feedback and the engineering team will be notified.
    ---

    ## How to capture acceptance

    When the reviewer replies "Accept" or equivalent:

    1. Confirm: "Thank you. I'll record your acceptance now.
       Gate: [gate name]
       Accepted by: [reviewer name]
       Date: [today's date]
       Is this correct?"

    2. Wait for confirmation.

    3. Update the gate artifact in SharePoint: change `Status: In progress` to `Status: Accepted`
       and append the acceptance record to the Metadata section.

    ## How to handle feedback

    If the reviewer replies with concerns or feedback instead of accepting:

    1. Record the feedback.
    2. Notify the engineering team in Teams: "Reviewer [name] has feedback on [gate name]:
       [feedback]. The gate remains In progress."
    3. Do not change the Status field.

    ## Rules that apply at all times

    - Never evaluate gate content yourself. You present and record — you do not judge.
    - Never mark a gate Accepted without explicit confirmation from the named reviewer.
    - Never advance the delivery workflow. Acceptance of a gate is recorded in the artifact;
      the engineering agent detects it on next invocation.
    - Plain language throughout. Do not reference stage numbers, filenames, or technical terms
      when communicating with reviewers.
    - If a reviewer asks what the gate means technically, say: "Please review the document
      directly and contact the engineering team if you need clarification on any technical detail."
    ```

### 4. Add knowledge sources

In the **Knowledge** tab:

- Click **Add knowledge**
- Select **SharePoint** and point to the `quality-gates/` folder in the initiative workspace
- This allows the agent to read gate artifact summaries when presenting them to reviewers

### 5. Create the Power Automate trigger flow

This flow watches for new or updated gate artifacts and fires the Teams notification.

#### Step A — Create the detection flow

1. Go to [make.powerautomate.com](https://make.powerautomate.com)
2. Click **Create** → **Automated cloud flow**
3. Choose **SharePoint — When a file is created or modified** as the trigger
4. Set:
   - **Site address:** your SharePoint site
   - **Library name:** the document library containing the initiative workspace
   - **Folder:** `quality-gates/`
5. Add a **SharePoint — Get file content** action to read the modified file
6. Add a **Condition** action:
   - Check if the file content contains `Status: In progress`
   - If yes: continue to the notification step
   - If no: terminate (do not notify for files already Accepted or not yet started)
7. Add a **SharePoint — Get file properties** action to extract:
   - Gate type (from filename or Metadata section)
   - Reviewer name (from the Reviewer field in the Metadata section)
   - Initiative name (from the file path)
8. Add a **Microsoft Teams — Post an Adaptive Card to a user** action:
   - **Recipient:** the reviewer's Teams account (looked up from the reviewer name)
   - **Card:** use the Adaptive Card template below

#### Adaptive Card template

```json
{
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "🔔 Quality gate ready for review",
      "weight": "Bolder",
      "size": "Medium"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Initiative", "value": "${initiativeName}" },
        { "title": "Gate", "value": "${gateName}" },
        { "title": "What it covers", "value": "${gateSummary}" },
        { "title": "Prepared by", "value": "${preparedBy}" }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "Open in SharePoint",
      "url": "${sharePointUrl}"
    },
    {
      "type": "Action.Submit",
      "title": "Accept",
      "data": { "action": "accept", "gateId": "${gateId}" }
    },
    {
      "type": "Action.Submit",
      "title": "Send feedback",
      "data": { "action": "feedback", "gateId": "${gateId}" }
    }
  ]
}
```

9. Save and name the flow: `BRS Gate — Detect Ready and Notify Reviewer`

### 6. Create the acceptance write-back flow

This flow handles the reviewer's response from the Adaptive Card.

1. Create a new flow triggered by **When Copilot Studio calls a flow** (or **When an adaptive card response is submitted**)
2. Add input parameters:
   - `gateFilePath` (string) — full path to the gate artifact in SharePoint
   - `reviewerName` (string) — name of the reviewer
   - `acceptanceDate` (string) — today's date
   - `action` (string) — `accept` or `feedback`
   - `feedbackText` (string) — reviewer's feedback if action = feedback
3. Add a **Condition**: if `action` = `accept`:
   - **SharePoint — Get file content** to read the current gate artifact
   - **Compose** to replace `Status: In progress` with `Status: Accepted` and append:
     ```
     | Accepted by | [reviewerName] |
     | Accepted on | [acceptanceDate] |
     ```
   - **SharePoint — Update file** to write the updated content back
4. If `action` = `feedback`:
   - **Microsoft Teams — Post a message** to the engineering channel with the feedback text
   - Do not modify the gate artifact
5. Save and name the flow: `BRS Gate — Write Back Acceptance`

### 7. Connect the write-back flow to the agent

1. In Copilot Studio, open the **Gate Review Assistant** agent
2. Go to **Topics** → create a topic called **Accept gate**
3. Trigger phrases: "accept", "I accept", "looks good", "approved"
4. Add an **Action** node → **Call an action** → **Power Automate flows**
5. Choose the write-back flow from Step 6
6. Pass the gate file path and reviewer name (captured earlier in the conversation)
7. Add a confirmation message: "Gate accepted. The engineering team has been notified and will continue."

### 8. Configure the Teams channel

- Click **Publish** in the top right
- Select **Microsoft Teams** as the channel
- The agent is used as a **personal app** — reviewers interact with it one-on-one, not in a shared channel
- Add the agent to reviewer accounts: Security, QA, Architecture, Business approval roles

### 9. Test before rollout

1. Create a test gate artifact with `Status: In progress` in the `quality-gates/` folder in SharePoint
2. Verify the detection flow fires and sends the Adaptive Card in Teams to the correct reviewer
3. Click **Accept** on the Adaptive Card and verify:
   - The gate artifact is updated to `Status: Accepted` in SharePoint
   - The acceptance record is appended to the Metadata section
4. Test the feedback path — click **Send feedback**, enter text, verify the engineering channel receives the message and the gate artifact is unchanged
5. Verify the engineering agent reads the updated status on next invocation and advances the workflow

---

## See also

- [Extended Integration Architecture](copilot-studio-extended-integration.md)
- [How to Create the BRS Intake Assistant](how-to-create-m365-copilot-agent.md)
- [How to Create the Decision Capture Agent](how-to-create-decision-capture-agent.md)
- [How to Create the Status Query Agent](how-to-create-status-query-agent.md)
