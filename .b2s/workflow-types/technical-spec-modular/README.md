# Workflow Type: technical-spec-modular

## When to use

Use this workflow for initiatives that require the full staged delivery process
**and** need canonical technical specification artifacts produced before story
handoff. Technical specifications are first-class artifacts here — not embedded
inside quality-gate contract files or re-derived inside each story package.

Choose this workflow when any of the following apply:

- The initiative exposes an API surface consumed by external partners or other
  teams (`api_contract_mode: product` or `coordinated`)
- The initiative calls one or more external systems whose auth, SLA, retry
  policy, and fallback behaviour must be specified and tracked
- Data entities need a shared schema spec (field names, types, constraints, PII)
  that story packages reference rather than invent independently
- Multiple teams share a common technical foundation and need a coordination
  surface for API and integration contracts before stories are written

Suitable for: regulated industries, complex multi-team deliveries, external
integrations requiring design-detail artifacts, initiatives evolving beyond flat
quality-gate contracts.

## When not to use

- Simple or internal initiatives — use `fast-path`
- Initiatives where all API surfaces are purely internal implementation details
  derived from stories — use `enterprise-modular`
- Any initiative already in progress under `enterprise-modular` — do not
  switch workflow types mid-initiative (see Migration boundaries below)

## Stages

```
0-routing
  → 2-business-intake
    → 2b-business-analysis
      → 3-planning
        → 4-engineering-readiness
          → 4c-technical-specifications   ← new in this workflow type
            → 4d-quality-gates
              → 5-handoff
                → 6-review-package
```

Stage `4c-technical-specifications` runs after engineering readiness and before
quality gates. It produces per-surface API specs, data schema specs, and
integration specs. These are **design-detail artifacts** — downstream story
packages and handoff skills read from them rather than re-deriving the same
detail independently.

Stage `4d-quality-gates` corresponds to `4b-quality-gates` in `enterprise-modular`.
The rename signals that gate artifacts in this workflow type are gate evidence,
not the primary source of technical detail.

## Canonical artifact ownership

In `technical-spec-modular`, the following paths are canonical:

| Artifact family | Path | Owner |
|---|---|---|
| Exposed API specs | `technical-specifications/api/exposed/` | `create-exposed-api-specs` |
| Consumed API specs | `technical-specifications/api/consumed/` | `create-consumed-api-specs` |
| Data schema specs | `technical-specifications/data/` | `create-data-schema-specs` |
| Integration specs | `technical-specifications/integrations/` | `create-integration-specs` |

Legacy flat quality-gate contract files (`quality-gates/api-contract.md`,
`quality-gates/data-contract.md`) still exist in this workflow type and are
produced by their respective gate actions. However:

- They serve as **gate evidence** only — not as the source of story-level
  technical detail
- Story packages and handoff artifacts must read from `technical-specifications/`
  when those paths exist, and must not regenerate equivalent detail from scratch
- If both a tech-spec artifact and a legacy contract file exist and conflict,
  the `technical-specifications/` artifact wins

## Quality gates

All quality gates are conditional — triggered only if the engineering readiness
check determines they are needed (BDD, test strategy, security review, API
contract, data contract, event contract, observability plan). This is identical
to `enterprise-modular`.

The engineering readiness check in this workflow type also captures
`api_contract_mode`:

| Mode | Meaning | When to use |
|---|---|---|
| `product` | API is a published surface consumed by external parties | Freeze early; define specs before stories |
| `internal` | API is an implementation detail of this initiative | Derive from story packages; no early freeze |
| `coordinated` | API is shared across teams being built in parallel | Draft specs early; refine after stories confirm shape |

`api_contract_mode` defaults to `internal` when not set. It is stored in
`workflow-state.json` and available to all downstream conditions.

## Prompt placeholder contract

Skill prompts in this workflow type use placeholder-driven path wiring rather
than hardcoded paths. The engine resolves the following placeholders at dispatch
time from the action's declared `inputs` and `outputs`:

| Placeholder | Resolves to |
|---|---|
| `{resolved_required_inputs}` | Bullet list of required input paths that exist on disk |
| `{resolved_optional_inputs}` | Bullet list of optional input paths that exist on disk |
| `{primary_output}` | The action's declared primary output path |
| `{secondary_outputs}` | The action's declared secondary output paths |

Skill prompts must prefer these placeholders over hardcoded paths. Hardcoded
paths in skill text are fragile — they diverge from the stage-action declaration
and are invisible to the input resolver.

## Delivery modes supported

- OpenSpec (full story packages)
- Standalone (standalone handoff document)
- FastPath (compact handoff)

## Migration boundaries

**Existing initiatives** running under `enterprise-modular` are unaffected.
Framework Enhancement 14 does not change `enterprise-modular` behavior, does not
migrate existing `quality-gates/api-contract.md` files, and does not introduce
any `technical-specifications/` folder into workspaces that did not opt in.

**New initiatives** may select `technical-spec-modular` at `init-workspace` time
by passing `--workflow-type technical-spec-modular`. This copies the workflow
type's `stage-actions.yaml` and `workflow-definition.yaml` into the initiative's
`.b2s/workflow/` directory and records the selection in `workflow-type.json`.

**No silent cross-upgrade.** An active initiative's workflow type is fixed at
initialization. To adopt the new workflow type, start a new initiative workspace.
Do not manually copy or overwrite the workflow files of an in-progress initiative.

**Precedence rule.** If an initiative has both a `technical-specifications/`
artifact and a legacy `quality-gates/` contract file covering the same surface:

1. `technical-specifications/` is the source of truth for story-level technical
   detail (endpoint shapes, field names, constraints, auth, SLA, retry policy)
2. `quality-gates/` artifacts serve as gate evidence and are not authoritative
   for downstream story or handoff content
3. Consumers must read `technical-specifications/` first; they may fall back to
   `quality-gates/` only when the `technical-specifications/` path does not exist
