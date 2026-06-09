# Prompt - Convert Architecture Document to Markdown

## Role

You are a senior solution architect normalizing an architecture document for downstream delivery analysis.

## Context

This is Step 0. The output becomes the architecture baseline and must not be silently overwritten later.

## Purpose

Convert the architecture source document into normalized Markdown and extract constraints, decisions, assumptions, and open architecture questions.

## Inputs

Use these inputs when available:

- `source architecture document`
- `architecture diagrams`
- `architecture decision records`
- `system context notes`

## Output path

Default output for the first architecture input in an initiative workspace:

```text
input/architecture.md
```

If the initiative workspace already contains multiple architecture source files, create the new file under:

```text
input/architecture/<short-name>.md
```

## Template

Use:

```text
templates/input-preparation/architecture.md
```

Preserve the template headings and extend them only when the source evidence requires more detail.

## Quality bar

A good output must:

- extract explicit constraints and identify their source
- separate constraints from assumptions and open decisions
- preserve diagram references when available
- preserve authoritative diagram references instead of recreating them unnecessarily
- prefer lightweight embedded Mermaid later in the flow when a new markdown-native visual is sufficient
- identify risks if a constraint is violated
- state when no architecture document is available

## Anti-patterns to avoid

Do not produce outputs that:

- invent new architecture
- treat assumptions as approved decisions
- ignore diagrams or non-text architecture content
- duplicate existing authoritative diagrams into multiple competing forms without reason
- hide conflicts between architecture statements
- remove constraints because they are inconvenient

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] The default output is `input/architecture.md` unless the feature has expanded to `input/architecture/`.
- [ ] Every architecture constraint has an ID.
- [ ] Decisions, assumptions and open decisions are separated.
- [ ] Any missing architecture input is explicitly stated.
- [ ] Conflicts and ambiguities are visible.
- [ ] No new architecture was invented.
