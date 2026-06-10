# Agent Integration

The framework ships its behavioral rules as a standalone referenceable prompt file:

```
.github/prompts/brs-to-spec-instructions.md
```

This file contains all framework rules — workspace conventions, artifact hierarchy, forbidden responses, intent recognition, stage gates — and nothing project-specific (no tech stack, no coding conventions, no team processes).

## Why a standalone file

When you adopt the framework in an existing repository, that repository likely already has its own `copilot-instructions.md` (or equivalent). Merging the framework rules into that file causes two problems:

1. The file becomes a maintenance burden — framework upgrades must be manually merged with project-specific content.
2. Conflicts arise when project-specific rules and framework rules overlap.

The standalone file solves both: the project keeps its own instructions, and the framework is pulled in by reference.

## How to reference it

### GitHub Copilot

Add one line to your project's `.github/copilot-instructions.md`:

```markdown
## BRS to Spec Framework

#file:.github/prompts/brs-to-spec-instructions.md
```

Copilot resolves the `#file:` reference and loads the full set of behavioral rules into context.

### Claude Code

Add to your project's `CLAUDE.md` or `.github/agents.md`:

```markdown
## BRS to Spec Framework

<include path=".github/prompts/brs-to-spec-instructions.md" />
```

Or reference it directly in a Claude Code session with `@.github/prompts/brs-to-spec-instructions.md`.

### Cursor

Add to your `.cursorrules` file:

```
@.github/prompts/brs-to-spec-instructions.md
```

### Codex / OpenAI Agents

In your `AGENTS.md`, add a section that pastes the file path and instructs the agent to read it at session start:

```markdown
## BRS to Spec Framework

Read and apply all rules from `.github/prompts/brs-to-spec-instructions.md` before processing any request.
```

## What the file contains

The instructions file covers:

| Section | What it governs |
|---|---|
| Required behavior (Rules 1–7) | What the agent must never do regardless of user request |
| Initiative workspace rule | Folder structure and canonical source set |
| Entry mode rule | How to identify BRS-first vs brownfield vs small-change |
| Workflow state file rule | How to read and update `planning/workflow-state.json` |
| Open decisions register rule | Single source of truth for blocking decisions |
| Source of truth hierarchy | Which artifact wins when they conflict |
| Stage sequence | The 13-stage gate chain with hard gates |
| Intent recognition | Trigger phrases that activate the full workflow |
| Forbidden responses | Exact patterns the agent must never produce |
| Output quality | What counts as "good enough" for each artifact type |

## What the file does NOT contain

- Project tech stack or language conventions
- Team-specific naming conventions
- Repository-specific file paths outside the framework workspace
- Coding style rules
- Secrets, credentials, or environment-specific config

These belong in your project's own instructions file, kept separate from the framework reference.

## Keeping the framework up to date

When you upgrade the framework (pull a new version of the `.brs2spec/` folder), the instructions file is updated automatically as part of the upgrade. Your project's `copilot-instructions.md` (or equivalent) does not need to change — it just references the file by path.

If you have customized `brs-to-spec-instructions.md` for your project, treat those customizations as a patch layer and reapply them after each framework upgrade.
