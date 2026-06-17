# Enhancement Prompt 07 — Make Test Stub Generation Automatic (Stage 13a)

## What this prompt does

1. Edits `.brs2spec/brs-to-spec-run-workflow.md` to add stage 13a (automatic test stub generation after handoff)
2. Edits `.brs2spec/skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md` to:
   - Add `quality-gates/test-plans/` as a primary input
   - Generate unit test stubs from TC-NNN rows of type Unit (not just BDD/integration stubs)
   - Include TC-NNN traceability metadata in every stub
   - Keep the existing BDD-driven stub generation unchanged

---

## File 1: `brs-to-spec-run-workflow.md`

### Add stage 13a to the stage table

After the stage 13 row (Handoff), insert:

```
| 13a | Test stub generation | Target application repository (stubs under test folder) | One stub file per story; stubs exist for all C1 and C2 TC-NNN from test-plan.md; stubs exist for all SCN-NNN from quality-gates/bdd/; every stub has a failing assertion (not a comment); traceability metadata (TC-NNN or SCN-NNN, Story ID, FR-NNN, AC-NNN) in every stub | `skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md` | (13) handoff complete; (9b) BDD accepted; (9f) test plans complete |
```

### Add stage 13a to Step 6 (Execute the next stage)

After the story enrichment inline behavior block, add:

```markdown
### Test stub generation (stage 13a — automatic after handoff)

When the handoff (stage 13) is complete, immediately execute stage 13a without waiting for user input.

**This step is automatic — do not ask the user whether to run it.**

Load `skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md` and execute it with:
- Scope: all stories in the handoff just generated
- Source 1: all `quality-gates/bdd/F-NNN.md` files (generates SCN-NNN-based stubs)
- Source 2: all `quality-gates/test-plans/F-XXX.X-test-plan.md` files (generates TC-NNN unit test stubs for rows where Test type = Unit)
- Target: the application repository path inferred from `input/repositories/*.md` or from `engineering-readiness/initiative-context.md` Technology Stack table

If the target repository path is not resolvable from framework artifacts, stop and ask the user for the path before generating stubs. State: "Test stubs are ready to generate. What is the path to the application repository's test folder?"

After stub generation, update `workflow-state.json`:
- Set `quality-gates/test-stubs` status to `complete` with a note listing the stub files generated
- Set `next_action` to stage 14 (review package) or stop if all stages are complete
```

### Add stage 13a to the hard gate table

```
| Test stub generation (13a) | Handoff (13) complete with all story folders; BDD accepted (9b); test plans complete (9f) |
```

### Add `quality-gates/test-stubs` to the pre-generation check

After the handoff check block, add:

```markdown
**For test stub generation (stage 13a):**
- [ ] `specs/` exists with at least one story folder containing `story.md` — handoff must be complete first
- [ ] `quality-gates/bdd/acceptance-checklist.md` has `Status: Accepted`
- [ ] At least one `quality-gates/test-plans/F-XXX.X-test-plan.md` exists
- [ ] Target test folder is known — read `input/repositories/*.md` or ask the user
- If handoff is incomplete: finish stage 13 first
- If test plans are missing: run stage 9f first
```

---

## File 2: `skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md`

### Update the Context section

Add to the end of the Context section:

```markdown
This prompt is now automatically triggered after handoff generation (stage 13a). It generates
two categories of stubs:

1. **BDD stubs** — one stub per SCN-NNN from `quality-gates/bdd/`, wrapping the Gherkin text.
   These operate at acceptance/integration test level.

2. **Unit test stubs** — one stub per TC-NNN of type Unit from `quality-gates/test-plans/`.
   These operate at unit test level and do not have corresponding Gherkin. They are derived
   from the test plan's unit test cases (business rule branches, boundary values, null inputs,
   error paths).

Both categories produce deliberate failing assertions. CI fails until each is implemented.
```

### Update the Inputs section

Add to the top of the inputs list (before `engineering-readiness/initiative-context.md`):

```markdown
- `quality-gates/test-plans/` — **primary input for unit test stubs**: read all F-XXX.X-test-plan.md files; for every TC-NNN row where Test type = Unit, generate a unit test stub with TC-NNN traceability metadata
```

### Update the Framework and runner selection

Add a note:

```markdown
**Unit test stubs use the same framework as integration/BDD stubs** — derive from
`quality-gates/test-strategy.md` Technology Stack table, specifically the Unit test framework row.
If the unit test framework differs from the BDD runner (e.g. pytest for unit vs pytest-bdd for BDD),
use the unit framework for TC-NNN unit stubs.
```

### Update the Output path section

Replace:
```markdown
Name each file after the story group or deliverable:

\`\`\`text
<target-test-folder>/<story-id>_<slug>.feature   (for Gherkin runners)
<target-test-folder>/test_<story-id>_<slug>.py   (for pytest-bdd)
<target-test-folder>/<StoryId>.Steps.cs           (for SpecFlow)
<target-test-folder>/<story-id>.steps.ts          (for Cucumber-js)
\`\`\`
```

Replace with:

```markdown
Name each file after the story group and stub category:

\`\`\`text
# BDD / acceptance stubs (SCN-NNN based)
<target-test-folder>/bdd/<story-id>_<slug>.feature     (Gherkin runners)
<target-test-folder>/bdd/test_<story-id>_<slug>.py     (pytest-bdd)
<target-test-folder>/bdd/<StoryId>.Steps.cs             (SpecFlow)
<target-test-folder>/bdd/<story-id>.steps.ts            (Cucumber-js)

# Unit test stubs (TC-NNN based)
<target-test-folder>/unit/test_<story-id>_units.py     (pytest)
<target-test-folder>/unit/<StoryId>Tests.cs             (xUnit / NUnit)
<target-test-folder>/unit/<story-id>.unit.test.ts       (Jest / Vitest)
<target-test-folder>/unit/<StoryId>UnitTests.java       (JUnit 5)
\`\`\`
```

### Add unit test stub output examples

After the existing SpecFlow example, add a new section:

```markdown
### Unit test stubs (TC-NNN based — all frameworks)

**Python (pytest):**

\`\`\`python
# TC-NNN — {{test case name}}
# Story: {{F-XXX.X}} | Requirement: {{FR-NNN}} | AC: {{AC-NNN}}
# Condition: {{condition from test plan}}
# Expected: {{expected outcome from test plan}}

import pytest

def test_tc_NNN_{{slug}}():
    """
    TC-NNN: {{test case name}}
    Condition: {{condition}}
    Expected: {{expected outcome}}
    """
    raise NotImplementedError("TC-NNN not yet implemented")
\`\`\`

**TypeScript (Jest / Vitest):**

\`\`\`typescript
// TC-NNN — {{test case name}}
// Story: {{F-XXX.X}} | Requirement: {{FR-NNN}} | AC: {{AC-NNN}}
// Condition: {{condition}} | Expected: {{expected outcome}}

describe("{{class / function name}}", () => {
  it("TC-NNN — {{test case name}}", () => {
    // Condition: {{condition}}
    // Expected: {{expected outcome}}
    throw new Error("TC-NNN not yet implemented");
  });
});
\`\`\`

**C# (xUnit):**

\`\`\`csharp
// TC-NNN — {{test case name}}
// Story: {{F-XXX.X}} | Requirement: {{FR-NNN}} | AC: {{AC-NNN}}

[Fact]
public void TC_NNN_{{SlugName}}()
{
    // Condition: {{condition}}
    // Expected: {{expected outcome}}
    throw new NotImplementedException("TC-NNN not yet implemented");
}
\`\`\`

**Java (JUnit 5):**

\`\`\`java
// TC-NNN — {{test case name}}
// Story: {{F-XXX.X}} | Requirement: {{FR-NNN}} | AC: {{AC-NNN}}

@Test
void tc_NNN_{{slugName}}() {
    // Condition: {{condition}}
    // Expected: {{expected outcome}}
    throw new UnsupportedOperationException("TC-NNN not yet implemented");
}
\`\`\`
```

### Update the Rules section

Add:
```markdown
- Generate one unit test stub per TC-NNN row in scope where Test type = Unit in the test plan
- Unit test stubs must include TC-NNN, Story ID, FR-NNN, AC-NNN, condition, and expected outcome as metadata
- Unit test stubs are placed in the `unit/` subfolder of the target test folder, not in the `bdd/` subfolder
- Do not generate unit test stubs for TC-NNN rows where Test type ≠ Unit — those are validated through BDD stubs or manual testing
```

### Update the Quality bar section

Add:
```markdown
- One unit test stub per TC-NNN row of type Unit in the test plan
- Unit stubs have failing assertions with TC-NNN traceability metadata (TC-NNN, Story ID, FR-NNN, AC-NNN, condition, expected outcome)
- Unit stubs are in the correct `unit/` subfolder
```

### Update the Self-review checklist

Add:
```markdown
- [ ] One unit test stub exists per TC-NNN row of type Unit in all test plans in scope
- [ ] Every unit stub has TC-NNN, Story ID, FR-NNN, AC-NNN, condition, and expected outcome in its metadata
- [ ] Unit stubs are in `unit/` subfolder; BDD stubs are in `bdd/` subfolder
- [ ] No unit stub implements any logic — failing assertion only
```

---

## Self-review after applying

Verify:
- [ ] Stage 13a exists in the workflow runner stage table with prerequisite (13)(9b)(9f)
- [ ] Stage 13a is described as automatic in Step 6 — no user confirmation required
- [ ] Hard gate table has a row for stage 13a
- [ ] Pre-generation check block exists for stage 13a
- [ ] `03-generate-test-stubs-from-bdd.md` has test-plans as a primary input
- [ ] Unit test stub output examples exist for all 4 frameworks
- [ ] Rules include unit stub placement in `unit/` subfolder
- [ ] Self-review checklist covers unit stubs
