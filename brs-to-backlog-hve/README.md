# BRS to Backlog — HVE-style Copilot Workflow

This project gives you a practical, folder-based workflow to transform a Business Requirements Specification (BRS) into:

1. extracted business capabilities
2. candidate epics
3. candidate user stories
4. backlog quality review
5. GitHub-ready issue definitions

It follows an HVE-style structure using:

- `.github/prompts` for executable Copilot prompts
- `.github/instructions` for reusable quality rules
- `.github/skills` for reusable skills and checklists
- `input` for your BRS and architecture
- `output` for generated artifacts

Important: this is not an official HVE Core package. It is a custom BRS-to-backlog project designed to work with GitHub Copilot / HVE-style workflows.

---

## Folder Structure

```text
brs-to-backlog-hve/
  input/
    brs.md
    architecture.md
  output/
    .gitkeep
  .github/
    copilot-instructions.md
    prompts/
      01-extract-capabilities.prompt.md
      02-create-epics.prompt.md
      03-create-stories.prompt.md
      04-review-backlog.prompt.md
      05-create-github-issues.prompt.md
      06-create-traceability-matrix.prompt.md
    instructions/
      brs-traceability.instructions.md
      story-quality.instructions.md
      backlog-governance.instructions.md
      output-format.instructions.md
    skills/
      backlog-splitting/
        SKILL.md
      acceptance-criteria/
        SKILL.md
      traceability-matrix/
        SKILL.md
  docs/
    execution-guide.md
    quality-gates.md
    customization-guide.md
```

---

## How to Use

### 1. Put your BRS into `input/brs.md`

Convert your Word/PDF BRS into Markdown if possible. Keep headings, tables, and numbered requirements.

### 2. Optionally add architecture

If you have architecture, add it to:

```text
input/architecture.md
```

If you do not have architecture yet, keep the placeholder file.

### 3. Run prompts in order

In VS Code with GitHub Copilot Chat, open each prompt file and ask Copilot:

```text
Run this prompt using the current workspace files.
```

Run them in this order:

```text
01-extract-capabilities.prompt.md
02-create-epics.prompt.md
03-create-stories.prompt.md
04-review-backlog.prompt.md
05-create-github-issues.prompt.md
06-create-traceability-matrix.prompt.md
```

### 4. Review outputs after every step

Do not blindly continue if an output is weak. Fix the input or rerun the relevant step with additional clarification.

---

## Recommended Execution Flow

```text
BRS
  ↓
Extracted capabilities
  ↓
Candidate epics
  ↓
Candidate stories
  ↓
Backlog review
  ↓
GitHub-ready issues
  ↓
Traceability matrix
```

---

## Quality Rule

Never move to implementation until every important BRS requirement can be traced to:

```text
BRS requirement → capability → epic → story → acceptance criteria → test note
```

