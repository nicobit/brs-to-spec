# Business Analysis Prompt Set

This folder contains draft prompts for the target business-analysis artifacts.

They are intended as redesign inputs for `.brs2spec2`, not as active framework files yet.

## Design rule

Canonical analysis artifacts are based on AI Unified Process prompt bodies, adapted to initiative-local paths and `.brs2spec2` execution expectations:

- `requirements.md`
- `entity-model.md`
- `use-cases.puml`
- `use-cases/UC-*.md`

Supporting analysis artifacts are adapted from existing `.brs2spec2` skills:

- `business-rules.md`
- `actors-and-personas.md`
- `process-flows.md`
- `gaps-and-questions.md`

## Files

- `01-create-requirements.md`
- `02-create-entity-model.md`
- `03-create-use-case-diagram.md`
- `04-create-use-case-spec.md`
- `05-create-business-rules.md`
- `06-create-actors-and-personas.md`
- `07-create-process-flows.md`
- `08-find-gaps-and-questions.md`

## Source basis

AIUP prompt bodies used as the base:

- Marketplace README: workflow and artifact chain
- AIUP `/requirements`
- AIUP `/entity-model`
- AIUP `/use-case-spec`
- AIUP `/use-case-diagram` behavior as documented in the README

Framework-native source prompts used as the base:

- `.brs2spec2/skills/product-owner/create-business-rules.md`
- `.brs2spec2/skills/product-owner/create-actors-and-personas.md`
- `.brs2spec2/skills/product-owner/create-process-flows.md`
- `.brs2spec2/skills/product-owner/find-gaps-and-questions.md`

## Adaptation rules applied

- Paths changed from `docs/...` to `business-analysis/...`
- Prompts written as initiative-local artifact prompts instead of global project prompts
- Added traceability expectations for later planning, readiness, and handoff
- Preserved one-artifact-per-prompt discipline
- Preserved one-use-case-per-file discipline
