# Test Strategy

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T19:07:00+00:00 |
| Created by | qa-analyst |
| Status | Draft |

## Strategy Overview

- Levels: unit, integration, contract, E2E, regression
- Responsible: QA, Dev, Eng
## Test Levels

- Unit tests: component-level, owned by developers
- Integration tests: service-to-service contracts (MOD-002 ↔ MOD-005)
- Contract tests: adapters (T24, Experian) with sandbox emulators
- End-to-end tests: full flow including disbursement in staging
- Regression suite: nightly E2E smoke and critical path checks

## Technology Stack

- Test framework: pytest / behave for BDD
- Contract tests: Pact or similar
- Test infra: Azure DevOps / GitHub Actions runners connected to AKS staging

## Coverage Targets

- Unit: 70% per module
- Integration: contract coverage for all adapter interfaces
- E2E: cover key happy paths and 80% of critical error paths

## Test Data Strategy

- Use synthetic data generators for applicant profiles; masked production extracts for realistic cases; dedicated T24 sandbox dataset.

## Quality Gate to Test Mapping

- BDD Scenarios -> E2E/behavioral tests
- Security Review -> security tests, penetration and static analysis
- API Contract -> contract tests per adapter and consumer
- Observability Plan -> integration tests for metrics/logging emission

## CI Pipeline Integration

- Unit and contract tests run on PRs; integration and E2E on merge to branch; nightly regression pipeline for staging environment.

## Accepted Risks

- Full T24 end-to-end will be validated in staging only once sandbox parity is sufficient; mitigations include feature flags and phased adapter rollout.

## Key Focus Areas

- Integration with T24 and Experian — contract and sandbox tests
- Scoring determinism and threshold regression

