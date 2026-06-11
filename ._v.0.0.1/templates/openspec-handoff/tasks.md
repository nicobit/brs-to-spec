# Tasks — {{F-XXX.X}}: {{User Story Name}}

> Implementation checklist for `/opsx:apply`.
> Scoped to this user story only. Tasks are ordered within this story — complete each before starting the next.
> See `openspec/changes/dependency-graph.md` for the order between stories.
>
> **Repository scope (omit this line if flat handoff structure):** These tasks cover the `{{repo-name}}` repository slice of story {{F-XXX.X}} only. Check `dependency-graph.md` § Cross-repo dependencies to see if this repo must wait for a sibling repo to deliver first.

## Implementation tasks

<!--
One task per independently reviewable unit of work (one PR boundary).
- [ ] OS-{{F-XXX.X}}-NNN: <verb> <what> — <one-line outcome>
  - Requirement: FR-NNN / NFR-NNN
  - Acceptance: <AC ID or location>
  - Architecture constraint: AR-XXX — <rule summary>  (omit if none)
  - Data: <tables created or modified>  (omit if none)
  - API: <endpoints created or modified>  (omit if none)
  - Events to emit: <signal names from design.md#observability>  (omit if none)
  - Evidence expected: <what proves this task is done>
-->

- [ ] OS-{{F-XXX.X}}-001:
  - Requirement:
  - Acceptance:
  - Architecture constraint:
  - Data:
  - API:
  - Events to emit:
  - Evidence expected:

## Validation tasks

<!-- One entry per AC that requires an explicit test or verification step. -->
<!-- Link each validation task to the BDD scenario(s) it executes — use SCN-NNN IDs from proposal.md. -->

- [ ] OS-{{F-XXX.X}}-V01: Verify {{criterion}} — {{SCN-NNN}}
  - Acceptance source: AC-NNN
  - BDD scenario: SCN-NNN (see `quality-gates/bdd-scenarios.md`)
  - How to validate:
  - Evidence expected:

## Done criteria

<!-- This story is done when ALL of the following are true. -->
<!-- Keep this short — these are the conditions, not implementation steps. -->

- [ ] All implementation tasks merged and passing CI
- [ ] All BDD scenarios referenced in proposal.md pass (SCN-NNN … SCN-NNN)
- [ ] All validation tasks executed with evidence attached
- [ ] Any telemetry signals from this story visible in staging
- [ ] Dependent stories unblocked — notify team when done (see dependency-graph.md)
