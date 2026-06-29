# Skill - Create Implementation Readiness

## Identity

```text
skill_id:    engineering-lead.create-implementation-readiness
persona:     engineering-lead
action_id:   create-implementation-readiness
produces:    planning/implementation-readiness.md
```

## When this skill is used

Run after coding handoff generation. This is the final implementation-safety review for `b2s-flow` before a coding agent starts work.

## Role for this task

You are the implementation readiness reviewer. You assess whether the generated `b2s-flow` package is safe, coherent, and explicit enough for an AI coding agent to implement without inventing missing architecture or scope.

## Preconditions

Before starting, verify:

- `governance/delivery-constitution.md` exists and is readable
- `requirements/atomic-requirements.md` exists and is readable
- `architecture/architecture-review.md` exists and is readable
- `architecture/impacted-systems.md` exists and is readable
- `architecture/solution-decisions.md` exists and is readable
- `planning/delivery-skeleton.md` exists and is readable
- `planning/fr-coverage.md` exists and is readable
- `epics/` exists and is readable

Optional context:

- `architecture/ui-specification.md`
- `planning/elaboration-plan.md`
- `input/brs.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Be strict. Do not mark an epic ready if key implementation facts are still implied rather than explicit
- Do not silently improve or rewrite upstream artifacts. Report readiness honestly
- A requirement with weak coverage (`Referenced Only`, `Spike Only`) prevents the owning epic from being marked fully ready
- If an external integration, dashboard/UI surface, callback flow, fallback path, or stateful handoff exists but lacks an owning implementation story or precise contract detail, mark the epic partial or blocked
- Every epic must receive an explicit readiness classification: `Ready`, `Partial`, or `Blocked`

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Assess readiness areas

Score these areas using `Ready`, `Partial`, or `Blocked` with concise evidence:

1. **Requirements coverage** - are in-scope requirements truly implemented rather than only referenced or carried by spike stories?
2. **Semantic traceability** - do stories, agent contracts, and coverage claims align without contradictions?
3. **Architecture and solution clarity** - are create-vs-modify decisions, system boundaries, and repository targets explicit?
4. **Implementation contract precision** - do epic contracts specify the APIs, entities, events, UI surfaces, state transitions, and constraints needed for safe coding?
5. **Integration and UI propagation** - are external adapters, callbacks, dashboards, pages, and fallback behavior represented in real implementation stories?
6. **AI handoff quality** - are the epic coding handoffs self-contained and specific enough for a coding agent?

### Step 3 - Classify each epic

For each epic folder under `epics/`:

- classify it as `Ready`, `Partial`, or `Blocked`
- explain the strongest evidence for that rating
- list the most important unresolved gaps
- identify whether the epic is safe for a coding agent now, after small fixes, or only after design clarification

Use these rules:

- `Ready` means the epic can be handed to a coding agent without expecting the agent to invent major scope, architecture, or contracts
- `Partial` means the epic is coherent but still has important gaps that should be fixed before coding
- `Blocked` means the epic still lacks critical information, missing implementation stories, or unresolved design decisions

### Step 4 - Produce the final recommendation

Determine the overall implementation readiness:

- `Ready` if every selected or in-scope coding epic is ready
- `Partially Ready` if some epics are ready but others still need targeted fixes
- `Not Ready` if major architectural, coverage, or handoff gaps remain

Also identify the top fixes that would most improve implementation safety.

## Output requirements

Write `planning/implementation-readiness.md` using `.b2s/artifact-templates/implementation-readiness.md`.

## Done criteria

- [ ] All readiness areas are assessed
- [ ] Every epic has a `Ready` / `Partial` / `Blocked` classification
- [ ] Weak coverage and missing implementation stories are surfaced explicitly
- [ ] The final recommendation is clear and evidence-based
- [ ] Top fixes are prioritized
- [ ] No placeholder text remains

## Stop conditions

- If any required input is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
