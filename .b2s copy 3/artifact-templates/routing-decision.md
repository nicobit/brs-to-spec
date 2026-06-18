# Routing Decision

> Produced by: orchestrator
> Primary consumer: all downstream personas
> Purpose: select the minimum safe staged path for this initiative
> This artifact is immutable after acceptance. Changes require a routing reset or rerun.

## Metadata

| Field | Value |
|---|---|
| Initiative ID | |
| Created at | |
| Created by | orchestrator |
| Status | Draft |

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | OpenSpec \| Standalone \| FastPath \| BusinessCopilot | | |
| Execution mode | Enterprise \| Enterprise+Modular \| Standard | | |
| Small-change path applicable? | Yes \| No | | |

## Delivery Mode Assessment

| Criterion | Score | Evidence from inputs | Impact on decision |
|---|---|---|---|
| Requirement ambiguity | Low \| Medium \| High | | |
| Architecture impact | Low \| Medium \| High | | |
| Compliance / audit relevance | Low \| Medium \| High | | |
| Business criticality | Low \| Medium \| High | | |
| Number of teams | Low \| Medium \| High | | |
| Delivery size | Low \| Medium \| High | | |
| AI context saturation risk | Low \| Medium \| High | | |
| Small-change path applicable? | Yes \| No | | |
| Regression / contract sensitivity | Low \| Medium \| High | | |

## Execution Mode Assessment

| Mode | Available? | Recommended? | Reason |
|---|---|---|---|
| OpenSpec | Yes \| No | Yes \| No | |
| Standalone | Yes \| No | Yes \| No | |
| BusinessCopilot | Yes \| No | Yes \| No | |

## Required Next Actions

| Order | Action ID | Reason required |
|---|---|---|
| 1 | | |

## Actions Not Needed

| Action ID | Reason not needed |
|---|---|
| | |

## Risks of Under-Processing

_Describe what could go wrong if fewer stages or artifacts than recommended are run._

## Risks of Over-Processing

_Describe what overhead is introduced if more work than needed is selected._

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | |
| Minimum required artifacts | |
| Readiness still required? | |
| Gates that still may trigger | |

## Workflow Type

| Field | Value |
|---|---|
| Recommended workflow type | {{enterprise-modular / fast-path}} |
| Rationale | {{one sentence}} |
| Current workflow type | {{read from .b2s/workflow/workflow-type.json}} |
| Match | {{yes / no — yes if recommended == current}} |

### Workflow Type Mismatch Warning

If `Match` is `no`, include this block:

> **Warning:** The initiative was initialised with workflow type `{{current}}` but
> this BRS analysis recommends `{{recommended}}`. To switch workflow type, delete
> this initiative workspace and re-run:
> ```
> python .b2s/scripts/b2s_cli.py init-workspace \
>   --initiative-id {{initiative_id}} \
>   --workflow-type {{recommended}}
> ```
> If you want to continue with the current workflow type, ignore this warning.

## Constraints

_Any routing constraints that apply: team tooling, regulation, timeline, or delivery model limits._

| Constraint | Source | Impact |
|---|---|---|
| | | |
