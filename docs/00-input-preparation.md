# Input Preparation

Input preparation happens inside an initiative workspace such as:

```text
initiatives/I001-onboarding-request/
```

Default inputs are:

```text
input/brs.md
input/architecture.md
input/input-package.md
```

Only expand to:

```text
input/brs/*.md
input/architecture/*.md
```

when the same initiative genuinely has multiple source documents.

Use `input/input-package.md` to record source inventory, completeness, overlap, conflicts, assumptions, and consolidation notes before downstream planning and readiness work begins.

## Optional: repository descriptors

When the initiative spans multiple repositories (API, UI, DB services, etc.), add descriptor files to:

```text
input/repositories/<alias>.md
```

The file name without `.md` becomes the subfolder name in the handoff output.

This folder is optional. If it is absent or empty, the handoff uses a flat structure (one folder per story, no repo subfolders).

To generate a descriptor file automatically from inside a target repository, use:

```text
.brs2spec/tools/prompts/describe-repository.md
```

See [Handoff](05-handoff.md) for how repo descriptors affect handoff output structure.

## Prompts

Input preparation prompts:

```text
.brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md
.brs2spec/skills/0-input-preparation/02-create-brs-from-text.md
.brs2spec/skills/0-input-preparation/03-normalize-input-package.md
.brs2spec/skills/0-input-preparation/04-draft-architecture-from-brs.md
```

