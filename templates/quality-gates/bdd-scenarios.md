# BDD Scenarios

> Primary consumer: QA, PO, engineering lead, coding agent
> Purpose: executable acceptance specification — one scenario per distinct behavior, grouped by user story
> Downstream use: OpenSpec handoff (proposal references SCN-NNN IDs); implementation tasks done criteria; test automation
> Do not duplicate: full AC text from BRS; architecture rationale; implementation steps

## Metadata

| Field | Value |
|---|---|
| Active deliverable |  |
| Author |  |
| Date |  |
| Status | Draft / In review / Accepted |

## Coverage summary

> One row per scenario. Every user story that is in scope must appear here.
> A story with no row is a coverage gap — do not advance to handoff until all stories have at least a happy-path scenario.

| Scenario ID | Story ID | Requirement ID | Business rule | Scenario type | Priority | Status |
|---|---|---|---|---|---|---|
| SCN-001 | F-XXX.X | FR-NNN | | Happy path | Must | Draft |

---

## Scenarios by user story

> Group all scenarios for the same story together under a heading.
> Each story must have: at least one happy-path scenario, at least one failure/negative scenario, and any authorization or boundary scenario implied by the AC.

---

### F-XXX.X — {{User story name}}

> As a {{role}}, I want {{capability}}, so that {{outcome}}.
> Requirement: {{FR-NNN}}
> AC location: `input/brs.md` § {{section}} or inline below

#### SCN-001 — {{Scenario name}} (Happy path)

| Field | Value |
|---|---|
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Happy path |
| Priority | Must |

```gherkin
Given ...
When ...
Then ...
```

#### SCN-002 — {{Scenario name}} (Failure / negative)

| Field | Value |
|---|---|
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Negative |
| Priority | Must |

```gherkin
Given ...
When ...
Then ...
```

#### SCN-003 — {{Scenario name}} (Authorization / boundary)

| Field | Value |
|---|---|
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Authorization |
| Priority | Should |

```gherkin
Given ...
When ...
Then ...
```

---

## Coverage gaps and open questions

| Question ID | Story | Question | Impact | Owner |
|---|---|---|---|---|

## Acceptance checklist

| Item | Done? | Notes |
|---|---|---|
| Every in-scope user story has at least one happy-path scenario | | |
| Every in-scope user story has at least one failure/negative scenario | | |
| Authorization paths covered for stories that have role-based access | | |
| Every scenario references a Story ID and a Requirement ID | | |
| Every scenario references the AC it validates | | |
| No scenario merely restates the feature name — each tests a distinct behavior | | |
| Coverage summary table is complete and matches the scenario blocks below | | |
