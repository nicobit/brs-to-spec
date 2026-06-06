# Enterprise SDD + OpenSpec + Copilot Delivery Kit

A practical project template for moving from a **Business Requirements Specification (BRS)** and a draft architecture to **safe, traceable AI-assisted implementation with GitHub Copilot**.

This kit is intentionally split into three layers:

```text
Layer 1 — Business Intake
Business PO / BA / Product Owner
BRS → requirements → user stories → acceptance criteria → gaps

Layer 2 — Engineering Contracts
Architect / Tech Lead / QA
requirements → domain model → BDD → architecture contract → test expectations

Layer 3 — OpenSpec + Copilot Implementation
Engineers / Copilot
proposal → design → tasks → implementation → review → archive
```

## Why this exists

Do **not** ask Copilot to implement directly from a Word BRS.

Instead, use this flow:

```text
BRS in Word
  ↓
Business Intake Package
  ↓
Engineering Contract Package
  ↓
OpenSpec Change
  ↓
Copilot Task-by-Task Implementation
  ↓
Human Review + QA Validation
```

## Recommended pilot mode

For the first real pilot, use only the minimum artifacts:

```text
business-intake/
  brs-summary.md
  requirements.md
  user-stories.md
  gaps-and-questions.md

engineering-contracts/
  technical-spec.md
  bdd-scenarios.md

openspec-change/
  proposal.md
  design.md
  tasks.md
```

Add full test plan, formal JSON contracts, and traceability matrix only when the feature is risky, regulated, audit-heavy, or cross-system.

## Folder overview

```text
.github/
  copilot-instructions.md
  workflows/validate-sdd.yml

docs/
  workflow.md
  pilot-quickstart.md
  roles-and-responsibilities.md
  artifact-decision-guide.md
  stop-conditions.md
  openspec-handoff.md
  copilot-usage.md

prompts/
  01-business-intake/
  02-engineering-contracts/
  03-openspec-handoff/
  04-copilot-implementation/
  05-reviewers/

templates/
  business-intake/
  engineering-contracts/
  openspec-change/
  quality-gates/
  reviews/
  copilot/

schemas/
  JSON Schemas for optional structured validation

tools/scripts/
  Helper scripts for creating features and validating artifacts

examples/
  onboarding-feature/
```

## Quick start

```bash
python tools/scripts/new_feature.py onboarding-client-approval
```

Then copy the BRS and draft architecture into:

```text
features/onboarding-client-approval/input/brs-original.md
features/onboarding-client-approval/input/architecture-draft.md
```

Use the prompts in order:

```text
prompts/01-business-intake/
prompts/02-engineering-contracts/
prompts/03-openspec-handoff/
prompts/04-copilot-implementation/
prompts/05-reviewers/
```

## Golden rule

```text
Business Intake is the upstream approved input.
OpenSpec is the engineering implementation source of truth.
Copilot implements only one reviewed task at a time.
```

## Prompt execution environments

Business users can run the business intake prompts using:

```text
Microsoft 365 Copilot
ChatGPT
An approved internal LLM
GitHub Copilot Chat, if available
```

Engineering prompts should be run in tools that can access the repository, preferably:

```text
VS Code Copilot Chat
VS Code Copilot Agent mode
GitHub Copilot Coding Agent
```

Read:

```text
docs/prompt-execution-environments.md
docs/business-user-guide.md
docs/engineering-user-guide.md
```

## Delivery hierarchy

The project now includes an explicit split before user stories:

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
  ↓
Acceptance Criteria
  ↓
BDD Scenario
  ↓
Test Case
  ↓
OpenSpec Task
  ↓
Code
```

The new artifact is:

```text
business-intake/epics-and-features.md
```

The new prompt is:

```text
prompts/01-business-intake/02a-create-epics-and-features.md
```

Read:

```text
docs/delivery-hierarchy.md
```

# Change Size Modes

Do not use the full framework for every change.

Use the flow that matches the risk and complexity.

## 1. Small Change — Minimal Flow

Use for simple, low-risk changes.

Examples:

```text
small UI text change
simple validation rule
minor bug fix with clear expected behavior
small configuration change
```

Required artifacts:

```text
business-intake/
  requirements.md
  epics-and-features.md
  user-stories.md
  gaps-and-questions.md

engineering-contracts/
  technical-spec.md

openspec-change/
  proposal.md
  design.md
  tasks.md
```

## 2. Medium Change — BDD + Test Strategy Flow

Use for normal feature work.

Examples:

```text
new feature in existing module
moderate backend + frontend change
workflow step
role-based behavior
non-trivial validation
```

Required artifacts:

```text
Small change artifacts
+
engineering-contracts/
  bdd-scenarios.md
  test-strategy.md
```

Optional:

```text
test-plan.md
traceability-matrix.md
```

## 3. Large / Risky Change — Full Framework

Use for high-risk enterprise work.

Examples:

```text
client-data-impacting feature
audit/compliance-heavy feature
security-sensitive change
cross-system integration
database migration with risk
major architecture change
external API/event contract
multi-team delivery
```

Required artifacts:

```text
business-intake/
  brs-summary.md
  requirements.md
  epics-and-features.md
  user-stories.md
  gaps-and-questions.md
  business-test-expectations.md

engineering-contracts/
  technical-spec.md
  bdd-scenarios.md
  test-strategy.md
  test-plan.md
  traceability-matrix.md

openspec-change/
  proposal.md
  design.md
  tasks.md

quality-gates/
  business-ready-checklist.md
  engineering-ready-checklist.md
  ready-for-copilot-checklist.md
```

## First step for every change

Run or manually complete:

```text
prompts/00-change-assessment/01-classify-change-size.md
templates/quality-gates/change-size-assessment.md
```

Read:

```text
docs/change-size-decision-model.md
```

# Word BRS Extraction and Business Intake Clarification

The project now includes a dedicated Word-BRS extraction prompt:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

Use it before summarization and requirement extraction when the source is a Word document.

The recommended early business flow is:

```text
Word BRS
  ↓
00a-extract-brs-from-word.md
  ↓
00-business-brs-summary.md
  ↓
01-extract-business-requirements.md
  ↓
02a-create-epics-and-features.md
  ↓
02-create-user-stories.md
```

The relationship is:

```text
Requirements describe what must be true.
Epics and features organize delivery.
User stories describe user-centered increments with acceptance criteria.
```

Read:

```text
docs/business-intake-step-guide.md
```
