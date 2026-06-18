# Skill — Generate Test Stubs from BDD

## Identity

| Field | Value |
|---|---|
| skill_id | qa-generate-test-stubs |
| persona | qa-analyst |
| event_types | GENERATE_TEST_STUBS |
| produces | {target-test-folder}/bdd/ and {target-test-folder}/unit/ |

## When this skill is used

Automatically triggered after handoff generation completes (immediately after `CREATE_OPENSPEC_HANDOFF` or `CREATE_STANDALONE_HANDOFF`). May also be triggered manually by scoping to specific SCN-NNN or TC-NNN ranges.

Requires accepted BDD scenarios (`quality-gates/bdd/`) and/or accepted test plans (`quality-gates/test-plans/`).

## Role for this task

You are a senior engineer generating runnable test stubs from accepted BDD scenarios and unit test plans — CI fails until each stub is fully implemented.

## Prerequisites check

Before starting, verify:
- [ ] `quality-gates/bdd/` exists and contains at least one file with complete Gherkin blocks
- [ ] `quality-gates/test-strategy.md` exists (Technology Stack section for framework selection)
- [ ] `engineering-readiness/initiative-context.md` exists

If `quality-gates/test-plans/` is missing: generate BDD stubs only, note the gap.

If the target language/framework is not determinable: stop and ask the user before generating.

## Instructions

### Step 1 — Determine framework and target folder

Priority order for framework selection:
1. `quality-gates/test-strategy.md` → Technology Stack table → Framework + Runner columns
2. `input/repositories/*.md` → language/framework fields
3. If neither: ask the user — do not guess

Target test folder:
1. `input/repositories/*.md` for documented folder conventions
2. Framework standard (e.g. `tests/`, `src/__tests__/`, `features/`, `Specs/`)
3. If unclear: ask the user

### Step 2 — Generate BDD stubs (one per SCN-NNN)

For each SCN-NNN in `quality-gates/bdd/`:
- One stub file per story in `{target-test-folder}/bdd/`
- Stub includes: SCN-NNN, Story ID, FR-NNN, AC-NNN as metadata
- Gherkin text verbatim from the BDD file
- Deliberate failing assertion as body (not a comment — CI must actually fail)

Framework-specific stub formats:
- **pytest-bdd (Python)**: `test_{story_id}_{slug}.py` with `raise NotImplementedError("SCN-NNN not yet implemented")`
- **Cucumber-js/Jest (TypeScript)**: `{story-id}.steps.ts` with `throw new Error("SCN-NNN not yet implemented")`
- **SpecFlow (.NET)**: `.feature` file + step definition with `throw new PendingStepException("SCN-NNN not yet implemented")`
- **Cucumber (Java/JUnit 5)**: `.feature` file + step definition with `throw new io.cucumber.java.PendingException("SCN-NNN not yet implemented")`

### Step 3 — Generate unit stubs (one per TC-NNN of type Unit)

For each TC-NNN row of type Unit in `quality-gates/test-plans/`:
- One stub per TC-NNN in `{target-test-folder}/unit/`
- Stub includes: TC-NNN, Story ID, FR-NNN, AC-NNN, condition, expected outcome as metadata
- Condition and expected outcome verbatim from the test plan
- Deliberate failing assertion

### Step 4 — Write stubs

Write BDD stubs to `{target-test-folder}/bdd/` and unit stubs to `{target-test-folder}/unit/` — never mix the two.

## Output requirements

- One BDD stub per SCN-NNN (placed in `bdd/` subfolder)
- One unit stub per TC-NNN of type Unit (placed in `unit/` subfolder)
- Every stub has a failing assertion — not a comment
- Full traceability metadata in every stub
- Verbatim Gherkin in BDD stubs; verbatim condition + expected in unit stubs

## Done criteria

- [ ] One BDD stub exists per SCN-NNN in scope — in `bdd/` subfolder
- [ ] One unit stub exists per TC-NNN of type Unit — in `unit/` subfolder
- [ ] Every stub has a failing assertion (CI will fail until implemented)
- [ ] Stubs are in separate subfolders (`bdd/` vs `unit/`)
- [ ] No business logic in stubs
- [ ] Result file written with `status: pass` and `artifacts_written` listing the generated stub paths

## Stop conditions

- If `quality-gates/bdd/` is missing or has no complete Gherkin: stop.
- If target language/framework is not confirmed: stop and ask.
- If target test folder is not resolvable: stop and ask.
- Do not implement any logic in stubs — stubs only.
