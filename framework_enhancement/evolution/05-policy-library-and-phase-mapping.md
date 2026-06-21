# Prompt 05 - Create a Policy Library and Map It to Phases

## Context

Context policies are the missing first-class piece in the current action model.
This prompt creates a reusable policy library and maps it to the most important
phases without forcing a full rewrite of all skills.

## Step 1 - Create policy folder conventions

Create a structured policy area under `.b2s/` such as:

```text
.b2s/policies/
  business/
  requirements/
  architecture/
  security/
  nfr/
  testing/
  handoff/
```

Add a short README at the top level explaining what a policy file is and how it
differs from a prompt or template.

## Step 2 - Seed core policy documents

Create concise starter policy files for:

- business glossary guidance
- business writing guidelines
- requirement writing standard
- definition of ready
- architecture principles
- technology standards
- security policy
- availability standard
- performance standard
- regulatory standard
- testing expectations
- AI handoff constraints

Keep them short and operational. They are governance inputs, not essays.

## Step 3 - Map policies to representative actions

Add `policy_refs` to a representative set of actions:

- business intake summary
- requirements
- architecture review
- security review or observability-related action
- handoff

Use a small but meaningful set. Do not try to annotate every action in one pass.

## Step 4 - Update prompts carefully

For the representative actions above, update the skill prompts so they consume
policy context explicitly.

The prompts should say things like:

- follow the requirement writing standard
- apply architecture principles
- do not invent requirements beyond the source inputs

## Step 5 - Document the phase policy model

Create or update a design note that maps:

- phase
- typical inputs
- typical policies
- target artifact

This should become the human-readable counterpart to the machine action
registry.

## Done criteria

- [ ] a policy library exists under `.b2s/policies/`
- [ ] representative actions reference policy files
- [ ] prompts acknowledge policy context
- [ ] phase-to-policy mapping is documented
