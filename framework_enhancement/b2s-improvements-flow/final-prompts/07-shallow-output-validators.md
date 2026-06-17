# Prompt 7 — Validators Against Shallow Story Output

## Context

You are working on the `.b2s` framework at the root of this repository.

The validation engine is in `.b2s/scripts/b2s_engine/validation.py`. It already validates structural artifacts (routing decision, architecture review, readiness check, business intake) using dedicated validators and profile-based checks. The `artifact-package` validation profile handles directory outputs like `specs/`.

Currently the `artifact-package` profile for `create-openspec-handoff` checks that the folder exists and contains files, but it does not check story content quality. A story with "Story 1" as a title and two vague bullet points passes validation.

Your task is to add a dedicated validator for the `specs/` story package output that detects shallow content.

## Step 1 — Add a dedicated story-package validator

Read `.b2s/scripts/b2s_engine/validation.py`.

Understand the existing pattern for dedicated validators. They are registered in `VALIDATORS_BY_ARTIFACT` and called when the artifact path matches.

Add a new dedicated validator function: `_validate_story_package_directory(artifact_path: Path, workspace_root: Path) -> list[dict]`.

This function receives the `specs/` directory path and must:

1. Find all `story.md` files recursively inside `specs/`.
2. For each `story.md`, run the checks listed below.
3. Return a list of check result dicts using the same format as existing validators:
   `{"name": "<check_name>", "result": "pass" | "fail" | "warn", "detail": "<message>"}`

Register it in `VALIDATORS_BY_ARTIFACT`:
```python
"specs/": _validate_story_package_directory,
```

## Step 2 — Story-level checks to implement

Implement the following checks. Each failing check must produce a `"fail"` result with a detail message naming the story file and the specific problem.

### story_has_id
Fail if the story file does not contain a pattern matching `F-\d{3}\.\d+` in the first heading.

### story_has_actor
Fail if the file does not contain the phrase "As a" followed by a non-generic actor name. Generic actors that must fail: "user", "person", "someone", "actor". These are too vague.

### story_has_business_outcome
Fail if the file does not contain "so that" in the user story section.

### story_not_generic_title
Fail if the first heading contains any of: "Story 1", "Story 2", "Implement feature", "Implement functionality", "TBD", "TODO", "{{".

### story_has_requirements_link
Fail if the file contains no reference matching `FR-\d{3}`.

### story_has_acceptance_criteria
Fail if the file has no section matching `## 4. Acceptance Criteria` or contains fewer than 2 lines of content under that section.

### story_has_bdd_scenarios
Fail if the file contains no Gherkin block (no ` ```gherkin ` fence).

### story_bdd_has_then
Fail if any Gherkin block exists but contains no line starting with `  Then` (indented). A scenario without a Then clause is not valid Gherkin.

### story_bdd_not_generic
Warn if any Then clause in a Gherkin block contains only: "it works", "it succeeds", "the feature works", "success", "done". These are vague outcomes.

### story_has_implementation_context
Fail if the file has no section matching `## 6. Implementation Context` or the section contains fewer than 3 lines of content.

### story_has_coding_prompt
Fail if the file has no section matching `## 12. Coding-Agent Prompt`.

### coding_prompt_has_constraints
Fail if the coding-agent prompt section exists but does not contain the word "constraint" or "must not" or "do not touch". A coding prompt without constraints is incomplete.

### coding_prompt_has_tests
Fail if the coding-agent prompt section exists but does not contain the word "test". A coding agent prompt that does not mention tests is incomplete.

### story_no_placeholders
Fail if the file contains any of: `{{`, `}}`, `NNN`, `XXX`, `TBD`, `TODO`, `[actor]`, `[capability]`. These are unfilled template placeholders.

## Step 3 — Add the validator to the dispatch table

Read `VALIDATORS_BY_ARTIFACT` in `validation.py`.

Add the entry:
```python
"specs/": _validate_story_package_directory,
```

Ensure it is called when `action_id == "create-openspec-handoff"` and the primary output is `specs/`.

## Step 4 — Add test fixtures

Create two new test fixtures under `.b2s/tests/fixtures/`:

### Fixture: shallow-story-package

Create `.b2s/tests/fixtures/shallow-story-package/` with:

- `.b2s/state/workflow-state.json`:
  ```json
  {
    "active_action": "create-openspec-handoff",
    "next_action": "create-openspec-handoff",
    "action_status": {},
    "artifact_status": {}
  }
  ```

- `specs/F-001.1-story-one/story.md`:
  ```markdown
  # Story 1

  ## Story
  As a user, I want to implement the feature.

  ## Acceptance Criteria
  - It works.
  ```

This fixture must fail validation on: `story_not_generic_title`, `story_has_actor`, `story_has_business_outcome`, `story_has_requirements_link`, `story_has_bdd_scenarios`, `story_has_implementation_context`, `story_has_coding_prompt`, `story_no_placeholders`.

### Fixture: valid-story-package

Create `.b2s/tests/fixtures/valid-story-package/` with:

- `.b2s/state/workflow-state.json`:
  ```json
  {
    "active_action": "create-openspec-handoff",
    "next_action": "create-openspec-handoff",
    "action_status": {},
    "artifact_status": {}
  }
  ```

- `specs/F-001.1-submit-application/story.md`: a minimal but complete story that passes all checks:
  - heading: `# F-001.1 — Submit Application`
  - user story with named actor (not "user"), "I want", "so that"
  - FR-001 reference
  - `## 4. Acceptance Criteria` section with 3+ lines
  - a Gherkin block with `Given`, `When`, `Then` (non-generic Then)
  - `## 6. Implementation Context` with 4+ lines
  - `## 12. Coding-Agent Prompt` section containing "constraint" and "test"
  - no `{{`, `NNN`, or `TBD`

## Step 5 — Add tests

Add a new test class `StoryPackageValidatorTests` in `.b2s/tests/test_engine_fixtures.py`.

Add these tests:

```python
def test_validate_story_package_fails_for_shallow_story(self):
    self.materialize_fixture("shallow-story-package")
    run_cli(
        "validate-artifact",
        "--workspace-root", str(self.workspace_root),
        "--action-id", "create-openspec-handoff",
    )
    validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
    self.assertEqual(validation["overall"], "fail")
    failures = " ".join(validation["failures"])
    self.assertIn("story_not_generic_title", failures)
    self.assertIn("story_has_bdd_scenarios", failures)
    self.assertIn("story_has_coding_prompt", failures)

def test_validate_story_package_passes_for_valid_story(self):
    self.materialize_fixture("valid-story-package")
    run_cli(
        "validate-artifact",
        "--workspace-root", str(self.workspace_root),
        "--action-id", "create-openspec-handoff",
    )
    validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
    self.assertEqual(validation["overall"], "pass")
```

Run all tests after implementing: `python -m pytest .b2s/tests/ -q`

## What not to change

- Do not change the `artifact-package` validation profile.
- Do not change any existing validators.
- Do not change stage-actions.yaml.
- Do not modify any initiative workspace files.

## Done criteria

- [ ] `_validate_story_package_directory` function exists in `validation.py`
- [ ] All 14 checks are implemented
- [ ] `VALIDATORS_BY_ARTIFACT["specs/"]` is registered
- [ ] `shallow-story-package` fixture exists and triggers the expected failures
- [ ] `valid-story-package` fixture exists and passes
- [ ] `StoryPackageValidatorTests` has both tests passing
- [ ] All 53+ existing tests still pass
