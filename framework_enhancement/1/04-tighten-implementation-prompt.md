# Enhancement 4 — Tighten the Implementation Prompt to Be Constraint-Based

## Context

`.brs2spec/8-copilot-implementation/01-implement-one-task.md` is currently a long narrative
prompt (~250 lines) that describes in prose how a coding agent should think about and approach
implementation. This is exactly the artifact type most vulnerable to model drift — a long
prose instruction fed to an LLM produces increasingly variable output as models change.

The article's key insight: the longer and more narrative the execution artifact, the more
interpretation variance accumulates across model versions. Constraint-based prompts
(short rules, structured outputs, machine-verifiable references) are more durable.

Current structure problems:
- Quality bar and anti-patterns are at the bottom — the model reads narrative first
- The prompt describes thinking process ("inspect existing patterns", "provide a short plan")
  rather than stating hard constraints
- Done criteria are prose-based ("implement exactly one task") not ID-anchored
- The self-review checklist doesn't reference BDD scenario IDs
- At 250+ lines of narrative, interpretation variance across model versions is high

## What needs to change

### 1. Restructure `.brs2spec/8-copilot-implementation/01-implement-one-task.md`

Reorder sections so constraints come first:

```
1. Hard constraints (the non-negotiables — short, bullet list)
2. Inputs (what to read, in order)
3. Required output structure (exact markdown template)
4. Done criteria (anchored to SCN-NNN IDs)
5. Process (condensed — 5 steps max)
6. Stop conditions
7. Self-review checklist (updated to include SCN reference check)
```

Remove or condense:
- Long narrative "Context" section — replace with 2 sentences
- "Read before coding" section — merge into Inputs
- Repeated content between "Mandatory rules" and "Anti-patterns" — consolidate into one list
- Verbose "Required process" section — condense to 5 numbered steps

Add:
- **Done criteria section** anchored to BDD scenario IDs:
  ```
  ## Done criteria
  An implementation task is done when:
  - The referenced SCN-NNN scenario(s) pass in CI
  - All required tests are added or updated
  - The implementation summary is written
  If no SCN-NNN is referenced for a task, stop and flag it before implementing.
  ```

Target length: under 120 lines. Current: ~250 lines.

### 2. Apply the same restructuring to `.brs2spec/8-copilot-implementation/02-fix-review-comments.md`

Same principle — move constraints to the top, condense narrative, remove repetition.
Target length: under 80 lines. Current: ~120 lines.

### 3. Update `.brs2spec/9-reviewers/01-senior-code-review.md`

Add a check to the review: "Does the implementation reference at least one SCN-NNN as
its done criterion?" If not, flag it as a gap.

### 4. Update `docs/12-prompt-quality-guidelines.md`

Add a concrete example showing the before/after of a narrative prompt vs a constraint-based
prompt. Use a simplified version of the implementation prompt restructure as the example.

Add the rule: "Constraints first. In execution artifacts, the quality bar and hard rules
must appear before narrative description. The model reads top-down — what it reads first
shapes everything after."

## Implementation steps

1. Read `.brs2spec/8-copilot-implementation/01-implement-one-task.md` in full
2. Rewrite it using the new structure — constraints first, condensed narrative, SCN anchoring
3. Read `.brs2spec/8-copilot-implementation/02-fix-review-comments.md` in full
4. Rewrite it using the same principle
5. Read `.brs2spec/9-reviewers/01-senior-code-review.md` — add SCN reference check
6. Read `docs/12-prompt-quality-guidelines.md` — add constraints-first rule with example

## Quality bar for this enhancement

- The implementation prompt is under 120 lines
- Hard constraints appear before any narrative description
- Every task's done criteria reference at least one SCN-NNN
- A developer reading the prompt understands the hard rules within the first 20 lines
- The self-review checklist includes SCN scenario reference verification
