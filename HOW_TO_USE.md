# Canonical Business Intake Sequence

Run the business intake prompts in this order:

```text
00a-extract-brs-from-word.md
00b-extract-architecture-from-word.md
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
07-create-business-test-expectations.md
```

The critical order is:

```text
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
```

Do not create the delivery structure before reviewing the BRS and extracted requirements against the architecture draft, unless no architecture input exists and the change is explicitly classified as small/no-architecture-impact.

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
prompts/01-business-intake/02-extract-requirements.md
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/06-find-gaps-and-questions.md
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
prompts/01-business-intake/04-create-delivery-structure.md
```

This creates:

```text
features/<feature-name>/business-intake/epics-and-features.md
```

Then run:

```text
prompts/01-business-intake/05-create-user-stories.md
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
prompts/01-business-intake/02-extract-requirements.md
prompts/01-business-intake/04-create-delivery-structure.md
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/06-find-gaps-and-questions.md

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
prompts/01-business-intake/01-summarize-brs.md
prompts/01-business-intake/02-extract-requirements.md
prompts/01-business-intake/04-create-delivery-structure.md
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/06-find-gaps-and-questions.md
prompts/01-business-intake/07-create-business-test-expectations.md

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

# How to Use 04 and 02

## First use 04

Run:

```text
prompts/01-business-intake/04-create-delivery-structure.md
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
prompts/01-business-intake/05-create-user-stories.md
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

# Optional Architecture Document Extraction

If you also have a Word architecture document, run:

```text
prompts/01-business-intake/00b-extract-architecture-from-word.md
```

Output:

```text
features/<feature-name>/input/architecture-draft.md
```

This step preserves the architecture draft in Markdown.

# Review BRS and Requirements Against Architecture

After extracting the BRS and architecture draft, run:

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

Output:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Use this to identify:

```text
BRS/requirements vs architecture contradictions
missing architecture decisions
integration gaps
data gaps
security gaps
audit/logging gaps
deployment/environment gaps
questions for business and architecture
```

# Updated early order

Recommended order when both BRS and architecture documents exist:

```text
00a-extract-brs-from-word.md
00b-extract-architecture-from-word.md
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
```

# Updated Business Intake Sequence

Use this sequence now:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
prompts/01-business-intake/00b-extract-architecture-from-word.md
prompts/01-business-intake/01-summarize-brs.md
prompts/01-business-intake/02-extract-requirements.md
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
prompts/01-business-intake/04-create-delivery-structure.md
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/06-find-gaps-and-questions.md
prompts/01-business-intake/07-create-business-test-expectations.md
```

The old confusing `02a` step has been renamed to:

```text
04-create-delivery-structure.md
```

Use it before user stories to organize requirements into:

```text
Business Objective → Epic → Feature / Capability
```

Then run:

```text
05-create-user-stories.md
```

# Optional Enablement Track

Use the Enablement Track when the feature requires infrastructure, CI/CD, environment, observability, release, rollback, or operational work.

## Step 1 — Identify enablement scope

```text
prompts/08-enablement/01-identify-enablement-scope.md
```

Output:

```text
features/<feature-name>/enablement/enablement-scope.md
```

## Step 2 — Create enablement structure

```text
prompts/08-enablement/02-create-enablement-structure.md
```

Output:

```text
features/<feature-name>/enablement/enablement-structure.md
```

## Step 3 — Create technical stories

```text
prompts/08-enablement/03-create-technical-stories.md
```

Output:

```text
features/<feature-name>/enablement/technical-stories.md
```

## Step 4 — Create infrastructure / CI-CD / operational specs as needed

```text
prompts/08-enablement/04-create-infrastructure-spec.md
prompts/08-enablement/05-create-cicd-spec.md
prompts/08-enablement/06-create-operational-readiness.md
```

Outputs:

```text
features/<feature-name>/enablement/infrastructure-spec.md
features/<feature-name>/enablement/cicd-spec.md
features/<feature-name>/enablement/observability-spec.md
features/<feature-name>/enablement/release-rollback-plan.md
features/<feature-name>/enablement/operational-readiness.md
```

## Step 5 — Add enablement tasks to OpenSpec

```text
prompts/08-enablement/07-create-iac-cicd-openspec-tasks.md
```

Output:

```text
features/<feature-name>/openspec-change/tasks.md
```

## Rule

Keep business user stories and technical stories separate.

```text
Business user stories → product behavior
Technical stories → infrastructure, CI/CD, observability, release, operations
```

# Architecture Alignment Usage

After running:

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

you get:

```text
business-intake/brs-architecture-alignment.md
```

Do not treat this as an archive-only document.

Use it as input for:

```text
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
01-create-technical-spec.md
OpenSpec proposal/design/tasks
Enablement scope, if needed
```

Purpose:

```text
Prevent BRS/requirements/architecture mismatches from being lost.
```

# Optional Architecture & Contract Extensions

Use this track after user stories / technical spec and before OpenSpec tasks when extra architecture precision is needed.

## Step 1 — Decide which artifacts are needed

Run:

```text
prompts/09-architecture-contracts/00-decide-architecture-contract-artifacts.md
```

Output:

```text
features/<feature-name>/architecture-contracts/artifact-decision.md
```

## Step 2 — Create only the required artifacts

Possible prompts:

```text
prompts/09-architecture-contracts/01-create-architecture-decisions.md
prompts/09-architecture-contracts/02-create-api-contract.md
prompts/09-architecture-contracts/03-create-openapi-contract.md
prompts/09-architecture-contracts/04-create-domain-model.md
prompts/09-architecture-contracts/05-create-data-model.md
prompts/09-architecture-contracts/06-create-event-contracts.md
prompts/09-architecture-contracts/07-create-quality-attribute-scenarios.md
prompts/09-architecture-contracts/08-create-threat-model.md
```

## Step 3 — Update OpenSpec

Run:

```text
prompts/09-architecture-contracts/09-update-openspec-from-architecture-contracts.md
```

This ensures that ADRs, API contracts, OpenAPI, domain model, data model, event contracts, quality scenarios, and threat model findings are reflected in:

```text
openspec-change/proposal.md
openspec-change/design.md
openspec-change/tasks.md
```

## Important rule

Do not use all artifacts for every change.

Use the smallest set that reduces implementation ambiguity or risk.

# Handoff Mode vs Standalone Mode

After business intake, technical spec, enablement, and optional architecture contracts, choose one mode.

## Mode A — Handoff to OpenSpec / Spec Kit / Kiro

Create the handoff package:

```text
prompts/10-handoff/01-create-spec-driven-handoff.md
```

Output:

```text
features/<feature-name>/handoff/spec-driven-handoff.md
```

Then assess readiness:

```text
prompts/10-handoff/02-assess-handoff-readiness.md
```

Then use one adapter:

```text
prompts/11-downstream-adapters/openspec/01-create-openspec-from-handoff.md
prompts/11-downstream-adapters/spec-kit/01-create-speckit-input-from-handoff.md
prompts/11-downstream-adapters/kiro/01-create-kiro-spec-input-from-handoff.md
```

After this point, the downstream framework should own engineering execution.

## Mode B — Standalone mode

Use this when no downstream framework is used.

Continue with:

```text
prompts/03-openspec-handoff/
prompts/04-copilot-implementation/
prompts/05-reviewers/
```

In standalone mode, this repository remains the source of truth for engineering execution.

## Important rule

Do not maintain two competing implementation task plans.

# Using gstack as a Downstream Adapter

After creating:

```text
features/<feature-name>/handoff/spec-driven-handoff.md
```

you can create a gstack-specific brief:

```text
prompts/11-downstream-adapters/gstack/01-create-gstack-brief-from-handoff.md
```

Output:

```text
features/<feature-name>/handoff/gstack-brief.md
```

Then create a role-based review plan:

```text
prompts/11-downstream-adapters/gstack/02-create-gstack-review-plan.md
```

Output:

```text
features/<feature-name>/handoff/gstack-review-plan.md
```

Recommended usage:

```text
Use gstack to review/challenge:
- plan
- engineering design
- UX/design
- QA
- security
- release/shipping
- documentation
```

Important:

```text
If gstack becomes the execution layer, do not maintain a second competing task plan.
If gstack is used only for review, keep OpenSpec / Spec Kit / Kiro / standalone mode as the execution source of truth.
```

# Large Feature / Multi-Quarter Planning

Use this track when the BRS describes a big feature or initiative that may span more than one quarter.

## Correct principle

```text
Do not create detailed user stories for the entire large BRS too early.
```

Instead:

```text
Decompose the whole BRS.
Align the whole BRS with architecture.
Create delivery structure.
Create delivery slicing / roadmap.
Select the next increment.
Create detailed stories only for the selected increment.
```

## Step 1 — Create delivery slicing and roadmap

Run:

```text
prompts/06-planning/01-create-delivery-slicing-and-roadmap.md
```

Output:

```text
features/<feature-name>/planning/delivery-slicing.md
```

## Step 2 — Select next increment scope

Run:

```text
prompts/06-planning/02-select-next-increment-scope.md
```

Output:

```text
features/<feature-name>/planning/next-increment-scope.md
```

## Step 3 — Create increment handoff

Run:

```text
prompts/06-planning/03-create-increment-handoff.md
```

Output:

```text
features/<feature-name>/planning/increment-handoff.md
```

## Step 4 — Detail only the selected increment

Then run:

```text
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/07-create-business-test-expectations.md
prompts/02-engineering-contracts/01-create-technical-spec.md
```

using the increment handoff as scope control.

## Step 5 — Continue with optional tracks

For the selected increment only, use as needed:

```text
prompts/08-enablement/
prompts/09-architecture-contracts/
prompts/10-handoff/
prompts/11-downstream-adapters/
```

# Business-Led Intake with Microsoft 365 Copilot

For business users, use the parallel prompt set:

```text
prompts/12-business-copilot-intake/
```

Recommended order:

```text
01-create-brs-business-summary.md
02-extract-business-objectives.md
03-extract-business-requirements-for-review.md
04-identify-business-gaps-and-questions.md
05-create-business-delivery-slicing.md
06-select-next-increment-for-business-review.md
07-create-business-acceptance-expectations.md
08-create-business-approval-checklist.md
```

Outputs should be saved in SharePoint first.

IT/engineering later maps approved outputs into repository artifacts.

Read:

```text
docs/copilot/how-to-run-business-intake-in-m365-copilot.md
docs/copilot/how-to-create-m365-copilot-agent.md
```
