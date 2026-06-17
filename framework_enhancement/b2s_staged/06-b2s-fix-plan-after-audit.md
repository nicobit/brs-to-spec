# `.b2s` Fix Plan After Audit

## Purpose

This document captures the concrete fixes needed after the `.b2s` audit of weak
business-intake output, shallow validation, and incomplete recovery behavior.

The goal is not to redesign `.b2s`. The goal is to harden the current staged
framework so weak artifacts are rejected early, recovery is smoother, and the
engine behavior matches the declared model.

## Root cause summary

The immediate cause of poor downstream artifacts is:

1. some `.b2s` generation prompts are weaker than the corresponding
   `.brs2spec2` prompts
2. `.b2s` validation accepts structural skeletons as valid artifacts
3. once a weak upstream artifact passes, downstream staged actions build on it

The highest-priority fix is therefore:

- strengthen prompt constraints
- strengthen deterministic validation

## Implementation order

Implement in this order:

1. restore prompt strength for upstream artifact generation
2. deepen validation for intake, requirements, use cases, and readiness
3. add a single-action retry path after gate rejection
4. clean misleading gate and workflow config
5. harden reset behavior and stage semantics

---

## Fix 1 - Restore prompt strength

### Goal

Bring the most important `.b2s` prompts back to the strength of the
`.brs2spec2` versions while keeping staged wording and removing event-specific
instructions.

### Files to modify

- `.b2s/skills/product-owner/create-business-intake-summary.md`
- `.b2s/skills/product-owner/create-requirements.md`
- `.b2s/skills/product-owner/create-use-case-diagram.md`
- `.b2s/skills/engineering-lead/check-engineering-readiness.md`

### Required changes

#### A. `create-business-intake-summary.md`

Restore the stronger controls from `.brs2spec2`:

- add explicit stop conditions for:
  - missing BRS
  - empty or heading-only BRS
  - no extractable requirements
- restore the count-and-compare quality pass:
  - count objectives in BRS vs rows in Objectives table
  - count atomic requirements in BRS vs Requirements rows
  - count NFRs vs NFR coverage
  - count unresolved questions vs GAP rows
- restore explicit rule that every atomic requirement gets its own row
- restore explicit rule that answered questions must not appear as unresolved gaps
- restore stronger anti-skeleton wording:
  - fail rather than output filler
  - do not output structure-only placeholders

#### B. `create-requirements.md`

Restore stronger normalization and anti-generic safeguards:

- restore explicit rejection of domain-mismatched starter content
- restore stronger conflict handling between BRS and intake summary
- restore stronger inventory guidance so all requirement clusters are captured
- restore explicit stop conditions section
- keep staged wording:
  - no event result file references
  - no dispatcher wording

#### C. `create-use-case-diagram.md`

Restore breadth-preservation and shallow-model prevention:

- restore scratch mapping step:
  - capability or epic -> candidate goals -> FR coverage
- restore explicit instruction to represent system-only FR clusters when they
  produce real governed outcomes
- restore explicit failure path when requirements are suspiciously tiny,
  contaminated, or domain-mismatched
- restore explicit rule that every major FR cluster must be covered or
  deliberately excluded with reason
- keep staged wording:
  - no event result file references

#### D. `check-engineering-readiness.md`

Restore stronger governance quality:

- restore explicit stop conditions section
- restore stronger wording that a single blocking issue overrides numeric score
- preserve explicit per-gate justification requirements
- keep staged wording and remove result-file references

### Verification

- prompts remain `.b2s`-native
- no `.flow/` or `.brs2spec2` execution semantics remain
- restored prompts are at least as strict as the prior `.brs2spec2` versions on
  completeness and anti-skeleton behavior

---

## Fix 2 - Deepen deterministic validation

### Goal

Reject skeleton artifacts mechanically instead of relying on prompt wording
alone.

### Files to modify

- `.b2s/scripts/b2s_engine/validation.py`
- optionally `.b2s/workflow/stage-actions.yaml` if new validation rule metadata
  is needed later

### Required changes

#### A. Strengthen `business-intake/business-intake-summary.md` validation

Upgrade `_validate_business_intake_summary()` from shape checks to completeness
checks.

Add checks such as:

- Objectives section contains at least one populated data row when the BRS
  contains objectives or goals
- Requirements table contains more than one real row when the BRS contains more
  than one requirement
- Capabilities table is not empty placeholder-only
- Scope table is not empty placeholder-only
- Gaps and Questions table is populated when the BRS contains unresolved
  questions, TBDs, or explicit open items
- Consolidation Notes table exists and is not removed
- Existing-System Context is populated when the BRS or intake mentions an
  existing system, migration, or integration
- reject obvious placeholder values:
  - blank cells across whole tables
  - repeated generic examples
  - untouched template language

Important:

- do not require exact one-to-one semantic matching in phase 1
- do reject obviously tiny or placeholder-only artifacts

#### B. Strengthen `business-analysis/requirements.md` validation

Upgrade `_validate_requirements_catalog()` to check:

- Functional Requirements has at least one populated FR row with non-empty title
  and source
- Non-Functional Requirements section is not left as untouched template text
- Constraints section is not left as untouched template text
- user-story text is not still generic template wording for all rows
- `Source` column is populated for every real row

#### C. Strengthen `business-analysis/use-cases.md` and `.puml` validation

Upgrade `_validate_use_cases_markdown()` and `_validate_use_cases_puml()` to
check:

- at least one actor and one use case node exist
- markdown UC catalog has at least one non-placeholder row
- UC IDs match a plausible set and are not only template examples
- `use-cases.md` and `use-cases.puml` contain consistent UC counts when both are
  produced by the action
- reject tiny outputs when requirements catalog has broad FR coverage
  Phase 1 heuristic:
  if requirements has many FR rows but only one or two UCs, fail with
  "suspiciously shallow use-case coverage"

#### D. Strengthen `engineering-readiness/readiness-check.md` validation

Upgrade `_validate_readiness_check()` to check:

- core checklist has real pass or fail entries
- gate table contains explicit Yes or No values
- "No" gate rows have non-empty justification text
- readiness score row contains a real numeric value
- decision row is populated

### Verification

- skeleton artifacts fail validation
- real thin-slice artifacts still pass
- current fixture suite is expanded with positive and negative validation cases

---

## Fix 3 - Add single-action retry after gate rejection

### Goal

Allow a rejected artifact to be regenerated without forcing a whole stage reset.

### Files to modify

- `.b2s/scripts/b2s_cli.py`
- `.b2s/scripts/b2s_engine/gates.py`
- `.b2s/scripts/b2s_engine/state.py`
- `.b2s/prompts/repair-state.md`
- `.b2s/prompts/resume-from-phase.md`
- possibly add `.b2s/prompts/retry-action.md`

### Required changes

Implement a staged retry path:

- when `reject-current-gate` runs:
  - mark the source action as failed
  - preserve valid upstream accepted actions
  - record which source action must be retried
- add a deterministic command, for example:
  - `retry-action --action-id <id>`
  or
  - a repair-state mode that reopens the last rejected source action

Preferred behavior:

- reset only the rejected action and its produced artifacts
- clear its blocked reason
- set `next_action` back to that source action
- do not wipe routing or unrelated accepted upstream progress

### Verification

- reject business-intake gate
- retry only `create-business-intake-summary`
- upstream routing stays accepted
- next-step selects the retried action, not full-stage restart

---

## Fix 4 - Clean gate model and misleading config

### Goal

Make config match engine reality.

### Files to modify

- `.b2s/workflow/stage-actions.yaml`
- `.b2s/scripts/b2s_engine/next_step.py`
- `.b2s/scripts/b2s_engine/state.py`
- optionally `.b2s/templates/state/open-decisions.md` and related state logic

### Required changes

#### A. Gate action cleanup

Fix the dual-gate anomaly:

- gate actions such as `gate-business-intake-review` should not themselves
  declare a nested `human_gate.required: true` if they are never dispatched as
  normal executable actions

Choose one model and document it:

- either gate actions remain declarative status markers only
- or remove them entirely and model gate state only on source actions

Recommended short-term fix:

- keep gate actions as status ids
- remove nested human gate semantics from the gate-action entries themselves

#### B. `blocked_by_stage`

Choose one:

- implement it in `next_step.py`
- or remove it from `stage-actions.yaml`

Recommended:

- implement `_blocked_by_stage_satisfied()` so YAML schema is truthful

#### C. `on_fail.raise_decision`

Choose one:

- implement open-decision writing
- or remove `on_fail.raise_decision` from the schema for now

Recommended short-term fix:

- do not leave it as silent dead config
- either remove it from stage actions now or implement minimal open-decision
  counting and persistence in `open-decisions.md`

### Verification

- no dead config fields remain silently ignored
- gate semantics are understandable from YAML plus engine code

---

## Fix 5 - Harden reset and stage semantics

### Goal

Make rewind behavior robust and less dependent on implicit ordering.

### Files to modify

- `.b2s/scripts/b2s_engine/reset.py`
- `.b2s/scripts/b2s_engine/next_step.py`

### Required changes

#### A. Reset by stage id semantics

In `reset.py`:

- clear routing fields based on semantic stage id such as `0-routing`, not only
  `target_index == 0`
- keep behavior stable even if workflow stage ordering changes later

#### B. Clarify stage completeness semantics

In `next_step.stage_is_complete()`:

- document whether condition-failing actions are intentionally treated as
  non-required
- if not intentional, change logic so conditionally required actions block stage
  completion when their condition is true and they are incomplete

### Verification

- resetting to `0-routing` always clears routing-derived state
- optional conditional actions are either clearly optional or clearly enforced

---

## Test expansion required

### Files to modify

- `.b2s/tests/test_engine_fixtures.py`
- `.b2s/tests/test_engine_runtime.py`
- `.b2s/tests/test_engine_maintenance.py`
- add fixtures under `.b2s/tests/fixtures/` as needed

### New tests to add

- business-intake skeleton fails validation
- requirements artifact with untouched template rows fails validation
- use-case artifact with suspiciously tiny UC set fails when requirements are
  broad
- readiness artifact with missing gate justifications fails validation
- reject gate then retry single action without full stage reset
- reset to `0-routing` clears delivery and execution mode by stage id semantics
- if `blocked_by_stage` is implemented, add at least one positive and one
  negative selection test

---

## Recommended execution slices

### Slice 1 - direct root cause

- strengthen the three upstream product-owner prompts
- strengthen intake and requirements validation
- add tests for skeleton rejection

### Slice 2 - downstream artifact quality

- strengthen use-case prompt
- strengthen use-case validation
- add shallow-coverage use-case tests

### Slice 3 - recovery behavior

- add single-action retry after rejection
- add tests for retry path

### Slice 4 - model cleanup

- fix gate-action declarations
- implement or remove `blocked_by_stage`
- implement or remove `on_fail.raise_decision`
- harden reset semantics

---

## Definition of done

This fix plan is complete only when:

- a skeleton `business-intake-summary.md` fails deterministically
- the strengthened `.b2s` prompts are at least as strict as the prior
  `.brs2spec2` prompts for the key upstream artifacts
- a rejected human gate can be retried without a full stage reset
- stage-action YAML no longer contains misleading unimplemented fields
- tests cover both positive and negative paths for the above behavior
