# Overview

## What this framework is

An enterprise BRS-to-delivery-readiness adapter.

It transforms one or more raw Business Requirements Specification (BRS) documents, plus optional architecture source material, into business-approved, architecture-aligned, delivery-ready increments.

The framework is not an application codebase. It is a structured collection of prompts, templates, and conventions that guide AI-assisted delivery work from business input through to engineering-ready output.

## What it is not

- A replacement for OpenSpec
- A coding-agent framework
- A replacement for Product Owners, architects, QA, security, or SRE
- A mandatory process for every small change
- A way to generate implementation directly from raw BRS without normalization

## Core operating unit

The primary operating model is an **initiative workspace**:

```text
initiatives/<initiative-id>-<slug>/
```

Each initiative workspace is isolated from others. All inputs, intermediate artifacts, and outputs live inside it.

## Workflow summary

```text
input preparation
  -> routing
  -> business intake
  -> architecture review and delivery planning
  -> engineering readiness
  -> conditional quality gates
  -> handoff (OpenSpec or standalone)
  -> implementation and review
```

Routing selects the delivery mode (Fast Path, Standard, Enterprise, Enterprise + Modular) and execution mode (OpenSpec, Standalone, Business Copilot).

## Key governance rules

Every important artifact should have:

- an obvious consumer
- an obvious downstream use

Governed boundaries must be made explicit:

- governed service or API boundary → usually trigger `API contract`
- governed data ownership or schema boundary → usually trigger `Data contract`
- governed asynchronous event boundary → usually trigger `Event contract`

## Quick start

Run:

```text
.brs2spec/brs-to-spec-run-workflow.md
```

to identify the active initiative workspace, the current stage, and the next required action.

## Artifact types

The framework produces two types of artifact with different durability characteristics.
**Human artifacts** (business summaries, architecture reviews, delivery specs) are validated
by human review and survive model upgrades unchanged. **Execution artifacts** (prompts fed
to LLMs, CI gate configs) are sensitive to model changes and should be kept short and
constraint-based. See [Artifact Durability](23-artifact-durability.md) for the full
classification and what to do after a model upgrade.

## See also

- [Decision Tree](03-decision-tree.md)
- [Entry Modes](18-entry-modes.md)
- [How to Use](../HOW_TO_USE.md)
