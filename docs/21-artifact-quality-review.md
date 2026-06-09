# Artifact Quality Review

## Purpose

This guide helps users and Copilot review whether a generated artifact is good enough to support the next workflow step.

Use it as a lightweight quality check.

It is not a new approval layer.

## Core rule

An artifact is not good enough just because the file exists.

It should be:

```text
clear enough
specific enough
decision-oriented enough
traceable enough
useful enough for the next step
```

## Quick quality review

Ask:

```text
What decision does this artifact support?
What evidence is actually present?
What next step depends on it?
What would go wrong if we used this artifact as-is?
```

Revise before proceeding if the answers are weak.

## Common failure patterns

Watch for artifacts that are:

- too generic
- repetitive instead of referential
- vague about risk, scope, or decision
- detached from the intended audience
- formally complete but not operationally useful
- missing ownership or required-before timing where it matters

## Minimum evidence of usefulness by artifact

### Business intake

Good enough when:

- business objective, scope, and requirements are understandable
- traceability to source inputs is visible
- gaps and questions are actionable
- the artifact supports PO review without technical overload

Revise if:

- goals are vague
- scope is fuzzy
- requirements are not traceable
- open questions have no impact or owner

### Delivery structure

Good enough when:

- Epic / Feature / User Story structure is clear
- story traceability is visible
- governed boundaries and slice logic are explicit where relevant
- downstream handoff can derive implementation tasks from it

Revise if:

- story structure is missing or weak
- slices are arbitrary
- boundaries are implicit
- acceptance or architecture detail is copied instead of referenced

### Readiness

Good enough when:

- the readiness decision is explicit
- each major decision has evidence
- triggered gates are justified
- blocking issues and accepted risks are real and owned

Revise if:

- Ready / Not ready is asserted without evidence
- gates look arbitrary
- risk text is generic
- required-before stages are unclear

### Delivery spec

Good enough when:

- the active deliverable is clearly bounded
- scope, out of scope, constraints, and validation references are visible
- engineers can understand what the deliverable is and what evidence is expected

Revise if:

- it reads like generic notes
- it duplicates source acceptance text
- it does not constrain implementation meaningfully

### Tasks

Good enough when:

- tasks are small enough to implement and review
- each task is traceable
- validation and evidence expectations are visible
- the task can be executed without guessing business intent or constraints

Revise if:

- tasks are broad
- tasks are not testable
- tasks copy stories instead of becoming engineering work
- evidence expectations are absent

### Planning view

Good enough when:

- the view is easy to scan
- planning items are traceable to source artifacts
- notes and enablement items are concise and evidence-based
- the projection helps the team coordinate without becoming a second source of truth

Revise if:

- it is bloated
- it repeats architecture or acceptance detail
- it looks like a second backlog
- implementation truth is being copied into it

## Workflow use

Use this review check:

- after generating a major artifact
- before moving to the next stage
- when Copilot output looks formally correct but not clearly useful

If the artifact fails the quick review, regenerate or refine it before proceeding.
