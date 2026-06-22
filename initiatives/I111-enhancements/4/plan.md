# Framework Enhancement 4 — Artifact Quality and AI Handoff Readiness

## Problem statement

The framework produces structurally correct artifacts but allows substantively thin ones to pass gate checks and advance the workflow. Two patterns were observed in I005:

1. **Business analysis layer skipped.** `delivery-structure.md` was created before `business-rules.md`, `actors-and-personas.md`, process flows, and entity model existed. Stories ended up with FR references but no BR links, no actor grounding, no data model.

2. **Quality gates accepted in isolation.** API contract, data contract, and BDD scenarios were each accepted without cross-referencing the upstream business analysis artifacts. The result is a set of individually correct but mutually disconnected gates.

The root cause is not missing skills — all the skills already exist. The root cause is:
- wrong sequencing: delivery-structure is created before business rules and actors
- missing cross-references: quality gate skills do not require business analysis inputs
- no enrichment gate: stories can pass to handoff without BR-NNN links, actor references, or testable AC

## What this enhancement does NOT do

- Does not add new phases or stages
- Does not require all artifacts upfront (not waterfall)
- Does not change the delivery modes (Fast Path, Standard, Enterprise)
- Does not rename or restructure the framework

## What this enhancement does

Five targeted changes to existing skills and the workflow runner:

| # | File | Change type | Effort |
|---|---|---|---|
| 1 | `01-fix-delivery-structure-sequencing.md` | Resequence: business-rules + actors before delivery-structure draft | Low |
| 2 | `02-strengthen-story-done-criteria.md` | Story quality bar: BR-NNN links, actor, testable AC mandatory before confirmed | Low |
| 3 | `03-cross-reference-quality-gates.md` | Gate skills read business analysis inputs; outputs cite BR-NNN and ACT-NNN | Medium |
| 4 | `04-add-story-enrichment-gate.md` | New gate between readiness and handoff: verify every story is substantively complete | Medium |
| 5 | `05-add-coding-prompt-to-handoff.md` | Add `coding-prompt.md` as mandatory output per story in the handoff skill | Medium |

## Recommended implementation order

1 → 2 → 4 → 3 → 5

Start with 1 and 2 (sequencing and done criteria — low risk, no new artifacts).
Then 4 (new gate — additive, does not modify existing skills).
Then 3 (cross-references — modifies quality gate skills, medium risk).
Then 5 (coding-prompt — modifies handoff skill, medium risk).

Each enhancement is self-contained and can be applied independently.

---

## Enhancement 1 — Fix delivery-structure sequencing

**File:** `01-fix-delivery-structure-sequencing.md`

**Problem:** the orchestrator workflow (step 3 stage table) currently places business-rules (2b) and actors-and-personas (2c) after delivery-structure draft (4). This means delivery-structure is built without knowing the business rules or the actors, producing stories that have FR references but no BR links and use invented actor names.

**Fix:** move stages 2b and 2c before stage 4. The delivery-structure draft must read `business-intake/business-rules.md` and `business-analysis/actors-and-personas.md` as required inputs, not optional ones.

Process flows (9b) and entity model (12b) stay where they are — they legitimately require confirmed stories and data contract respectively.

---

## Enhancement 2 — Strengthen story done criteria

**File:** `02-strengthen-story-done-criteria.md`

**Problem:** the confirmed-stage story quality bar in `create-delivery-structure.md` requires F-XXX.X ID, "As a / I want / so that", AC-NNN reference, and FR-NNN. It does not require BR-NNN links or explicit actor references using ACT-NNN IDs from `actors-and-personas.md`.

**Fix:** add two mandatory fields to every confirmed story:
- At least one `BR-NNN` link (or explicit "no business rules apply — reason: ...")
- Actor reference using the `ACT-NNN` ID from `actors-and-personas.md` (not a free-text role name)

Also add to the orchestrator stage 9 done criteria and the pre-generation gate check.

---

## Enhancement 3 — Cross-reference quality gates to business analysis

**File:** `03-cross-reference-quality-gates.md`

**Problem:** BDD, API contract, and data contract skills each read their own inputs in isolation. BDD reads delivery-structure and BRS but not process flows or business rules. API contract does not reference actors. Data contract does not reference entity model.

**Fix:** update the inputs section and output rules of three skills:

- `create-bdd-scenarios.md`: add `business-analysis/process-flows.md` as input; require each scenario group to cite the PF-NNN it exercises
- `create-api-contract.md` (quality-gates): add `business-analysis/actors-and-personas.md` as input; require each endpoint to name the ACT-NNN caller
- `create-data-contract.md` (quality-gates): add `business-analysis/entity-model.md` as input when it exists; require schema tables to match entity model attribute tables

---

## Enhancement 4 — Add story enrichment gate

**File:** `04-add-story-enrichment-gate.md`

**Problem:** there is no checkpoint between readiness=Ready and handoff that verifies every story is substantively complete. A story can be a structural stub (has F-XXX.X ID and "As a / I want / so that") and still pass to handoff.

**Fix:** add a new stage 9d "story enrichment check" in the orchestrator workflow, after delivery-structure confirmed (9) and before quality gates (12). This is not a new skill — it is a validation step inside the orchestrator that reads each story and checks:

- Has at least one BR-NNN link or explicit "no BR applies" note
- Uses ACT-NNN ID for the primary actor
- Has at least one AC that is testable (not "the system works correctly")
- References the PF-NNN process flow it belongs to (after process flows are created at 9b)

Stories that fail are returned to the delivery-lead skill for enrichment before gates run.

---

## Enhancement 5 — Add coding-prompt.md to handoff

**File:** `05-add-coding-prompt-to-handoff.md`

**Problem:** the handoff produces `story.md + design.md + tasks.md` per story. A coding agent receiving this must read all three files and still has to infer: which business rules constrain this story, which architecture rules apply, what the acceptance criteria look like as verifiable statements, and what the definition of done is.

**Fix:** add `coding-prompt.md` as a mandatory fourth file per story folder in the OpenSpec handoff skill. It is a synthesis artifact — it does not add new information, it aggregates the most important constraints from the other three files into a single, directly usable prompt for a coding agent.

Content structure:
- One-sentence goal (from story.md "so that" clause)
- Business rules that apply (BR-NNN list with rule text)
- Architecture rules that apply (AR-NNN list with rule text)
- Acceptance criteria as verifiable statements (AC-NNN with testable wording)
- BDD scenario IDs that must pass (SCN-NNN list)
- Files likely affected (from design.md)
- Definition of done checklist
- What the agent must NOT do (forbidden patterns from AR-NNN)
