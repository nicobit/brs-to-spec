# Engineering User Guide

This guide is for architects, tech leads, developers, QA, and reviewers.

## Your goal

Your goal is to transform the approved business intake into engineering-ready contracts and OpenSpec implementation tasks.

## Tools you can use

Recommended:

```text
VS Code Copilot Chat
VS Code Copilot Agent mode
GitHub Copilot Coding Agent
Approved internal engineering LLM
```

Use tools that can inspect the repository when producing technical specs and tasks.

## What engineering produces

```text
engineering-contracts/technical-spec.md
engineering-contracts/bdd-scenarios.md
engineering-contracts/test-strategy.md
engineering-contracts/test-plan.md
engineering-contracts/traceability-matrix.md

openspec-change/proposal.md
openspec-change/design.md
openspec-change/tasks.md

code and tests
```

## Step-by-step

### Step 1 — Review business intake

Read:

```text
business-intake/requirements.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
business-intake/business-test-expectations.md
```

Do not continue if critical business questions are open.

### Step 2 — Create technical specification

Use:

```text
prompts/02-engineering-contracts/01-create-technical-spec.md
```

Prefer VS Code Copilot Chat so it can inspect existing code patterns.

### Step 3 — Create BDD scenarios

Use:

```text
prompts/02-engineering-contracts/02-create-bdd-scenarios.md
```

### Step 4 — Create test strategy and optional test plan

Use:

```text
prompts/02-engineering-contracts/03-create-test-strategy.md
prompts/02-engineering-contracts/04-create-test-plan.md
```

### Step 5 — Create OpenSpec handoff

Use:

```text
prompts/03-openspec-handoff/01-create-openspec-proposal.md
prompts/03-openspec-handoff/02-create-openspec-design.md
prompts/03-openspec-handoff/03-create-openspec-tasks.md
```

### Step 6 — Check readiness for Copilot

Complete:

```text
quality-gates/ready-for-copilot-checklist.md
```

### Step 7 — Implement one task at a time

Use:

```text
prompts/04-copilot-implementation/01-implement-one-task.md
```

Use Copilot Agent or Coding Agent.

### Step 8 — Review

Use:

```text
prompts/05-reviewers/
```

## Golden rule

OpenSpec is the implementation source of truth once engineering starts.

Business intake is upstream approved input, not a competing engineering spec.
