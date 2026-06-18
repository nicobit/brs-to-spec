# Prompt — Generate Test Stubs from BDD Scenarios

## Role

You are a senior engineer generating runnable test stubs from accepted BDD scenarios,
so that CI fails until each scenario is fully implemented.

## Context

This prompt is automatically triggered at stage 13a — immediately after handoff generation (stage 13) completes. It does not require manual invocation.

BDD scenarios are the most durable artifact in the initiative workspace. They survive model upgrades because they are machine-verifiable. This prompt bridges the gap between completed BDD and test-plan markdown files and a CI-executable test suite.

This prompt generates **two categories of stubs**:

1. **BDD stubs (SCN-NNN based)** — one stub per SCN-NNN from `quality-gates/bdd/`, wrapping the Gherkin text verbatim. These operate at acceptance/integration test level and are driven by observable business behavior.

2. **Unit test stubs (TC-NNN based)** — one stub per TC-NNN row of type Unit from `quality-gates/test-plans/`. These operate at unit test level and do not have corresponding Gherkin. They are derived from the test plan's unit test case definitions: business rule branches, boundary values, null inputs, error paths.

Each stub:
- represents one SCN-NNN scenario or one TC-NNN unit test case
- includes the scenario/condition text as a docstring or comment for traceability
- has a deliberate failing assertion as its body — CI must fail until the test is implemented
- is placed in the correct test folder for the target repository

## Inputs

Load in this order:

```text
quality-gates/test-plans/               (primary — TC-NNN unit test cases for unit stubs)
quality-gates/bdd/                      (primary — SCN-NNN scenarios for BDD stubs)
quality-gates/test-strategy.md          (Technology Stack section for framework and runner)
engineering-readiness/initiative-context.md
input/repositories/*.md                 (test folder conventions if present)
```

**Framework and runner selection — in priority order:**

1. Read `quality-gates/test-strategy.md` → Technology Stack table → Backend or Frontend row → Test framework + Test runner columns. Use this if populated.
2. Read `input/repositories/*.md` → infer from language/framework fields (e.g. TypeScript + NestJS → Jest; C# + .NET → xUnit or SpecFlow; Python → pytest-bdd).
3. If neither source has the answer, ask the user to confirm:
   - Python → pytest-bdd (BDD stubs) + pytest (unit stubs)
   - Java → Cucumber / JUnit 5 (BDD stubs) + JUnit 5 (unit stubs)
   - JavaScript / TypeScript → Cucumber-js or Jest (BDD stubs) + Jest / Vitest (unit stubs)
   - C# / .NET → SpecFlow (BDD stubs) + xUnit or NUnit (unit stubs)
   - Other → ask the user to specify

**Unit test framework:** use the same language runtime as the BDD framework. If unit tests use a different runner from BDD (e.g. xUnit for unit, SpecFlow for BDD), use each in its correct category.

**Target test folder — in priority order:**

1. Read `input/repositories/*.md` for folder conventions if documented.
2. Infer from framework standard (e.g. `tests/`, `src/__tests__/`, `features/`, `Specs/`).
3. If unclear, ask the user.

**Scope** — by default: all stories in the handoff just generated. When invoked manually: all scenarios or a specific subset by SCN-NNN / TC-NNN range or story group.

## Output path

Place generated stubs in the target test folder, split by category:

```text
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
```

## Required output per scenario

### pytest-bdd (Python)

```python
# SCN-NNN — [Scenario name]
# Story: [Story ID] | Requirement: [FR-NNN] | AC: [AC-NNN]
#
# Given [...]
# When [...]
# Then [...]

import pytest

@pytest.mark.bdd
def test_scn_NNN_scenario_slug():
    """
    SCN-NNN: [Scenario name]
    Given [...]
    When [...]
    Then [...]
    """
    raise NotImplementedError("SCN-NNN not yet implemented")
```

### Cucumber (Java / JUnit 5)

```java
// SCN-NNN — [Scenario name]
// Story: [Story ID] | Requirement: [FR-NNN] | AC: [AC-NNN]

Feature: [Story name]

  Scenario: [Scenario name]  # SCN-NNN
    Given [...]
    When [...]
    Then [...]
```

Step definition stub:

```java
@Given("[...]")
public void given_step() {
    // SCN-NNN — not yet implemented
    throw new io.cucumber.java.PendingException("SCN-NNN not yet implemented");
}
```

### Cucumber-js / Jest (TypeScript)

```typescript
// SCN-NNN — [Scenario name]
// Story: [Story ID] | Requirement: [FR-NNN] | AC: [AC-NNN]

describe("[Story name]", () => {
  it("SCN-NNN — [Scenario name]", () => {
    // Given [...]
    // When [...]
    // Then [...]
    throw new Error("SCN-NNN not yet implemented");
  });
});
```

### SpecFlow (.NET)

```gherkin
# SCN-NNN — [Scenario name]
# Story: [Story ID] | Requirement: [FR-NNN] | AC: [AC-NNN]

Feature: [Story name]

  Scenario: [Scenario name]
    Given [...]
    When [...]
    Then [...]
```

Step definition stub:

```csharp
[Given("...")]
public void GivenStep()
{
    // SCN-NNN — not yet implemented
    throw new PendingStepException("SCN-NNN not yet implemented");
}
```

## Unit test stub output examples

### Python (pytest)

```python
# TC-NNN — [test case name]
# Story: [F-XXX.X] | Requirement: [FR-NNN] | AC: [AC-NNN]
# Condition: [condition from test plan]
# Expected: [expected outcome from test plan]

def test_tc_NNN_slug():
    """
    TC-NNN: [test case name]
    Condition: [condition]
    Expected: [expected outcome]
    """
    raise NotImplementedError("TC-NNN not yet implemented")
```

### TypeScript (Jest / Vitest)

```typescript
// TC-NNN — [test case name]
// Story: [F-XXX.X] | Requirement: [FR-NNN] | AC: [AC-NNN]
// Condition: [condition] | Expected: [expected outcome]

describe("[class / function name]", () => {
  it("TC-NNN — [test case name]", () => {
    // Condition: [condition]
    // Expected: [expected outcome]
    throw new Error("TC-NNN not yet implemented");
  });
});
```

### C# (xUnit)

```csharp
// TC-NNN — [test case name]
// Story: [F-XXX.X] | Requirement: [FR-NNN] | AC: [AC-NNN]

[Fact]
public void TC_NNN_SlugName()
{
    // Condition: [condition]
    // Expected: [expected outcome]
    throw new NotImplementedException("TC-NNN not yet implemented");
}
```

### Java (JUnit 5)

```java
// TC-NNN — [test case name]
// Story: [F-XXX.X] | Requirement: [FR-NNN] | AC: [AC-NNN]

@Test
void tc_NNN_slugName() {
    // Condition: [condition]
    // Expected: [expected outcome]
    throw new UnsupportedOperationException("TC-NNN not yet implemented");
}
```

## Rules

- Generate one BDD stub per SCN-NNN — do not merge scenarios
- Generate one unit stub per TC-NNN row of type Unit in the test plan — do not merge test cases
- Every stub must have a deliberate failing assertion or pending exception as its body — not a comment
- BDD stubs: include the Gherkin text verbatim from the BDD scenarios file — do not paraphrase
- Unit stubs: include the condition and expected outcome verbatim from the test plan TC-NNN row
- BDD stubs: include SCN-NNN, Story ID, FR-NNN, AC-NNN as metadata
- Unit stubs: include TC-NNN, Story ID, FR-NNN, AC-NNN, condition, expected outcome as metadata
- BDD stubs go in `<target-test-folder>/bdd/` — unit stubs go in `<target-test-folder>/unit/`
- Do not implement any logic — stubs only
- Do not skip NFR scenarios — generate BDD stubs for them too
- Do not skip C1 unit test cases — generate unit stubs for all TC-NNN rows of type Unit regardless of criticality

## Quality bar

A good stub generation pass must:

- produce one BDD stub per SCN-NNN in scope (in `bdd/` subfolder)
- produce one unit stub per TC-NNN of type Unit in scope (in `unit/` subfolder)
- include verbatim Gherkin text in BDD stubs; verbatim condition + expected outcome in unit stubs
- have a failing assertion in every stub — CI must fail until the test is implemented
- include full traceability metadata in every stub
- place files in the correct subfolders (`bdd/` vs `unit/`)

## Anti-patterns to avoid

- Do not implement any business logic in the stubs
- Do not skip scenarios or test cases because they seem complex
- Do not merge multiple SCN-NNN into one test function
- Do not merge multiple TC-NNN into one test function
- Do not use placeholder comments instead of failing assertions — CI must actually fail
- Do not place unit stubs in the `bdd/` folder or BDD stubs in the `unit/` folder

## Stop conditions

- If `quality-gates/bdd/` is missing or has no complete Gherkin blocks, stop. Stubs can only be generated from accepted scenarios with full Given/When/Then blocks.
- If `quality-gates/test-plans/` is missing or empty, unit stubs cannot be generated — generate BDD stubs only and note the gap.
- If the target language or framework is not confirmed, stop and ask before generating.
- If the target test folder path is not resolvable from framework artifacts, stop and ask: "Test stubs are ready to generate. What is the path to the application repository's test folder?"

## Self-review checklist

Before finalizing, verify:

- [ ] One BDD stub exists per SCN-NNN in the requested scope — placed in `bdd/` subfolder
- [ ] One unit stub exists per TC-NNN of type Unit in the test plans in scope — placed in `unit/` subfolder
- [ ] Every BDD stub has a failing assertion (not just a comment) and verbatim Gherkin text
- [ ] Every unit stub has a failing assertion and verbatim condition + expected outcome from test plan
- [ ] Traceability metadata (SCN-NNN or TC-NNN, Story ID, FR-NNN, AC-NNN) is present in every stub
- [ ] NFR scenarios are included in BDD stubs
- [ ] C1 unit test cases are included in unit stubs
- [ ] BDD stubs and unit stubs are in separate subfolders
