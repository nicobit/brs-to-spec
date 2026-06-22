# Enhancement 1 — Fix Delivery Structure Sequencing

## Problem

The orchestrator workflow (`brs-to-spec-run-workflow.md` Step 3 stage table) currently places:

- Stage 2b: business-rules — after business intake
- Stage 2c: actors-and-personas — after business intake
- Stage 4: delivery-structure draft — after business intake + architecture draft

Stages 2b and 2c run before stage 4 in the table but the `create-delivery-structure` skill lists them as "optional inputs when available", not required. The result: the orchestrator creates delivery-structure from BRS + intake summary alone, and business-rules and actors are filled in later — after stories already exist without BR links or ACT-NNN actor references.

## What needs to change

### Change 1 — `brs-to-spec-run-workflow.md` Step 3 stage table

The `Blocked by` column for stage 4 (Draft delivery shape) must be updated:

**Current:**
```
| 4 | Draft delivery shape | `planning/delivery-structure.md` (epics + features only) | ... | ... | (2) |
```

**Change to:**
```
| 4 | Draft delivery shape | `planning/delivery-structure.md` (epics + features only) | ... | ... | (2)(2b)(2c) |
```

This makes delivery-structure draft depend on both business-rules and actors-and-personas being present first.

Also update the hard gate rules table:

**Current:**
```
| Architecture review (5) | `business-intake/business-intake-summary.md` with objectives and gaps; `planning/delivery-structure.md` draft with epics |
```

**Change to:**
```
| Architecture review (5) | `business-intake/business-intake-summary.md` with objectives and gaps; `business-intake/business-rules.md`; `business-analysis/actors-and-personas.md`; `planning/delivery-structure.md` draft with epics |
```

### Change 2 — `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md`

The Inputs section currently reads:

```
Use these inputs when available:
- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`
```

**Change to:**

```
## Inputs

Required:
- `input/brs.md` or `input/brs/*.md` — functional requirements (FR-NNN) and acceptance criteria (AC-NNN)
- `business-intake/business-intake-summary.md` — objectives, scope, requirements summary

Required before confirmed stage (must exist before stories can be confirmed):
- `business-intake/business-rules.md` — BR-NNN rules; stories must reference the rules that constrain them
- `business-analysis/actors-and-personas.md` — ACT-NNN IDs; every story actor must use these IDs, not free-text role names

Optional:
- `input/architecture.md` or `input/architecture/*.md` — system components and integration context
```

Also add to the **Stop conditions** section:

```
- If `business-intake/business-rules.md` is missing and stories are being confirmed (not just drafted at epics level): stop. Business rules must be extracted before stories can be confirmed. Run `skills/2-business-intake/02-extract-business-rules.md` first.
- If `business-analysis/actors-and-personas.md` is missing and stories are being confirmed: stop. Actors must be extracted before stories can be confirmed. Run `skills/2-business-intake/03-extract-actors-and-personas.md` first.
```

### Change 3 — `brs-to-spec-run-workflow.md` Step 5 pre-generation gate check

Add a new block for the delivery-structure pre-generation gate:

```
**For `planning/delivery-structure.md` (confirmed — stage 9):** [existing block, add to it]
- [ ] `business-intake/business-rules.md` exists → read it → confirm BR-NNN rules are present
- [ ] `business-analysis/actors-and-personas.md` exists → read it → confirm ACT-NNN IDs are present
- If either missing: generate the missing artifact first. Do not confirm delivery-structure.
```

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`
2. In Step 3 stage table: update the `Blocked by` cell for stage 4 from `(2)` to `(2)(2b)(2c)`
3. In Step 3 hard gate rules table: update the Architecture review (5) row to include business-rules and actors-and-personas
4. In Step 5 pre-generation gate check: add the two checklist items for stage 9 (confirmed delivery-structure)
5. Open `.brs2spec/skills/3-planning-and-modular-delivery/03-create-delivery-structure.md`
6. Update the Inputs section as described above
7. Add the two stop conditions as described above

## Quality bar

After this change:
- The orchestrator cannot create a confirmed delivery-structure without business-rules and actors-and-personas already present
- The `create-delivery-structure` skill explicitly reads and uses BR-NNN and ACT-NNN in story authoring
- Stories created at the draft stage (epics + features) can still be created with only BRS + intake — this is correct and not blocked
