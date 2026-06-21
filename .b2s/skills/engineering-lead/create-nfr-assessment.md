# Skill - Create NFR Assessment

## Identity

```text
skill_id:    engineering-lead.create-nfr-assessment
persona:     engineering-lead
action_id:   create-nfr-assessment
produces:    quality-gates/nfr-assessment.md
```

## When this skill is used

Run this after readiness is accepted and before the implementation handoff is
produced. This is the consolidated enterprise NFR view.

## Role for this task

You are acting as a security architect and SRE reviewer producing the
cross-cutting non-functional assessment for engineering delivery.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` exists
- `business-analysis/requirements.md` exists
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists

Optional but important:
- `planning/delivery-structure.md`
- `quality-gates/security-review.md`
- `quality-gates/observability-plan.md`
- `quality-gates/api-contract.md`
- `quality-gates/data-contract.md`
- `quality-gates/event-contract.md`

If required inputs are missing, stop and report the blocker instead of
inventing NFRs.

## Instructions

### Step 1 - Read all inputs before writing

Read every path listed in `{resolved_required_inputs}` in full before writing.
If `{resolved_optional_inputs}` contains files that exist, read them too.
Read every policy file listed in `{resolved_policy_inputs}` in full before
producing the assessment.

### Step 2 - Extract explicit NFRs

Create explicit NFR entries with identifiers `NFR-001`, `NFR-002`, and so on.

Each NFR must:
- map to one primary domain
- state the requirement clearly
- include a measurable target or control expectation when the source allows it
- cite its source evidence
- say whether it is blocking before handoff

Do not invent precision that the inputs do not support. If a target is required
but not defined, record that as a gap.

### Step 3 - Cover all core domains

The artifact must explicitly assess:
- security
- availability
- resiliency
- observability
- supportability
- scalability
- compliance

For each domain:
- summarize the expected behaviour or control
- cite evidence from the inputs
- identify gaps or risks
- identify ownership or follow-up

### Step 4 - Produce a delivery decision

Make the NFR decision explicit:
- `Ready for handoff`
- `Ready with NFR risks`
- `Not ready`

A major unresolved security, compliance, resiliency, or operational gap should
prevent a fully ready decision.

### Step 5 - Write the artifact

Write `quality-gates/nfr-assessment.md` using
`.b2s/artifact-templates/nfr-assessment.md`.

## Done criteria

- [ ] the NFR catalog contains typed `NFR-XXX` identifiers
- [ ] all seven core domains are assessed explicitly
- [ ] each domain includes evidence and gaps or risks
- [ ] required follow-ups and owners are listed
- [ ] the final decision is explicit
- [ ] status is `Draft`

## Stop conditions

- If required inputs are missing, stop and report the blocker.
- If the inputs do not support a real decision, produce `Not ready` and list the
  missing evidence as blocking gaps.
