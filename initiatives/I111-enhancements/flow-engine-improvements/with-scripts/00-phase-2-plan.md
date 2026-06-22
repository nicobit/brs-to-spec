# Phase 2 Plan — Scripted Flow Engine Core

## Problem statement

The current flow engine still relies on the model to faithfully perform orchestration
steps that are mechanical:

- read every `read_from` file
- instantiate runtime events correctly
- move queue files between folders
- keep `workflow-state.json`, `event-log.jsonl`, and `open-decisions.md` consistent
- reject malformed runtime events

The observed failures in initiatives such as I009, I010, and I012 show that when the
AI skips or improvises those steps, the framework can drift into:

- fabricated failure reasons
- stale or mixed-version event chains
- duplicate or orphan queue files
- contradictory event log vs workflow state
- malformed runtime events missing `must_include` / `validation_rules`

## Phase 2 objective

Move the engine from **protocol-by-prompt** to **protocol-by-script** for all
deterministic orchestration mechanics, while keeping artifact authoring prompt-driven.

## What success looks like

After Phase 2:

1. Every runtime event is created by a script from a template, never hand-crafted.
2. Every Step 10 input read is performed by a script and emits machine-generated
   `read_evidence`.
3. Every queue transition is performed as a real move by a script.
4. Every result file is validated by a script before state updates happen.
5. Every state update is produced by a script from authoritative event/result inputs.
6. AI prompts receive prepared inputs and are asked only to produce the artifact and
   structured execution outcome.

## Boundary of responsibility

### Script-owned

- template lookup and event instantiation
- workspace root resolution
- `read_from` path expansion and existence checks
- `read_evidence` capture
- queue lifecycle transitions
- result contract validation
- event-log append
- workflow-state updates
- repair/reset mechanics

### AI-owned

- artifact content generation
- semantic failure explanation when inputs are genuinely insufficient
- interpretation of BRS/architecture/business context
- natural-language validation reasoning

## Preferred implementation style

Use **Python** for the scripted engine core.

Reasons:

- strong cross-platform support
- good fit for YAML/Markdown/JSONL orchestration
- simpler than shell for path handling and atomic file operations
- easier to test than prompt-only behavior
- aligns well with the repo’s state-heavy engine design

Thin wrappers may be added later:

- `scripts/brs2spec.ps1`
- `scripts/brs2spec.sh`

but the real logic should live in Python modules.

## Recommended rollout order

1. Script runtime event instantiation
2. Script input resolution + `read_evidence`
3. Script queue transitions
4. Script result-contract validation
5. Script state updates
6. Script repair/reset flows

This ordering reduces risk quickly without requiring a full engine rewrite on day one.
