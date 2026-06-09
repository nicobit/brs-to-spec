# Prompt - Create Delivery Structure

## Role

You are a delivery architect structuring business scope into deliverable units.

## Context

This prompt is the early delivery-shaping step. It should create enough planning structure to make later architecture refinement initiative-specific. It must not create implementation tasks for the whole BRS.

## Purpose

Create an early delivery structure connecting objectives, epics, features, user stories, candidate increments, and the known high-level architecture context.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`

## Output path

```text
planning/delivery-structure.md
```

## Template

Use:

```text
templates/planning-and-modular-delivery/delivery-structure.md
```

Preserve the template headings. Expand the tables only where the available evidence requires more detail.
Keep the output structurally rich but concise. Use tables and short rules rather than long narrative sections.
Keep Epic / Feature / User Story structure, governed boundaries, and traceability rules detailed.
Keep capability overviews, candidate modules, and candidate slices summary-level unless more detail changes delivery decisions.
Use the initial architecture input as high-level solution context when it exists; do not wait for later architecture refinement to shape the first delivery view.
Add an optional compact slice/dependency or capability-to-module orientation view only when it materially improves planning, handoff, or review clarity.

## Story hierarchy rule

Every feature must have at least two user stories.

A feature with only one story is not a feature — it is a story that has been mislabeled. Collapse it into a story under the parent epic or split the feature further.

Derive multiple stories per feature by asking:

- Are there different personas who interact with this feature differently?
- Are there distinct scenarios — happy path, failure path, edge case — that represent separate deliverable behaviors?
- Are there different entry points, states, or contexts that a user experiences separately?
- Is there a support or admin view that is distinct from the customer-facing view?

A minimum of two stories per feature is a floor, not a target. A feature covering a complex capability may have four or more stories.

Do not write stories that merely restate the feature name with "As a user, I want to..." wrapper text. Each story must represent a distinct, independently testable behavior.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- define Epic / Feature / User Story structure early enough to guide later architecture review and downstream handoff
- produce at least two user stories per feature — a feature with one story must be restructured
- write stories that represent distinct, independently testable behaviors — not restatements of the feature name
- derive stories from different personas, scenarios, failure paths, and edge cases present in the BRS
- use classic Agile user story wording: `As a <persona>, I want <capability>, so that <business value>.`
- make clear that stories are planning parents and tasks are engineering children
- surface existing-system impact where it affects slicing, validation, compatibility, or rollout
- make governed service/API, data, and event boundaries explicit where they exist
- mark conflicts instead of resolving them silently
- assign owners for gaps and decisions
- avoid creating low-level implementation tasks
- avoid repeating acceptance detail or architecture rationale that belongs in source artifacts
- avoid over-explaining candidate modules or slices when a concise summary is enough
- avoid pretending initiative-specific architecture refinement is already complete at this stage
- keep any optional visual as orientation support, not as a second planning artifact

## Anti-patterns to avoid

Do not produce outputs that:

- have only one story per feature
- write stories that restate the feature name with a user story wrapper
- write stories only for the happy path — failure paths, retry flows, and support views are stories too
- invent architecture not present in the inputs
- slice work only by technical layer
- leave user stories until the later planning projection step
- create tasks for all future deliverables
- ignore impacted components or regression-sensitive behaviors when the initiative changes an existing system
- hide governed boundary changes inside generic capability names
- ignore architecture conflicts
- produce a table without evidence or owner

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Architecture constraints are referenced.
- [ ] Business requirements remain traceable.
- [ ] Epic / Feature / User Story structure is defined and traceable.
- [ ] Every feature has at least two user stories — any feature with one story has been restructured.
- [ ] Each story represents a distinct, independently testable behavior — not a restatement of the feature name.
- [ ] Stories cover multiple personas, failure paths, and edge cases where the BRS implies them.
- [ ] User stories use `As a <persona>, I want <capability>, so that <business value>.`
- [ ] Story entries point to acceptance / validation references.
- [ ] Existing-system impact is visible where it changes slicing or validation expectations.
- [ ] Governed service/API, data, and event boundaries are visible where relevant.
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] The output gives later architecture review a concrete initiative shape to assess.
- [ ] The artifact is specific enough for readiness and handoff shaping, not just structurally complete.
