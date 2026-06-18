# Skill — Create Use Case Specs

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-use-case-specs |
| persona | product-owner |
| event_types | CREATE_USE_CASE_SPECS |
| produces | business-analysis/use-cases/UC-NNN.md (one file per use case) |

## When this skill is used

After `CREATE_USE_CASE_DIAGRAM` completes and `business-analysis/use-cases.puml` and `business-analysis/use-cases.md` exist. The UC-NNN IDs assigned in the diagram are the stable identifiers this skill writes files for. One file per UC-NNN — no exceptions. Downstream artifacts (BDD, delivery structure, handoff) read from `business-analysis/use-cases/` folder.

## Role for this task

You are a senior business analyst writing structured use case specifications that capture every significant user goal, main success scenario, alternative flows, and exception paths — providing a complete behavioural contract at the business level.

## Prerequisites check

Before starting, verify:
- [ ] `business-analysis/requirements.md` exists and has FR-NNN rows
- [ ] `business-analysis/use-cases.puml` exists and contains UC-NNN IDs
- [ ] `business-analysis/use-cases.md` exists (UC catalog for cross-reference)

Optional inputs (read if available, do not block if missing):
- [ ] `business-analysis/business-rules.md` (BR-NNN IDs for exception paths)
- [ ] `business-analysis/actors-and-personas.md` (ACT-NNN IDs for actors)
- [ ] `architecture/architecture-review.md` (optional: architecture feedback on boundaries and constraints)

If required inputs are missing, stop and report what is absent.

## Instructions

### Step 1 — Read the UC-NNN list from the diagram

Read `business-analysis/use-cases.puml`. Extract every UC-NNN ID and title declared in the diagram. This is the authoritative list. Do not invent UC-NNNs not present in the diagram.

Read `business-analysis/requirements.md`. This is the source for FR-NNN traceability.

Before writing any UC file, create a private coverage map for yourself:
- `UC-NNN -> covered FR-NNNs`
- `FR-NNN -> owning UC-NNN(s)`

Do not start writing files until every FR-NNN is assigned to at least one UC or deliberately marked as out-of-scope for use-case treatment with justification.

### Step 2 — For each UC-NNN, write one file

File path: `business-analysis/use-cases/UC-NNN.md` (e.g. `UC-001.md`, `UC-002.md`).

Use the artifact template at `.brs2spec2/artifact-templates/use-case-detail.md`.

Each file must contain:

1. **Overview** — UC-NNN ID, title, primary actor (ACT-NNN if available, else role name), goal in one sentence, Status: Draft
2. **Preconditions** — system and actor state required before the UC can start
3. **Main Success Scenario** — numbered steps; one actor action + system response per step; business language only, no implementation detail
4. **Alternative Flows** — numbered, branching from a specific main scenario step; cover optional paths and error recoveries
5. **Exception Paths** — what happens when a BR-NNN constraint is violated or a system error occurs; reference BR-NNN if available
6. **Postconditions** — observable business state after the UC completes (success and failure)
7. **Business Rules Referenced** — BR-NNN IDs governing this UC's behaviour (if business-rules.md exists)
8. **FR Sources** — which FR-NNN entries from requirements.md this UC covers

Depth rules:
- A UC file must feel like a real behavioral contract, not a title with filler sections
- Main Success Scenario should normally have 4 to 8 meaningful business steps for non-trivial flows
- Alternative Flows should cover at least one meaningful branch or failure-handling path, not just restate the happy path
- If a UC covers many FRs, the file must expand enough to show how those FRs interact; do not hide breadth behind one-sentence sections

### Step 3 — Validate completeness across all UC files

After all UC files are written, verify:

1. Every FR-NNN in `requirements.md` is covered by at least one UC file. If an FR-NNN is not covered, either add it to an existing UC or note the explicit exclusion with justification.
2. Every UC-NNN from `use-cases.puml` has exactly one corresponding file in `use-cases/`.
3. No UC file contains more than one UC.
4. All actor references use ACT-NNN IDs where `actors-and-personas.md` is available; otherwise use stable role names flagged for later alignment.
5. No UC file is just a skeletal expansion of the title — each one must explain a complete business interaction with enough detail that planning, BDD, and handoff can consume it.

### Step 4 — Quality rules

- One file per use case. Never merge two UCs into one file.
- Main flow steps must be in business language — no technology names, no implementation detail.
- Each UC must represent a complete, observable actor goal.
- Alternative flows branch from real decision points, not invented scenarios.
- Postconditions describe observable business state, not system internals.
- Do not seed from prior conversation artifacts — derive from requirements.md and use-cases.puml.

## Output requirements

- One `business-analysis/use-cases/UC-NNN.md` file per UC-NNN in `use-cases.puml`
- No monolithic file — every UC is its own file
- Every file uses the structure from `artifact-templates/use-case-detail.md`
- Every file has `Status: Draft`

## Done criteria

- [ ] `business-analysis/use-cases/` folder contains one file per UC-NNN from `use-cases.puml`
- [ ] No UC-NNN from the diagram is missing a file
- [ ] No file contains more than one UC
- [ ] Every file has preconditions, main success scenario, at least one alternative flow, postconditions
- [ ] Every UC file traces to at least one FR-NNN from `requirements.md`
- [ ] Across the folder, every FR-NNN from `requirements.md` is covered by at least one UC file or explicit exclusion note
- [ ] No UC file is a shallow stub with one-line sections only
- [ ] Main scenario steps use business language only
- [ ] `Status: Draft` in every file's overview section
- [ ] Result file written with `status: pass` and `artifacts_written` listing all `business-analysis/use-cases/UC-NNN.md` files produced

## Stop conditions

- If `use-cases.puml` is missing or contains no UC-NNN entries, stop and report the blocker.
- If `requirements.md` is missing, stop and report the blocker.
- If `actors-and-personas.md` is missing, continue with role names and flag for ID alignment.
- If `business-rules.md` is missing, continue and note missing BR-NNN cross-references rather than inventing rules.
- Do not invent use cases, steps, or outcomes not derivable from `requirements.md` and `use-cases.puml`.
