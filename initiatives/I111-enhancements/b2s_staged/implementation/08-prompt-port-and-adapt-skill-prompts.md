# Prompt 08 - Port and Adapt Skill Prompts

## Goal

Reuse `.brs2spec2` skill prompts for `.b2s` artifact generation, adapted for
staged orchestration.

## Files to create

Create `.b2s/skills/...` by porting the `.brs2spec2` prompts needed for the
first implementation slice.

## Adaptation rules

- keep artifact-generation instructions
- keep quality bar and done-criteria intent
- remove event/result-file coupling
- remove `.flow/events/` assumptions
- replace `.brs2spec2` references with `.b2s` references
- assume machine-prepared staged inputs rather than event `read_from` semantics
- preserve explicit source-path awareness where prompts rely on concrete artifact references

## Priority prompts

Start with:

- route-initiative
- create-business-intake-summary
- create-requirements
- create-use-case-diagram
- create-delivery-structure
- check-engineering-readiness

## Verification

Verify:

1. prompts still produce `.brs2spec2`-compatible artifacts
2. prompts no longer depend on runtime event files
3. prompts fit the `.b2s` stage-action model
4. prompts still reference concrete source artifacts clearly enough for traceability
