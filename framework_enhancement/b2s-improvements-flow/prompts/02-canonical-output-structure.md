# Prompt 2 — Create the New Canonical Output Structure

Refactor the `.b2s` framework so that the canonical output structure is centered around delivery packages.

Current issue:

The existing framework has many enterprise artifacts, but the Epic → Feature → Story → AI handoff chain is not prominent enough. The output should not only contain `delivery-structure.md`; it should generate concrete story packages that can be directly used by AI coding agents.

Create or update the framework so that the generated output follows this structure:

```text
output/
  01-business-intake/
    business-intake-summary.md
    gaps-and-questions.md

  02-business-analysis/
    requirements.md
    business-rules.md
    actors-and-personas.md
    use-cases.md
    process-flows.md

  03-architecture/
    architecture-review.md
    architecture-rules.md
    existing-system-impact.md
    data-impact.md
    integration-impact.md

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
    openspec-handoff.md
    standalone-handoff.md
    compact-handoff.md

  08-review/
    review-package.md
```

Requirements:

1. `delivery-structure.md` must become a summary/index, not the only story artifact.
2. Each Epic must have its own file.
3. Each Feature must have its own file.
4. Each Story must have its own folder.
5. Each Story folder must include:
   - `story.md`
   - `acceptance-criteria.md`
   - `bdd-scenarios.md`
   - `implementation-context.md`
   - `tasks.md`
   - `coding-prompt.md`
   - `validation-checklist.md`
6. The OpenSpec handoff should either reuse these story packages or map cleanly to them.
7. The traceability matrix must link BRS references, requirements, business rules, epics, features, stories, AC, BDD scenarios, and test cases.

Do not create a disconnected output structure. The delivery package must be derived from the business analysis, architecture review, and readiness checks.
