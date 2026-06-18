# Proposal — {{F-XXX.X}}: {{User Story Name}}

> OpenSpec change proposal for one user story. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder (`specs/{{F-XXX.X}}-{{slug}}/`) into the target code repository before applying.
>
> **Repository scope (omit this line if flat handoff structure):** This proposal covers the `{{repo-name}}` repository slice of story {{F-XXX.X}}. Other repos involved in this story have their own proposal in sibling subfolders.

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

<!-- MULTI-REPO ONLY — omit this table if flat handoff structure: -->
<!-- Cross-repo dependencies within this story (intra-story repo sequencing): -->
<!-- | This repo | Depends on repo | Reason | -->
<!-- | {{repo-name}} | {{other-repo}} | e.g. requires stable API contract before UI integration can start | -->
<!-- See specs/dependency-graph.md § Cross-repo dependencies for the full picture. -->

## Acceptance criteria

| AC ID | Criterion | How to verify | BDD scenario(s) | Evidence expected |
|---|---|---|---|---|

<!-- AC IDs must match the BRS (AC-NNN). BDD scenario IDs must match quality-gates/bdd/<F-NNN.md> (SCN-NNN). -->
<!-- Every AC must have at least one BDD scenario or an explicit note that it is verified by manual review. -->

## BDD scenarios

| Scenario ID | Type | Summary |
|---|---|---|
| SCN-NNN | Happy path / Negative / Boundary / Authorization | One-line description |

<!-- List only the scenarios that directly validate this story. Full Gherkin is in quality-gates/bdd/<F-NNN.md> for this story's feature. -->
<!-- Minimum: one happy-path and one failure scenario. Add boundary/authorization where the AC implies them. -->

## Out of scope

<!-- Explicit list of what this story does NOT do. -->
<!-- One bullet per exclusion. If nothing is explicitly excluded, write "none." -->

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| BDD scenarios | `quality-gates/bdd/<F-NNN.md>` | Full Gherkin for SCN-NNN referenced above (use this story's feature file) |
| Architecture rules | `architecture/architecture-rules.md` | Binding rules that apply to this story |
| Data contract | `quality-gates/data-contract.md` | Full schema, PII mapping, retention |
| API contract | `quality-gates/api-contract.md` | Full endpoint specs, sandbox credentials |
| Security review | `quality-gates/security-review.md` | Security checklist |
| Observability plan | `quality-gates/observability-plan.md` | Full telemetry catalog, runbooks |
