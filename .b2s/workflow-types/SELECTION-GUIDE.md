# Workflow Type Selection Guide

## Available workflow types

| Workflow type | Best for | Delivery modes |
|---|---|---|
| `enterprise-modular` | Full staged delivery with quality gates and story packages | OpenSpec, Standalone, FastPath |
| `technical-spec-modular` | Same as enterprise-modular + canonical technical specifications produced before story handoff | OpenSpec, Standalone, FastPath |
| `fast-path` | Simple, internal, or low-risk initiatives where full analysis and quality gates are not needed | FastPath only |
| `agile-delivery-flow` | Progressive decomposition with governance, capability mapping, per-story quality gates, and dispatch routing | OpenSpec, Standalone |

## Decision guide

Start here:

**Is the initiative internal, a spike, or a small well-understood change?**
→ Use `fast-path`

**Does the initiative need full business analysis, quality gates, and story packages?**
→ Continue below

**Does the initiative expose an API to external consumers, call external systems
with explicit auth/SLA/retry requirements, or need shared schema specs for
multi-team coordination?**
→ Use `technical-spec-modular`

**Does the initiative need architecture impact mapped per requirement, capability
mapping, per-story quality gates, or explicit dispatch routing?**
→ Use `agile-delivery-flow`

**Otherwise:**
→ Use `enterprise-modular`

## Stage graph comparison

`enterprise-modular`:
```
0-routing → 2-business-intake → 2b-business-analysis → 3-planning
  → 4-engineering-readiness → 4b-quality-gates → 5-handoff → 6-review-package
```

`technical-spec-modular`:
```
0-routing → 2-business-intake → 2b-business-analysis → 3-planning
  → 4-engineering-readiness → 4c-technical-specifications → 4d-quality-gates
  → 5-handoff → 6-review-package
```

`fast-path`:
```
0-routing → 2-business-intake → 3-planning → 5-handoff → 6-review-package
```

`agile-delivery-flow`:
```
0-governance → 1-requirements → 2-domain-analysis → 3-architecture-context
  → 4-architecture-impact → 5-delivery-planning → 6-story-quality-gate
  → 7-bdd-and-testing → 8-handoff → 9-readiness-review → 10-dispatch
```

## Artifact ownership: technical-spec-modular vs enterprise-modular

In `enterprise-modular`, technical detail lives in quality-gate contract files:
- `quality-gates/api-contract.md` — all exposed API contracts in one file
- `quality-gates/data-contract.md` — all data contracts in one file

In `technical-spec-modular`, technical detail is split into per-surface files
under `technical-specifications/`, produced in stage `4c` before quality gates:
- `technical-specifications/api/exposed/` — one file per exposed API surface
- `technical-specifications/api/consumed/` — one file per consumed external API
- `technical-specifications/data/` — one file per data domain
- `technical-specifications/integrations/` — one file per external integration

Legacy flat quality-gate files still exist in `technical-spec-modular` as gate
evidence. `technical-specifications/` is canonical for story-level detail.

## Migration rules

- **Never switch workflow types mid-initiative.** The workflow type is fixed at
  `init-workspace` time. Starting a new workspace is the only supported path to
  adopting a different workflow type.
- **Existing initiatives are unaffected.** Framework Enhancement 14 does not
  change `enterprise-modular` behavior or migrate any existing workspace.
- **Opt-in only.** `technical-spec-modular` must be explicitly selected at
  initialization. No existing workspace is automatically upgraded.
- **Precedence when both sources exist.** If a `technical-specifications/`
  artifact and a `quality-gates/` contract file cover the same surface,
  `technical-specifications/` wins for downstream story and handoff content.
