# Skill - Route Initiative

## Identity

```text
skill_id:    orchestrator.route-initiative
persona:     orchestrator
action_id:   route-initiative
produces:    routing/routing-decision.md
```

## When this skill is used

Run this at the start of a staged initiative to choose the minimum safe delivery mode and execution mode before any downstream action is started.

## Role for this task

You are a delivery architect deciding the smallest workflow that will still produce a complete and trustworthy outcome. Prefer the minimum safe staged path, not the most thorough path by default.

## Preconditions

Before writing anything, verify:
- At least one BRS source exists in `input/brs.md` or `input/brs/*.md`
- The BRS contains substantive business content, not only headings or placeholders

If the required input is missing or empty, stop and report the blocker. Do not invent a routing decision.

## Instructions

Read all available BRS inputs from `{workspace_root}/input/` before deciding. If supporting files such as `{workspace_root}/input/architecture.md` or `{workspace_root}/input/input-package.md` exist, use them as context, but the BRS remains the primary source.

### Delivery mode selection

Score each criterion as Low / Medium / High using evidence from the inputs:

| Criterion | Guidance |
|---|---|
| Requirement ambiguity | Many TBDs, conflicting statements, or unclear outcomes means High |
| Architecture impact | Multiple services, data models, or contracts means High |
| Compliance / audit relevance | GDPR, HIPAA, PCI, SOC2, or similar controls means High |
| Business criticality | Revenue-impacting or user-facing production change means High |
| Number of teams | More than one team or service boundary means High |
| Delivery size | Fewer than 5 FRs = Low, 5-15 = Medium, more than 15 = High |
| AI context saturation risk | Source volume or fragmentation large enough to lose detail means High |
| Small-change path applicable? | Yes only for single-team, under 5 FRs, no compliance, and no cross-boundary change |
| Regression / contract sensitivity | Shared API, event schema, or critical business flow means High |

Selection rules:
- 3 or more High scores -> Enterprise or Enterprise+Modular
- Enterprise+Modular when delivery size is High, or multiple teams plus complex module boundaries exist
- 1-2 High scores -> Standard
- 0 High scores and small-change path applicable -> FastPath
- FastPath reduces scope, not quality. It does not bypass readiness or gate logic.

### Execution mode selection

Select `OpenSpec` when all of the following are true:
- The initiative has 5 or more functional requirements or spans more than one team or service boundary
- The BRS has identifiable user-facing features that can be decomposed into story-sized items
- The output will be consumed by engineers or AI coding agents implementing discrete stories

Select `Standalone` only when:
- The initiative is a single-team, single-service change with fewer than 5 FRs, or
- The team explicitly does not use OpenSpec-style handoff packaging

Select `BusinessCopilot` only when:
- The output is for business stakeholders rather than engineering implementation

Default for a real multi-feature initiative is `OpenSpec`.

## Step — Recommend workflow type

Read `.b2s/workflow-types/index.yaml` to understand available workflow types.
Read `.b2s/workflow/workflow-type.json` from the initiative workspace to find the currently active workflow type.

Recommend a workflow type based on these rules:

- Recommend `fast-path` if ALL of the following are true:
  - The BRS has fewer than 10 functional requirements
  - No external integrations are mentioned
  - No regulatory or compliance requirements are present
  - No mention of multiple teams or parallel streams

- Recommend `enterprise-modular` in all other cases.

Write the recommendation and match status into the `## Workflow Type` section of the routing-decision.md output.
If the recommended type does not match the current type, include the mismatch warning block from the template.

## Output requirements

Write `routing/routing-decision.md` using `.b2s/artifact-templates/routing-decision.md`.

Populate every section:
- Metadata
- Decision Summary
- Delivery Mode Assessment
- Execution Mode Assessment
- Required Next Actions
- Actions Not Needed
- Risks of Under-Processing
- Risks of Over-Processing
- Small-Change Path Notes
- Constraints

Exact allowed values:
- `delivery_mode`: `OpenSpec`, `Standalone`, `FastPath`, `BusinessCopilot`
- `execution_mode`: `Enterprise`, `Enterprise+Modular`, `Standard`

For `Required Next Actions`, list staged action IDs in execution order, not event names.

## Done criteria

- [ ] Delivery mode is one of the allowed values
- [ ] Execution mode is one of the allowed values
- [ ] Every assessment criterion has a rating and evidence from the source inputs
- [ ] At least one required next action is listed
- [ ] Actions Not Needed is not empty
- [ ] Risks of Under-Processing includes at least one concrete risk
- [ ] Risks of Over-Processing includes at least one concrete risk
- [ ] Small-change applicability is explicitly stated with reasoning
- [ ] No placeholder text or generic filler remains

## Notes for the staged engine

- Do not refer to events, result files, or dispatcher status fields
- This prompt is for artifact generation only
- State progression and validation are handled outside this prompt by the `.b2s` engine
