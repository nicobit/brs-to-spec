# BDD Gate — Acceptance Checklist

> **The gate Status is set here — this is the only authoritative Status row for the BDD gate.**
> BDD scenarios now live inside each story folder (`specs/F-XXX.X-<slug>/story.md`).
> This checklist confirms that all story.md files exist and coverage is complete before handoff proceeds.

## Metadata

| Field | Value |
|---|---|
| Active deliverable | |
| Author | |
| Date | |
| **Status** | **In progress** — change to `Accepted` when all checklist items are Done |

## Story coverage index

> One row per user story. Update as each story.md is written.

| Story ID | Story name | story.md exists? | Happy path? | Failure scenario? | AC-NNN refs? |
|---|---|---|---|---|---|
| F-XXX.X | | | | | |

## Global coverage checklist

| Item | Done? | Notes |
|---|---|---|
| Every in-scope user story has a story.md with full Gherkin (not just a summary table) | | |
| Every story has at least one happy-path and one failure/negative scenario | | |
| Authorization paths covered for stories with role-based access | | |
| Every scenario metadata block has: Requirement (FR-NNN), AC (AC-NNN), Scenario type | | |
| Every AC in each story's AC table has at least one BDD scenario or "Manual review" noted | | |
| No scenario uses the same AC-NNN as every other scenario in its story | | |
| Every When has exactly one action; every Then describes an observable outcome | | |
| High-risk stories (async, RBAC, dry-run, state transitions, export) meet minimum scenario counts | | |
| SCN-NNN IDs are sequential across all story.md files with no gaps or duplicates | | |

## CI Gate

> Add this section when Status reaches Accepted.

| Field | Value |
|---|---|
| Test runner / tool | (e.g. pytest-bdd, Cucumber, SpecFlow, Cucumber-js) |
| CI command | (e.g. pytest features/ -v --tb=short) |
| CI step name | (e.g. BDD acceptance gate) |
| Gate status | Not wired / Wired / Passing |
