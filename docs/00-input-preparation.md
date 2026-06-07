# Input Preparation

Input Preparation turns real source documents into normalized Markdown inputs.

## Why this exists

Enterprise work usually starts with:
- Word BRS documents,
- architecture drafts,
- SharePoint files,
- Confluence pages,
- diagrams exported as text,
- mixed-format documents.

Downstream prompts need stable inputs.

## Official outputs

```text
input/brs.md
input/initial-architecture.md
input/input-package.md
```

## `input/brs.md`

The normalized BRS.

It should preserve:
- document title,
- document version/date,
- sections,
- business objectives,
- requirements,
- rules,
- assumptions,
- tables,
- open questions,
- source references where possible.

## `input/initial-architecture.md`

The normalized architecture document.

It should preserve:
- system context,
- current architecture,
- target architecture,
- technology stack,
- integration constraints,
- security model,
- deployment model,
- data ownership,
- APIs,
- diagrams as text descriptions,
- open architecture decisions.

## `input/input-package.md`

The package metadata.

It should record:
- source files,
- versions,
- missing inputs,
- conversion notes,
- assumptions,
- known limitations.

## If architecture is missing

Create `input/initial-architecture.md` with:

```text
No initial architecture document provided.
```

Then downstream architecture prompts must mark architecture assumptions as open decisions.
