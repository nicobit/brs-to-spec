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
state/routing-decision.md
input/architecture.md or input/architecture/*.md
input/repositories/*.md                           (repository descriptors — use for Technology Constraints if present)
business-intake/business-intake-summary.md
```

When `input/repositories/*.md` files exist, use them as the authoritative source for the Technology Constraints table — they contain structured language, framework, runtime, database, and infrastructure fields per repository. If no descriptor exists, derive technology constraints from `input/architecture.md` prose and note "repository descriptor not yet created" in the Source column.

## Output path

```text
engineering-readiness/initiative-context.md
```

## Template

Use:

```text
.brs2spec/templates/engineering-readiness/initiative-context.md
```

Preserve all headings. Complete every section from evidence in the source artifacts.
Do not add sections not in the template.
Do not copy full artifact content — extract only binding constraints and active facts.

Populate the `AI model version` field in the Metadata table with your own model identifier
(e.g. `claude-sonnet-4-6`, `gpt-4o`). Do not leave it blank or ask the user to fill it in —
you know which model you are.

## Carried-Forward Context population rule

The `## Carried-Forward Context` section must be populated from these sources — do not leave it empty if the source material contains any of these:

- **Active assumptions** — copy from `architecture/architecture-review.md` → Active assumptions. Include only assumptions still in force at implementation time. If none exist in that section, scan the review for phrases like "we assume", "assuming", "subject to", "pending confirmation of" and extract those as rows.
- **Known unknowns** — copy from `architecture/architecture-review.md` → Known unknowns. If none exist, scan for phrases like "not yet determined", "TBD", "unclear", "depends on" that describe things not yet known (distinct from pending decisions).
- **Non-obvious constraint rationale** — for each AR-NNN rule in the Architecture Rules in Force section, check whether the reason is self-evident from the rule text alone. If not, add a row explaining why the rule exists and what breaks if it is ignored. Derive this from the architecture review rationale or BRS context.

If none of the three sub-sections can be populated from evidence, write `> None identified` in each sub-section rather than deleting it — keeping the section visible reminds downstream consumers that context loss was checked.

## Quality bar

A good output must:

- fit in a single compact file a coding agent can read before touching the codebase
- contain only facts that constrain or inform implementation — no governance narrative
- reflect the approved readiness decision, not a re-assessment
- list architecture rules verbatim from the source, not paraphrased
- make governed boundaries and active gates immediately scannable
- state rollback and regression sensitivity clearly with a reason
- keep open risks visible so implementation agents do not treat them as resolved
- populate Carried-Forward Context from evidence — never leave it empty without checking

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
- [ ] Carried-Forward Context is populated or explicitly marked `> None identified` — never silently empty.
