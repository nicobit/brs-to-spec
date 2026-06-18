# Prompt — Create Test Strategy

## Role

You are a senior QA lead performing a Conditional Quality Gate review.

## Context

This gate runs at **stage 10** — after BDD scenarios (stage 9b) and test plans per story (stage 9f) are complete. It is always required and is not conditional on the readiness check.

The test strategy is informed by concrete evidence from BDD and test plans — it does not estimate coverage. By the time this skill runs, every story has SCN-NNN acceptance scenarios and TC-NNN test cases with C1–C4 risk classifications. The test strategy aggregates this evidence into an initiative-level view.

Scale the depth to the initiative size: a Fast Path change needs a minimal strategy (scope note + technology stack + key test levels); an Enterprise initiative needs the full strategy. The scope note at the top of the output must state which applies.

## Purpose

Define test levels, validation evidence, automation targets, data needs, environments, entry and exit criteria — grounded in the SCN-NNN and TC-NNN inventory already produced by BDD and test plans.

## Inputs

Read in this order — primary inputs first:

**Primary inputs (must be read before writing a single section):**
- `quality-gates/bdd/` — read all F-NNN.md files and `acceptance-checklist.md`; extract SCN-NNN IDs per story and per FR-NNN; the acceptance test coverage is now known — do not estimate it
- `quality-gates/test-plans/` — read all F-XXX.X-test-plan.md files; extract TC-NNN rows grouped by test type and criticality (C1–C4); use these to populate Test Levels with real counts and Risks with story-level signals

**Supporting inputs:**
- `engineering-readiness/initiative-context.md` — Technology Constraints table is the primary source for the Technology Stack section
- `engineering-readiness/readiness-check.md`
- `input/repositories/*.md` — repository descriptors; use for test framework, runner, and CI environment if present
- `input/brs.md` or `input/brs/*.md`
- `input/architecture.md` or `input/architecture/*.md`
- `architecture/architecture-rules.md`
- `planning/traceability-matrix.md`
- `business-intake/business-intake-summary.md`

## Output path

```text
quality-gates/test-strategy.md
```

## Generation steps

**Follow these steps in order. Do not skip or reorder.**

1. Read `.brs2spec/templates/quality-gates/test-strategy.md` — this is the required output structure
2. Read all primary inputs (`quality-gates/bdd/` and `quality-gates/test-plans/`) before writing any section
3. Read all supporting inputs
4. Write `quality-gates/test-strategy.md` starting with the `## Metadata` table exactly as it appears in the template — `| **Status** | **In progress** |` must be the first table in the file
5. **Technology Stack** — populate from `engineering-readiness/initiative-context.md` Technology Constraints table; cross-check with test-plan.md test type rows to confirm frameworks are consistent
6. **Test Levels** — for each level (Unit, Integration, API, UI, Security, Performance, Audit/Compliance): aggregate from test plans — count TC-NNN rows by type; record C1 count, C2 count, automation target, framework; do not estimate what is already known from test plans
7. **Requirement-to-Test Mapping** — for each FR-NNN in `business-intake/business-intake-summary.md`: find matching SCN-NNN in `quality-gates/bdd/` and TC-NNN in `quality-gates/test-plans/`; record FR-NNN → SCN-NNN list → TC-NNN list → test levels covered. This is a concrete mapping, not a generic estimate
8. **Risks** — derive from test plans: any story with overall risk C1 and automation = None is a testing risk; any test type with zero TC-NNN rows across all stories is a coverage gap; record owner and mitigation for each
9. Complete all remaining sections: Scope, Test Objectives, Test Data, Environments, Entry Criteria, Exit Criteria
10. Fill every table with initiative-specific content — do not leave rows empty
11. Set `Status: In progress` — the reviewer changes it to `Accepted` after sign-off

**The output file must start with `## Metadata` and the Status row. Free-form prose without a Metadata table is wrong — the workflow cannot detect gate acceptance without it.**

## Prerequisites

Before writing this artifact, verify:
- [ ] `quality-gates/bdd/acceptance-checklist.md` exists and has `Status: Accepted` — BDD must be complete; the test strategy must not estimate acceptance coverage that BDD already defines
- [ ] At least one `quality-gates/test-plans/F-XXX.X-test-plan.md` exists — test plans provide the TC-NNN inventory and risk classifications that feed the Test Levels and Requirement-to-Test Mapping sections
- [ ] `engineering-readiness/initiative-context.md` exists — provides Technology Stack source

If BDD or test plans are missing: stop. State which is missing and which stage must run first.

## Quality bar

A good output must:

- include evidence for each assessment drawn from BDD and test plans — not generic statements
- link findings to specific FR-NNN, SCN-NNN, and TC-NNN IDs
- assign owners and required-before stages
- distinguish blockers from accepted risks
- produce actionable findings, not generic advice
- Requirement-to-Test Mapping must reference specific SCN-NNN and TC-NNN IDs — a row that says "FR-001 → Integration test" without citing scenario IDs is incomplete
- Test Levels must include C1/C2 counts derived from test plans — not estimated
- Risks must include at least one row per story where overall risk is C1 and automation is None

## Anti-patterns to avoid

Do not produce outputs that:

- say 'looks good' without evidence
- list risks without owners
- estimate BDD coverage — read `quality-gates/bdd/` to know what is actually covered
- estimate unit test scope — read `quality-gates/test-plans/` to know what TC-NNN unit cases are defined
- write the Requirement-to-Test Mapping with generic test types only — cite SCN-NNN and TC-NNN IDs
- ignore triggered gate reason from readiness check
- approve with unresolved critical findings
- create implementation code

## Stop conditions

- If `quality-gates/bdd/` is missing or has no accepted scenarios: stop. State: "Test strategy requires BDD scenarios (stage 9b) to be complete and accepted first."
- If `quality-gates/test-plans/` is missing or empty: stop. State: "Test strategy requires test plans per story (stage 9f) to be complete first."
- If other inputs are missing, list them and produce only the parts supported by available evidence.
- Do not invent evidence.

## Self-review checklist

Before finalizing, verify:

- [ ] Scope note is present — states Fast Path / Standard / Enterprise and scales the depth accordingly.
- [ ] `quality-gates/bdd/` was read before writing — Requirement-to-Test Mapping is populated from actual SCN-NNN IDs, not estimated.
- [ ] `quality-gates/test-plans/` was read before writing — Test Levels table includes C1/C2 counts from actual TC-NNN rows.
- [ ] Requirement-to-Test Mapping table cites specific SCN-NNN and TC-NNN IDs for every FR-NNN — not generic test types only.
- [ ] Test Levels table includes automation target and framework for each level, derived from initiative-context.md and test plans.
- [ ] At least one Risk row exists for every story where overall risk = C1 and automation = None.
- [ ] Every finding has evidence linked to a specific artifact (SCN-NNN, TC-NNN, AR-NNN, or BR-NNN).
- [ ] Every required action has an owner and required-before stage.
- [ ] Residual risks are explicit with owners.
- [ ] The final decision is clear.


