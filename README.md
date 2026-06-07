# Enterprise BRS to Delivery Readiness Framework

This framework transforms one or more raw **Business Requirements Specification (BRS)** documents, plus optional architecture source material, into business-approved, architecture-aligned, delivery-ready increments.

OpenSpec is the default engineering downstream, but it is not mandatory. The framework also supports standalone execution, Microsoft 365 Copilot / Copilot Studio business intake, and GitHub Copilot / VS Code guided delivery workflows.

## Why this framework exists

Do not ask an AI coding agent to implement directly from a large Word BRS.

A real enterprise initiative usually spans ambiguity, implicit assumptions, architecture constraints, regulatory expectations, dependencies, hidden delivery risks, and review obligations across multiple roles. Sometimes the source material is one BRS and one architecture note. Sometimes it is split across several documents. This framework creates a controlled path from business intent to delivery-ready work.

## Core workspace model

The primary operating model is an **initiative workspace**:

```text
initiatives/<initiative-id>-<slug>/
```

Each initiative workspace represents one delivery initiative.

### Default input model

For the common case, keep the inputs simple:

```text
initiatives/<initiative-id>-<slug>/
  input/
    brs.md
    architecture.md
    input-package.md
```

### Expanded input model

Only expand into folders when the same initiative has multiple source documents:

```text
initiatives/<initiative-id>-<slug>/
  input/
    brs/
      main.md
      compliance.md
    architecture/
      main.md
      security-constraints.md
    input-package.md
```

Use `input/input-package.md` to record inventory, completeness, overlap, conflicts, assumptions, and consolidation notes.

## What this framework is

It is an adaptive front door for enterprise delivery.

```text
one or more BRS inputs + optional architecture inputs
  -> normalized source set
  -> business intake summary
  -> architecture-aware planning
  -> traceability
  -> engineering readiness
  -> conditional quality gates
  -> planning projection when needed
  -> OpenSpec change or standalone delivery package
```

The framework is designed so generated artifacts are evidence-based, traceable, decision-oriented, and ready for structured review.

Prompts consistently define:

```text
role
context
purpose
inputs
output path
required structure
quality bar
anti-patterns
stop conditions
self-review checklist
```

Templates and review artifacts consistently capture:

```text
evidence
risk
owner
required-before stage
decision status
traceability
review outcome
acceptance and exit criteria
```

## Initiative-Scoped Outputs

All outputs belong to the active initiative workspace. For example:

```text
initiatives/<initiative-id>-<slug>/
  business-intake/business-intake-summary.md
  architecture/architecture-review.md
  planning/delivery-increments.md
  planning/traceability-matrix.md
  engineering-readiness/readiness-check.md
  quality-gates/*.md
  openspec/changes/... or standalone-delivery/...
  perspectives/agile-planning/gitlab-planning-view.md
```

This keeps artifacts for separate initiatives isolated from each other while still allowing an initiative to grow from a simple single-document input model into a multi-document one when needed.

## What this framework is not

It is not:

- a replacement for OpenSpec
- a coding-agent framework
- a replacement for Product Owners, architects, QA, security, or SRE
- a mandatory process for every small change
- a way to generate implementation directly from raw BRS sources without normalization

## Core principle

Use the smallest workflow that gives enough control.

## Delivery modes

| Delivery mode | Use when | Typical output |
|---|---|---|
| Fast Path | The change is already clear and engineering-ready | OpenSpec directly or small standalone package |
| Standard Path | Some clarification is needed | Business intake + readiness + handoff |
| Enterprise Path | Formal BRS, architecture impact, compliance, multiple stakeholders | Intake + architecture + traceability + gates |
| Enterprise + Modular Delivery | Large, multi-team, multi-quarter work or AI context saturation risk | Modules + increments + active-deliverable handoff |

## Execution modes

| Execution mode | Use when | Output |
|---|---|---|
| OpenSpec | OpenSpec is available and should be the engineering source of truth | `openspec/changes/D1-<name>/` inside the initiative workspace |
| Standalone | OpenSpec is not used | `standalone-delivery/D1-<name>/` inside the initiative workspace |
| Business Copilot | Business users work in Microsoft 365 / SharePoint / Word / Teams | SharePoint/Word review outputs plus initiative-scoped framework artifacts |

## Official normalized inputs

Within an initiative workspace, the canonical inputs are:

```text
input/brs.md or input/brs/*.md
input/architecture.md or input/architecture/*.md
input/input-package.md
```

## Conditional quality gates

Quality gates are not optional.

They are not always required, but when triggered by the readiness check, they become mandatory before the relevant implementation, merge, or handoff step.

## Planning view

The framework can generate an Agile / GitLab planning view as a read-only projection.

It does not create a second source of truth. The source of truth remains:

```text
business-intake/business-intake-summary.md
planning/delivery-structure.md
planning/delivery-increments.md when the initiative uses Modular Delivery
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
quality-gates/*.md
openspec/changes/... or standalone-delivery/...
```

Downstream helper outputs are not source of truth:

```text
perspectives/agile-planning/gitlab-planning-view.md
prompts/8-copilot-implementation execution summaries
prompts/9-reviewers review findings
```

The planning view maps those artifacts into the language used by delivery teams:

```text
Epic
Feature / Issue
User Story
Task / Checklist
Milestone
Labels
```

Generated output:

```text
perspectives/agile-planning/gitlab-planning-view.md
```

If scope, requirements, architecture constraints, quality gates, or implementation tasks change, update the source artifacts first and regenerate the planning view.

## Copilot guidance

The repository includes guidance for GitHub Copilot and VS Code so assistants understand that this is a BRS-to-delivery-readiness framework, not an application codebase.

Relevant support files include:

```text
.github/copilot-instructions.md
.github/prompts/
docs/15-github-copilot-workflow.md
docs/16-prompt-execution-environments.md
docs/17-copilot-usage.md
.vscode/settings.json
```

The Copilot instructions also define a critical operating rule: work inside one initiative workspace at a time, and treat all workflow paths as relative to that workspace.

For implementation and review, the framework also includes:

```text
prompts/8-copilot-implementation/
prompts/9-reviewers/
templates/quality-gates/ready-for-copilot-checklist.md
```

Quality gate artifacts and reviewer prompts are intentionally separate:

- quality gates are governance artifacts created before implementation, merge, or release when triggered
- reviewer prompts are downstream helpers used after implementation to review actual code and tests against the approved source artifacts

## Template quality rule

Every important review artifact should answer:

```text
What decision was made?
What evidence supports it?
What risk remains?
Who owns the action?
By when / before which stage is it required?
Which requirement or architecture constraint is affected?
```

## Recommended use

Create an initiative workspace:

```bash
python tools/scripts/new_initiative.py onboarding-request --initiative-id I001 --mode enterprise --execution-mode openspec
```

Add another BRS source only if the initiative really has more than one source document:

```bash
python tools/scripts/add_brs.py initiatives/I001-onboarding-request compliance
```

Add another architecture source only if needed:

```bash
python tools/scripts/add_architecture.py initiatives/I001-onboarding-request security-constraints
```

Then run the prompts against that initiative workspace, treating every input and output path as relative to:

```text
initiatives/I001-onboarding-request/
```
