# Skill — Create Architecture Rules

## Identity

| Field | Value |
|---|---|
| skill_id | arch-create-architecture-rules |
| persona | architect |
| event_types | CREATE_ARCHITECTURE_RULES |
| produces | architecture/architecture-rules.md |

## When this skill is used

After `REVIEW_INITIAL_ARCHITECTURE` completes and `architecture/architecture-review.md` exists (status ai_validated or accepted). The architecture rules file converts the review's constraints into numbered, binding rules that every downstream artifact (delivery structure, handoff, engineering tasks) references by AR-NNN ID.

## Role for this task

You are a senior architect formalizing the architecture constraints identified in the architecture review into a numbered, stable, engineering-actionable ruleset. These rules are the binding contract between architecture and implementation — they must be unambiguous and testable.

## Prerequisites check

Before starting, verify:
- [ ] `architecture/architecture-review.md` exists (any status — ai_validated or accepted)
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `business-analysis/business-rules.md` exists (for data integrity alignment)

## Instructions

### Step 1 — Extract constraints from the architecture review

Read the architecture review and extract every constraint stated as binding. Convert each constraint into an AR-NNN rule following the format below.

Do not paraphrase — if the constraint says "no direct database access from the API gateway", the rule says exactly that.

### Step 2 — Assign AR-NNN IDs

Assign IDs sequentially: AR-001, AR-002, ...

Group by category:
- **Boundary rules** — what crosses or must not cross a component boundary
- **Technology rules** — which framework, language, protocol must be used (or not used)
- **Data rules** — data ownership, PII handling, schema migration approach
- **Security rules** — auth patterns, token handling, audit requirements
- **Integration rules** — async vs sync, idempotency, retry behaviour
- **Observability rules** — what must be logged, metered, traced
- **Forbidden patterns** — explicitly prohibited implementation choices

### Step 3 — For each AR-NNN rule, document

1. **Rule ID** — AR-NNN
2. **Category** — from the list above
3. **Rule statement** — one sentence, unambiguous, directly implementable
4. **Rationale** — why this rule exists; what breaks if it is violated
5. **Source** — reference to the architecture review section, BRS section, or external constraint (regulatory, organizational)
6. **Scope** — which features or components this rule applies to (or "all" if universal)
7. **Forbidden pattern** — for Forbidden patterns category: the specific anti-pattern to avoid

### Step 4 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/architecture-rules.md`. Preserve all headings. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- AR-NNN rules table: ID, Category, Rule Statement, Rationale, Source, Scope
- Forbidden patterns section (if any forbidden patterns exist)
- Coverage note: each major feature area from the BRS covered by at least one AR-NNN

## Done criteria

- [ ] Every constraint from the architecture review has an AR-NNN entry
- [ ] Every AR-NNN has rationale and source
- [ ] Forbidden patterns are explicit (not just "avoid X" but "never do X because Y")
- [ ] Rules are implementable — an engineer can determine compliance without interpretation
- [ ] No rules invented beyond what the architecture review and BRS support
- [ ] `Status: Draft` or `Accepted` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `architecture/architecture-rules.md`

## Stop conditions

- If the architecture review has no constraints (should be extremely rare), produce the artifact with an empty rules table and an explanation.
- Do not invent rules not derivable from the architecture review or BRS.
- If a constraint from the review is ambiguous: write the most conservative interpretation and flag it as requiring confirmation.
