# Prompt 09 - Architecture Review Gate

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/routing/routing-decision.md`
- `initiatives/<id>-<slug>/input/brs.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/business-analysis/gaps-and-questions.md`
- `initiatives/<id>-<slug>/input/architecture.md`

## Output file to create

- no framework artifact is created in this step

## Prompt for Office 365 Copilot

You are supporting the `.b2s` architecture review gate.

Review the provided `architecture-review.md` against the business intake,
routing decision, BRS, and any available architecture context. Do not rewrite
the artifact unless a concrete issue is found.

Produce a review note with these sections:

- Overall gate recommendation: `Approve` or `Needs changes`
- Missing or weak fit analysis
- Missing constraints or weak rationale
- Brownfield impact gaps
- Open decisions that lack owners or default assumptions
- Active assumptions that do not state `If False, Then`
- Quality attribute coverage gaps
- Confidence level

Approval rules:

- approve only if the architecture review is specific enough to act as the
  authority artifact for downstream planning
- recommend changes if the review is too generic, misses material constraints,
  or leaves unowned architectural uncertainty

If the recommendation is `Needs changes`, list the minimum concrete fixes
required before delivery structure generation.
