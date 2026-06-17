# Step 4 — Add Gap-to-Planning Gate

## Purpose

Prevent delivery structure from starting when `gaps-and-questions.md` contains unresolved blocking gaps with no stated assumption. Today the framework allows planning to proceed as long as the event is unblocked by stage — it does not verify that the spec is complete enough to decompose into stories.

This step adds a semantic gate to EVT-TPL-011 (CREATE_DELIVERY_STRUCTURE).

## Prerequisites

Steps 1–3 complete. `spec-anchoring.md` exists. Intake-summary is demoted in EVT-TPL-011.

## Design

### What changes in EVT-TPL-011

**Add to `must_include`:**
```yaml
- "If business-analysis/gaps-and-questions.md exists and contains Severity: Blocking rows,
   every such row must have either a 'Stated Assumption' or 'Resolution' recorded in the artifact
   before delivery structure may be written — the Delivery Structure Metadata section must include
   a 'Blocking Gaps Resolved' field listing GAP-NNN IDs or stating 'None'"
```

**Extend `validation_rules.natural_language`:**
```
(N) Read business-analysis/gaps-and-questions.md if it exists.
    Count every row with Severity: Blocking.
    For each blocking gap: check whether the 'Suggested Resolution' column contains a stated
    assumption (a concrete assumption that permits proceeding, not a blank or "TBD").
    If any blocking gap has no stated assumption and no resolution, fail this event and raise
    a decision requiring the gap to be resolved or explicitly assumed before planning can proceed.
    If all blocking gaps have stated assumptions, list them in the delivery-structure.md
    Metadata section under 'Blocking Gaps Proceeded With Assumption: GAP-001 (assumption text)'.
```

**Extend `on_failure`:**
```yaml
on_failure:
  raise_decision:
    question: >
      Delivery structure blocked: gaps-and-questions.md contains one or more Severity: Blocking
      gaps without stated assumptions. List each blocking gap by GAP-NNN ID. Either resolve the
      gaps in gaps-and-questions.md or add an explicit assumption for each before re-running
      CREATE_DELIVERY_STRUCTURE.
    blocking: true
    owner: "delivery-lead"
```

Note: the `on_failure.blocking: true` is intentional — unresolved blocking gaps must stop planning.

### What changes in the skill prompt

`.brs2spec2/skills/delivery-lead/create-delivery-structure.md` must add a prerequisites check:

```
- [ ] Read business-analysis/gaps-and-questions.md if it exists
- [ ] For each Severity: Blocking gap: confirm a stated assumption or resolution exists
- [ ] If any blocking gap has no assumption: stop and report the blocker before writing any delivery-structure content
```

And a new step in the instructions:

```
### Step 0 — Gap gate check (before any other step)

1. Read business-analysis/gaps-and-questions.md.
2. Identify every row with Severity: Blocking.
3. For each blocking gap:
   - If 'Suggested Resolution' contains a concrete assumption → note it; proceed.
   - If 'Suggested Resolution' is blank, TBD, or vague → STOP. Do not write delivery-structure.md.
     Report: "Blocked by GAP-NNN: [description]. Add a stated assumption to gaps-and-questions.md
     before running delivery structure."
4. If all blocking gaps have stated assumptions, proceed. Record each assumption in the
   delivery-structure.md Metadata section.
5. If gaps-and-questions.md does not exist → proceed with a note that gap analysis has not been run.
```

## Run this prompt

```text
Read the design anchor first:
- framework_enhancement/business-analysis-improvement/plan3/00-spec-anchoring-principles.md
  Focus on Principle 4 (gap-to-planning gate).

Read the current files:
- .brs2spec2/workflow/event-templates/EVT-TPL-011-create-delivery-structure.yaml
- .brs2spec2/skills/delivery-lead/create-delivery-structure.md

Make the changes described in this step prompt exactly as specified.
Do not change inputs, outputs, blocked_by, or on_success.
Only change must_include, validation_rules, on_failure, and the skill prompt prerequisites + instructions.

After changes, confirm:
- EVT-TPL-011 must_include has the blocking-gap resolution check
- EVT-TPL-011 validation_rules checks gap-and-questions.md before validating the artifact
- EVT-TPL-011 on_failure is blocking: true with the gap-specific question
- Skill prompt has Step 0 gap gate check before any other step
```

## Done when

- EVT-TPL-011 `must_include` requires blocking gaps to have stated assumptions
- EVT-TPL-011 `validation_rules` actively reads and checks `gaps-and-questions.md`
- EVT-TPL-011 `on_failure` raises a blocking decision when gaps are unresolved
- Skill prompt `create-delivery-structure.md` has a Step 0 gate check before story decomposition
