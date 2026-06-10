# Enhancement 2 — CI Wiring Guidance for Quality Gates

## Context

The BRS to Spec framework produces structured quality gate artifacts:
- BDD scenarios (Gherkin)
- API contracts (endpoint tables, request/response schemas)
- Data contracts
- Event contracts
- Test strategy
- Security review
- Observability plan

These artifacts currently live as markdown files in the initiative workspace. They are
reviewed by humans but have no defined path to becoming CI gates. The framework stops
at "write the artifact" — it does not tell the team how to make it machine-verifiable.

The gap: a quality gate that only a human reads is a spec. A quality gate that blocks
a merge is a fact. The framework needs to bridge that gap.

## What needs to change

### 1. Create a new doc: `docs/22-wiring-quality-gates-to-ci.md`

A new reference page covering how each quality gate artifact type connects to CI.
Structure it as a table followed by per-type guidance sections:

| Artifact | CI mechanism | Tool examples | Blocks merge? |
|---|---|---|---|
| BDD scenarios | Test runner (Gherkin) | pytest-bdd, Cucumber, SpecFlow | Yes — recommended |
| API contract | Contract test | Pact, Dredd, Schemathesis | Yes — recommended |
| Data contract | Schema validation | Great Expectations, dbt tests | Yes — for data pipelines |
| Event contract | Schema registry check | Confluent Schema Registry, AsyncAPI | Recommended |
| Security review | SAST / secret scan | Semgrep, Trivy, GitLeaks | Yes — mandatory |
| Observability plan | Smoke test / alert check | Prometheus rules lint, OTel validator | Optional |
| Test strategy | Coverage gate | Coverage.py, Istanbul, Jacoco | Optional |

For each type, provide:
- what the artifact contains that maps to a CI check
- the minimum viable CI gate (one command, one exit code)
- tool recommendations by language/stack
- where to place the CI config in the repository

### 2. Add a CI wiring section to `docs/06-conditional-quality-gates.md`

After the existing quality gate decision table, add a short section:
"After generating a quality gate artifact, wire it to CI before the first implementation
task begins. See [Wiring Quality Gates to CI](22-wiring-quality-gates-to-ci.md)."

### 3. Create a new prompt: `.brs2spec/quality-gates/generate-ci-gate-config.md`

A prompt that reads one quality gate artifact (BDD scenarios or API contract) and produces:
- A CI workflow step (GitHub Actions YAML or GitLab CI YAML)
- The test runner command
- The failure condition and what it means
- A note on what to do if the gate fails

The prompt should ask the user: which CI platform (GitHub Actions / GitLab CI / Azure DevOps),
which test framework, and which artifact to wire.

### 4. Update `.brs2spec/templates/templates/quality-gates/bdd-scenarios.md`

Add a footer section:

```
## CI Gate

| Field | Value |
|---|---|
| Test runner | (e.g. pytest-bdd, Cucumber) |
| Command | (e.g. pytest --co -q features/) |
| CI step name | (e.g. BDD acceptance gate) |
| Gate status | Not wired / Wired / Passing |
```

This makes CI wiring a tracked deliverable, not an afterthought.

### 5. Add to `mkdocs.yml` nav

Add `22-wiring-quality-gates-to-ci.md` under the Reference section.

## Implementation steps

1. Create `docs/22-wiring-quality-gates-to-ci.md` with the full guidance page
2. Update `docs/06-conditional-quality-gates.md` — add CI wiring callout
3. Update `.brs2spec/templates/templates/quality-gates/bdd-scenarios.md` — add CI Gate section
4. Create `.brs2spec/quality-gates/generate-ci-gate-config.md` prompt
5. Update `mkdocs.yml` nav to include the new page

## Quality bar for this enhancement

- A developer can read the framework and know exactly how to wire their BDD scenarios to CI
- The CI gate config prompt produces a working GitHub Actions or GitLab CI step
- The BDD scenarios template makes CI wiring a tracked field, not an assumption
- The guidance covers at least 3 quality gate types with concrete tool recommendations
