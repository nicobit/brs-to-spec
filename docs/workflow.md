# Full Workflow

## Phase 0 — Input preparation

Inputs:

```text
BRS Word document
Draft architecture
Existing codebase
Existing coding standards
Existing QA approach
```

Convert the Word document to Markdown before using the prompts.

## Phase 1 — Business Intake

Owner: Business PO / BA  
Reviewers: Product Owner, QA, Tech Lead if needed

Artifacts:

```text
business-intake/brs-summary.md
business-intake/requirements.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
business-intake/business-test-expectations.md
```

Purpose:

- Clarify the business intent.
- Extract functional and non-functional requirements.
- Create user stories and acceptance criteria.
- Identify unresolved business decisions.
- Avoid implementing from ambiguous BRS text.

Exit gate:

```text
quality-gates/business-ready-checklist.md
```

## Phase 2 — Engineering Contracts

Owner: Tech Lead / Architect  
Reviewers: QA, Security, DB Lead, relevant engineers

Artifacts:

```text
engineering-contracts/technical-spec.md
engineering-contracts/bdd-scenarios.md
engineering-contracts/architecture-contract.md
engineering-contracts/api-event-contracts.md
engineering-contracts/test-strategy.md
engineering-contracts/test-plan.md
engineering-contracts/traceability-matrix.md
```

Purpose:

- Translate business intent into technical constraints.
- Define component responsibilities.
- Define behavior through BDD scenarios.
- Define API/event/data impact.
- Define test approach.
- Prevent Copilot from inventing architecture.

Exit gate:

```text
quality-gates/engineering-ready-checklist.md
```

## Phase 3 — OpenSpec Change

Owner: Engineering Lead  
Reviewers: Architect, QA, Product Owner if needed

Artifacts:

```text
openspec-change/proposal.md
openspec-change/design.md
openspec-change/tasks.md
openspec-change/specs/
```

Purpose:

- Create the engineering implementation source of truth.
- Keep implementation tasks small.
- Use an OpenSpec-like change lifecycle.

Critical rule:

```text
After the OpenSpec change is approved, implementation follows OpenSpec tasks.
Business intake remains upstream evidence, not a parallel implementation spec.
```

## Phase 4 — Copilot Implementation

Owner: Engineer  
Assistant: GitHub Copilot

Rules:

- Implement one task at a time.
- Read business intake and engineering contracts first.
- Follow OpenSpec `tasks.md`.
- Do not change unrelated files.
- Add tests.
- Provide traceability summary.

## Phase 5 — Review and Validation

Review dimensions:

- Business coverage
- Architecture compliance
- Security and authorization
- Audit and logging
- Test coverage
- Backward compatibility
- No unrelated refactoring

## Phase 6 — Archive / Close

After implementation:

- Update task statuses.
- Update traceability matrix.
- Archive or mark OpenSpec change complete.
- Capture lessons learned.

# Prompt Execution Responsibility

| Phase | Prompt Folder | Owner | Recommended Tool |
|---|---|---|---|
| Business Intake | `prompts/01-business-intake` | Business PO / BA | Microsoft 365 Copilot, ChatGPT, or approved LLM |
| Engineering Contracts | `prompts/02-engineering-contracts` | Architect / Tech Lead / QA | VS Code Copilot Chat |
| OpenSpec Handoff | `prompts/03-openspec-handoff` | Engineering Lead | VS Code Copilot Chat |
| Implementation | `prompts/04-copilot-implementation` | Developer | VS Code Copilot Agent / Coding Agent |
| Review | `prompts/05-reviewers` | Reviewer / QA / Architect / Security | PR review + Copilot Chat |

## Updated Planning Hierarchy

The business intake now uses this hierarchy:

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

Requirements are not the same as epics or features.

- Requirements describe obligations or expected behavior.
- Epics group a large business outcome.
- Features/capabilities organize deliverable product functionality.
- User stories describe user-centered delivery increments.

# Flow Selection

The workflow is scalable.

## Small change

```text
BRS/change description
 → requirements
 → epics/features
 → user stories
 → gaps
 → lightweight technical spec
 → OpenSpec proposal/design/tasks
 → Copilot task
 → code review
```

## Medium change

```text
Small flow
 + BDD scenarios
 + test strategy
```

## Large/risky change

```text
Full business intake
 + full engineering contracts
 + test plan
 + traceability matrix
 + quality gates
 + reviewer prompts
```

## Governance principle

Use the smallest flow that controls the real risk.
