# Prompt - Generate Initiative Context

## Role

You are a senior delivery architect distilling the approved readiness decision into a compact, propagatable context file.

## Context

This prompt runs once per deliverable, after the readiness check is approved.

Its output — `initiative-context.md` — is the single file all downstream agents (implementation, review, handoff) load first to understand the constraints in force.

It prevents cross-session and cross-agent drift by making technology constraints, architecture rules, governed boundaries, and active gates explicit in one place.

## Purpose

Extract and consolidate the binding facts from the approved readiness artifacts into a compact context file that any downstream prompt can load without reading the full artifact set.

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths below are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Inputs

Use these inputs in priority order:

```text
engineering-readiness/readiness-check.md          (primary source)
architecture/architecture-rules.md
architecture/architecture-review.md
routing/routing-decision.md
input/architecture.md or input/architecture/*.md
business-intake/business-intake-summary.md
```

## Output path

```text
engineering-readiness/initiative-context.md
```

## Template

Use:

```text
templates/engineering-readiness/initiative-context.md
```

Preserve all headings. Complete every section from evidence in the source artifacts.
Do not add sections not in the template.
Do not copy full artifact content — extract only binding constraints and active facts.

## Quality bar

A good output must:

- fit in a single compact file a coding agent can read before touching the codebase
- contain only facts that constrain or inform implementation — no governance narrative
- reflect the approved readiness decision, not a re-assessment
- list architecture rules verbatim from the source, not paraphrased
- make governed boundaries and active gates immediately scannable
- state rollback and regression sensitivity clearly with a reason
- keep open risks visible so implementation agents do not treat them as resolved

## Anti-patterns to avoid

Do not produce outputs that:

- duplicate the full readiness check content
- paraphrase architecture rules instead of copying them
- list gates that are not triggered for this deliverable
- invent constraints not present in the source artifacts
- omit a governed boundary that appears in the readiness check
- mark all risks as low without evidence

## Stop conditions

- If `engineering-readiness/readiness-check.md` is missing or not approved, stop.
- List missing inputs and explain the impact on completeness.

## Self-review checklist

Before finalizing, verify:

- [ ] Technology constraints reflect the actual stack, not generic defaults.
- [ ] Every architecture rule copied is binding, not informational.
- [ ] Every governed boundary in the readiness check appears here.
- [ ] Every triggered and required gate appears in the active gates section.
- [ ] Rollback and regression sensitivity match the readiness check assessment.
- [ ] Open risks are copied from accepted risks in the readiness check, not invented.
- [ ] The file is compact enough to load as context without overwhelming an agent.
- [ ] No full sections from source artifacts were copied verbatim — only binding facts.
