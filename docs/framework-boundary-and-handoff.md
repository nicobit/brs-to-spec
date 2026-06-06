# Framework Boundary and Handoff Model

This project supports two modes.

```text
Mode A — Handoff mode
Use this framework to prepare enterprise-grade inputs, then hand over to OpenSpec, GitHub Spec Kit, Kiro, or another spec-driven engineering framework.

Mode B — Standalone mode
Use this framework end-to-end when no downstream framework is used.
```

## Clean boundary

```text
Enterprise readiness and contract handoff = this framework
Engineering spec/task/implementation loop = downstream framework
```

## Recommended stop point

```text
features/<feature-name>/handoff/spec-driven-handoff.md
```

At that point, the framework has produced enough context for a downstream spec-driven engineering tool.

## What your framework owns

```text
BRS normalization
requirements extraction
BRS / requirements / architecture alignment
delivery structure
user stories
technical spec
architecture contracts
enablement scope
risks and open questions
handoff readiness
```

## What downstream frameworks own in handoff mode

```text
native engineering spec
implementation plan
task generation
coding loop
test iteration
completion/archive workflow
```

## Standalone fallback

If no downstream framework is used, continue with the existing prompts:

```text
prompts/03-openspec-handoff/
prompts/04-copilot-implementation/
prompts/05-reviewers/
```

## Source of truth rule

Avoid two competing implementation sources of truth.

```text
Handoff mode:
  handoff package → downstream framework owns execution

Standalone mode:
  this repository remains the source of truth for engineering execution
```

## Why keep existing OpenSpec-like prompts?

They are kept for:

```text
standalone execution
fallback when no external framework is available
pilot usage
teams that want OpenSpec-like artifacts without adopting OpenSpec immediately
```

The existing `prompts/03-openspec-handoff/` folder should be seen as either:

```text
standalone execution prompts
```

or:

```text
adapter-style prompts for OpenSpec-like artifacts
```

# gstack Boundary

gstack is supported as a downstream adapter.

Use gstack either as:

```text
1. Downstream execution/review layer
2. Reviewer around OpenSpec / GitHub Spec Kit / Kiro / standalone mode
```

The existing handoff package remains valid.

Add a gstack-specific brief when gstack is used:

```text
handoff/gstack-brief.md
handoff/gstack-review-plan.md
```

Source of truth rule:

```text
If gstack owns execution, gstack artifacts/reviews drive execution.
If gstack is only a reviewer, the selected downstream framework or standalone mode remains the source of truth.
```

# Relationship with Large Feature Planning

For multi-quarter BRS initiatives, the final downstream handoff should normally be created for the selected next increment, not for the entire BRS.

The whole BRS remains visible through:

```text
planning/delivery-slicing.md
```

The implementation scope is controlled by:

```text
planning/next-increment-scope.md
planning/increment-handoff.md
```
