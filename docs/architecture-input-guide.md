# Architecture Input Guide

This guide explains how architecture documents are used in the framework.

## Why architecture enters early

A BRS often describes business intent, but architecture documents can reveal:

```text
existing systems involved
integration constraints
data ownership
security boundaries
audit/logging expectations
deployment constraints
non-functional requirements
technical dependencies
architecture assumptions
```

If architecture is used only at the technical-spec stage, contradictions may be found too late.

## Inputs

```text
features/<feature-name>/input/brs-original.md
features/<feature-name>/input/architecture-draft.md
```

## Extraction prompt

Use this if the architecture is in Word:

```text
prompts/01-business-intake/00b-extract-architecture-from-word.md
```

Output:

```text
features/<feature-name>/input/architecture-draft.md
```

## Alignment prompt

Use this after BRS and architecture are available:

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

Output:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

## What the alignment review checks

```text
BRS requirements supported by architecture
BRS requirements not clearly supported
contradictions
missing architecture decisions
data/integration gaps
security/authorization gaps
audit/logging gaps
NFR implications
deployment/environment/configuration gaps
questions for business
questions for architecture
questions for QA
```

## Principle

```text
BRS = business intent
Architecture draft = constraints, feasibility, dependencies, and risks
```

The architecture draft should not silently change the business requirement.
If the architecture and BRS do not match, create an explicit question.
