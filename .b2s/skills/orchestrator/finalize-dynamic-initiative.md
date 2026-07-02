# Skill — Finalize Dynamic Initiative

## Identity

```text
skill_id:    orchestrator.finalize-dynamic-initiative
persona:     orchestrator
action_id:   finalize-dynamic-initiative
produces:    orchestration/implementation-roadmap.md
```

## Purpose

Produce a single ordered delivery document that a development team can
hand to a squad lead on day one. It sequences the coding packages already
produced, explains why they must be built in that order, surfaces any
remaining open questions, and gives a confidence assessment for each package.

## Inputs — read all before starting

- `orchestration/iteration-log.md` — what was produced, in what order, with what gaps remaining
- `input/brs.md` — authoritative capability list and acceptance bar
- `input/architecture.md` — if present, technology stack and deployment context
- All files under `coding-packages/` — read each package's scope and dependency notes
- All files under `requirements/`, `architecture/`, `quality-gates/` — cross-check coverage

## What to produce

### Section 1 — Delivery summary

- Total capabilities addressed
- Total coding packages produced
- Number of ACs with Gherkin coverage
- Number of integration contracts
- Number of CI gates defined
- Count of open questions blocking delivery

### Section 2 — Delivery sequence

An ordered list of coding packages. For each:

1. Package ID and name
2. Capabilities it covers (FR-NNN list)
3. Why it comes at this position (dependency rationale — what it unblocks)
4. Implementation confidence: `HIGH` / `MEDIUM` / `LOW` with one-line reason
5. Pre-conditions a developer must meet before starting this package
6. Estimated complexity: `S / M / L / XL` with justification

Sort by: foundational dependencies first (domain model → business rules →
integrations → UI → CI). Within a tier, sort by FR priority from the BRS.

### Section 3 — Open questions

List every question from the iteration log that was not resolved during
the loop. For each:
- Question (developer-level specificity — name the FR, the missing fact)
- Impact: what a developer cannot implement until it is answered
- Suggested owner (product owner / IT architecture / legal / vendor)
- Urgency: blocks wave 1 / blocks wave 2 / non-blocking

If there are no open questions, state that explicitly.

### Section 4 — Coverage gaps

List any BRS functional requirement not covered by any coding package.
For each gap: FR-NNN, capability summary, reason not covered (out of scope /
deferred / blocked by open question), recommended next action.

If coverage is complete, state that explicitly with a count.

### Section 5 — Best-practice checklist

For each best-practice set that applies to this initiative (derived from
iteration 1's goal state), confirm that the produced packages address it:

- [ ] Idempotency strategy defined
- [ ] Audit log design present
- [ ] Circuit breakers specified for all external integrations
- [ ] GDPR/data-erasure compatible model documented
- [ ] Acceptance criteria traceable to FR-NNN IDs
- [ ] CI gate definitions present
- [ ] Error response catalogues complete for all integration contracts

Mark each `[x]` present / `[ ]` absent with a note.

## Constraints

- Do not invent capabilities not in the BRS.
- Do not modify any existing artifact — this is a read-and-summarise task.
- The roadmap must be actionable: a squad lead reads it and knows what to
  build, in what order, and where the risks are. No filler.
- Every package reference must include its full path so a developer can
  open it immediately.
