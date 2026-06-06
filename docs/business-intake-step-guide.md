# Business Intake Step Guide

This guide explains the early business-intake steps:

```text
Word BRS
  ↓
00a Extract BRS from Word
  ↓
00 Business BRS Summary
  ↓
01 Extract Business Requirements
  ↓
02a Create Epics and Features
  ↓
02 Create User Stories
  ↓
03 Find Gaps and Questions
  ↓
04 Create Business Test Expectations
```

## Step 00a — Extract BRS from Word

Prompt:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

Purpose:

Convert the Word BRS into a clean Markdown input file.

Output:

```text
features/<feature-name>/input/brs-original.md
```

Use this when the source is a Word document, SharePoint document, Teams file, or copied Word content.

Important:

```text
This step is extraction, not interpretation.
```

Do not create user stories, epics, technical design, or implementation tasks here.

## Step 00 — Summarize BRS

Prompt:

```text
prompts/01-business-intake/00-business-brs-summary.md
```

Purpose:

Create a concise business summary from the extracted BRS.

Output:

```text
features/<feature-name>/business-intake/brs-summary.md
```

This helps reviewers understand the business context before detailed requirement extraction.

## Step 01 — Extract Business Requirements

Prompt:

```text
prompts/01-business-intake/01-extract-business-requirements.md
```

Purpose:

Create formal requirements from the BRS.

Output:

```text
features/<feature-name>/business-intake/requirements.md
```

Requirements describe what must be true.

Examples:

```text
FR-001 — The system shall allow authorized users to create an onboarding request.
SEC-001 — Only users with Relationship Manager role may create onboarding requests.
AUD-001 — Every status change must be auditable.
```

Important:

```text
Requirements are not epics.
Requirements are not implementation tasks.
Requirements are obligations, rules, behaviors, constraints, and qualities.
```

## Step 02a — Create Epics and Features

Prompt:

```text
prompts/01-business-intake/02a-create-epics-and-features.md
```

Purpose:

Group the requirements into a delivery structure.

Output:

```text
features/<feature-name>/business-intake/epics-and-features.md
```

This step answers:

```text
What are the business objectives?
What are the epics?
What are the features/capabilities?
Which requirements belong to which feature?
What is the recommended delivery slicing?
```

### When to use it

Always use it for medium and large/risky changes.

For small changes, keep it lightweight. One epic and one feature may be enough.

### Why it comes before user stories

Do not create user stories directly from raw requirements.

First organize the work:

```text
Business Objective
  ↓
Epic
  ↓
Feature / Capability
  ↓
Requirement
  ↓
User Story
```

### Example

Requirements:

```text
FR-001 — Create onboarding request
FR-002 — Approve onboarding request
SEC-001 — Only Relationship Managers can create requests
SEC-002 — Only Compliance users can approve requests
AUD-001 — Every status change must be auditable
```

Epics and features:

```text
BO-001 — Improve onboarding control and auditability

EPIC-001 — Client Onboarding Workflow

FEAT-001 — Onboarding Request Creation
FEAT-002 — Compliance Approval
FEAT-003 — Audit Trail
```

Requirement mapping:

| Requirement ID | Requirement Title | Epic | Feature |
|---|---|---|---|
| FR-001 | Create onboarding request | EPIC-001 | FEAT-001 |
| FR-002 | Approve onboarding request | EPIC-001 | FEAT-002 |
| SEC-001 | Role-based creation | EPIC-001 | FEAT-001 |
| SEC-002 | Role-based approval | EPIC-001 | FEAT-002 |
| AUD-001 | Audit status changes | EPIC-001 | FEAT-001, FEAT-002, FEAT-003 |

## Step 02 — Create User Stories

Prompt:

```text
prompts/01-business-intake/02-create-user-stories.md
```

Purpose:

Create user-centered delivery slices with acceptance criteria.

Output:

```text
features/<feature-name>/business-intake/user-stories.md
```

Input:

```text
features/<feature-name>/business-intake/requirements.md
features/<feature-name>/business-intake/epics-and-features.md
```

Each user story must reference:

```text
Parent epic
Parent feature/capability
Related requirements
Acceptance criteria
```

### Example user story

```markdown
## US-001 — Create onboarding request

Parent epic:
- EPIC-001 — Client Onboarding Workflow

Parent feature:
- FEAT-001 — Onboarding Request Creation

As a Relationship Manager,  
I want to create an onboarding request,  
so that the client onboarding process can start.

### Requirements Covered
- FR-001
- DATA-001
- SEC-001
- AUD-001

### Acceptance Criteria

#### AC-001 — Successful creation
Given I am a Relationship Manager  
And I enter all mandatory fields  
When I submit the onboarding request  
Then the system creates the request  
And an audit event is recorded.

#### AC-002 — Missing mandatory fields
Given I am a Relationship Manager  
When I submit the request without mandatory fields  
Then validation errors are shown  
And the request is not created.

#### AC-003 — Unauthorized user
Given I am not a Relationship Manager  
When I try to create an onboarding request  
Then access is denied.
```

## Common mistakes

### Mistake 1 — Treating requirements as epics

Wrong:

```text
FR-001 becomes EPIC-001
FR-002 becomes EPIC-002
SEC-001 becomes EPIC-003
```

Correct:

```text
EPIC-001 — Client Onboarding Workflow
  FEAT-001 — Request Creation
    FR-001, DATA-001, SEC-001, AUD-001
  FEAT-002 — Compliance Approval
    FR-002, SEC-002, AUD-001
```

### Mistake 2 — Creating user stories before understanding features

Wrong:

```text
BRS → user stories
```

Correct:

```text
BRS → requirements → epics/features → user stories
```

### Mistake 3 — User stories without acceptance criteria

Every user story must include testable acceptance criteria.

### Mistake 4 — Business users creating implementation tasks

Business users should create business intake artifacts only.

Engineering creates OpenSpec tasks later.

## Output chain

```text
input/brs-original.md
business-intake/brs-summary.md
business-intake/requirements.md
business-intake/epics-and-features.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
business-intake/business-test-expectations.md
```
