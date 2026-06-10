# Prompt — Generate Test Stubs from BDD Scenarios

## Role

You are a senior engineer generating runnable test stubs from accepted BDD scenarios,
so that CI fails until each scenario is fully implemented.

## Context

BDD scenarios are the most durable artifact in the initiative workspace. They survive model
upgrades because they are machine-verifiable. This prompt bridges the gap between a completed
BDD scenarios markdown file and a CI-executable test suite.

Each stub:
- represents one SCN-NNN scenario
- includes the Gherkin text as a docstring or comment for traceability
- has a deliberate failing assertion as its body — CI must fail until the test is implemented
- is placed in the correct test folder for the target repository

## Inputs

Load first:

```text
engineering-readiness/initiative-context.md
quality-gates/bdd-scenarios.md
```

Then confirm with the user:

1. **Target language and test framework** — choose one:
   - Python → pytest-bdd
   - Java → Cucumber (JUnit 5)
   - JavaScript / TypeScript → Cucumber-js or Vitest/Jest with describe/it
   - C# / .NET → SpecFlow
   - Other → ask the user to specify

2. **Target test folder** — where test files should be placed in the repository
   (e.g. `tests/acceptance/`, `src/__tests__/`, `features/`)

3. **Scope** — all scenarios in the file, or a specific subset by SCN-NNN range or story group

## Output path

Place generated stubs in the target test folder specified by the user.
Name each file after the story group or deliverable:

```text
<target-test-folder>/<story-id>_<slug>.feature   (for Gherkin runners)
<target-test-folder>/test_<story-id>_<slug>.py   (for pytest-bdd)
<target-test-folder>/<StoryId>.Steps.cs           (for SpecFlow)
<target-test-folder>/<story-id>.steps.ts          (for Cucumber-js)
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

## Rules

- Generate one stub per SCN-NNN — do not merge scenarios
- Every stub must have a deliberate failing assertion or pending exception as its body
- Include the Gherkin text verbatim from the BDD scenarios file — do not paraphrase
- Include SCN-NNN, Story ID, and Requirement ID as metadata in every stub
- Do not implement any logic — stubs only
- Do not skip NFR scenarios — generate stubs for them too

## Quality bar

A good stub generation pass must:

- produce one stub per SCN-NNN in the scope
- include verbatim Gherkin text from the source file
- have a failing assertion that causes CI to fail until the test is implemented
- include full traceability metadata (SCN-NNN, Story ID, FR-NNN, AC-NNN)
- place files in the correct test folder

## Anti-patterns to avoid

- Do not implement any business logic in the stubs
- Do not skip scenarios because they seem complex
- Do not merge multiple SCN-NNN into one test function
- Do not use placeholder comments instead of failing assertions — CI must actually fail

## Stop conditions

- If `quality-gates/bdd-scenarios.md` is missing or has no complete Gherkin blocks, stop.
  Stubs can only be generated from accepted scenarios with full Given/When/Then blocks.
- If the target language or framework is not confirmed, stop and ask before generating.

## Self-review checklist

Before finalizing, verify:

- [ ] One stub exists per SCN-NNN in the requested scope
- [ ] Every stub has a failing assertion (not just a comment)
- [ ] Gherkin text is verbatim from the source file
- [ ] Traceability metadata is present in every stub
- [ ] NFR scenarios are included
- [ ] Files are placed in the correct test folder
