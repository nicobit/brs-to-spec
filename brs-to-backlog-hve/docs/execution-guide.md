# Execution Guide

This guide explains how to execute the BRS-to-backlog workflow in VS Code with GitHub Copilot Chat and an HVE-style setup.

## Prerequisites

Recommended:

- VS Code
- GitHub Copilot Chat
- HVE Core installed if you want HVE-style agents, prompts, instructions, and skills available

This project works even if HVE Core is not installed, because the core prompts and instructions are included in this repository.

## Step 1 — Prepare Inputs

Put the BRS here:

```text
/input/brs.md
```

Optionally put architecture here:

```text
/input/architecture.md
```

## Step 2 — Run Capability Extraction

Open:

```text
.github/prompts/01-extract-capabilities.prompt.md
```

In Copilot Chat, ask:

```text
Run this prompt using the current workspace files and create the requested output file.
```

Expected output:

```text
/output/01-extracted-capabilities.md
```

## Step 3 — Run Epic Generation

Open:

```text
.github/prompts/02-create-epics.prompt.md
```

Run it after checking the capability output.

Expected output:

```text
/output/02-candidate-epics.md
```

## Step 4 — Run Story Generation

Open:

```text
.github/prompts/03-create-stories.prompt.md
```

Expected output:

```text
/output/03-candidate-stories.md
```

## Step 5 — Run Backlog Review

Open:

```text
.github/prompts/04-review-backlog.prompt.md
```

Expected output:

```text
/output/04-backlog-review.md
```

Do not skip this step.

## Step 6 — Create GitHub Issue Definitions

Open:

```text
.github/prompts/05-create-github-issues.prompt.md
```

Expected output:

```text
/output/05-github-issues.md
```

You can use this file to manually create issues or automate issue creation later.

## Step 7 — Create Traceability Matrix

Open:

```text
.github/prompts/06-create-traceability-matrix.prompt.md
```

Expected output:

```text
/output/06-traceability-matrix.md
```

## Practical Advice

Do not run all prompts blindly. After each output:

1. review quality
2. fix obvious gaps
3. add clarification to input files if needed
4. rerun the step

The best results come from iterative refinement.
