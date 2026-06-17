# Prompt Adoption Strategy

## Objective

Reuse the AI Unified Process marketplace prompts as the base where they already define the right artifact shape, and keep framework-native prompts where the framework adds stronger governance or supporting analysis value.

## Source Prompts To Reuse As The Base

These should be the base prompts for `.brs2spec2`, adapted rather than rewritten from scratch:

| Target artifact | AIUP source prompt | Why reuse it |
|---|---|---|
| `business-analysis/requirements.md` | AIUP `/requirements` | Strong separation of FR, NFR, and constraints; simple artifact contract; good quality checks |
| `business-analysis/entity-model.md` | AIUP `/entity-model` | Clean ER diagram plus attribute-table structure; good artifact discipline |
| `business-analysis/use-cases.puml` | AIUP `/use-case-diagram` | Clear actor/use-case map with stable `UC-NNN` IDs |
| `business-analysis/use-cases/UC-*.md` | AIUP `/use-case-spec` | Best-practice one-use-case-per-file model; keeps behavior specs modular |

## Framework-Native Prompts To Keep

These should remain framework-native, though some should be refocused to consume the new canonical artifacts:

| Artifact | Keep native? | Reason |
|---|---|---|
| `business-intake/business-intake-summary.md` | Yes | AIUP starts from `vision.md`; your framework needs a stronger intake normalization layer from BRS-style inputs |
| `business-analysis/business-rules.md` | Yes | Useful as a cross-cutting rule catalog across use cases and quality gates |
| `business-analysis/actors-and-personas.md` | Yes | Useful for stable actor/system IDs across framework artifacts |
| `business-analysis/process-flows.md` | Yes | Valuable for end-to-end operational journeys beyond individual use cases |
| `business-analysis/gaps-and-questions.md` | Yes | One of the framework's best governance artifacts; AIUP does not foreground it enough |

## Adaptation Rules For AIUP-Based Prompts

When porting AIUP prompt bodies into `.brs2spec2`, keep these changes minimal and deliberate.

### Keep unchanged where possible

- Artifact shape
- Core workflow logic inside the prompt
- Quality checks
- ID conventions where they already fit
- The one-file-per-use-case rule

### Adapt for `.brs2spec2`

- Change paths from `docs/...` to initiative-local paths under `business-analysis/...`
- Add framework metadata conventions where needed
- Add result-file and event-driven execution requirements
- Add compatibility notes for `routing/routing-decision.md` and initiative-local context
- Add traceability hooks to later planning, readiness, and handoff artifacts

### Do not add unless there is a strong framework reason

- Extra prose sections that dilute the AIUP artifact shape
- Framework-only fields that clutter the canonical analysis artifacts
- Planning or implementation detail in business-analysis artifacts
- Multiple use cases in one file

## Recommended Prompt Ownership Model

### Canonical artifact prompts

These should stay as close to AIUP as possible:

- `requirements`
- `entity-model`
- `use-case-diagram`
- `use-case-spec`

### Supporting artifact prompts

These should stay framework-specific:

- `create-business-intake-summary`
- `create-business-rules`
- `create-actors-and-personas`
- `create-process-flows`
- `find-gaps-and-questions`

## Recommended Consumption Rule

Later phases should read the AIUP-shaped canonical artifacts first:

1. `requirements.md`
2. `entity-model.md`
3. `use-cases.puml`
4. `use-cases/UC-*.md`

Then use supporting artifacts for enrichment, validation, and governance:

5. `business-rules.md`
6. `actors-and-personas.md`
7. `process-flows.md`
8. `gaps-and-questions.md`

This rule will keep the redesigned framework coherent even before every downstream prompt has been updated.
