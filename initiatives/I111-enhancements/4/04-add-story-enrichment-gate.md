# Enhancement 4 — Add Story Enrichment Gate

## Problem

There is no checkpoint between delivery-structure confirmed (stage 9) and quality gates (stage 12) that verifies every story is substantively complete. Enhancement 2 strengthens the confirmed-stage done criteria inside `create-delivery-structure.md`, but the orchestrator's pre-generation gate check for handoff only verifies structural completeness (F-XXX.X ID present, "As a / I want / so that" present). It does not check substantive completeness (BR-NNN links, ACT-NNN actor, testable AC).

This means a story can pass the structural gate and reach the handoff with thin content.

## What needs to change

### Change 1 — `brs-to-spec-run-workflow.md` Step 3 stage table

Add a new stage 9d between process flows (9b) and use case specs (9c):

```
| 9d | Story enrichment check | `planning/delivery-structure.md` (all stories enriched) | Every confirmed story has: ACT-NNN actor; at least one BR-NNN link or explicit "no BR applies" note; at least one testable AC-NNN; PF-NNN reference (if process flows exist). Stories that fail are returned to delivery-lead skill for enrichment. | (orchestrator inline check — no separate skill) | (9)(9b) |
```

### Change 2 — `brs-to-spec-run-workflow.md` Step 5 pre-generation gate check

Replace the current delivery-structure confirmed check with a more explicit story-by-story check:

**In the "For handoff (`openspec/changes/`)" block, add:**

```
**Story enrichment check (run before creating any story folder):**

For every `F-XXX.X` story in `planning/delivery-structure.md`, verify ALL of the following:

| Check | Pass condition | Fail condition |
|---|---|---|
| Actor | Uses `ACT-NNN` ID from actors-and-personas.md | Free-text role name only ("Applicant", "Underwriter") |
| Business rules | Has at least one `BR-NNN` link | Has no BR link and no "no BR applies" note |
| Acceptance criteria | At least one AC describes an observable outcome | AC is vague ("system works", "processed correctly") |
| Process flow | References `PF-NNN` if process flows exist | No PF reference and process flows exist |

If any story fails any check: do not create the story folder. Instead:
1. List every failing story with the specific fields that need enrichment
2. Run `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` targeting only the failing stories
3. After enrichment, re-run the story enrichment check
4. Only proceed to handoff generation when every story passes all checks
```

### Change 3 — `brs-to-spec-run-workflow.md` Step 3 stage table, stage 13 (Handoff) blocked-by

Update the `Blocked by` column for stage 13 to include `(9d)`:

**Current:** `all gates Accepted; zero blocking open decisions`

**Change to:** `(9d) story enrichment check passed; all gates Accepted; zero blocking open decisions`

### Change 4 — New inline enrichment behavior in the orchestrator

Add a new execution rule to the orchestrator (Step 6 — Execute the next stage):

```
### Story enrichment (stage 9d)

When executing story enrichment (stage 9d), the orchestrator acts as the delivery-lead persona for enrichment only — it does not create new stories, does not change story scope, and does not change F-XXX.X IDs.

For each story that fails the enrichment check:
1. Read the story's FR-NNN from `input/brs.md` to find the matching functional requirement
2. Read `business-intake/business-rules.md` to find BR-NNN rules whose "impacted features" column includes this story's F-XXX.X ID
3. Read `business-analysis/actors-and-personas.md` to find the ACT-NNN that matches the story's persona
4. Read `business-analysis/process-flows.md` to find the PF-NNN where this story's F-XXX.X appears in "Related features and stories"
5. Update the story's fields in `planning/delivery-structure.md` in-place — do not change the story's scope, just add the missing references
6. Record the enrichment in `state/workflow-state.json`: `"story_enrichment": { "stories_enriched": ["F-XXX.X", ...], "date": "..." }`
```

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`
2. In Step 3 stage table: add stage 9d after 9b/9c
3. In Step 5 pre-generation gate check (handoff block): add the story enrichment check table
4. In Step 3 stage 13 `Blocked by` column: add `(9d)`
5. In Step 6: add the "Story enrichment (stage 9d)" inline behavior section

## Quality bar

After this change:
- The orchestrator cannot proceed to quality gates or handoff while any story has a free-text actor, missing BR link, vague AC, or missing PF reference (when process flows exist)
- Enrichment is a targeted fix — it adds missing references to existing stories, it does not rewrite stories
- The check is fast: the orchestrator reads delivery-structure.md and validates each story against the already-present business analysis artifacts
- Stories that were correctly authored at confirmed stage pass immediately with no extra work
