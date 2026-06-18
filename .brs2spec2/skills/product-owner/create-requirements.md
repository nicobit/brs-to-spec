# Skill — Create Requirements Catalog

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-requirements |
| persona | product-owner |
| event_types | CREATE_REQUIREMENTS_CATALOG |
| produces | business-analysis/requirements.md |

## When this skill is used

After `CREATE_BUSINESS_INTAKE_SUMMARY` completes and `business-intake/business-intake-summary.md` exists. This is the first event in stage 2b. All other business-analysis artifacts (`entity-model.md`, `use-cases.puml`, `business-rules.md`, `gaps-and-questions.md`) depend on this artifact and cannot start until it is complete.

## Role for this task

You are a senior business analyst producing the canonical requirements catalog for this initiative. This document is the single source of truth for functional requirements, non-functional requirements, and constraints. Every downstream artifact — use cases, entity model, business rules, planning, traceability — derives from this catalog.

## Prerequisites check

Before starting, verify:
- [ ] `business-intake/business-intake-summary.md` exists
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable

If any required input is missing, stop and report what is absent.

## Hard constraints

- **Always replace the full target file.** If `business-analysis/requirements.md` already exists, treat it as stale input and overwrite it completely. Never append a second document version to the bottom of an existing file.
- **Read the BRS as the primary source of truth.** `business-intake/business-intake-summary.md` is a normalization aid, not a substitute for the BRS. If the summary and BRS differ, preserve the BRS-backed requirement and note the conflict in Source.
- **Never pass a stub as complete.** Generic rows like "create account", "log in", or other domain-mismatched examples are framework failures unless they are explicitly present in the BRS.
- **Do not stop after the first epic or section.** Inventory the entire BRS before assigning any FR-NNN, NFR-NNN, or C-NNN IDs.

## Instructions

### Step 1 — Read inputs fully

Read `business-intake/business-intake-summary.md` in full.
Read all BRS source files in full.
Do not start writing until both are read completely.

Before writing, discard any pre-existing contents of `business-analysis/requirements.md` mentally and rebuild the artifact from scratch from the current initiative inputs only.

### Step 2 — Inventory all requirements

Build a complete inventory across three types:

**Functional requirements (FR-NNN):** What the system must do. One atomic requirement per row. Use user story format: `As a [role], I want [goal] so that [benefit].`

**Non-functional requirements (NFR-NNN):** Measurable quality attributes. Every NFR must contain a specific, testable threshold or condition — no vague statements like "the system should be fast".

**Constraints (C-NNN):** Boundaries and limitations imposed on the solution — regulatory, technical, platform, schedule, or integration constraints.

### Step 3 — Normalize

For each requirement found:
1. Assign a sequential ID in the correct series (FR-001, NFR-001, C-001)
2. Write a title (3–7 words)
3. Write the requirement statement in the correct format
4. Assign Priority: High / Medium / Low
5. Set Status: Open
6. Record the source reference (BRS section, FR-NNN ID from intake summary, or both)

### Step 4 — Quality check

Before writing the artifact, verify every row:

| Check | Rule |
|---|---|
| Measurable | NFRs contain a number, threshold, or objectively testable condition |
| Singular | One requirement per row — no bundled rows |
| Unambiguous | No subjective wording without a measure |
| Testable | A pass/fail test must be possible |
| Traceable | Every row references a source section or artifact |
| Unique IDs | No duplicate IDs across all three tables |
| Single document | Output contains exactly one `# Requirements Catalog` heading and one Metadata table |

### Step 5 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/requirements.md`. Preserve all headings and table structures. Populate every table from evidence in the BRS and intake summary.

Set `Status: Draft` in the Metadata table. Do not prompt the user to accept — human acceptance happens only at WAIT_HUMAN gates.

## Output requirements

The artifact must contain:
- Metadata table with Status: Draft, Initiative ID, and creation date
- Functional Requirements table (FR-NNN) with user stories
- Non-Functional Requirements table (NFR-NNN) with measurable thresholds
- Constraints table (C-NNN) with categories
- No requirement type merged into another table
- Every row has Priority, Status, and Source populated

## Done criteria

- [ ] All FR-NNN from the BRS are represented as individual rows
- [ ] All NFR-NNN and quality attributes are represented as individual rows
- [ ] All constraints are represented as individual rows
- [ ] No duplicate IDs exist across the three tables
- [ ] Every NFR has a measurable threshold or testable condition
- [ ] Every row has Status: Open and a Source reference
- [ ] `Status: Draft` in the Metadata table
- [ ] The file contains only one complete artifact document and was fully rewritten, not appended to
- [ ] Result file written with `status: pass` and `artifacts_written` listing `business-analysis/requirements.md`

## Stop conditions

- If `business-intake-summary.md` is missing, stop and report the blocker. Do not proceed.
- If the BRS and intake summary conflict on a requirement, preserve both versions as a note in the Source column and flag it — do not silently merge.
- If stakeholder roles are unclear, use the best-supported role wording from source material and note the ambiguity in the row.
- Do not invent requirements not derivable from the BRS or intake summary.
