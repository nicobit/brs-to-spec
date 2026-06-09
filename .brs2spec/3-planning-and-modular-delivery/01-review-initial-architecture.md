# Prompt - Review Initial Architecture

## Role

You are a solution architect reviewing whether the initial architecture supports the BRS.

## Context

This prompt is the initiative-specific architecture review step. It uses the early delivery shape plus the initial architecture input to refine concrete constraints, conflicts, and risks.

## Purpose

Review architecture constraints, conflicts, missing decisions, brownfield impact, and delivery impact against the initiative's current delivery shape.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `architecture/existing-system-impact.md` when brownfield impact is material

## Output path

```text
architecture/architecture-review.md
```

## Template

Use:

```text
templates/planning-and-modular-delivery/architecture-review.md
```

Preserve the template headings. Expand the tables only where the available evidence requires more detail.
Prefer sharp decisions and evidence over broad explanatory prose.
Treat the initial architecture input as high-level solution context unless the evidence already makes initiative-specific decisions explicit.
Use it to understand systems, containers, integrations, boundaries, and major constraints before refining what matters for this initiative specifically.
Add an optional compact context, container, or integration-flow view only when it materially improves understanding of boundaries, constraints, or impacted areas.
Do not add a visual that merely restates simple tables or already-clear text.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- evaluate the architecture against the initiative's planned epics, features, stories, and slices
- distinguish clearly between early solution context and later initiative-specific delivery implications
- identify initiative-specific impacted components, interface implications, contract implications, governed boundaries, rollout / rollback constraints, and validation implications when the evidence supports them
- surface affected components, contract impacts, and compatibility risks when the initiative changes an existing system
- mark conflicts instead of resolving them silently
- assign owners for gaps and decisions
- avoid creating low-level implementation tasks
- keep each section focused on decisions, conflicts, risks, and constraints that affect downstream delivery
- keep any optional visual focused on one initiative-relevant concern, not as a full replacement for architecture text
- avoid treating the absence of an optional visual as a failure when the artifact is already clear enough in text

## Anti-patterns to avoid

Do not produce outputs that:

- invent architecture not present in the inputs
- slice work only by technical layer
- create tasks for all future deliverables
- ignore brownfield contract, schema, or operational impact when evidence exists
- ignore architecture conflicts
- produce a table without evidence or owner
- treat the high-level architecture input as if it already fully resolves initiative-specific delivery questions

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Architecture constraints are referenced.
- [ ] Business requirements remain traceable.
- [ ] The review clearly references the initiative delivery shape it assessed.
- [ ] The output makes clear what came from high-level architecture context versus initiative-specific refinement.
- [ ] The output is specific enough to shape readiness, contracts, and handoff.
- [ ] Brownfield impact is summarized when relevant.
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] The output supports architecture rule creation and delivery planning.
