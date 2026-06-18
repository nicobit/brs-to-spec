# Skill — Create Traceability Matrix

## Identity

| Field | Value |
|---|---|
| skill_id | dl-create-traceability-matrix |
| persona | delivery-lead |
| event_types | CREATE_TRACEABILITY_MATRIX |
| produces | planning/traceability-matrix.md |

## When this skill is used

After `CREATE_DELIVERY_STRUCTURE` completes and F-XXX.X story IDs are stable. This skill creates the end-to-end traceability chain from BRS requirements (FR-NNN) through business rules (BR-NNN) through user stories (F-XXX.X) through acceptance criteria (AC-NNN). Required before engineering handoff.

## Role for this task

You are a senior delivery lead and QA analyst assembling the full traceability matrix — ensuring every business requirement maps to a deliverable story, every story maps to acceptance criteria, and every acceptance criterion maps back to a BRS source.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs
- [ ] `business-intake/business-intake-summary.md` exists

Optional but preferred:
- [ ] `business-analysis/business-rules.md` (BR-NNN for traceability chain)
- [ ] `business-analysis/actors-and-personas.md` (ACT-NNN for actor traceability)

## Instructions

### Step 1 — Build the FR → Story mapping

For every FR-NNN in the BRS:
1. Find all F-XXX.X stories that implement this FR (one FR can map to multiple stories)
2. Find all BR-NNN rules that govern this FR
3. Find all AC-NNN criteria from the BRS that validate this FR

If a FR-NNN has no story: flag as a gap (possible scope omission or intentional exclusion — state which).

### Step 2 — Build the Story → AC mapping

For every F-XXX.X story:
1. List the FR-NNN it implements (may be multiple)
2. List the AC-NNN criteria it must satisfy
3. List the BR-NNN rules it must respect
4. Note the delivery increment (if Enterprise+Modular)

### Step 3 — Check coverage completeness

After building both mappings:
- Every FR-NNN must map to at least one F-XXX.X story (or explicitly excluded)
- Every F-XXX.X story must map to at least one FR-NNN
- Every AC-NNN must appear in at least one story's AC list
- Every BR-NNN must appear in at least one story's constraints (or explicitly not applicable to stories)

Flag every gap found — do not silently skip unmapped items.

### Step 4 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/traceability-matrix.md` if available. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- FR → Story matrix: FR-NNN, Description, Stories (F-XXX.X), BR-NNN rules, AC-NNN, Coverage status
- Story → Requirements matrix: F-XXX.X, FR-NNN(s), AC-NNN(s), BR-NNN(s), Increment
- Coverage summary: total FRs, total stories, unmapped FRs, unmapped stories
- Gaps section: any FR or story that is not fully covered, with explanation

## Done criteria

- [ ] Every FR-NNN from the BRS is in the matrix (mapped or explicitly excluded)
- [ ] Every F-XXX.X story from the delivery structure is in the matrix
- [ ] Every AC-NNN appears in the story matrix
- [ ] Coverage gaps are explicitly listed and explained
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `planning/traceability-matrix.md`

## Stop conditions

- If delivery-structure.md has no F-XXX.X IDs: stop — the delivery structure must be confirmed before traceability can be built.
- If the BRS has no FR-NNN numbering: assign FR-NNN IDs to the requirements first, document the mapping, then proceed.
