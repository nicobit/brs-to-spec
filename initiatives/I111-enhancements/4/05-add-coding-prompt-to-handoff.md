# Enhancement 5 — Add coding-prompt.md to Handoff

## Problem

The OpenSpec handoff produces three files per story folder: `story.md`, `design.md`, `tasks.md`. A coding agent receiving this package must:
- Read all three files
- Infer which business rules constrain this specific story
- Infer which architecture rules apply
- Interpret AC-NNN references back to the BRS to understand what testable means
- Construct their own definition of done

This inference work is error-prone. The agent may miss a BR-NNN rule buried in a different file, misinterpret a vague AC, or not know which BDD scenarios they must make pass.

The fix is a synthesis file — `coding-prompt.md` — that aggregates the constraints from all three files into a single, directly usable artifact. It adds no new information; it is a targeted summary for the coding agent.

## What needs to change

### Change 1 — `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`

**Add to the Inputs section (before Step 1):**

```
Additional inputs required for coding-prompt.md generation (read after reading all other inputs):
- `business-intake/business-rules.md` — BR-NNN rules; filter to rules that apply to this story
- `quality-gates/bdd/F-NNN.md` (if triggered) — SCN-NNN scenario IDs that this story must make pass
```

**Add to the story folder generation rules (after the tasks.md section):**

```
### 4. coding-prompt.md (mandatory — generate for every story folder)

Generate `coding-prompt.md` last, after `story.md`, `design.md`, and `tasks.md` are complete for this story.

This file is a synthesis artifact. Do not add new information — aggregate from the files already written.

**File structure:**

---
Story: F-XXX.X — <story name>
---

## Goal

One sentence. Copy the "so that" clause from story.md and make it the agent's objective.
Example: "Enable an applicant to submit a personal loan application and receive an application reference number."

## Business rules that constrain this story

List every BR-NNN rule from `business-intake/business-rules.md` whose "impacted features/stories" column includes this story's F-XXX.X ID.

Format:
| Rule | Text | Enforcement |
|---|---|---|
| BR-005 | DTI ratio must not exceed 43% for automatic approval | Reject application at scoring step; return 422 with reason |

If no BR-NNN rules apply to this story: write `No business rules constrain this story.` — do not leave the section empty.

## Architecture rules that constrain this story

List every AR-NNN rule from `architecture/architecture-rules.md` that is relevant to this story's scope (from the story's constraints table in story.md).

Format:
| Rule | Text | Applies to |
|---|---|---|
| AR-002 | All PII must be encrypted at rest using AES-256 | LoanApplication entity storage |

## Acceptance criteria (testable)

Copy the AC-NNN acceptance criteria from story.md and rewrite each as a verifiable statement if not already in that form.

Format:
| AC | Verifiable statement |
|---|---|
| AC-003 | POST /applications returns 201 with `{ arn }` when all required fields are present and valid |
| AC-004 | POST /applications returns 400 with field-level errors when any required field is missing |

Do not paraphrase — use the exact AC text from story.md; add a testable restatement only when the original is vague.

## BDD scenarios to make pass

If the BDD gate was triggered: list the SCN-NNN IDs from `quality-gates/bdd/F-NNN.md` that correspond to this story's F-XXX.X scenarios.

Format:
- SCN-001: Applicant submits valid application — happy path
- SCN-002: Applicant submits application with missing NI number — validation error

If BDD gate was not triggered: write `BDD gate not triggered for this initiative.`

## Tasks

Copy the task list from `tasks.md` verbatim. Do not summarize or change task scope.

## What you must NOT do

Derive from the AR-NNN forbidden patterns in `architecture/architecture-rules.md` and from the security-review constraints relevant to this story.

Format:
- Do not add business logic inside API controllers (AR-001)
- Do not persist raw Experian report data — store only transientData subset (AR-006, SEC-003)
- Do not create anonymous endpoints — all routes require role-based authorization (AR-003)

## Definition of done

- [ ] All tasks in the Tasks section implemented
- [ ] All AC-NNN acceptance criteria verifiable as stated above
- [ ] All BDD scenarios listed above pass
- [ ] All AR-NNN rules respected — no forbidden patterns introduced
- [ ] All BR-NNN rules enforced in the implemented code
- [ ] No files outside the scope of this story modified
- [ ] Tests added for each AC-NNN
```

**Add to the Step 1 dependency graph generation rules:**

```
The dependency graph preamble must note whether coding-prompt.md was generated for every story folder. If any story folder is missing coding-prompt.md, flag it as incomplete.
```

**Add to the self-review checklist for the handoff skill:**

```
- [ ] Every story folder contains coding-prompt.md
- [ ] Every coding-prompt.md lists at least one BR-NNN row or an explicit "no business rules" statement
- [ ] Every coding-prompt.md lists the SCN-NNN scenarios to pass (or notes gate not triggered)
- [ ] Every coding-prompt.md "What you must NOT do" section has at least one item derived from AR-NNN rules
```

### Change 2 — Add `coding-prompt.md` template

Create a new template at `.brs2spec/templates/openspec-handoff/coding-prompt.md`:

```markdown
---
Story: {{F-XXX.X}} — {{story name}}
Generated: {{date}}
---

# Coding Prompt — {{F-XXX.X}} {{story name}}

## Goal

{{one sentence from story "so that" clause}}

## Business rules that constrain this story

| Rule | Text | Enforcement |
|---|---|---|
| BR-NNN | {{rule text}} | {{how to enforce in code}} |

## Architecture rules that constrain this story

| Rule | Text | Applies to |
|---|---|---|
| AR-NNN | {{rule text}} | {{scope}} |

## Acceptance criteria (testable)

| AC | Verifiable statement |
|---|---|
| AC-NNN | {{testable restatement}} |

## BDD scenarios to make pass

- SCN-NNN: {{scenario title}}

## Tasks

{{copy from tasks.md verbatim}}

## What you must NOT do

- {{forbidden pattern}} ({{AR-NNN or SEC-NNN}})

## Definition of done

- [ ] All tasks implemented
- [ ] All AC-NNN acceptance criteria pass
- [ ] All BDD scenarios listed above pass
- [ ] All AR-NNN rules respected
- [ ] All BR-NNN rules enforced
- [ ] No files outside this story's scope modified
- [ ] Tests added for each AC-NNN
```

### Change 3 — `brs-to-spec-run-workflow.md` Step 3 stage 13 done criteria

Update the done criteria for handoff:

**Current:** `Proposal + design + tasks; dependency-graph.md first; all story folders present; tasks traceable to stories`

**Change to:** `dependency-graph.md first; all story folders present; each folder contains story.md + design.md + tasks.md + coding-prompt.md; tasks traceable to stories; coding-prompt.md lists BR-NNN, AR-NNN, SCN-NNN, and forbidden patterns`

## Implementation steps

1. Open `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`
   - Add `business-intake/business-rules.md` and relevant BDD files to the Inputs list
   - Add the `coding-prompt.md` generation section (section 4) to the story folder rules
   - Add the dependency graph note
   - Add four items to the self-review checklist

2. Create `.brs2spec/templates/openspec-handoff/coding-prompt.md` with the template above

3. Open `.brs2spec/brs-to-spec-run-workflow.md`
   - Update stage 13 done criteria to include coding-prompt.md

## Quality bar

After this change:
- Every story folder in every handoff has a `coding-prompt.md`
- A coding agent can read only `coding-prompt.md` and have everything needed: goal, rules, ACs, scenarios to pass, tasks, forbidden patterns, definition of done
- The file is generated, not hand-written — it costs no extra human effort
- A handoff with missing `coding-prompt.md` files fails the stage 13 done criteria and is regenerated
