# Migration from 0.x

## What changed in v1.x

### Prompt and template locations

All prompts now live under `.brs2spec/` (not at the repository root or under `tools/`):

```text
.brs2spec/0-input-preparation/
.brs2spec/1-routing/
.brs2spec/2-business-intake/
.brs2spec/3-planning-and-modular-delivery/
.brs2spec/4-engineering-readiness/
.brs2spec/5-handoff/
.brs2spec/6-business-copilot/
.brs2spec/7-perspectives/
.brs2spec/8-copilot-implementation/
.brs2spec/9-reviewers/
```

All templates now live under `.brs2spec/templates/` (not under `templates/` at the root):

```text
.brs2spec/templates/
  openspec-handoff/
  standalone-delivery/
  quality-gates/
  planning-and-modular-delivery/
  ...
```

All scripts now live under `.brs2spec/tools/scripts/` (not under `tools/`):

```text
.brs2spec/tools/scripts/new_initiative.py
.brs2spec/tools/scripts/add_brs.py
.brs2spec/tools/scripts/add_architecture.py
.brs2spec/tools/scripts/check_program.py
.brs2spec/tools/scripts/check_prompt_sequence.py
```

### GitHub Copilot prompt wrappers

`.github/prompts/` files are now thin wrappers only. They contain a `description:` frontmatter line and a single delegation line pointing to `.brs2spec/`. All logic lives in `.brs2spec/`.

### New features since v1.0.0

- `planning/workflow-state.json` — fast-path hint for workflow runner; auto-initialised if missing
- Multi-repository handoff — `input/repositories/<alias>.md` descriptors; folder-per-story with optional subfolder-per-repo
- NFR BDD scenarios — non-functional requirements that are measurable produce Gherkin scenarios in `quality-gates/bdd-scenarios.md`
- `tools/prompts/describe-repository.md` — standalone utility to generate a repo descriptor from inside a target repository
- Architecture review multi-repo signal — stage 5 surfaces a notice when architecture spans multiple repos

## Migration steps

If you are migrating an initiative workspace from 0.x:

1. Rename any `templates/` references in existing artifacts to `.brs2spec/templates/`.
2. Rename any `tools/scripts/` references to `.brs2spec/tools/scripts/`.
3. Rename any `.github/.brs2spec/` references to `.github/prompts/`.
4. Add `planning/workflow-state.json` by asking the workflow runner to initialise it.
5. Review whether `input/repositories/` descriptors are needed for multi-repo initiatives.

Do not delete existing initiative workspace artifacts — they remain valid inputs.
