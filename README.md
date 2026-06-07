# Canonical Business Intake Sequence

Use this exact order for business intake:

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

Reason:
`02-extract-requirements.md` creates structured requirements.  
`03-review-brs-and-requirements-against-architecture.md` checks the original BRS and extracted requirements against the architecture draft.  
`04-create-delivery-structure.md` must use the alignment findings before creating epics/features/capabilities.

Do not jump directly from requirements extraction to delivery structure when an architecture draft exists.

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
prompts/01-business-intake/04-create-delivery-structure.md
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
01-summarize-brs.md
  ↓
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
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

# Architecture Draft Extraction and Early Alignment

The framework now supports architecture input earlier in the flow.

New prompt to extract an architecture document from Word:

```text
prompts/01-business-intake/00b-extract-architecture-from-word.md
```

New prompt to compare BRS and architecture:

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

New output artifact:

```text
business-intake/brs-architecture-alignment.md
```

Updated early flow when both BRS and architecture documents exist:

```text
Word BRS
  ↓
00a-extract-brs-from-word.md
  ↓
Word Architecture Draft
  ↓
00b-extract-architecture-from-word.md
  ↓
01-summarize-brs.md
  ↓
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
```

Important principle:

```text
BRS = business intent
Architecture draft = constraints, dependencies, feasibility, and risk input
```

The architecture document should not silently override the BRS.
If they conflict, create a question or contradiction.

# Clear Business Intake Prompt Numbering

The old `02a-create-epics-and-features.md` step has been renamed.

Use this clear sequence instead:

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

The key step is:

```text
04-create-delivery-structure.md
```

It creates:

```text
Business Objectives
Epics
Features / Capabilities
Requirement-to-feature mapping
Delivery slicing recommendations
```

Then:

```text
05-create-user-stories.md
```

creates user stories under the correct epic and feature.

Read:

```text
docs/business-intake-prompt-sequence.md
```

# Optional Enablement Track

The project now includes an optional Enablement Track for infrastructure, CI/CD, environments, observability, release/rollback, and operational readiness.

Use it when a feature needs:

```text
new infrastructure
new Azure/cloud resources
new database/storage
new queue/topic/event stream
pipeline changes
environment configuration
secret management
monitoring/alerting
release/rollback procedure
operational readiness
SRE/support handover
```

New prompt folder:

```text
prompts/08-enablement/
```

New template folder:

```text
templates/enablement/
```

Main enablement prompts:

```text
01-identify-enablement-scope.md
02-create-enablement-structure.md
03-create-technical-stories.md
04-create-infrastructure-spec.md
05-create-cicd-spec.md
06-create-operational-readiness.md
07-create-iac-cicd-openspec-tasks.md
```

Read:

```text
docs/enablement-track.md
```

The Enablement Track does not replace business user stories. It adds technical stories for platform, deployment, SRE, infrastructure, CI/CD, and operations.

# Architecture Alignment Is a Control Artifact

`business-intake/brs-architecture-alignment.md` is now explicitly used downstream.

It is produced by:

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

It is consumed by:

```text
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
02-engineering-contracts/01-create-technical-spec.md
03-openspec-handoff/01-create-openspec-proposal.md
03-openspec-handoff/02-create-openspec-design.md
03-openspec-handoff/03-create-openspec-tasks.md
08-enablement/01-identify-enablement-scope.md
```

Read:

```text
docs/architecture-alignment-usage.md
```

# Optional Architecture & Contract Extensions

The project includes an optional Architecture & Contract Extensions track.

Use it when the feature needs stronger engineering contracts before OpenSpec and Copilot implementation.

New prompt folder:

```text
prompts/09-architecture-contracts/
```

New template folder:

```text
templates/architecture-contracts/
```

Main optional artifacts:

```text
architecture-contracts/artifact-decision.md
architecture-contracts/architecture-decisions.md
architecture-contracts/adr/ADR-001-<decision>.md
architecture-contracts/api-contract.md
architecture-contracts/openapi.yaml
architecture-contracts/domain-model.md
architecture-contracts/data-model.md
architecture-contracts/event-contracts.md
architecture-contracts/quality-attribute-scenarios.md
architecture-contracts/threat-model.md
```

Use the decision prompt first:

```text
prompts/09-architecture-contracts/00-decide-architecture-contract-artifacts.md
```

Then run only the needed prompts.

Decision rule:

| Situation | Artifact |
|---|---|
| Important technical choice | ADR / architecture decisions |
| REST API change | API contract / OpenAPI |
| Complex business rules or workflow | Domain model / DDD |
| Database changes | Data model |
| Event-driven integration or audit events | Event contracts |
| Important NFRs | Quality attribute scenarios |
| Security-sensitive change | Threat model |

Read:

```text
docs/architecture-contract-extensions.md
```

# Handoff Boundary and Standalone Fallback

The framework supports two usage modes:

```text
Mode A — Handoff mode
Prepare enterprise-grade inputs, then hand over to OpenSpec, GitHub Spec Kit, Kiro, or another downstream framework.

Mode B — Standalone mode
Continue using the existing OpenSpec-like, Copilot implementation, review, enablement, and contract prompts when no downstream framework is used.
```

Recommended stop point for handoff mode:

```text
features/<feature-name>/handoff/spec-driven-handoff.md
```

New handoff prompts:

```text
prompts/10-handoff/01-create-spec-driven-handoff.md
prompts/10-handoff/02-assess-handoff-readiness.md
```

New downstream adapter prompts:

```text
prompts/11-downstream-adapters/openspec/01-create-openspec-from-handoff.md
prompts/11-downstream-adapters/spec-kit/01-create-speckit-input-from-handoff.md
prompts/11-downstream-adapters/kiro/01-create-kiro-spec-input-from-handoff.md
```

Standalone fallback remains available:

```text
prompts/03-openspec-handoff/
prompts/04-copilot-implementation/
prompts/05-reviewers/
```

Read:

```text
docs/framework-boundary-and-handoff.md
docs/downstream-framework-selection.md
```

# gstack Adapter

The project now includes gstack as an additional downstream adapter.

gstack is treated differently from OpenSpec, GitHub Spec Kit, and Kiro:

```text
OpenSpec / Spec Kit / Kiro
  → downstream specification and task frameworks

gstack
  → role-based execution, review, QA, security, documentation, and shipping support
```

New files:

```text
docs/gstack-adapter.md

prompts/11-downstream-adapters/gstack/
  01-create-gstack-brief-from-handoff.md
  02-create-gstack-review-plan.md

templates/downstream-adapters/gstack/
  gstack-brief.md
  gstack-review-plan.md
```

Use gstack in two ways:

```text
Option A — gstack as downstream execution/review layer

Option B — gstack as reviewer around OpenSpec / Spec Kit / Kiro / standalone mode
```

Read:

```text
docs/gstack-adapter.md
```

# Large Feature / Multi-Quarter Planning

The framework now includes a planning track for large BRS-driven initiatives that may span more than one quarter.

Use it when a BRS is too large to turn directly into detailed user stories.

New prompt folder:

```text
prompts/06-planning/
```

New templates:

```text
templates/planning/
  delivery-slicing.md
  next-increment-scope.md
  increment-handoff.md
```

Recommended large BRS approach:

```text
Decompose the whole BRS.
Align the whole BRS with architecture.
Plan and slice the whole BRS.
Detail only the next increment.
```

New prompts:

```text
prompts/06-planning/01-create-delivery-slicing-and-roadmap.md
prompts/06-planning/02-select-next-increment-scope.md
prompts/06-planning/03-create-increment-handoff.md
```

Read:

```text
docs/large-feature-planning.md
```

# Business Copilot Intake Prompts

The project includes a parallel business-facing prompt set for Microsoft 365 Copilot and Copilot Studio.

These prompts are wrappers of the canonical business-intake framework prompts. They do not replace the framework prompts.

New folder:

```text
prompts/12-business-copilot-intake/
```

Prompts:

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

Dedicated guides:

```text
docs/business-copilot-intake.md
docs/copilot/how-to-run-business-intake-in-m365-copilot.md
docs/copilot/how-to-create-m365-copilot-agent.md
docs/copilot/copilot-studio-agent-design.md
```

# Adaptive Delivery Modes and Modular Delivery

The framework now supports adaptive delivery modes:

```text
Fast Path
Standard Path
Enterprise Path
Enterprise + Modular Delivery
```

Use the smallest process that gives enough control.

For small and clear changes, go directly to OpenSpec.

For large BRS-driven initiatives, use the business intake and, when needed, the Modular Delivery Track.

New routing prompt:

```text
prompts/00-routing/01-select-delivery-mode.md
```

New simplified PO intake prompt:

```text
prompts/01-business-intake/01-create-business-intake-summary.md
```

Updated delivery structure prompt:

```text
prompts/01-business-intake/04-create-delivery-structure.md
```

New Modular Delivery prompts:

```text
prompts/07-modular-delivery/
  01-create-global-architecture-rules.md
  02-identify-software-modules.md
  03-map-capabilities-to-modules.md
  04b-define-delivery-increments.md
  05-create-module-spec.md
  06-create-openspec-change-for-active-deliverable.md
```
