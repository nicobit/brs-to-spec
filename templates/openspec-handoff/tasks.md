# Tasks — {{Deliverable ID}}: {{Deliverable Name}}

> Implementation checklist for `/opsx:apply`.
> Each task is independently reviewable and traceable to a requirement, user story, and acceptance source.
> Tasks are ordered: complete each before starting the next — later tasks may depend on earlier ones.

## Implementation tasks

<!--
One task block per unit of work. Keep tasks small enough to review in one PR.
Format:
- [ ] OS-NNN: <verb> <what> — <one-line outcome>
  - User story: F-XXX.X — <story summary>
  - Requirement: FR-NNN / NFR-NNN
  - Acceptance: <where the AC lives — brs.md, design.md#section, specs/api.md>
  - Architecture constraint: AR-XXX — <rule summary>
  - Data: <tables created or modified>
  - API: <endpoints created or modified>
  - Events to emit: <telemetry signals from design.md#observability-requirements>
  - Evidence expected: <what proves this task is done — test result, endpoint response, metric visible in staging>
-->

- [ ] OS-001: <!-- task -->
  - User story:
  - Requirement:
  - Acceptance:
  - Architecture constraint:
  - Data:
  - API:
  - Events to emit:
  - Evidence expected:

## Validation tasks

<!--
One entry per acceptance criterion that requires an explicit test or check.
These run after implementation tasks are complete.
-->

- [ ] OS-V01: Verify <criterion> in staging
  - Acceptance source:
  - How to validate:
  - Evidence expected:

## Handoff checklist

<!-- Gate items that must be true before this increment is considered done. -->
<!-- Tick each when confirmed — do not mark tasks complete until this checklist is done. -->

- [ ] All implementation tasks merged and passing CI
- [ ] All validation tasks executed with evidence attached
- [ ] Telemetry signals visible in staging dashboard
- [ ] API contract verified against sandbox (happy path + failure modes)
- [ ] Data contract: PII fields encrypted, retention rules applied
- [ ] Security checklist items from `quality-gates/security-review.md` confirmed in staging
- [ ] Runbooks linked to alert rules and reviewed by SRE
- [ ] `specs/` folder copied into code repo alongside this handoff folder
