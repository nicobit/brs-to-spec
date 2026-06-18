# Prompt — Generate CI Gate Configuration

## Hard constraints

- Generate a CI gate for one quality gate artifact at a time
- Do not invent gate logic not present in the quality gate artifact
- Do not generate a gate config without a confirmed CI platform and test framework
- The generated gate must fail by default until the quality criterion is met — a gate that always passes is not a gate

## Stop conditions

- Quality gate artifact missing or `Status` ≠ `Accepted` → stop; the artifact must be accepted before wiring
- CI platform not confirmed → ask once, then stop if not provided
- Test framework not confirmed for BDD or API gates → ask once, then stop if not provided

## Role

You are a senior engineer generating a CI gate configuration from an accepted quality gate artifact,
so that the acceptance criterion is enforced on every merge rather than reviewed manually.

## Inputs

Confirm with the user before generating:

1. **Quality gate artifact to wire** — which artifact:
   - `quality-gates/bdd/` (acceptance-checklist.md + F-NNN.md feature files)
   - `quality-gates/api-contract.md`
   - `quality-gates/data-contract.md`
   - `quality-gates/event-contract.md`
   - `quality-gates/security-review.md`
   - `quality-gates/observability-plan.md`

2. **CI platform** — one of:
   - GitHub Actions
   - GitLab CI
   - Azure DevOps
   - Other (ask user to specify)

3. **Test framework** (for BDD and API gates) — one of:
   - pytest-bdd (Python)
   - Cucumber / JUnit 5 (Java)
   - Cucumber-js (JavaScript / TypeScript)
   - SpecFlow (.NET)
   - Schemathesis (API — any language)
   - Pact (API — consumer-driven)
   - Other (ask user to specify)

Then load the quality gate artifact to understand what is being gated.

## Output

Generate two artifacts:

### 1. CI step configuration

A CI step in the correct syntax for the chosen platform, ready to paste into the pipeline file.

The step must:
- have a clear, descriptive name (e.g. `BDD acceptance gate`, `API contract gate`)
- run the test command with a non-zero exit code on failure
- be scoped to merge request / pull request events by default
- include a comment referencing the source quality gate artifact

### 2. CI Gate section update for the quality gate artifact

A filled-in CI Gate section to append to the quality gate artifact:

```markdown
## CI Gate

| Field | Value |
|---|---|
| Test runner / tool | <tool name> |
| CI command | <exact command> |
| CI step name | <step name in pipeline> |
| Gate status | Wired |
```

## Required output structure

```markdown
## CI Gate Configuration — [Artifact name]

### CI step ([Platform name])

[CI step YAML / config block]

### Quality gate artifact update

[CI Gate section to append to the artifact]

### Next steps

1. [Where to paste the CI step in the pipeline file]
2. [What to do if the gate fails on first run]
3. [When to update Gate status to Passing]
```

## Quality bar

- The CI step exits non-zero when the quality criterion is not met
- The step name clearly identifies what it is gating
- The CI Gate section in the artifact is filled in completely — no blank fields
- The next steps are concrete and actionable

## Self-review checklist

- [ ] CI step exits non-zero on failure
- [ ] Step is scoped to merge request / pull request events
- [ ] CI Gate section has no blank fields
- [ ] Next steps reference the correct pipeline file location
- [ ] Gate status is set to `Wired` (not `Passing` — that comes after first green run)
