# Proposal — {{F-XXX.X}}: {{User Story Name}}

> OpenSpec change proposal for one user story. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder (`openspec/changes/{{F-XXX.X}}-{{slug}}/`) into the target code repository before applying.

## User story

**As a** {{role}},
**I want** {{capability}},
**so that** {{outcome}}.

**Requirement:** {{FR-NNN / NFR-NNN}}
**Acceptance criteria:** {{location in brs.md or inline}}

## Why now

<!-- One sentence: why this story is needed at this point in the sequence. -->
<!-- Reference the business driver or the story that unblocks this one. -->

## What changes

<!-- Bullet list — one line per concrete system change this story introduces. -->
<!-- No implementation detail — that belongs in design.md. -->

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on (must be deployed first) | | |
| Can run in parallel with | | |
| Blocks (cannot start until this is done) | | |

<!-- If no dependency, write "none" in the Story ID column. -->
<!-- Derive from delivery-structure.md increment grouping and shared schema/API dependencies. -->

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Architecture rules | `architecture/architecture-rules.md` | Binding rules that apply to this story |
| Data contract | `quality-gates/data-contract.md` | Full schema, PII mapping, retention |
| API contract | `quality-gates/api-contract.md` | Full endpoint specs, sandbox credentials |
| Security review | `quality-gates/security-review.md` | Security checklist |
| Observability plan | `quality-gates/observability-plan.md` | Full telemetry catalog, runbooks |
