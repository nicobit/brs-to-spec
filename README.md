# Enterprise BRS to Delivery Readiness Framework

This framework transforms a raw **Business Requirements Specification (BRS)** and an optional **initial architecture document** into business-approved, architecture-aligned, delivery-ready increments.

OpenSpec is the default engineering downstream, but it is not mandatory. The framework also supports standalone execution, Microsoft 365 Copilot / Copilot Studio business intake, and GitHub Copilot / VS Code guided delivery workflows.

## Why this framework exists

Do not ask an AI coding agent to implement directly from a large Word BRS.

A real enterprise BRS usually contains ambiguity, implicit assumptions, architecture constraints, regulatory expectations, dependencies, hidden delivery risks, and review obligations across multiple roles. This framework creates a controlled path from business intent to delivery-ready work.

## What this framework is

It is an adaptive front door for enterprise delivery.

```text
BRS + initial architecture
  -> normalized inputs
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

## What this framework is not

It is not:

- a replacement for OpenSpec
- a coding-agent framework
- a replacement for Product Owners, architects, QA, security, or SRE
- a mandatory process for every small change
- a way to generate implementation directly from a raw BRS

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
| OpenSpec | OpenSpec is available and should be the engineering source of truth | `openspec/changes/D1-<name>/` |
| Standalone | OpenSpec is not used | `standalone-delivery/D1-<name>/` |
| Business Copilot | Business users work in Microsoft 365 / SharePoint / Word / Teams | SharePoint/Word review outputs |

## Official normalized inputs

```text
input/brs.md
input/initial-architecture.md
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
planning/delivery-increments.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
quality-gates/*.md
openspec/changes/... or standalone-delivery/...
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

The repository also includes guidance for GitHub Copilot and VS Code so assistants understand that this is a BRS-to-delivery-readiness framework, not an application codebase.

Relevant support files include:

```text
.github/copilot-instructions.md
.github/prompts/
docs/15-github-copilot-workflow.md
.vscode/settings.json
```

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

For OpenSpec mode:

```bash
python tools/scripts/new_feature.py my-project --mode enterprise --execution-mode openspec
```

For standalone mode:

```bash
python tools/scripts/new_feature.py my-project --mode enterprise --execution-mode standalone
```

For large initiatives:

```bash
python tools/scripts/new_feature.py my-project --mode enterprise-modular --execution-mode openspec
```
