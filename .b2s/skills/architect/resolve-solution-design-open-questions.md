# Skill - Resolve Solution Design Open Questions

## Identity

```text
skill_id:    architect.resolve-solution-design-open-questions
persona:     architect
action_id:   resolve-solution-design-open-questions
produces:    architecture/solution-design-clarification-request.md
```

## When this skill is used

Run after `create-solution-decisions` and before delivery planning begins.

This skill identifies unresolved initiative-blocking questions that prevent safe solution decisions or delivery planning and produces a human-readable clarification request. Human answers are captured separately in `input/clarifications/solution-design.yaml`.

## Role for this task

You are a senior architect surfacing only the clarifications that materially block architectural commitment and delivery planning.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If `computed_inputs` is present, read every path listed there. Use computed clarification context as authoritative human input already provided.

## Hard constraints

- Include only unresolved initiative-blocking questions that prevent safe solution decisions or delivery planning
- Do not invent questions that are not present in upstream artifacts
- Exclude questions already answered in `input/clarifications/solution-design.yaml`
- Exclude epic-blocking and coding-handoff questions that can safely be deferred
- Exclude non-blocking advisory questions
- If no unresolved blocking questions remain, write the explicit no-blockers text
- Do not modify `architecture/solution-decisions.md`
- Do not modify the clarification input file

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
If `computed_inputs` is present, read every path listed there in full.

Critical reads:
- `architecture/solution-decisions.md`
- `architecture/impacted-systems.md`
- `architecture/technical-landscape.md`
- computed clarification context, when present

### Step 2 - Identify blocking solution-design questions

Identify unresolved blockers that prevent safe planning decisions such as:
- target repository ownership
- create-new vs modify-existing ambiguity
- service or data ownership
- integration contract approach
- source-of-truth ambiguity
- cross-application UI ownership
- platform/auth boundary ambiguity

Ignore:
- answered questions already present in the clarification input
- page-level UX detail
- non-blocking advisory questions
- implementation details that can be deferred to epic elaboration

When reading `## Open Solution Design Questions` or `## Open UI Questions`:

- include only rows where `Blocking? = Yes` and `Required Before = delivery-planning`
- exclude rows where `Required Before = epic-elaboration` or `coding-handoff`
- if `Required Before` is missing, use conservative judgment and include the question only when delivery planning is clearly unsafe without the answer

### Step 3 - Write the clarification request

Create `architecture/solution-design-clarification-request.md` using `.b2s/artifact-templates/solution-design-clarification-request.md`.

If blockers remain:
- write a short summary explaining why delivery planning is blocked
- populate the Blocking Questions table
- keep each row concise and specific
- classify each row with exactly one `Blocker Type`:
  - `missing-evidence`
  - `missing-decision`
  - `missing-ownership`
  - `missing-user-intent`
- make `Why It Matters Now` stage-specific rather than generic
- make `Blocks Next Artifact` explicit so the pause reason says what cannot be generated safely

If only epic-blocking or coding-handoff questions remain:
- write the explicit no-blockers text
- do not escalate those deferred questions into this clarification request

If no blockers remain:
- write the explicit text:

```text
No blocking solution design questions require clarification.
```

### Step 4 - Final self-check

Before finalizing, verify:
- every question is truly delivery-planning-blocking
- no answered question is repeated as unresolved
- every question explains why the answer is needed
- every question has the correct blocker taxonomy
- every question names the next artifact blocked by the missing answer
- answer instructions reference `input/clarifications/solution-design.yaml`

## Output requirements

Write:

```text
architecture/solution-design-clarification-request.md
```

## Done criteria

- [ ] Clarification request exists
- [ ] Only unresolved blocking solution-design questions are listed
- [ ] Already answered questions are excluded
- [ ] If no blockers remain, the explicit no-blockers text is present
- [ ] Answer instructions point to `input/clarifications/solution-design.yaml`
- [ ] No placeholder text remains

## Stop conditions

- If `architecture/solution-decisions.md` does not exist, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes one clarification request artifact
- Validation and state updates are handled by the `.b2s` engine
