# Wiring Quality Gates to CI

A quality gate that only a human reads is a spec. A quality gate that blocks a merge is a fact.
This page shows how to connect each framework quality gate artifact to a CI gate.

## Overview

| Artifact | CI mechanism | Tool examples | Blocks merge? |
|---|---|---|---|
| BDD scenarios | Test runner (Gherkin) | pytest-bdd, Cucumber, SpecFlow, Cucumber-js | Recommended — yes |
| API contract | Contract test | Pact, Dredd, Schemathesis | Recommended — yes |
| Data contract | Schema validation | Great Expectations, dbt tests, Pandera | Recommended for data pipelines |
| Event contract | Schema registry check | Confluent Schema Registry, AsyncAPI validator | Recommended |
| Security review | SAST / secret scan | Semgrep, Trivy, GitLeaks, Bandit | Mandatory — yes |
| Threat model | Manual gate or policy check | OPA, custom script | Recommended |
| Observability plan | Smoke test / alert rule lint | Prometheus rules lint, OTel validator | Optional |
| Test strategy | Coverage gate | Coverage.py, Istanbul, Jacoco | Optional |
| QA review | Manual approval gate | GitHub required reviewers, GitLab approval rules | Recommended |

## BDD Scenarios → Test Runner

BDD scenarios are the most durable CI gate — they survive model upgrades because they
pass through a test runner exit code, not model interpretation.

### Minimum viable gate

1. Generate test stubs from the accepted BDD scenarios file using:
   ```text
   .brs2spec/skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md
   ```
2. Place the stub files in the target test folder
3. Add the test runner command to CI

### GitHub Actions example (pytest-bdd)

```yaml
- name: BDD acceptance gate
  run: pytest features/ -v --tb=short
```

### GitLab CI example (pytest-bdd)

```yaml
bdd-acceptance-gate:
  script:
    - pytest features/ -v --tb=short
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### Azure DevOps example (Cucumber / Java)

```yaml
- task: Maven@3
  inputs:
    goals: 'test'
    options: '-Dcucumber.filter.tags="@acceptance"'
  displayName: BDD acceptance gate
```

### When to add it

Add the CI gate immediately after the BDD scenarios artifact reaches `Status: Accepted`.
Do not wait until implementation is complete — the gate should fail first, then go green
as each scenario is implemented.

---

## API Contract → Contract Test

### Minimum viable gate

Use [Pact](https://docs.pact.io/) for consumer-driven contract testing or
[Schemathesis](https://schemathesis.readthedocs.io/) for schema-based API testing.

### GitHub Actions example (Schemathesis)

```yaml
- name: API contract gate
  run: schemathesis run quality-gates/api-contract.yaml --checks all
```

### GitHub Actions example (Pact)

```yaml
- name: Pact contract gate
  run: |
    npm run test:pact
    npx pact-broker publish ./pacts --broker-base-url $PACT_BROKER_URL
```

### When to add it

Add after the API contract artifact reaches `Status: Accepted` and before the first
implementation task that touches the governed API boundary.

---

## Data Contract → Schema Validation

### Minimum viable gate (Great Expectations)

```yaml
- name: Data contract gate
  run: great_expectations checkpoint run data_contract_checkpoint
```

### Minimum viable gate (dbt)

```yaml
- name: dbt schema test gate
  run: dbt test --select tag:contract
```

### When to add it

Add after the data contract artifact reaches `Status: Accepted`. Run on every pipeline
that touches the governed data boundary.

---

## Event Contract → Schema Registry Check

### Minimum viable gate (AsyncAPI validator)

```yaml
- name: Event contract gate
  run: asyncapi validate quality-gates/event-contract.yaml
```

### When to add it

Add after the event contract reaches `Status: Accepted`. Run on every pipeline that
publishes or consumes the governed event.

---

## Security Review → SAST Gate

### Minimum viable gate (Semgrep)

```yaml
- name: Security gate
  run: semgrep --config=auto --error
```

### Minimum viable gate (Trivy — container / dependency scan)

```yaml
- name: Trivy vulnerability gate
  run: trivy fs --exit-code 1 --severity HIGH,CRITICAL .
```

### When to add it

The security gate should be present from the first commit. It is not conditional on the
security review artifact — it is mandatory for all initiatives.

---

## Tracking CI wiring status

Add a CI Gate section to each triggered quality gate artifact to track wiring status.
Use the CI Gate section in the BDD scenarios template as the model.

| Field | Value |
|---|---|
| Test runner / tool | |
| CI command | |
| CI step name | |
| Gate status | Not wired / Wired / Passing |

Update `Gate status` to `Passing` once the gate runs green in CI for the first time.
A gate with `Status: Accepted` in the artifact but `Gate status: Not wired` is a delivery risk —
it means the acceptance criterion exists on paper but is not enforced.

---

## See also

- [Conditional Quality Gates](06-conditional-quality-gates.md)
- [Artifact Durability](23-artifact-durability.md)
- [Generate Test Stubs from BDD](.brs2spec/skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md)
