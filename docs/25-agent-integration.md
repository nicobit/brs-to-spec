# Agent Integration

## The problem

When you adopt this framework in an existing repository, that repo likely already has its own `copilot-instructions.md`, `CLAUDE.md`, or `.cursorrules`. You cannot replace those files — they contain your project-specific rules. And inlining the framework rules into them creates a maintenance burden: every framework upgrade requires a manual merge.

## The solution

The framework uses a different file for each integration layer:

| File | Who reads it | What it does |
|---|---|---|
| `.brs2spec/agent-instructions.md` | Canonical source | All framework rules live here |
| `.github/instructions/brs-to-spec.instructions.md` | GitHub Copilot | Scoped to `initiatives/**` — does not touch your `copilot-instructions.md` |
| `.brs2spec/` prompts | GitHub Copilot Chat | All prompt logic lives here — reference directly |
| `.brs2spec/brs-to-spec-run-workflow.md` | All agents | Full workflow prompt content |

Your existing `copilot-instructions.md`, `CLAUDE.md`, and `.cursorrules` are **untouched**.

---

## What to copy into your existing repo

```
.brs2spec/                                        ← all framework content
.github/instructions/brs-to-spec.instructions.md  ← Copilot scoped rules
.brs2spec/                                        ← all prompt logic (use directly)
```

That is the complete adoption. Nothing else needs to change in your repo.

---

## How it works per agent

### GitHub Copilot (existing repo)

GitHub Copilot automatically loads **all** `.instructions.md` files under `.github/instructions/` alongside `copilot-instructions.md`. Each file can declare an `applyTo` glob to limit when it activates.

`brs-to-spec.instructions.md` uses:

```yaml
---
applyTo: "initiatives/**"
---
```

This means the framework rules only activate when Copilot is working inside an `initiatives/` workspace. Your project rules in `copilot-instructions.md` apply everywhere else. There is no conflict.

### Claude Code

Reference the canonical file from your `CLAUDE.md` or `AGENTS.md`:

```markdown
## BRS to Spec Framework
@.brs2spec/agent-instructions.md
```

Claude Code reads the file at session start. On framework upgrade, the file updates automatically — no change needed in your `CLAUDE.md`.

### Cursor

Add to `.cursorrules`:

```
@.brs2spec/agent-instructions.md
```

### Codex

Add to `AGENTS.md`:

```markdown
## BRS to Spec Framework
Read and apply all rules from `.brs2spec/agent-instructions.md` before processing any request.
```

---

## Agent support summary

| Agent | Mechanism | Your existing instructions | Framework instructions |
|---|---|---|---|
| GitHub Copilot | `.github/instructions/brs-to-spec.instructions.md` with `applyTo: "initiatives/**"` | Untouched | Scoped — active only inside `initiatives/` |
| Claude Code | `@.brs2spec/agent-instructions.md` in `CLAUDE.md` | Untouched | Always active |
| Cursor | `@.brs2spec/agent-instructions.md` in `.cursorrules` | Untouched | Always active |
| Codex | Read instruction in `AGENTS.md` | Untouched | Always active |

---

## Keeping up to date

When you upgrade the framework (pull a new version of `.brs2spec/`):

- **Claude Code / Cursor / Codex**: no change needed — they reference the file by path and pick up the new content automatically.
- **GitHub Copilot**: `.github/instructions/brs-to-spec.instructions.md` is part of the framework folder pattern — replace it with the new version as part of the upgrade. Your `copilot-instructions.md` remains untouched.

---

## This framework's own repo

This repo uses `copilot-instructions.md` with the rules inlined directly — because this repo has no project-specific Copilot instructions to protect. For any other repo, the `.github/instructions/` approach above is the correct integration pattern.
