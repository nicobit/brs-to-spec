# Skill - Resolve Epic Open Questions

## Identity

```text
skill_id:    delivery-lead.resolve-epic-open-questions
persona:     delivery-lead
action_id:   resolve-epic-open-questions
produces:    epics/
```

## When this skill is used

Run after `create-epic-shells` for the current epic and before `create-epic-stories`.

This skill identifies unresolved blocking questions for the current epic and produces a human-readable clarification request. Human answers are captured separately in `input/clarifications/{current_item}.yaml`.

## Role for this task

You are a senior delivery lead surfacing only the clarifications that matter for the current epic. Your job is to make the blocker set small, specific, and actionable.

## Per-item execution

This action runs once per epic. The engine provides `{current_item}` (the epic ID) and `{item_folder}` (the resolved epic folder path, e.g. `epics/E-002-ai-pre-screening-scoring/`).

**Always use `{item_folder}` for file paths.** Never construct the folder path from `{current_item}` — the folder includes a slug that only the engine knows.

- Produce a clarification request ONLY for that one epic
- Do not ask questions for other epics
- Do not answer questions yourself

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If `computed_inputs` is present, read every path listed there. Use computed epic context and clarification context as authoritative scope filters.

## Hard constraints

- Create `clarification-request.md` only inside the current epic folder
- Include only unresolved blocking questions relevant to the current epic
- Do not invent questions that are not present in upstream artifacts
- Exclude questions already answered in `input/clarifications/{current_item}.yaml`
- If no unresolved blocking questions remain, write the explicit no-blockers text
- Do not modify `implementation-contract.md`
- Do not modify the clarification input file

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
If `computed_inputs` is present, read every path listed there in full.

Critical reads:
- current epic `implementation-contract.md`
- `architecture/ui-specification.md`
- computed epic context
- computed clarification context, when present

### Step 2 - Identify relevant blockers

For the current epic only, identify unresolved blockers that prevent safe story generation.

Sources of blockers include:
- `## Open Design Questions` in the current epic contract
- `Blocking dependencies` carried from the initiative UI specification
- unresolved UI questions (UIQ-NNN) tied to pages or routes owned by this epic

Ignore:
- questions already answered in the clarification input for this epic
- non-blocking advisory questions
- blockers that belong only to another epic

### Step 3 - Write the clarification request

Create `{item_folder}clarification-request.md` using `.b2s/artifact-templates/epic-clarification-request.md`.

If blockers remain:
- write a short summary explaining why story generation is blocked
- populate the Blocking Questions table
- keep each row concise and specific
- classify each row with exactly one `Blocker Type`:
  - `missing-evidence`
  - `missing-decision`
  - `missing-ownership`
  - `missing-user-intent`
- make `Why It Matters Now` specific to the current epic
- make `Blocks Next Artifact` explicit so the pause reason says what cannot be generated safely

If no blockers remain:
- write the explicit text:

```text
No blocking questions require clarification for this epic.
```

### Step 4 - Final self-check

Before finalizing, verify:
- every question listed is relevant to the current epic
- no answered question is repeated as unresolved
- every question explains why the answer is needed
- every question has the correct blocker taxonomy
- every question names the next artifact blocked by the missing answer
- the answer location references `input/clarifications/{current_item}.yaml`

## Output requirements

Write:

```text
{item_folder}clarification-request.md
```

## Done criteria

- [ ] Clarification request exists for the current epic
- [ ] Only unresolved blocking questions for this epic are listed
- [ ] Already answered questions are excluded
- [ ] If no blockers remain, the explicit no-blockers text is present
- [ ] Answer instructions point to `input/clarifications/{current_item}.yaml`
- [ ] No placeholder text remains

## Stop conditions

- If the current epic folder does not yet exist, stop and report the blocker
- If `implementation-contract.md` does not exist for the current epic, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes one clarification request per current epic
- Validation and state updates are handled by the `.b2s` engine
