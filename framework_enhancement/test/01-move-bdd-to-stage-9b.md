# Enhancement Prompt 01 — Move BDD to Stage 9b

## What this prompt does

Edits `.brs2spec/brs-to-spec-run-workflow.md` to:
1. Move the BDD gate from stage 12 to stage 9b (immediately after delivery structure confirmed)
2. Update the hard gate table so architecture review (5) and engineering readiness (8) are no longer prerequisites for BDD
3. Make BDD a prerequisite for test strategy (stage 10) and engineering readiness (stage 8, for referencing scenarios)
4. Update the pre-generation gate check for BDD to reflect new prerequisites
5. Update stage 12 to exclude BDD (it now only covers security, API contract, data contract, observability)

## File to edit

```
.brs2spec/brs-to-spec-run-workflow.md
```

## Step 1 — Update the stage table (Step 3)

Find the stage table in "Step 3 — Assess and sequence stages". The table currently has:

- Stage 9: Delivery structure confirmed
- Stage 9b: Business analysis (confirmed) — Process flows
- Stage 9c: Business analysis (confirmed) — Use cases
- Stage 9d: Story enrichment check
- Stage 12: Quality gates (includes BDD + test-strategy)

Replace with the new ordering. Insert stage 9b (BDD) immediately after stage 9, push current 9b/9c/9d down by one letter:

```
| 9  | Delivery structure confirmed | `planning/delivery-structure/` (full stories) | [existing done criteria unchanged] | [existing prompt] | readiness = Ready; (2b); (2c) |
| 9b | BDD scenarios (three amigos) | `quality-gates/bdd/` | One F-NNN.md per feature group; acceptance-checklist.md exists with Status row; every F-XXX.X story has ≥1 happy-path and ≥1 failure scenario with full Gherkin; SCN-NNN IDs sequential across initiative | `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | (9) — delivery structure confirmed with F-XXX.X IDs |
| 9c | Business analysis (confirmed) — Process flows | `business-analysis/process-flows.md` (confirmed) | PF-NNN flows enriched with confirmed F-XXX.X story IDs, AC-NNN references, and correct step ordering | `skills/2-business-intake/04-create-process-flows.md` | (9)(2d) |
| 9d | Business analysis (confirmed) — Use cases | `business-analysis/use-case-spec.md` (confirmed) | UC-NNN specs enriched with F-XXX.X story IDs, AC-NNN coverage table, and alternative flows | `skills/2-business-intake/05-create-use-case-specs.md` | (9)(9c)(2e) |
| 9e | Story enrichment check | `planning/delivery-structure/` (all stories enriched) | Every confirmed story has: ACT-NNN actor; ≥1 BR-NNN link or explicit "none apply"; ≥1 testable AC-NNN; PF-NNN reference if process flows exist | (orchestrator inline — no separate skill) | (9)(9c) |
```

For stage 12, update its note to remove BDD:
```
| 12 | Quality gates | `quality-gates/<gate>.md` (triggered gates only — security, API contract, data contract, observability) | Each gate: real content, ticked checklist, `Status: Accepted` in the Metadata table at the top of the file. **BDD and test strategy are handled at stages 9b and 10 respectively — do not re-run them here.** | `skills/4-engineering-readiness/quality-gates/create-<gate>.md` | (8)(9e)(11) |
```

## Step 2 — Update the hard gate table

Find "Hard gate rules" table. Update the row for quality gates (stage 12):

Old:
```
| Handoff (13) | All triggered gates with `Status: Accepted`; `state/open-decisions.md` with zero blocking decisions |
```

Add a new row for BDD:
```
| BDD scenarios (9b) | `planning/delivery-structure/` confirmed with F-XXX.X IDs — no other upstream gate required |
| Handoff (13) | All triggered gates with `Status: Accepted` including BDD (9b) and test strategy (10); `state/open-decisions.md` with zero blocking decisions |
```

## Step 3 — Update the pre-generation gate check for BDD

Find "For `quality-gates/bdd/` (stage 12 — BDD gate):" in Step 5.

Replace the heading and prerequisite check:

Old heading: `**For \`quality-gates/bdd/\` (stage 12 — BDD gate):**`
New heading: `**For \`quality-gates/bdd/\` (stage 9b — BDD gate — three amigos):**`

Replace the prerequisite check:
Old:
```
- [ ] Read `planning/delivery-structure.md` → confirm it contains at least one story with an `F-XXX.X` ID. If no `F-XXX.X` IDs are present anywhere in the file, delivery-structure is still at draft stage — do NOT invoke `qa.create_bdd_scenarios`. Execute stage 9 (expand delivery structure) first, then re-invoke the BDD gate.
- If delivery-structure is still a draft: stop. State: "BDD scenarios require confirmed user stories with F-XXX.X IDs. Executing stage 9 first."
```

New:
```
- [ ] Read `planning/delivery-structure/` — confirm it contains at least one story with an `F-XXX.X` ID, a "As a / I want / so that" statement, and at least one AC-NNN. If no `F-XXX.X` IDs are present, delivery-structure is still at draft stage — execute stage 9 first.
- [ ] **No other upstream gate is required.** BDD does not require engineering readiness, architecture review, or test strategy. It requires only confirmed stories. This is by design — BDD is the three-amigos output written during refinement, before engineering readiness.
- If delivery-structure is still a draft: stop. State: "BDD scenarios require confirmed user stories (F-XXX.X IDs). Executing stage 9 first."
```

## Step 4 — Update the stale artifact check (Step 2a)

Find the stale artifact check table. The row for BDD currently reads:

```
| `quality-gates/bdd/` or `quality-gates/bdd-scenarios.md` (if either exists) | Coverage summary story IDs vs delivery-structure story IDs | Any `F-XXX.X` ID present in `delivery-structure.md` that is absent from the BDD coverage — mark bdd as stale and re-run `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
```

This row is still correct — no change needed. BDD staleness detection works the same regardless of phase.

## Step 5 — Update the handoff pre-generation check

Find the BDD check inside "For handoff (`specs/`)":

Old:
```
- [ ] If the BDD gate is triggered: check which BDD artifact exists — `quality-gates/bdd/acceptance-checklist.md` (new format) or `quality-gates/bdd-scenarios.md` (legacy format). Read whichever exists and check its `Status` row. For the new format: every `F-NNN.md` feature file must exist and every `F-XXX.X` story ID must appear in that file's coverage summary. For the legacy format: every `F-XXX.X` story ID from `delivery-structure.md` must appear in the coverage summary table. If any story ID is missing, the BDD gate is stale. A BDD gate Accepted on a stub delivery-structure does not count.
```

No change needed to this check — it already validates the right things.

## Self-review after applying

Verify:
- [ ] Stage 9b in the stage table is BDD scenarios with prerequisite (9) only
- [ ] Old 9b/9c/9d are renumbered to 9c/9d/9e
- [ ] Stage 12 no longer mentions BDD
- [ ] Hard gate table has a row for BDD (9b) with only (9) as prerequisite
- [ ] Handoff hard gate requires BDD `Status: Accepted`
- [ ] Pre-generation check for BDD says stage 9b and has no architecture review prerequisite
