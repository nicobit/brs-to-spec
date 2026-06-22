# `.brs2spec2` Business Analysis Artifact Map

## Goal

Define the target artifact contract for the business-analysis phase so later framework improvements can redesign prompts, event templates, dependencies, and downstream consumers around a stable structure.

## Guiding Principle

Use the AI Unified Process marketplace as the base shape for the canonical analysis artifacts:

- `requirements.md`
- `entity-model.md`
- `use-cases.puml`
- `use-cases/UC-*.md`

Retain framework-native support artifacts where they add governance or downstream value:

- `business-rules.md`
- `actors-and-personas.md`
- `process-flows.md`
- `gaps-and-questions.md`

## Artifact Map

| Artifact | Base prompt | Inputs | Outputs | Should block what | Later consumers |
|---|---|---|---|---|---|
| `business-intake/business-intake-summary.md` | Framework-native prompt: `.brs2spec2/skills/product-owner/create-business-intake-summary.md` | `input/brs.md`; optional `input/architecture.md`; optional `routing/routing-decision.md` | PO-readable normalized intake summary with canonical IDs and gaps | Blocks all business-analysis artifacts | `requirements.md`; `gaps-and-questions.md`; architecture review; delivery structure; readiness review |
| `business-analysis/requirements.md` | AIUP `/requirements` as the base prompt, adapted to initiative-local paths and event execution | `business-intake/business-intake-summary.md`; `input/brs.md`; optional `routing/routing-decision.md` | Canonical requirements catalog with separate FR, NFR, and constraints tables | Blocks `entity-model.md`; `use-cases.puml`; `business-rules.md`; provides the minimum baseline for architecture to start; should strongly gate `delivery-structure.md` and `traceability-matrix.md` | Entity model; use-case diagram; business rules; architecture review; planning; traceability; readiness; quality gates |
| `business-analysis/entity-model.md` | AIUP `/entity-model` as the base prompt, adapted to initiative-local paths and event execution | `business-analysis/requirements.md`; optional `business-analysis/business-rules.md`; optional `gaps-and-questions.md`; optional architecture feedback | Domain entity model with Mermaid ER diagram and attribute tables | Should block `data-contract.md`; should refine architecture once started; should inform but not fully block architecture kickoff unless data-heavy initiative | Architecture review; security review; data contract; API/event contracts; handoff design |
| `business-analysis/use-cases.puml` | AIUP `/use-case-diagram` as the base prompt, adapted to initiative-local paths and event execution | `business-analysis/requirements.md` | PlantUML use case diagram with stable `UC-NNN` IDs | Blocks `use-cases/UC-*.md`; should inform actors/personas validation | Use-case specs; actors/personas; planning; stakeholder review; handoff traceability |
| `business-analysis/use-cases/UC-*.md` | AIUP `/use-case-spec` as the base prompt, adapted to initiative-local paths and event execution | `business-analysis/requirements.md`; `business-analysis/use-cases.puml`; optional `business-analysis/business-rules.md`; optional `business-analysis/actors-and-personas.md`; optional architecture feedback | One markdown file per use case, each with overview, preconditions, main success scenario, alternative flows, postconditions, business rules | Should strongly gate `delivery-structure.md`, `bdd/*`, `test-strategy.md`, and story-scoped handoff quality; does not need to fully complete before architecture starts | Delivery structure; BDD; test strategy; handoff story/design/tasks; implementation prompts |
| `business-analysis/business-rules.md` | Framework-native prompt: `.brs2spec2/skills/product-owner/create-business-rules.md` | `business-analysis/requirements.md`; optional `input/brs.md`; optional `business-intake/business-intake-summary.md`; optional architecture feedback on integrations and boundaries | Cross-cutting `BR-NNN` catalog for validation, authorization, calculation, state, notification, and integration rules | Should not block `use-cases.puml`; should inform `UC-*.md`; should be refined by architecture in integration-heavy initiatives; should block rule-heavy BDD scenarios and validation-oriented quality gates if missing | Use-case specs; process flows; BDD; architecture rules; implementation acceptance criteria |
| `business-analysis/actors-and-personas.md` | Framework-native prompt: `.brs2spec2/skills/product-owner/create-actors-and-personas.md`, refocused to derive from requirements and use-case diagram | `business-analysis/requirements.md`; `business-analysis/use-cases.puml`; optional `business-analysis/business-rules.md` | Stable `ACT-NNN` and `SYS-NNN` catalog with goals and interaction matrix | Should not block `use-cases.puml`; should inform `UC-*.md`; should block `process-flows.md` | Process flows; use-case specs; architecture review; handoff role mapping |
| `business-analysis/process-flows.md` | Framework-native prompt: `.brs2spec2/skills/product-owner/create-process-flows.md`, refocused to derive from UCs instead of directly from BRS | `business-analysis/use-cases/UC-*.md`; `business-analysis/actors-and-personas.md`; optional `business-analysis/business-rules.md` | Cross-use-case `PF-NNN` operational journeys with Mermaid flowcharts | Should not block initial delivery structure; should inform architecture review, observability, integration planning, and operations-oriented stories | Architecture review; observability plan; event contract; ops stories; handoff design notes |
| `business-analysis/gaps-and-questions.md` | Framework-native prompt: `.brs2spec2/skills/product-owner/find-gaps-and-questions.md` | `business-intake/business-intake-summary.md`; `business-analysis/requirements.md`; optional `entity-model.md`; optional `use-cases/UC-*.md`; optional `business-rules.md`; optional architecture findings | Structured gap catalog with severity, owner, critical path, and assumptions | Should provide the minimum risk baseline for architecture to start; should block `delivery-structure.md` when blocking gaps exist; should block readiness acceptance when critical scope or compliance gaps remain unresolved | Open decisions; architecture review; planning; readiness; handoff risk notes |

## Notes On Canonical vs Supporting Artifacts

Canonical business-analysis artifacts:

- `requirements.md`
- `entity-model.md`
- `use-cases.puml`
- `use-cases/UC-*.md`

Supporting business-analysis artifacts:

- `business-rules.md`
- `actors-and-personas.md`
- `process-flows.md`
- `gaps-and-questions.md`

This distinction matters because later phases should preferentially read from the canonical analysis spine first, then use the supporting artifacts for clarification, enrichment, validation, and risk handling.

## Main Design Shift From Current `.brs2spec2`

Current v2 business-analysis production is centered on:

- `business-rules.md`
- `actors-and-personas.md`
- `process-flows.md`
- `use-case-spec.md`
- `gaps-and-questions.md`

Target business-analysis production should be centered on:

- `requirements.md`
- `entity-model.md`
- `use-cases.puml`
- `use-cases/UC-*.md`

with existing artifacts retained around that center rather than replacing it.
