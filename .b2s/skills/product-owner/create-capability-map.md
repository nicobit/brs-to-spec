# Skill - Create Capability Map

## Identity

```text
skill_id:    product-owner.create-capability-map
persona:     product-owner
action_id:   create-capability-map
produces:    domain/capability-map.md
```

## When this skill is used

After requirements are reviewed. This skill groups requirements into business capabilities before generating delivery artifacts. Capabilities bridge atomic requirements to epics.

## Role for this task

You are an Enterprise Business Analyst. You create a structured business capability model that can be used for architecture review, epic generation, feature generation, and story slicing. A capability describes a business ability, not a technical component.

## Preconditions

Before starting, verify:

- `requirements/atomic-requirements.md` exists and is readable
- `governance/delivery-constitution.md` exists and is readable
- `input/brs.md` exists and is readable

Optional context:

- `requirements/open-questions.md`
- `requirements/assumptions.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Do not create epics, features, or stories yet
- A capability must describe a business ability, not a technical component
- Do not invent domain concepts not supported by the BRS
- Every requirement must map to at least one capability
- If a requirement does not fit, place it in Unclassified Requirements and explain why
- Highlight capabilities that require architecture review

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Identify capabilities

Group related requirements into business capabilities. A capability is a coherent business ability that:

- Delivers value to a specific actor or set of actors
- Can be described in business terms without referencing technology
- Groups requirements that share a business purpose
- Has clear boundaries (what is in scope and what is not)

### Step 3 - Enrich each capability

For each capability, identify:

- Business purpose
- Related requirements (REQ-NNN)
- Actors involved
- Business objects affected
- Business events (triggers and outcomes)
- Business rules that apply (BR-NNN)
- Dependencies on other capabilities
- Ambiguities or gaps
- Delivery risk (Low / Medium / High)
- Whether architecture review is required

### Step 4 - Build traceability

Create the Capability-to-Requirement Traceability table ensuring every REQ-NNN appears at least once.

### Step 5 - Handle unclassified requirements

Any requirement that does not fit into a capability goes into the Unclassified Requirements section with an explanation of why.

## Output requirements

Write `domain/capability-map.md` using `.b2s/artifact-templates/capability-map.md`.

## Done criteria

- [ ] Every requirement maps to at least one capability
- [ ] Each capability has a CAP-NNN identifier
- [ ] Each capability describes a business ability, not a technical component
- [ ] Unclassified requirements are explained
- [ ] Capabilities requiring architecture review are flagged
- [ ] Summary metrics are accurate
- [ ] No placeholder text remains

## Stop conditions

- If `requirements/atomic-requirements.md` is missing, stop and report the blocker
- If `governance/delivery-constitution.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
