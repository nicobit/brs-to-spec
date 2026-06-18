# Skill — Review Initial Architecture

## Identity

| Field | Value |
|---|---|
| skill_id | arch-review-initial-architecture |
| persona | architect |
| event_types | REVIEW_INITIAL_ARCHITECTURE |
| produces | architecture/architecture-review.md |

## When this skill is used

After `CREATE_BUSINESS_INTAKE_SUMMARY` is accepted and `routing/routing-decision.md` confirms delivery mode. Runs before `CREATE_ARCHITECTURE_RULES` and before `CREATE_DELIVERY_STRUCTURE`. The output is the initiative-specific architecture authority — all downstream artifacts reference it.

## Role for this task

You are a senior architect performing an initiative-specific architecture review: not a general audit, but a targeted assessment of how the proposed initiative interacts with the existing system, what constraints apply, what risks exist, and what architectural decisions must be made before engineering begins.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `input/architecture.md` (or `input/architecture/*.md`) is readable
- [ ] `business-intake/business-intake-summary.md` exists
- [ ] `routing/routing-decision.md` is available

Optional but preferred:
- [ ] `business-analysis/business-rules.md` (data integrity and integration constraints)

If `input/architecture.md` is missing, proceed but flag it as a critical gap — architecture decisions will be based on BRS alone and will be weaker.

## Instructions

### Step 1 — Read all inputs before writing

Read the BRS, architecture document, and business-intake-summary in full before writing a single line of the review. Architecture reviews that are generated incrementally while reading miss cross-file constraints.

### Step 2 — Assess initiative-architecture fit

For each major feature in the BRS:
1. Which existing system components does it touch?
2. Which new components or boundaries does it introduce?
3. What contracts (API, data, event) are created or changed?
4. What is the blast radius if this feature fails?

### Step 3 — Identify architecture constraints

For each constraint that applies to this initiative:
- State it as a binding rule (will become an AR-NNN in `CREATE_ARCHITECTURE_RULES`)
- Provide the rationale (why does this constraint exist?)
- State what would break if it were violated

### Step 4 — Assess brownfield impact

If the initiative changes an existing system:
- Identify compatibility concerns (existing consumers of changed interfaces)
- Assess migration risk (data migration, feature flag, parallel run requirements)
- Evaluate rollback sensitivity (can this change be reversed if it goes wrong?)
- State the regression surface (what existing functionality is at risk?)

### Step 5 — Document open decisions and active assumptions

List every architecture decision that cannot be made from the available information:
- What information is missing?
- What is the default assumption if no decision is made?
- Who must make this decision?

List every assumption that is being made:
- What is assumed to be true that has not been confirmed?
- What would change if this assumption turns out to be false?

### Step 6 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/architecture-review.md`. Preserve all headings. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Initiative-architecture fit assessment (per major feature area)
- Architecture constraints list (each with rationale and violation consequence)
- Brownfield impact section (or explicit "greenfield — no impact" statement)
- Open decisions table (each with owner and default assumption)
- Active assumptions table (each with "if false, then..." consequence)
- Known unknowns (things not yet determinable)
- Quality attributes assessment (performance, security, scalability as relevant)

## Done criteria

- [ ] Every major BRS feature area has been assessed for architecture fit
- [ ] Every constraint has rationale and violation consequence
- [ ] Brownfield impact is explicitly assessed (not silently skipped)
- [ ] Open decisions have owners and default assumptions
- [ ] Active assumptions have "if false" consequences
- [ ] No implementation decisions leaked into architecture constraints (WHAT not HOW at wrong level)
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `architecture/architecture-review.md`

## Stop conditions

- If `input/architecture.md` is missing: proceed with BRS-only assessment, flag the gap.
- If the BRS is too vague to assess architecture impact: flag specific FR-NNN gaps and produce a partial review.
- Do not invent architecture constraints not derivable from the inputs.
