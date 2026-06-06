# gstack Adapter

This adapter prepares the existing handoff package for gstack.

gstack is different from OpenSpec, GitHub Spec Kit, and Kiro.

It is best treated as:

```text
a role-based execution, review, QA, security, documentation, and shipping layer
```

rather than only a specification framework.

## When to use gstack

Use the gstack adapter when the team wants Claude Code / gstack roles to help with:

```text
planning review
engineering review
design review
security review
QA
code review
release readiness
documentation
shipping
```

## How it fits

```text
This framework
  ↓
handoff/spec-driven-handoff.md
  ↓
gstack brief
  ↓
gstack planning/review/spec/QA/security/ship skills
```

or:

```text
This framework
  ↓
OpenSpec / Spec Kit / Kiro
  ↓
gstack as reviewer around the downstream plan and implementation
```

The second option is often the most useful: use OpenSpec/Spec Kit/Kiro for the native spec/task flow, and use gstack for role-based challenge and review.

## Source artifacts

The gstack adapter should read:

```text
handoff/spec-driven-handoff.md
business-intake/requirements.md
business-intake/brs-architecture-alignment.md
business-intake/user-stories.md
engineering-contracts/technical-spec.md
architecture-contracts/*
enablement/*
openspec-change/* if present
```

## Output artifacts

The adapter creates:

```text
handoff/gstack-brief.md
handoff/gstack-review-plan.md
```

## Recommended gstack usage

The exact gstack commands available may evolve, so confirm the installed gstack skills in the target environment.

Typical useful skills include planning/review, QA, security, documentation, and shipping oriented skills such as:

```text
/spec
/plan-eng-review
/plan-design-review
/plan-ceo-review
/review
/qa
/cso
/document-generate
/document-release
/ship
```

## Important boundary

If gstack becomes the downstream execution layer, do not maintain a competing implementation task plan in this framework.

If gstack is used only for review, keep the selected downstream framework or standalone mode as the source of truth and use gstack to challenge it.
