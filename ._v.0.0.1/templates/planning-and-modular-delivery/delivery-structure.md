# Delivery Structure

> Primary consumer: Delivery lead, Product Owner, architect, engineering lead
> Purpose of this artifact: define the planning structure, story hierarchy, slices, governed boundaries, and traceability expectations
> Downstream use: traceability, readiness, handoff, GitLab Planning View projection
> Do not duplicate: full acceptance text, repeated architecture rationale, or step-by-step implementation instructions
> Keep this artifact structurally rich but text-light.
> Use it to show delivery-shaping decisions, not to narrate the whole initiative.
> Reference acceptance and architecture sources instead of copying them.
> Keep Epic / Feature / User Story structure, governed boundaries, and traceability logic detailed.
> Keep business capability overviews, candidate modules, and candidate slices summary-level unless more detail changes delivery decisions.
> Optional visual view: add a compact slice/dependency or capability-to-module orientation view only when it materially improves planning, handoff, or review clarity.

## Business Capabilities

List capabilities only at the level needed to shape epics, features, and slices.
Keep this section summary-level.

## Epic Breakdown

This section should be detailed enough to support planning and traceability.

| Epic ID | Epic title | Business objective | Source requirement(s) | Notes |
|---|---|---|---|---|

## Feature / Capability Breakdown

This section should be detailed enough to support story grouping and handoff shaping.

| Feature ID | Parent epic | Feature / capability | Business value | Source requirement(s) | Notes |
|---|---|---|---|---|---|

## User Story Breakdown

This section should be detailed enough for downstream handoff and planning projection.

Every feature must have at least one well-formed user story. A feature with only one story must include a one-line justification for why further splitting is not useful or not yet needed (e.g. "single atomic capability — no meaningful split at this stage"). Do not force artificial stories.

Derive multiple stories where scope warrants it from: different personas, happy path vs failure path, retry flows, support/admin views, edge cases, and distinct entry points implied by the BRS. Do not write stories that merely restate the feature name.

| Story ID | Parent feature | User story | Source requirement(s) | Acceptance / validation reference | Architecture constraints | Likely quality gates | Likely enablement needs |
|---|---|---|---|---|---|---|---|

## Story Traceability Rules

State how stories map back to requirements and how downstream tasks must preserve that traceability.
Keep the rules compact and operational.

## Acceptance / Validation References

List where acceptance behavior is actually defined so it is referenced, not duplicated.
Do not restate full acceptance criteria here.

## Existing-System Impact Summary

Include only brownfield impact that changes slicing, validation, rollout, or risk.

| Area | Impact | Source evidence | Validation / mitigation expectation |
|---|---|---|---|

## Governed Boundaries

List only real service, data, or event boundaries that affect contracts or control points.

| Boundary ID | Boundary type | Producer / Owner | Consumer(s) | Created / Changed? | Why governed? | Likely contract gate |
|---|---|---|---|---|---|---|

## Candidate Modules

Keep this section summary-level unless module detail changes slice design, ownership, or contract decisions.

## Optional Visual View

Add only when a compact slice/dependency or capability-to-module orientation view clarifies the delivery shape better than tables alone.
Prefer one focused embedded diagram, not a second planning artifact.

## Candidate Delivery Slices

Keep this section summary-level until active deliverables are selected.
