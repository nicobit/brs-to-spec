# Skill — Create Business Rules

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-business-rules |
| persona | product-owner |
| event_types | CREATE_BUSINESS_RULES |
| produces | business-analysis/business-rules.md |

## When this skill is used

After `CREATE_REQUIREMENTS_CATALOG` completes and `business-analysis/requirements.md` exists. Runs in parallel with `CREATE_ENTITY_MODEL`, `FIND_GAPS_AND_QUESTIONS`, and the use-case diagram. The BR-NNN catalog is consumed by use-case specs, process flows, BDD generation, and the entity model.

## Role for this task

You are a senior business analyst extracting and formalizing every implicit and explicit business rule from the requirements catalog, normalizing them into a numbered, traceable catalog that engineers can implement and QA can test against.

## Prerequisites check

Before starting, verify:
- [ ] `business-analysis/requirements.md` exists and has FR-NNN, NFR-NNN, and constraint rows

Optional inputs (read if available, do not block if missing):
- [ ] `input/brs.md` (or `input/brs/*.md`) — fallback context and cross-check
- [ ] `business-intake/business-intake-summary.md` — additional business context

If the required input is missing, stop and report what is absent.

## Instructions

### Step 1 — Identify all rule sources

Scan `business-analysis/requirements.md` for every constraint, condition, decision rule, validation rule, threshold, and authorization rule. Look in:
- FR-NNN rows encoding conditional logic or allowed/forbidden behavior
- NFR-NNN rows encoding data integrity, performance thresholds, or security constraints
- Constraint rows encoding policy or regulatory rules
- Acceptance criteria that encode a testable business constraint (not just a process step)
- Domain rules implicit in described behavior (e.g. a status transition implies state transition rules)

If `input/brs.md` is available, cross-check for additional rules not yet surfaced in the requirements catalog.

### Step 2 — Normalize into BR-NNN catalog

For each rule found:
1. Assign a sequential BR-NNN ID starting at BR-001
2. Identify the rule category: Authorization / Validation / Calculation / State Transition / Data Integrity / Notification / Integration / Configuration
3. Write the rule in a single, unambiguous, implementation-testable statement
4. Record the source reference (FR-NNN, NFR-NNN, or constraint ID)
5. Record which requirements and actors are affected

### Step 3 — Check for completeness

After the first pass:
- Check that every FR-NNN or constraint in requirements.md that encodes a business decision has at least one BR-NNN, or is explicitly noted as "no business rule — pure process step"
- Check that every actor's permissions and restrictions are captured as authorization rules
- Check that every data field with a constraint (format, range, required condition) has a validation rule

### Step 4 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/business-rules.md`. Preserve all headings. Populate every table from evidence in requirements.md.

Set `Status: Draft` in the Metadata table. Human acceptance happens only at WAIT_HUMAN gates — do not prompt the user to accept this artifact.

Include a coverage table mapping each requirement ID to the BR-NNN rules that cover it:

| Requirement ID | Business rule(s) | Status |
|---|---|---|
| FR-001 | BR-001, BR-002 | Covered |
| NFR-001 | BR-003 | Covered |

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, and creation date
- BR-NNN catalog table with columns: ID, Category, Rule Statement, Source, Affected Requirements, Affected Actors, Notes
- Coverage table mapping every FR-NNN and constraint that encodes a business decision to at least one BR-NNN
- At least one validation rule per field type that has explicit constraints in requirements.md

## Done criteria

- [ ] Every BR-NNN has an unambiguous, testable rule statement
- [ ] Every BR-NNN traces to a requirements.md source reference (FR-NNN / NFR-NNN / constraint)
- [ ] Every FR-NNN or constraint with business decisions has at least one BR-NNN
- [ ] Rule categories are consistent (no mixed-category rules)
- [ ] No rules were invented beyond what requirements.md supports
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `business-analysis/business-rules.md`

## Stop conditions

- If `requirements.md` is missing or has no FR-NNN rows, stop and report the blocker.
- If the initiative genuinely has very few explicit business rules, produce a small catalog and explain why.
- Do not invent rules not derivable from requirements.md.
