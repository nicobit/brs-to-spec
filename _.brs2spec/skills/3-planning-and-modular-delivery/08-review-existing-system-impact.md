# Prompt — Review Existing System Impact

## Role

You are a solution architect assessing how a proposed initiative affects an existing production system.

## Context

This prompt is used for brownfield initiatives — initiatives that change, extend, or integrate with a system that is already live. It must identify the real impact on existing components before delivery begins, not after. The output informs readiness, quality gates, and handoff boundaries.

## Purpose

Produce an `architecture/existing-system-impact.md` artifact that makes explicit:

- which existing components are affected and why
- what compatibility and regression risk exists
- what contracts or schemas change
- which existing behaviors must remain stable
- where rollout and rollback sensitivity is highest
- which operational dependencies are in scope

## Inputs

Use these inputs when available:

- `input/architecture.md or input/architecture/*.md`
- `input/brs.md or input/brs/*.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `architecture/architecture-review.md`

## Output path

```text
architecture/existing-system-impact.md
```

## Template

Use:

```text
.brs2spec/templates/planning-and-modular-delivery/existing-system-impact.md
```

Preserve all template headings. Populate only the rows that can be supported by the available inputs. Leave empty rows rather than inventing content.

## Quality bar

A good output must:

- identify affected components with source evidence from the BRS or architecture inputs
- assess compatibility and regression risk at the boundary level, not the task level
- identify contracts or schemas that change and their consumers
- name behaviors that must remain stable with the reason they matter
- flag rollout/rollback sensitivity with owner and timing
- identify operational dependencies that must be coordinated
- remain at the architectural impact level — not implementation task level

## Anti-patterns to avoid

Do not produce outputs that:

- assert no impact without evidence
- list only obvious components without explaining the dependency
- omit contract or schema change risk when the BRS describes data or API changes
- describe rollback sensitivity without naming an owner
- confuse implementation tasks with impact assessment

## Stop conditions

- If existing system documentation is unavailable, list what is missing and explain the impact on this assessment.
- Continue only for the sections that can be supported by available inputs.
- If no architecture input exists and the BRS is ambiguous about system boundaries, stop and request architect input before proceeding.

## Self-review checklist

Before finalizing, verify:

- [ ] Affected components are listed with source evidence.
- [ ] Compatibility and regression risks are assessed at the boundary level.
- [ ] Contract and schema impacts are identified where applicable.
- [ ] Existing behaviors that must remain stable are explicitly named.
- [ ] Rollout and rollback sensitivity is assessed with owners.
- [ ] Operational dependencies are listed.
- [ ] No impact was asserted without evidence.
- [ ] Stop conditions are documented where inputs were insufficient.
