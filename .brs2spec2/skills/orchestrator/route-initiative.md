# Skill — Route Initiative

## Identity

```
skill_id:    orchestrator.route-initiative
persona:     orchestrator
event_types: [ROUTE_INITIATIVE]
produces:    routing/routing-decision.md
```

## When this skill is used

Referenced at the start of every new initiative to select the delivery mode and execution mode before any other events are dispatched.

## Role for this task

You are a delivery architect deciding the minimum safe process for this initiative. Your job is to select the smallest workflow that will produce a complete, trustworthy result — not the most thorough one by default.

## Prerequisites check

Before doing any work, verify:
- At least one BRS source file exists in `read_from` (input/brs.md or a file matching input/brs/*.md)
- If no BRS input exists: stop. Write result file with `failure_reason: "required input missing: no BRS source file found in input/"`. Do not produce partial output.

## Instructions

Read all available input files. Assess the initiative against the scoring criteria below and select delivery mode and execution mode.

### Delivery mode selection

Score each criterion as Low / Medium / High using evidence from the inputs:

| Criterion | Guidance |
|---|---|
| Requirement ambiguity | How clearly stated are the requirements? Many TBDs or conflicting statements → High |
| Architecture impact | Does this change multiple services, data models, or contracts? → High if yes |
| Compliance / audit relevance | GDPR, HIPAA, PCI, SOC2 mentioned? → High |
| Business criticality | Revenue-impacting or user-facing production change? → High |
| Number of teams | More than one team or service boundary? → High |
| Delivery size | Count distinct functional requirements: <5 = Low, 5–15 = Medium, >15 = High |
| AI context saturation risk | Is the total source text so large it risks losing detail in a single session? → High if yes |
| Small-change path applicable? | Single-team, <5 FRs, no compliance, no cross-boundary changes? → Yes only if all true |
| Regression / contract sensitivity | Does this touch a shared API, event schema, or critical business flow? → High if yes |

**Selection rules:**
- 3+ High scores → Enterprise or Enterprise + Modular
- Enterprise + Modular when: delivery size High OR multiple teams AND complex module boundaries
- 1–2 High scores → Standard
- 0 High scores AND small-change path applicable → Fast Path
- Fast Path does not skip readiness or gate triggers — it reduces scope, not quality

### Execution mode selection

Select **OpenSpec** when ALL of the following are true:
- The initiative has ≥5 functional requirements OR spans more than one team / service boundary
- The BRS has identifiable user-facing features that can be broken into `F-NNN.N` user stories
- The output will be consumed by engineers or AI coding agents implementing discrete stories

Select **Standalone** only when:
- The initiative is a single-team, single-service change with fewer than 5 FRs, OR
- The team explicitly does not use OpenSpec tooling and needs a flat task list

Select **BusinessCopilot** only when:
- The output is for a business user or non-technical stakeholder, not for engineers

**Default for a new initiative with a real BRS (≥5 FRs, multiple features): OpenSpec.** "Do not make OpenSpec the default" means: do not blindly apply it to trivial changes — not that Standalone is preferred for substantial initiatives.

### Output constraints

- Do not give a decision without evidence for each criterion
- Do not leave any criterion blank without a stated reason
- State uncertainty explicitly with its impact on downstream events
- Explicitly list which next events are required and which are excluded, with reasons

## Output requirements

Write `routing/routing-decision.md` using the structure from `artifact_template_ref`. All sections must be populated:

- **Metadata**: initiative_id, created_at, created_by (orchestrator)
- **Decision Summary**: delivery_mode, execution_mode, small-change path applicable — all with reason and confidence
- **Delivery Mode Assessment**: one row per criterion, all nine criteria scored with evidence
- **Execution Mode Assessment**: OpenSpec / Standalone / BusinessCopilot row for each — recommended one, reasons for others
- **Required Next Events**: which event templates are triggered, in order
- **Events Not Needed**: which event templates are excluded and why
- **Risks of Under-Processing**: at least one concrete risk
- **Risks of Over-Processing**: at least one concrete risk
- **Small-Change Path Notes**: applicable or not, with reasoning

The `delivery_mode` field value must be exactly one of: `OpenSpec`, `Standalone`, `FastPath`, `BusinessCopilot`
The `execution_mode` field value must be exactly one of: `Enterprise`, `Enterprise+Modular`, `Standard`

## Done criteria

- [ ] `delivery_mode` is present and is one of the four allowed values
- [ ] `execution_mode` is present and is one of the three allowed values
- [ ] Every scoring criterion has a Low/Medium/High rating AND evidence from the source inputs (not generic statements)
- [ ] `Required Next Events` section lists at least one event
- [ ] `Events Not Needed` section exists and is not empty
- [ ] `Risks of Under-Processing` contains at least one specific risk
- [ ] `Risks of Over-Processing` contains at least one specific risk
- [ ] No placeholder text (TBD / TODO / [fill in]) in the output
- [ ] Small-change path applicability is stated explicitly (Yes or No) with reasoning

## Stop conditions

- No BRS source file found in `read_from` → `failure_reason: "required input missing: no BRS source file found in input/"`
- BRS file exists but is empty or contains only headings → `failure_reason: "required input insufficient: BRS source file has no extractable requirements"`
