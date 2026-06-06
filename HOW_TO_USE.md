# How to Use This Project

## 1. Create a feature

```bash
python tools/scripts/new_feature.py my-feature
```

## 2. Add the BRS and architecture

Paste converted BRS into:

```text
features/my-feature/input/brs-original.md
```

Paste draft architecture into:

```text
features/my-feature/input/architecture-draft.md
```

## 3. Run the Business Intake prompts

Use:

```text
prompts/01-business-intake/01-extract-business-requirements.md
prompts/01-business-intake/02-create-user-stories.md
prompts/01-business-intake/03-find-gaps-and-questions.md
```

Review:

```text
features/my-feature/quality-gates/business-ready-checklist.md
```

## 4. Run Engineering Contract prompts

Use:

```text
prompts/02-engineering-contracts/01-create-technical-spec.md
prompts/02-engineering-contracts/02-create-bdd-scenarios.md
prompts/02-engineering-contracts/03-create-test-strategy.md
```

Optional:

```text
prompts/02-engineering-contracts/04-create-test-plan.md
prompts/02-engineering-contracts/05-create-traceability-matrix.md
```

Review:

```text
features/my-feature/quality-gates/engineering-ready-checklist.md
```

## 5. Create OpenSpec handoff

Use:

```text
prompts/03-openspec-handoff/01-create-openspec-proposal.md
prompts/03-openspec-handoff/02-create-openspec-design.md
prompts/03-openspec-handoff/03-create-openspec-tasks.md
```

## 6. Ask Copilot to implement

Use:

```text
prompts/04-copilot-implementation/01-implement-one-task.md
```

Implement only one task at a time.

## 7. Review

Use:

```text
prompts/05-reviewers/01-senior-code-review.md
prompts/05-reviewers/02-qa-review.md
prompts/05-reviewers/03-architecture-review.md
prompts/05-reviewers/04-security-review.md
```

## 8. Validate project skeleton

```bash
python tools/scripts/check_program.py
```

## Main principle

The process is not meant to create documents for the sake of documents.

It is meant to create a safe bridge:

```text
Business BRS → Engineering Spec → OpenSpec Tasks → Copilot Implementation
```

# Which tool should I use?

## Business PO / BA

Use:

```text
Microsoft 365 Copilot
ChatGPT
another approved LLM
```

Run:

```text
prompts/01-business-intake/*
```

Create:

```text
business-intake/*
```

## Architect / Tech Lead / QA

Use:

```text
VS Code Copilot Chat
approved engineering LLM with repository context
```

Run:

```text
prompts/02-engineering-contracts/*
prompts/03-openspec-handoff/*
```

Create:

```text
engineering-contracts/*
openspec-change/*
```

## Developer

Use:

```text
VS Code Copilot Agent mode
GitHub Copilot Coding Agent
```

Run:

```text
prompts/04-copilot-implementation/*
```

## Reviewer

Use:

```text
GitHub PR review
VS Code Copilot Chat
ChatGPT or approved LLM with diff and context
```

Run:

```text
prompts/05-reviewers/*
```

# Epics and Features Step

After extracting requirements, run:

```text
prompts/01-business-intake/02a-create-epics-and-features.md
```

This creates:

```text
features/<feature-name>/business-intake/epics-and-features.md
```

Then run:

```text
prompts/01-business-intake/02-create-user-stories.md
```

The user stories should reference:

```text
Parent epic
Parent feature/capability
Related requirements
```

# Choose the Right Flow First

Before running the full prompt chain, classify the change.

Use:

```text
prompts/00-change-assessment/01-classify-change-size.md
```

Output:

```text
features/<feature-name>/quality-gates/change-size-assessment.md
```

## Small Change — Minimal Flow

Use when the change is low risk and clear.

Run:

```text
prompts/01-business-intake/01-extract-business-requirements.md
prompts/01-business-intake/02a-create-epics-and-features.md
prompts/01-business-intake/02-create-user-stories.md
prompts/01-business-intake/03-find-gaps-and-questions.md

prompts/02-engineering-contracts/01-create-technical-spec.md

prompts/03-openspec-handoff/01-create-openspec-proposal.md
prompts/03-openspec-handoff/02-create-openspec-design.md
prompts/03-openspec-handoff/03-create-openspec-tasks.md

prompts/04-copilot-implementation/01-implement-one-task.md
```

You may skip:

```text
business-test-expectations.md
bdd-scenarios.md
test-strategy.md
test-plan.md
traceability-matrix.md
```

unless they are useful.

## Medium Change — BDD + Test Strategy Flow

Use for normal feature work.

Run the small flow plus:

```text
prompts/02-engineering-contracts/02-create-bdd-scenarios.md
prompts/02-engineering-contracts/03-create-test-strategy.md
```

Optional:

```text
prompts/02-engineering-contracts/04-create-test-plan.md
prompts/02-engineering-contracts/05-create-traceability-matrix.md
```

## Large / Risky Change — Full Framework

Use for security-sensitive, audit-heavy, cross-system, regulated, or high-impact changes.

Run the full chain:

```text
prompts/01-business-intake/00-business-brs-summary.md
prompts/01-business-intake/01-extract-business-requirements.md
prompts/01-business-intake/02a-create-epics-and-features.md
prompts/01-business-intake/02-create-user-stories.md
prompts/01-business-intake/03-find-gaps-and-questions.md
prompts/01-business-intake/04-create-business-test-expectations.md

prompts/02-engineering-contracts/01-create-technical-spec.md
prompts/02-engineering-contracts/02-create-bdd-scenarios.md
prompts/02-engineering-contracts/03-create-test-strategy.md
prompts/02-engineering-contracts/04-create-test-plan.md
prompts/02-engineering-contracts/05-create-traceability-matrix.md

prompts/03-openspec-handoff/01-create-openspec-proposal.md
prompts/03-openspec-handoff/02-create-openspec-design.md
prompts/03-openspec-handoff/03-create-openspec-tasks.md

prompts/04-copilot-implementation/01-implement-one-task.md

prompts/05-reviewers/01-senior-code-review.md
prompts/05-reviewers/02-qa-review.md
prompts/05-reviewers/03-architecture-review.md
prompts/05-reviewers/04-security-review.md
```

## Practical rule

If unsure:

```text
Small vs Medium → choose Medium
Medium vs Large → choose Large only if risk is real
```

Do not overuse the large flow.

# Word BRS Extraction

If your starting point is a Word BRS, start here:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

Output:

```text
features/<feature-name>/input/brs-original.md
```

This step preserves the original BRS structure in Markdown.

Do not create user stories or technical design during this step.

# How to Use 02a and 02

## First use 02a

Run:

```text
prompts/01-business-intake/02a-create-epics-and-features.md
```

Input:

```text
business-intake/brs-summary.md
business-intake/requirements.md
```

Output:

```text
business-intake/epics-and-features.md
```

Purpose:

```text
Group requirements into business objectives, epics, and features/capabilities.
```

## Then use 02

Run:

```text
prompts/01-business-intake/02-create-user-stories.md
```

Input:

```text
business-intake/requirements.md
business-intake/epics-and-features.md
```

Output:

```text
business-intake/user-stories.md
```

Purpose:

```text
Create user stories and acceptance criteria under the correct epic and feature.
```

## Correct order

```text
requirements.md
  → epics-and-features.md
  → user-stories.md
```

Do not skip `epics-and-features.md` for medium or large changes.
