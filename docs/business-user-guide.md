# Business User Guide

This guide is for Business Product Owners, Business Analysts, and SMEs.

## Your goal

Your goal is not to create code.  
Your goal is to create a clear, reviewed business intake package that engineering can safely use.

## Tools you can use

You can use any company-approved tool, for example:

```text
Microsoft 365 Copilot
ChatGPT
An approved internal LLM
GitHub Copilot Chat, if available
```

Use the tool that is approved for your data classification.

## What you produce

You produce these artifacts:

```text
business-intake/brs-summary.md
business-intake/requirements.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
business-intake/business-test-expectations.md
```

## What you do not produce

You do not produce:

```text
technical architecture
database scripts
API implementation
OpenSpec implementation tasks
code
```

Those are engineering responsibilities.

## Step-by-step

### Step 1 — Prepare the BRS

Start from the Word BRS.  
Export or copy the content into a text/Markdown format.

Save it as:

```text
features/<feature-name>/input/brs-original.md
```

### Step 2 — Summarize the BRS

Use:

```text
prompts/01-business-intake/01-summarize-brs.md
```

Output:

```text
business-intake/brs-summary.md
```

### Step 3 — Extract requirements

Use:

```text
prompts/01-business-intake/02-extract-requirements.md
```

Output:

```text
business-intake/requirements.md
```

### Step 4 — Create user stories and acceptance criteria

Use:

```text
prompts/01-business-intake/05-create-user-stories.md
```

Output:

```text
business-intake/user-stories.md
```

### Step 5 — Identify gaps and questions

Use:

```text
prompts/01-business-intake/06-find-gaps-and-questions.md
```

Output:

```text
business-intake/gaps-and-questions.md
```

### Step 6 — Create business test expectations

Use:

```text
prompts/01-business-intake/07-create-business-test-expectations.md
```

Output:

```text
business-intake/business-test-expectations.md
```

### Step 7 — Review manually

Complete:

```text
quality-gates/business-ready-checklist.md
```

## Business ready means

Engineering can continue only when:

```text
business objective is clear
main users are identified
requirements are clear
user stories are testable
critical gaps are resolved
remaining assumptions are accepted
```

## Golden rule

If the LLM invented something that is not in the BRS or not agreed by business, remove it or mark it as an assumption.

## Epics and features

After extracting requirements, create the delivery structure:

```text
prompts/01-business-intake/04-create-delivery-structure.md
```

This produces:

```text
business-intake/epics-and-features.md
```

Use this to organize the BRS into:

```text
Business Objectives
Epics
Features / Capabilities
Requirement-to-feature mapping
Delivery slicing recommendations
```

Important:

```text
Requirements are not epics.
Requirements describe what must be true.
Epics and features organize delivery.
```

# Word BRS Extraction

When the input is a Word document, start with:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

The purpose is to create:

```text
features/<feature-name>/input/brs-original.md
```

This is not a summarization step. It is a faithful extraction step.

After that, continue with:

```text
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
```

## How to use 04

`04-create-delivery-structure.md` groups requirements into:

```text
Business objectives
Epics
Features / capabilities
Requirement-to-feature mapping
Delivery slicing recommendations
```

Use it after requirements and before user stories.

## How to use 02

`05-create-user-stories.md` creates user stories under the features from `epics-and-features.md`.

Each story should have:

```text
Parent epic
Parent feature
Requirements covered
Acceptance criteria
```
