# Business Analysis Improvement Package

This folder captures the design material needed to improve the `.brs2spec2` business-analysis phase using the AI Unified Process marketplace as the reference shape for the core artifacts.

## Scope

Focus area:

- Business-analysis artifacts only
- Their dependencies and production order
- How those artifacts should be consumed by later `.brs2spec2` phases
- Which AIUP prompts should be reused as the base

Out of scope for this package:

- Direct framework code changes
- Event-template rewrites
- Workflow-state schema changes
- Handoff redesign beyond business-analysis inputs

## Contents

- `artifact-map.md`
  Concrete artifact map for the target business-analysis phase:
  `artifact | base prompt | inputs | outputs | should block what | later consumers`

- `proposed-stage-design.md`
  Recommended production order, dependencies, and gating logic for the business-analysis phase.

- `prompt-adoption-strategy.md`
  Guidance on which AIUP prompts should become the base for `.brs2spec2` artifacts, and where framework-native prompts should remain.

## Working Position

Recommended target artifact set for business analysis:

- `business-analysis/requirements.md`
- `business-analysis/entity-model.md`
- `business-analysis/use-cases.puml`
- `business-analysis/use-cases.md`
- `business-analysis/use-cases/UC-*.md`
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`
- `business-analysis/process-flows.md`
- `business-analysis/gaps-and-questions.md`

The first four are the AIUP-style canonical analysis spine.
The last four are retained framework artifacts that enrich, validate, and support later planning, readiness, and handoff phases.
