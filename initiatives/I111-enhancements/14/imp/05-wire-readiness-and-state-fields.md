# Prompt 05 - Wire Readiness and State Fields

## Context

The new workflow type needs state-level decisions that determine whether
technical specifications are generated early, late, or not at all.

Before making changes, read these files in full:

- `.b2s/artifact-templates/readiness-check.md`
- `.b2s/scripts/b2s_engine/state.py`
- `.b2s/scripts/b2s_engine/next_step.py`
- `framework_enhancement/14/04-contract-mode-and-stage-wiring.md`

## Goal

Extend readiness and state parsing so the new workflow type can drive
technical-spec sequencing cleanly.

## Required work

1. Add the state fields needed by the new workflow type.
2. Parse them from the readiness artifact or another single authoritative
   artifact.
3. Ensure condition evaluation can use those fields without special-case hacks.

## Minimum state fields

- `api_contract_mode`
- any equivalent mode field for data, events, or integrations only if truly
  needed
- do not add separate state fields for everything unless there is a real routing
  need

## Important rule

Use one authoritative decision point for technical-spec timing. Do not scatter
the same sequencing decision across:

- route-initiative
- architecture review
- readiness
- handoff

unless each layer has a clearly different responsibility.

## Preferred responsibility split

- architecture review:
  recommendation only
- readiness:
  operational decision used by workflow conditions
- state parsing:
  authoritative extraction into machine-readable fields

## Done criteria

- [ ] Required state fields are parsed from an authoritative artifact
- [ ] Workflow conditions can use those fields cleanly
- [ ] The decision model is documented and not duplicated ambiguously
