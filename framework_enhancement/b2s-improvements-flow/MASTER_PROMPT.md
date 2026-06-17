# Master Prompt — Improve `.b2s` Delivery Output

Use this prompt if you want to give a single consolidated instruction to an AI coding agent.

---

You are working on my `brs-to-spec` / `.b2s` framework.

The framework already contains useful enterprise artifacts, including business intake, requirements, business rules, architecture review, readiness checks, traceability, BDD, test strategy, handoff, and review package.

The problem is that the framework feels heavy because it creates many artifacts, but the most important output is not yet central and strong enough:

```text
Epic → Feature → Story → Acceptance Criteria → BDD → Tasks → Coding Prompt
```

The goal is to refactor `.b2s` so that the central output becomes AI-ready story packages.

Do not remove enterprise governance artifacts unless they are clearly duplicated or unused. Instead, make all governance artifacts feed into the delivery package.

## New positioning

`brs-to-spec` transforms raw enterprise BRS documents into AI-ready story packages with business traceability, architecture context, acceptance criteria, BDD scenarios, implementation tasks, and coding prompts.

It is not a BMAD competitor. It sits before BMAD, OpenSpec, GitHub Copilot, Codex, Claude Code, Cursor, Devin, or other coding agents.

## Required changes

1. Add or improve Epic package generation.
2. Add or improve Feature package generation.
3. Add a first-class Story Package template.
4. Make each story package the atomic unit of implementation.
5. Make BDD mandatory for business-facing stories in Standard and Full Governance mode.
6. Add delivery modes: Compact, Standard, Full Governance.
7. Improve validators to detect shallow output.
8. Generate a realistic golden example.
9. Update README positioning.

## Target output structure

```text
output/
  01-business-intake/
  02-business-analysis/
  03-architecture/
  04-delivery/
    delivery-structure.md
    epics/
      E-001-<slug>.md
    features/
      F-001-<slug>.md
    stories/
      F-001.1-<slug>/
        story.md
        acceptance-criteria.md
        bdd-scenarios.md
        implementation-context.md
        tasks.md
        coding-prompt.md
        validation-checklist.md
  05-traceability/
    traceability-matrix.md
  06-readiness/
    readiness-check.md
  07-handoff/
  08-review/
```

## Story package requirements

Each story package must include:

- Story ID and title
- User story
- Business goal
- Scope and out-of-scope
- Source traceability
- Linked requirements
- Linked business rules
- Linked architecture constraints
- Acceptance criteria
- BDD scenarios
- Implementation context
- Impacted components
- Data/API/UI/integration impact where applicable
- Constraints
- Dependencies
- Implementation tasks
- Test expectations
- Definition of done
- Coding-agent prompt

## Validation rules

Fail or warn if:

- story is generic
- title is generic
- actor is missing or generic
- business outcome is missing
- story has no linked requirement
- story has no acceptance criteria
- acceptance criteria are not testable
- BDD is missing when required
- BDD scenarios describe developer activity instead of observable behavior
- implementation tasks are generic
- coding prompt does not include constraints, tests, impacted components, and out-of-scope instructions

## Final expectation

The framework should no longer feel like it produces many disconnected governance artifacts.

It should feel like it produces a strong AI-ready delivery package, where every artifact supports the story package and every story package is ready to be used by a coding agent.
