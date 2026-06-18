# Framework Enhancement 14 — Technical Specifications

## Problem Statement

The framework has no dedicated place to collect technical specifications. Currently:

- `quality-gates/api-contract.md` — a single flat file for all APIs you expose
- `quality-gates/data-contract.md` — a single flat file for all schemas
- `quality-gates/event-contract.md` — a single flat file for all events
- No place for APIs you consume from external systems
- No place for integration-level specs (auth, SLA, retry policy, fallback behaviour)
- No place for database schema specs as first-class artifacts
- No distinction between contracts you own vs contracts you depend on

This causes several real problems:
1. API contracts are generated in stage 4b with insufficient detail (no story-level endpoint shapes)
2. Consumed external APIs (Experian, HMRC, T24) are referenced in stories but their specs are never captured
3. Database schemas are buried inside story implementation context, not surfaced as shared artifacts
4. Multi-team scenarios have no coordination mechanism for shared API surfaces
5. No `contract_mode` concept — "API as product" (freeze early) vs "API as implementation detail" (derive from stories)

## Design Decision

Introduce a `technical-specifications/` folder in the initiative workspace as the canonical home for all technical specs, replacing the flat files in `quality-gates/`.

```
technical-specifications/
  api/
    exposed/          ← OpenAPI-level specs you own and publish
    consumed/         ← External system specs you depend on
  database/           ← Table schemas, migrations, ownership
  events/             ← Domain events you emit and subscribe to
  integrations/       ← Auth, SLA, retry, fallback per external system
```

## Contract Mode

Introduce `api_contract_mode` set during engineering readiness:
- `product` — expose to external consumers; define early, freeze, version strictly
- `internal` — implementation detail; derive from story packages after handoff
- `coordinated` — multiple teams; draft early, refine gate after stories

This drives when `create-api-contract` runs and how strictly changes are gated.

## Implementation Prompts

| # | Prompt | What it changes |
|---|---|---|
| 01 | Create technical-specifications folder structure | New folder convention, workspace init update |
| 02 | Create artifact templates for exposed API, consumed API, integration spec, database schema | 4 new templates in `.b2s/artifact-templates/` |
| 03 | Create skills for each technical spec type | 4 new skills, seeded from architecture-review impacted systems |
| 04 | Introduce contract_mode and wire into stage-actions.yaml | New routing field, conditional action sequencing |
| 05 | Update create-openspec-handoff to read technical-specifications/ | Story packages get concrete endpoint/schema detail from specs |
| 06 | Update architecture-review skill to seed integration list | Architecture review identifies which integrations need specs |

## Scope Boundary

- Does NOT migrate existing `quality-gates/api-contract.md` — existing initiatives are unaffected
- Does NOT change validation.py yet — validator extension is a follow-on
- Does NOT touch story-package template — enrichment comes from step 05
