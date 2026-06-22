# Prompt 06 - Add Missing Enterprise Coverage as Additive Actions

## Context

The current framework already covers a lot, but there are still a few places
where the action model can be strengthened using additive workflow steps rather
than framework replacement.

This prompt focuses on two especially valuable additions:

- explicit NFR assessment
- explicit AI coding handoff

## Step 1 - Read the current planning, readiness, and handoff actions

Read in full:

- `.b2s/workflow/stage-actions.yaml`
- current quality-gate and handoff skill prompts relevant to readiness,
  observability, security, and handoff

Understand what already exists before adding anything new.

Before implementing any new action, write a short decision note that lists:

- existing actions that partially cover the need
- exact gaps that remain
- whether the right move is `extend-existing-action` or `add-new-action`

Do not proceed until that decision is explicit.

## Step 2 - Add an NFR assessment action

Only add a new action if the decision note shows that extending an existing
quality-gate or readiness action would make the workflow less clear.

- action intent: produce `nfr-assessment.md`

Inputs should typically include:

- requirements
- architecture review
- architecture rules
- readiness signals where useful

Policies should typically include:

- security
- availability
- performance
- regulatory

The artifact should explicitly cover:

- security
- availability
- resiliency
- observability
- supportability
- scalability
- compliance

## Step 3 - Add an AI coding handoff action

Only add a dedicated handoff action if the decision note shows that extending an
existing handoff artifact would create an overloaded or ambiguous output.

Inputs should typically include:

- stories or delivery structure
- BDD
- architecture review
- architecture rules
- API or data contracts
- NFR assessment

Policies should typically include:

- coding constraints
- testing expectations
- AI handoff constraints

The output should provide:

- business context
- technical context
- constraints
- acceptance criteria
- test expectations
- likely impacted files or areas

## Step 4 - Keep stage placement pragmatic

Place new actions where they fit the existing model best. Do not rearrange the
whole workflow unless absolutely necessary.

Preferred approach:

- NFR assessment in quality gates or readiness-adjacent flow
- AI coding handoff in handoff

If an existing action is extended instead of adding a new one, keep the same
stage placement and document the artifact contract change clearly.

## Step 5 - Add templates and prompts

Create the needed template and skill files for any new action introduced.

Keep them aligned with the richer action contract from earlier prompts:

- policy-aware
- template-driven
- validation-friendly

If you extend an existing action instead of adding a new one:

- update the existing template carefully
- update validation rules accordingly
- avoid producing two overlapping artifacts with nearly the same purpose

## Done criteria

- [ ] enterprise gaps are addressed with additive actions
- [ ] no existing action is removed
- [ ] new artifacts have templates and skill prompts
- [ ] new actions declare inputs, policies, validation, and gates clearly
