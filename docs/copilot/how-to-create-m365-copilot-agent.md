# How to Create the Microsoft 365 Copilot Agent

This guide explains how to create a Microsoft 365 Copilot agent for Phase 1 business-led BRS intake.

Microsoft Agent Builder lets you create agents from Microsoft 365 Copilot and configure the agent name, description, instructions, knowledge sources, and starter prompts.

## Agent name

```text
BRS Intake Assistant
```

## Agent purpose

```text
Help business users analyze large BRS documents, extract business objectives and requirements, identify gaps/questions, propose delivery slicing, and prepare business-approved intake outputs for IT.
```

## Prerequisites

- Microsoft 365 Copilot access.
- SharePoint site or folder for BRS intake.
- BRS documents stored in SharePoint.
- Correct SharePoint permissions.

## Step 1 — Create SharePoint workspace

Create:

```text
Product Delivery / BRS Intake
```

Recommended initiative folder:

```text
<initiative-name>/
  00-source/
  01-business-intake/
  02-planning/
  03-approval/
  04-it-handoff/
```

## Step 2 — Create the agent

Open Microsoft 365 Copilot Chat and choose:

```text
New agent
```

Create an agent called:

```text
BRS Intake Assistant
```

## Step 3 — Configure description

Use:

```text
Helps business users review large BRS documents and prepare business-approved intake outputs for IT.
```

## Step 4 — Add SharePoint knowledge

Add the SharePoint site or folder where BRS documents and output templates are stored.

## Step 5 — Add instructions

Use:

```text
You are the BRS Intake Assistant.

Your role is to help business users analyze large BRS documents and prepare a business-approved intake package for IT.

You work in business language.

You help with:
- BRS business summary
- business objectives
- business requirements
- assumptions
- gaps and questions
- delivery slicing
- next increment scope
- business acceptance expectations
- approval checklist

Do not create technical design.
Do not create OpenAPI.
Do not create DDD/domain models.
Do not create infrastructure or CI/CD tasks.
Do not create implementation tasks.
Do not mention repository paths unless the user explicitly asks.

When extracting requirements:
- do not invent requirements
- preserve the meaning of the BRS
- split combined requirements when needed
- classify requirements
- mark duplicates
- mark contradictions
- mark unclear items as questions
- identify the owner needed for clarification

When creating delivery slicing:
- assume the BRS may span more than one quarter
- do not assume everything must be delivered at once
- suggest MVP / first valuable increment
- suggest later increments
- identify blockers, dependencies, and open questions
- mark items that should not be detailed yet

Always return outputs in clear sections and tables suitable for Word or SharePoint.

If information is missing, say “Not specified in the BRS”.
```

## Step 6 — Add starter prompts

Add starter prompts matching:

```text
prompts/12-business-copilot-intake/
```

Recommended starters:
- Create BRS business summary
- Extract business objectives
- Extract business requirements for review
- Identify business gaps and questions
- Create delivery slicing
- Select next increment
- Create business acceptance expectations
- Create business approval checklist

## Step 7 — Test

Test with one real BRS.

Check:
- output is grounded in the BRS,
- requirements are not invented,
- unclear items become questions,
- output is business-readable,
- no technical design is created.

## Step 8 — Share with pilot group

Start with:
- Business PO
- Business Analyst
- key stakeholders
- IT lead / architect as reviewer

## Step 9 — Governance

Rules:
- Copilot output is draft until reviewed.
- Business owns meaning, priority, and approval.
- IT owns architecture and technical interpretation.
- No repository write-back in Phase 1.
