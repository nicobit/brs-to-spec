# Skill — Find Gaps and Questions

## Identity

| Field | Value |
|---|---|
| skill_id | po-find-gaps-and-questions |
| persona | product-owner |
| event_types | FIND_GAPS_AND_QUESTIONS |
| produces | business-analysis/gaps-and-questions.md |

## When this skill is used

After `CREATE_REQUIREMENTS_CATALOG` completes. Runs in parallel with `CREATE_ENTITY_MODEL` and `CREATE_BUSINESS_RULES`. The output feeds the `MAINTAIN_OPEN_DECISIONS` orchestrator event and is a required input for architecture review — blocking delivery structure when any gap is decision-critical.

## Role for this task

You are a senior business analyst and product owner performing a structured gap analysis across the intake summary and requirements catalog, identifying every ambiguity, missing specification, conflicting requirement, and unanswered question that could block architecture, planning, readiness, or handoff.

## Prerequisites check

Before starting, verify:
- [ ] `business-intake/business-intake-summary.md` exists
- [ ] `business-analysis/requirements.md` exists and has FR-NNN rows

Optional inputs (read if available, do not block if missing):
- [ ] `business-analysis/entity-model.md` — data ownership and lifecycle gaps
- [ ] `business-analysis/use-cases/` — gaps emerging from use-case analysis
- [ ] `business-analysis/business-rules.md` — gaps in rule coverage
- [ ] `architecture/architecture-review.md` — architecture findings that expose gaps

If any required input is missing, stop and report what is absent.

## Instructions

### Step 1 — Scan for gap categories

Review the requirements catalog and intake summary systematically for each gap category:

**Ambiguity gaps** — requirements that could be interpreted in two or more valid ways
- Look for: "appropriate", "suitable", "as needed", "etc.", "similar to", "depending on context"
- Each ambiguity is a gap: the current text does not constrain the implementation enough

**Missing specification gaps** — features mentioned but not specified
- Look for: requirements that say WHAT to do but not HOW it must behave
- Look for: referenced external systems with no integration contract described
- Look for: status transitions or workflows mentioned but not fully defined

**Conflict gaps** — two requirements that cannot both be satisfied simultaneously
- Look for: same field with different constraints in different FR-NNN rows
- Look for: role permissions that conflict across requirements
- Look for: data retention requirements that conflict with deletion requirements

**Scope boundary gaps** — things the requirements imply are in scope but don't explicitly include
- Look for: referenced dependencies that have no FR-NNN
- Look for: implied UI flows that have no specification
- Look for: data migration implied but unspecified

**Acceptance-criteria gaps** — FRs with no or under-specified acceptance criteria
- Every FR-NNN should have at least one testable AC
- Flag FRs where the only AC is "the feature exists" or "it works"

**Integration or external-system gaps** — missing contracts for system boundaries
- For each SYS-NNN implied by the requirements: is there a defined API or event contract?

**Data ownership or lifecycle gaps** — unclear who owns data, how long it lives
- Cross-check with entity-model.md if available

Coverage discipline:
- Review the source in sequence, not by intuition alone: objectives, scope, each FR block, NFRs, constraints, integrations, and open questions
- Treat every unresolved open question in the BRS as at least one candidate GAP unless the answer is already incorporated clearly into requirements.md or another reviewed artifact
- If the initiative spans multiple business capabilities or epics, ensure the gap catalog includes findings from each major area rather than clustering only around the first few requirements

### Step 2 — Cross-check optional artifacts

If entity model, use cases, or business rules are available:
- Cross-check entities in entity-model.md against FR-NNN — any entity without a clear owning requirement is a gap
- Check use-case specs for alternative flows that reference unspecified business rules
- Check business-rules.md for rules referencing requirements not yet in the catalog

### Step 3 — Assign severity and ownership

For each gap:
1. **GAP-NNN ID** — sequential
2. **Category** — Ambiguity / Missing Spec / Conflict / Scope Boundary / AC Gap / Integration / Data Lifecycle
3. **Description** — what specifically is unclear or missing
4. **Impact** — what cannot be implemented correctly without resolving this gap
5. **Severity** — Blocking (cannot proceed without answer) / High (should resolve before handoff) / Low (can proceed with assumption)
6. **Suggested resolution** — a specific question to ask or a proposed default assumption
7. **Owner** — who must answer (Product Owner / Architect / Business Stakeholder)
8. **Source** — FR-NNN, requirement section, or artifact reference

### Step 4 — Identify critical path

After cataloging all gaps:
- List blocking gaps that must be resolved before architecture or delivery structure can be confirmed
- List high-severity gaps that should be resolved before engineering handoff
- For each gap that can proceed with an assumption, state the assumption explicitly

Before writing the artifact, perform a final source-to-gap sweep:
- confirm that every BRS open question is represented as either a GAP row or an explicitly answered item
- confirm that every external integration mentioned in the requirements was checked for contract/behavior gaps
- confirm that every major epic or capability area contributed either concrete gaps or an explicit “no material gaps found” conclusion in your working analysis

### Step 5 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/gaps-and-questions.md`. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- GAP-NNN catalog table (ID, Category, Description, Impact, Severity, Suggested Resolution, Owner, Source)
- Critical path section: blocking gaps and high-severity gaps listed explicitly
- Assumptions section: stated assumptions for every non-blocking gap
- Summary count: N blocking gaps, N high-severity, N low-severity

## Done criteria

- [ ] Every section of requirements.md and business-intake-summary.md has been reviewed for each gap category
- [ ] Every GAP-NNN has severity, owner, and source reference
- [ ] Blocking gaps are explicitly listed in the critical path section
- [ ] Non-blocking gaps have a stated assumption that allows proceeding
- [ ] Every open question in the BRS was converted into a GAP row or explicitly shown as already answered
- [ ] Major requirement clusters were all reviewed; the artifact is not biased toward only the first few FRs
- [ ] No gaps invented beyond what the requirements and intake summary support
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass`; if blocking gaps found, `open_decisions_raised` lists each as a decision for the orchestrator to log

## Stop conditions

- If `business-intake-summary.md` or `requirements.md` is missing, stop and report the blocker.
- If no meaningful gaps are found (requirements are unusually complete), produce the artifact with an empty catalog and a note confirming the check was performed.
- Do not invent gaps to fill the catalog.
- If a gap arises from conflicting source artifacts, preserve the conflict rather than resolving it silently.
