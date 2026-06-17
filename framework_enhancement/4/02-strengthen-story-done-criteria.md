# Enhancement 2 — Strengthen Story Done Criteria

## Problem

The confirmed-stage story quality bar in `create-delivery-structure.md` currently requires:
- `F-XXX.X` ID
- "As a / I want / so that" statement
- At least one `AC-NNN` acceptance criterion reference
- A `FR-NNN` requirement ID

It does not require:
- A `BR-NNN` link (or explicit statement that no business rules apply)
- An actor reference using `ACT-NNN` from `actors-and-personas.md` — free-text role names pass today
- A testability check on the AC — vague AC like "the system works correctly" currently passes

Stories that lack these fields look complete but produce thin handoff packages that give coding agents insufficient constraint information.

## What needs to change

### Change 1 — `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md`

In the **Draft vs confirmed** section, update the confirmed-stage requirements:

**Current:**
```
- **Confirmed stage** (after readiness = Ready): all stories must be fully formed. Every story MUST have:
  - An `F-XXX.X` ID (assign sequentially if not yet present)
  - A verbatim "As a `<persona>`, I want `<capability>`, so that `<business value>`." statement
  - At least one `AC-NNN` acceptance criterion reference pointing to a specific row in `input/brs.md`
  - A `FR-NNN` requirement ID
  - A story that lacks any of these is still a stub — expand it before marking delivery-structure as confirmed.
```

**Change to:**
```
- **Confirmed stage** (after readiness = Ready): all stories must be fully formed. Every story MUST have:
  - An `F-XXX.X` ID (assign sequentially if not yet present)
  - An actor reference using the `ACT-NNN` ID from `business-analysis/actors-and-personas.md` — free-text role names are not accepted at confirmed stage
  - A verbatim "As a `ACT-NNN <persona>`, I want `<capability>`, so that `<business value>`." statement
  - At least one `AC-NNN` acceptance criterion reference pointing to a specific row in `input/brs.md`; the AC text must be a testable statement (observable outcome, not "the system works correctly")
  - A `FR-NNN` requirement ID
  - At least one `BR-NNN` link from `business-intake/business-rules.md` — or an explicit inline note: `Business rules: none apply — [reason]`
  - A story that lacks any of these is still a stub — expand it before marking delivery-structure as confirmed.
```

### Change 2 — `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md`

In the **Self-review checklist**, add two new items:

```
- [ ] **Confirmed stage only:** every story uses an `ACT-NNN` ID for its actor — no free-text role names at confirmed stage.
- [ ] **Confirmed stage only:** every story has at least one `BR-NNN` link, or an explicit "Business rules: none apply — [reason]" note. Stories with no BR link and no explicit note are stubs.
- [ ] **Confirmed stage only:** every `AC-NNN` acceptance criterion is a testable statement describing an observable outcome — not "the system must handle X correctly".
```

### Change 3 — `brs-to-spec-run-workflow.md` Step 3 stage table

Update the done criteria for stage 9 (Delivery structure confirmed):

**Current:**
```
| 9 | Delivery structure confirmed | `planning/delivery-structure.md` (full stories) | Every feature has ≥1 user story with an `F-XXX.X` ID, a verbatim "As a / I want / so that" statement, at least one AC-NNN reference, and a FR-NNN requirement ID. Epics-only or bullet-list stories without IDs fail this bar. Single-story features need a splitting justification. | ... |
```

**Change to:**
```
| 9 | Delivery structure confirmed | `planning/delivery-structure.md` (full stories) | Every feature has ≥1 user story with: `F-XXX.X` ID; actor using `ACT-NNN` ID from actors-and-personas.md; verbatim "As a / I want / so that" statement; at least one testable `AC-NNN` reference; `FR-NNN` requirement ID; at least one `BR-NNN` link or explicit "no BR applies" note. Epics-only, stories without IDs, stories with free-text actors, or stories without BR links all fail this bar. Single-story features need a splitting justification. | ... |
```

### Change 4 — `brs-to-spec-run-workflow.md` Step 5 pre-generation gate check

Update the confirmed delivery-structure gate check block:

**Add to the existing check:**
```
- [ ] Read each story in `planning/delivery-structure.md` — confirm every confirmed story has:
  - An ACT-NNN actor reference (not a free-text role name)
  - At least one BR-NNN link or explicit "no BR applies" note
  - At least one AC that describes an observable, testable outcome
- If any story fails: that story is still a stub — run `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` to enrich it before proceeding to handoff.
```

## Quality bar

After this change:
- A story with "As a Applicant, I want..." fails (no ACT-NNN) — must be "As a ACT-001 Applicant, I want..."
- A story with AC: "the system processes the application correctly" fails — not a testable statement
- A story with no BR-NNN link and no explicit "no BR applies" note fails
- These checks run at stage 9 (confirmed) — they do NOT block the draft stage (epics + features)
