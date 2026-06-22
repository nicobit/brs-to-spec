# Prompt 14 - Strengthen Upstream `.b2s` Skill Prompts

## Goal

Restore the strongest completeness and anti-skeleton safeguards from
`.brs2spec2` into the key upstream `.b2s` skill prompts while keeping staged
execution semantics.

## Files to modify

- `.b2s/skills/product-owner/create-business-intake-summary.md`
- `.b2s/skills/product-owner/create-requirements.md`
- `.b2s/skills/product-owner/create-use-case-diagram.md`
- `.b2s/skills/engineering-lead/check-engineering-readiness.md`

## Required work

### `create-business-intake-summary.md`

Restore the stronger `.brs2spec2` guidance for:

- full-BRS read before writing
- explicit count-and-compare checks for objectives, FRs, NFRs, and unresolved
  questions
- atomic requirement extraction rules
- separation of answered vs unresolved questions
- explicit stop conditions for:
  - missing BRS
  - empty or heading-only BRS
  - no extractable requirements
- anti-skeleton rules:
  - fail instead of emitting placeholder-only content
  - do not write structure-only output to satisfy validation

### `create-requirements.md`

Restore stronger controls for:

- full input inventory before writing
- stronger conflict handling between BRS and intake summary
- rejection of domain-mismatched generic starter rows
- explicit stop conditions
- stronger normalization guidance so all requirement clusters are captured

### `create-use-case-diagram.md`

Restore stronger breadth and anti-shallow modeling rules:

- scratch mapping step:
  - capability or epic -> candidate goals -> FR coverage
- explicit rule that major FR clusters must be represented or deliberately
  excluded with reason
- explicit handling of system-only FR clusters when they create real business
  outcomes
- explicit failure path when `requirements.md` is suspiciously tiny, generic, or
  domain-mismatched

### `check-engineering-readiness.md`

Restore stronger governance wording:

- explicit stop conditions section
- stronger wording that one blocking issue overrides a high numeric score
- explicit per-gate justification expectations preserved in staged wording

## Constraints

- keep `.b2s` staging semantics
- do not reintroduce `.flow/`, event queue, dispatcher, or result-file
  execution assumptions
- keep the prompts artifact-focused; deterministic pass or fail still belongs to
  the engine

## Verification

Verify:

1. the strengthened `.b2s` prompts are at least as strict as the corresponding
   `.brs2spec2` prompts on completeness
2. no event-queue wording remains
3. stop conditions and anti-skeleton rules are explicit in the key prompts
