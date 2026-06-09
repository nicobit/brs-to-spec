# Small-Change Paths

## Purpose

Use this guidance when the initiative is narrow enough that a lighter path may be appropriate.

This is not a second framework.

It is a way to use the current framework proportionally.

## Suitable cases

Typical small-change situations include:

```text
single-story enhancement
small brownfield improvement
bug fix with architecture sensitivity
low-scope change with clear constraints
single active deliverable with narrow scope
```

## Minimum rule

A small change can be lighter.

It cannot be careless.

Do not skip:

```text
traceability
architecture awareness
readiness discipline
triggered quality gates
handoff quality
```

Do not add visual documentation by default for a small change.

Add a visual only when the change is still hard to understand without it, for example because of:

```text
non-trivial boundary interaction
contract behavior that is clearer as a sequence or flow
existing-system dependency that is easy to misunderstand in text alone
```

## Recommended small-change pattern

Use this when the change is narrow and the affected area is already reasonably understood:

1. choose entry mode
2. run routing
3. use Fast Path only if the change is already clear and engineering-ready
4. still run readiness when architecture, contract, regression, security, or operational risk exists
5. run only the quality gates that readiness actually triggers
6. create one narrow handoff for one active deliverable
7. implement one approved task at a time

## Minimum artifact expectation

For a small change, expect at least:

```text
input/input-package.md
routing/routing-decision.md
engineering-readiness/readiness-check.md when the change is not trivially safe
openspec/... or standalone-delivery/... for the active deliverable
```

## Fast Path rule

Fast Path is acceptable when:

```text
scope is narrow
affected area is known
architecture constraints are already clear
no unresolved business ambiguity blocks implementation
the change can be handed off as one small active deliverable
```

Fast Path is not a license to skip discipline.

It is also not a license to add diagram overhead when text is already sufficient.

## Small changes that still need gates

Even a small change may still trigger gates if it affects:

```text
API boundaries
data contracts
events
security-sensitive flows
operational behavior
regression-sensitive existing behavior
release or rollback sensitivity
```

If one of these areas is complex enough that text alone stays weak, a compact embedded visual may help.

That does not make visuals mandatory for all small changes.

## Practical question

Before taking the lighter path, ask:

```text
Is this change truly small, or only easy to describe?
```

If the answer is uncertain, prefer the smallest safe step up in control.
