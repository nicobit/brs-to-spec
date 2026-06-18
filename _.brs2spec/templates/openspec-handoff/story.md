# Story — {{F-XXX.X}}: {{User Story Name}}

> Complete specification for one user story: the "why", acceptance criteria, and BDD scenarios.
> Drive implementation with `/opsx:apply` against this folder (story.md + design.md + tasks.md).
> Self-contained: an engineer implements from this folder without opening any other artifact.
>
> **Repository scope (omit this line if flat handoff structure):** This story covers the `{{repo-name}}` repository slice of story {{F-XXX.X}}. Other repos involved in this story have their own story.md in sibling subfolders.

## User story

**As a** {{role}},
**I want** {{capability}},
**so that** {{outcome}}.

**Requirement:** {{FR-NNN}}
**Why now:** {{one sentence — business driver or the story that unblocks this one}}

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

<!-- MULTI-REPO ONLY — omit this table if flat handoff structure: -->
<!-- Cross-repo dependencies within this story (intra-story repo sequencing): -->
<!-- | This repo | Depends on repo | Reason | -->
<!-- | {{repo-name}} | {{other-repo}} | e.g. requires stable API contract before UI integration can start | -->

## Acceptance criteria

<!-- Copy each AC verbatim from input/brs.md — do not paraphrase. -->
<!-- Every AC must have at least one BDD scenario (see BDD scenarios section) and at least one TC-NNN test case (see Test plan section), or an explicit note that it is verified by manual review. -->

| AC ID | Criterion (verbatim from BRS) | Verified by |
|---|---|---|
| AC-NNN | | SCN-NNN / TC-NNN / Manual review |

## BDD scenarios

<!-- BDD scenarios are authored in quality-gates/bdd/ — the single source of truth. -->
<!-- Do not copy Gherkin into this file — reference the scenarios below. -->
<!-- The coding-prompt.md and test-plan.md for this story reference the same SCN-NNN IDs. -->

**Canonical source:** `quality-gates/bdd/F-NNN.md` — section "F-XXX.X — {{User Story Name}}"

Scenarios in scope for this story:

| SCN-ID | Scenario name | Type | Priority | AC |
|---|---|---|---|---|
| SCN-NNN | {{scenario name}} | Happy path | Must | AC-NNN |
| SCN-NNN | {{scenario name}} | Failure / negative | Must | AC-NNN |
| SCN-NNN | {{scenario name}} | Boundary | Should | AC-NNN |
| SCN-NNN | {{scenario name}} | Authorization | Must | AC-NNN |

<!-- Fill the table from quality-gates/bdd/F-NNN.md coverage summary for this story. -->
<!-- Do not add rows that are not in the BDD file. Do not write Gherkin here. -->

## Test plan

<!-- The test plan defines what will be tested, at what level, and with what priority for this story. -->
<!-- It is the output of the three-amigos session and is the contract the developer implements against. -->

**Full test plan:** `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md`

### C1 — Critical (blocks merge)

<!-- Copy the C1 rows from quality-gates/test-plans/{{F-XXX.X}}-test-plan.md -->

| TC-ID | Test type | Condition | Expected outcome |
|---|---|---|---|
| TC-NNN | {{Unit / Integration / Security}} | {{condition}} | {{expected outcome}} |

### C2 — High (blocks sprint done)

| TC-ID | Test type | Condition | Expected outcome |
|---|---|---|---|
| TC-NNN | {{test type}} | {{condition}} | {{expected outcome}} |

<!-- C3 and C4 test cases are tracked in the full test plan — not repeated here. -->
<!-- Overall story risk: {{C1 / C2 / C3 / C4}} — see full test plan for rationale. -->

## Out of scope

<!-- Explicit list of what this story does NOT do. At minimum one item. -->

## Files likely impacted

<!-- List files the engineer is likely to create or modify for this story. -->
<!-- Derive from: story scope, design.md integration points, architecture-rules.md, input/repositories/ descriptors. -->
<!-- Omit if repo context is not available — do not invent paths. -->
<!-- Format: one file per line, grouped by layer. -->

```
# API / backend
src/...

# Data / migrations
db/migrations/...

# Tests
tests/...
```

## Constraints inherited from upstream

| Rule ID | Type | Constraint | How applied in this story |
|---|---|---|---|

<!-- Include AR-NNN rules from architecture-rules.md and BR-NNN rules from business-intake/business-rules.md that directly affect this story. -->
<!-- Reference the rule ID — not a generic restatement. Type = AR (architecture) or BR (business rule). -->

## Carried-forward context

<!-- Copy any rows from engineering-readiness/initiative-context.md that affect this story's implementation. -->
<!-- Delete this section if none apply. -->

## Open questions

<!-- Questions that must be resolved before coding starts. Delete if none. -->

| # | Question | Owner | Needed before |
|---|---|---|---|

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Architecture rules | `architecture/architecture-rules.md` | Binding rules that apply to this story |
| Data contract | `quality-gates/data-contract.md` | Full schema, PII mapping, retention |
| API contract | `quality-gates/api-contract.md` | Full endpoint specs, auth, error codes |
| Security review | `quality-gates/security-review.md` | Security checklist and accepted risks |
| Observability plan | `quality-gates/observability-plan.md` | Telemetry catalog, alert rules, runbooks |
