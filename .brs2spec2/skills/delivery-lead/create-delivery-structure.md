# Skill — Create Delivery Structure

## Identity

| Field | Value |
|---|---|
| skill_id | dl-create-delivery-structure |
| persona | delivery-lead |
| event_types | CREATE_DELIVERY_STRUCTURE |
| produces | planning/delivery-structure.md |

## When this skill is used

After `REVIEW_INITIAL_ARCHITECTURE` completes and delivery mode is confirmed from `routing/routing-decision.md`. This skill produces the canonical planning artifact: the epic → feature → user story hierarchy with F-XXX.X IDs. All downstream artifacts (traceability matrix, handoff, BDD, test stubs) derive from this.

## Role for this task

You are a senior delivery lead and product manager decomposing the initiative's approved scope into a structured delivery hierarchy — from epics to features to confirmed user stories with stable IDs, sized for independent delivery.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `business-intake/business-intake-summary.md` exists
- [ ] `routing/routing-decision.md` is available (delivery mode and execution mode)
- [ ] `architecture/architecture-review.md` exists (architecture constraints affect story scope)

Optional:
- [ ] `business-analysis/business-rules.md` (BR-NNN IDs for story constraints)
- [ ] `business-analysis/actors-and-personas.md` (ACT-NNN for user story actors)

## Instructions

### Step 1 — Understand scope and delivery mode

From `routing/routing-decision.md`:
- Delivery mode: OpenSpec / Standalone / FastPath / BusinessCopilot
- Execution mode: Enterprise / Enterprise+Modular / Standard

FastPath mode: produce a simplified delivery structure with fewer stories — prioritize the minimum scope needed.

Enterprise+Modular mode: group stories into delivery increments (D1, D2, ...) in addition to the standard hierarchy.

### Step 2 — Define epics

Each epic is a major business capability or feature area. Typical sources:
- Each major section of the BRS
- Each major actor goal from actors-and-personas.md
- Each major process flow from process-flows.md

Assign epic IDs: E-001, E-002, ...

### Step 3 — Define features within each epic

Each feature is a coherent, deliverable sub-capability of the epic. One feature = something that can be demoed to a stakeholder as a working unit.

Assign feature IDs: F-001, F-002, ... (sequential across all epics, not per-epic)

### Step 4 — Define user stories within each feature

Each user story is independently implementable, testable, and deployable.

Rules for stories:
- One story = one F-XXX.X ID where XXX is the feature number and the decimal is the story sequence within that feature
- Each story follows the format: "As a [actor], I want to [action], so that [outcome]"
- Each story must have: acceptance criteria (AC-NNN sourced from BRS), a priority (Must/Should/Could), and an increment assignment (D1/D2/... for Enterprise+Modular)
- Stories must be sized for one engineer, one sprint — split if needed
- Do not create placeholder stories ("implement backend") — every story must name the specific capability

### Step 5 — Assign increment grouping (Enterprise+Modular only)

If execution mode is Enterprise+Modular:
- Assign each story to a delivery increment: D1, D2, D3, ...
- D1 contains the stories required for the minimum viable state of the initiative
- D2+ contains extensions, optimizations, or lower-priority capabilities
- Stories within the same increment must have no blocking dependency on each other (except explicitly noted)

### Step 6 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/delivery-structure.md`. Preserve all headings. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, delivery mode, execution mode, creation date
- Epic → Feature → Story hierarchy with all IDs stable and sequential
- Each story with: user story text, AC-NNN, priority, increment (if applicable)
- Story count assertion: "N stories total, M required (Must), K optional"

## Done criteria

Before writing the result file, perform these checks by cross-referencing `input/brs.md` with the artifact you just produced:

- [ ] Count the major epic/section headings in `input/brs.md`. Count the E-NNN entries in the artifact. They must be equal — if not, add the missing epics before proceeding.
- [ ] List every FR-NNN ID in `input/brs.md`. Verify each one has its own row in the FR Coverage table with at least one F-NNN.X story ID. A range notation (e.g. FR-001..FR-023) is not acceptable — each FR needs its own row.
- [ ] Count the F-NNN.X story rows in the artifact. Verify this count matches the Story Count Assertion number. Correct the assertion if they differ.
- [ ] Every story has a user story statement (As a [actor] / I want [action] / so that [outcome]) — all three parts present.
- [ ] Every story has at least one AC-NNN from the BRS.
- [ ] Stories are sized for independent delivery — not epic-level, not sub-task-level.
- [ ] Delivery increment assignments are consistent (Enterprise+Modular only).
- [ ] No invented stories beyond what the BRS supports.
- [ ] `Status: Draft` in the Metadata table.
- [ ] Result file written with `status: pass` and `artifacts_written` listing `planning/delivery-structure.md`.

## Stop conditions

- If the BRS has no decomposable requirements (configuration-only): produce a minimal delivery structure and flag it.
- If gaps from `FIND_GAPS_AND_QUESTIONS` are blocking: note which gaps prevent story decomposition.
- Do not create stories that span multiple unrelated capabilities — split them.
