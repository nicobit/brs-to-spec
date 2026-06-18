# BRS to Spec — Persona Skill Registry (Full Reference)

> For routing and skill selection, `module-index.md` is sufficient.
> To load a specific persona's definition, required_inputs, done_criteria, or stop_conditions — load only the relevant file from `module-personas/`.
> Do not load this file and all persona files together — load only what the active skill needs.

---

## How to use this registry

1. Identify the current phase using `state/workflow-state.json` or the stage lookup table in `module-index.md`.
2. Find the right persona for the required work using the quick-reference table in `module-index.md`.
3. Load only `module-personas/<persona>.md` for the selected persona — do not load all persona files.
4. Find the skill in that file to get the prompt path, required inputs, and done criteria.
5. Load only that prompt. Do not load unrelated prompts.
6. Produce only the output artifact listed for the skill.
7. Update `state/workflow-state.json` after the artifact is produced.
8. Check stop conditions before and during execution.

---

## Framework purpose

`brs-to-spec` transforms one or more raw Business Requirements Specification (BRS) documents, plus optional architecture source material, into business-approved, architecture-aligned, delivery-ready increments structured so that an AI coding agent can implement safely, one story at a time.

```
Phase     = where we are in the lifecycle
Persona   = who should think or act
Skill     = what that persona can do
Prompt    = how the skill is executed
Artifact  = what must be produced or updated
Gate      = what must be true before moving on
```

**Artifacts own the process. Personas execute registered skills against artifacts.** No autonomous multi-agent chat. No rewriting the whole framework.

---

## Persona files

| Persona | File | Phases covered |
|---|---|---|
| Orchestrator | `module-personas/orchestrator.md` | All phases — workflow control |
| Product Owner | `module-personas/product-owner.md` | 0 (intake), 2 (business intake) |
| Architect | `module-personas/architect.md` | 0 (input prep), 3 (planning and architecture) |
| Delivery Lead | `module-personas/delivery-lead.md` | 3 (planning), 7 (perspectives) |
| QA Analyst | `module-personas/qa-analyst.md` | 4 (quality gates), 8 (implementation), 9 (review) |
| Security Reviewer | `module-personas/security-reviewer.md` | 4 (quality gates), 9 (review) |
| Engineering Lead | `module-personas/engineering-lead.md` | 4 (readiness), 5 (handoff), 8 (implementation) |
| Reviewer | `module-personas/reviewer.md` | 9 (review) |

Each persona file contains: persona definition, responsibilities, must-read, may-produce, must-not-do, handoff targets, and full skill tables with required_inputs, done_criteria, and stop_conditions.
