# Enhancement 1 — Elevate BDD Scenarios as the Primary Durable Artifact

## Context

The BRS to Spec framework currently produces BDD scenarios in Gherkin format as one of several
quality gate artifacts. However, the framework treats them as documentation — they are written
in markdown, stored in the initiative workspace, but never explicitly connected to a test runner
or CI pipeline.

The article "Stop Writing Specs. Start Writing Facts." makes a key distinction:
- Prose specs are interpreted by LLMs differently on every model version — they are fragile
- Executable assertions (tests, Gherkin scenarios wired to a runner) are model-agnostic and durable

The BDD scenarios template already uses the right language (Given/When/Then, SCN-NNN IDs,
requirement traceability). The gap is that the framework does not:
1. Explicitly state that BDD scenarios are the most durable artifact in the initiative workspace
2. Provide guidance on converting Gherkin blocks into runnable test stubs
3. Connect scenario IDs to task done-criteria in the implementation prompt

## What needs to change

### 1. Update `docs/06-conditional-quality-gates.md`

Add a section that explicitly states the hierarchy of artifact durability:

- BDD scenarios (Gherkin) — most durable: machine-verifiable, model-agnostic
- API / data / event contracts (structured tables) — durable: human-reviewed, stable structure
- Architecture reviews, delivery specs (prose) — least durable: model-interpreted, review on model upgrade

Add a note that BDD scenarios should be written before implementation begins — not after —
because they are the acceptance criterion for each task, not a post-hoc description.

### 2. Add a new prompt: `.brs2spec/quality-gates/generate-test-stubs-from-bdd.md`

This prompt reads the completed BDD scenarios file and produces test stub files in the
target test framework. The user specifies the language and test framework. The stubs:
- Have one test function per SCN-NNN
- Include the Gherkin text as a docstring or comment
- Include the scenario ID and requirement ID as metadata
- Have a failing assertion as the body (so CI fails until the test is implemented)
- Are placed in the correct test folder for the target repository

Supported frameworks to cover: pytest-bdd (Python), Cucumber (Java / JS), SpecFlow (.NET),
Vitest / Jest with describe/it blocks (TypeScript).

### 3. Update `.brs2spec/skills/8-copilot-implementation/01-implement-one-task.md`

Add a rule that every task must reference at least one SCN-NNN from the BDD scenarios file
as its done criterion. The implementation is not complete until the referenced scenario passes.

Add to the self-review checklist:
- [ ] Every implemented behavior is covered by at least one referenced SCN-NNN
- [ ] Referenced BDD scenarios pass (or stubs exist with clear failure reason)

### 4. Update `.brs2spec/templates/templates/quality-gates/bdd-scenarios.md`

Add a header note making the artifact's primary role explicit:
"This is the most durable artifact in the initiative workspace. It survives model upgrades
because it is machine-verifiable. Write it before implementation, not after."

## Implementation steps

1. Read `docs/06-conditional-quality-gates.md` — add artifact durability hierarchy section
2. Read `.brs2spec/templates/templates/quality-gates/bdd-scenarios.md` — add header note
3. Read `.brs2spec/skills/8-copilot-implementation/01-implement-one-task.md` — add SCN reference rule
4. Create `.brs2spec/quality-gates/generate-test-stubs-from-bdd.md` as a new prompt
5. Verify that all cross-references between files are consistent

## Quality bar for this enhancement

- BDD scenarios are clearly positioned as the primary durable artifact in the framework
- A developer reading the framework understands that scenarios must exist before implementation
- The test stub prompt produces runnable (failing) stubs, not placeholder comments
- The implementation prompt anchors every task to at least one scenario ID
