# Test Strategy

## Approach

- Unit tests for modules
- Integration tests for adapters (Experian, DocuSign, T24)
- Contract tests for APIs
- Performance tests for AI scoring (60s SLA)

## Environments

- `int` runs integration tests
- `pre-prod` runs performance and smoke tests

## Artefacts

- BDD scenarios in `quality-gates/bdd/`
- Test plans and scripts
