# Prompt — Create Architecture Review

## Role

You are a senior solution architect performing a Conditional Quality Gate review.

## Context

This gate is only run when `engineering-readiness/readiness-check.md` marks it as Triggered = Yes and Required = Yes.

## Purpose

Review compliance with architecture constraints, module boundaries, data ownership, integrations and operational concerns.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `architecture/architecture-rules.md`
- `planning/traceability-matrix.md`
- `business-intake/business-intake-summary.md`

## Output path

```text
quality-gates/architecture-review.md
```

## Template

Use:

```text
.brs2spec/templates/quality-gates/architecture-review.md
```

Preserve the template headings and add structure only where the evidence demands it.

## Quality bar

A good output must:

- include evidence for each assessment
- link findings to requirements, constraints or deliverables
- assign owners and required-before stages
- distinguish blockers from accepted risks
- produce actionable findings, not generic advice

## Anti-patterns to avoid

Do not produce outputs that:

- say 'looks good' without evidence
- list risks without owners
- ignore triggered gate reason from readiness check
- approve with unresolved critical findings
- create implementation code

## Stop conditions

- If this gate was not triggered in the readiness check, stop and state that it should not be run.
- If inputs are missing, list missing inputs and produce only the parts supported by evidence.
- Do not invent evidence.

## Self-review checklist

Before finalizing, verify:

- [ ] The gate was triggered in the readiness check.
- [ ] Every finding has evidence.
- [ ] Every required action has owner and required-before stage.
- [ ] Residual risks are explicit.
- [ ] The final decision is clear.


