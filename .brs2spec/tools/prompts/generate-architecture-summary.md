# Prompt — Generate Architecture Summary

## Role

You are a delivery documentation assistant producing a readable, non-technical architecture summary for an active initiative.

## When to use

Run this prompt **ad hoc** when you want a human-readable summary of the architecture constraints, key decisions, and binding rules — written for a mixed audience (business stakeholders, new developers, architects reviewing scope). It is not part of the delivery workflow — run it manually when needed.

It is useful for:
- Onboarding new developers to the governed boundaries
- Architecture review preparation
- Stakeholder briefings on technical constraints
- Post-delivery architecture documentation

## What to read

Read the following from the active initiative workspace. Skip gracefully if a file does not exist.

- `architecture/architecture-review.md` — constraints, open decisions, review outcome
- `architecture/architecture-rules.md` — binding rules with IDs and enforcement
- `input/architecture.md` — source architecture document (for context)
- `engineering-readiness/initiative-context.md` — technology constraints, governed boundaries
- `planning/open-decisions.md` — architecture-related open decisions
- `architecture/diagrams/` — read any `.mmd` (Mermaid) files present; embed them inline in the output verbatim — do not alter the diagram type keyword (`graph TD`, `graph LR`, `architecture-beta`) or any syntax

## Output

Save the output to `docs/initiatives/<initiative-slug>/architecture-summary.md`.

Tell the user the exact path before writing.

## Template

```markdown
# Architecture Summary — [Initiative Name]

> Generated from initiative workspace. Last updated: [date].
> Authoritative sources are `architecture/architecture-review.md` and `architecture/architecture-rules.md`.
> This document is a readable summary — not a replacement for the governed architecture artifacts.

## Review outcome

| Field | Value |
|---|---|
| Review decision | Approved / Approved with conditions / Pending |
| Reviewed by | |
| Date | |
| Key finding | [One sentence] |

## Diagrams

> Include one subsection per diagram file found in `architecture/diagrams/`. Skip if no diagrams exist.

### Component diagram

```mermaid
[paste content of component.mmd verbatim — preserve the diagram type keyword as-is]
```

### Deployment topology

```mermaid
[paste content of deployment.mmd verbatim — preserve the diagram type keyword as-is (may be `graph LR` or `architecture-beta`)]
```

## Technology context

| Area | Detail |
|---|---|
| Platform / runtime | |
| Key frameworks | |
| Database / storage | |
| Infrastructure | |
| Integration points | |

## Binding architecture rules

These rules apply to all implementation work on this initiative. They are enforced at code review.

| Rule ID | Rule | Enforcement | Applies to |
|---|---|---|---|
| AR-NNN | | Code review / CI gate / Architecture review | All / [specific area] |

## Key constraints

Things implementation must respect — derived from the architecture review:

- [Constraint — one sentence each]

## Governed boundaries

Areas where implementation must not cross without explicit sign-off:

| Boundary | What it protects | Consequence of crossing |
|---|---|---|

## Architecture decisions made

| Decision | Answer | Impact on implementation |
|---|---|---|

## Open architecture decisions

| ID | Decision | Owner | Impact if unresolved |
|---|---|---|---|

## What implementation must not do

Explicit prohibitions from the architecture review:

- [Prohibition — one sentence each]
```

## Quality bar

A good architecture summary:
- Lists every AR-NNN rule from `architecture-rules.md` — does not cherry-pick
- Writes constraints and prohibitions in plain language readable by a developer unfamiliar with the initiative
- Does not invent rules or constraints not present in the source artifacts
- Clearly separates binding rules (enforced) from guidance (recommended)
- Notes any open architecture decisions that could affect implementation

## After producing the summary

Tell the user:
1. The file has been saved to `docs/initiatives/<slug>/architecture-summary.md`
2. Re-run after the architecture rules are updated or new decisions are resolved
3. This file is documentation only — the governed rules live in `architecture/architecture-rules.md`
4. Share this file with developers at the start of implementation — it is their constraint reference
5. If this is a new initiative, add its nav block to `mkdocs.yml` under `Initiative Samples:` — see `generate-initiative-summary.md` for the exact block to add.
