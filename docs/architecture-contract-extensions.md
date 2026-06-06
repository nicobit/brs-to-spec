# Optional Architecture & Contract Extensions

This track adds optional architecture and contract artifacts that help turn business requirements and user stories into precise engineering contracts.

It does **not** replace the core business intake, enablement, OpenSpec, or Copilot flows.

Use it when a feature needs additional architectural precision before OpenSpec tasks and Copilot implementation.

## Where this track fits

```text
Business Intake
  ↓
BRS + Requirements + Architecture Alignment
  ↓
Delivery Structure
  ↓
User Stories
  ↓
Engineering Contracts
  ↓
Optional Architecture & Contract Extensions
      - ADRs
      - API contract / OpenAPI
      - Domain model / DDD
      - Data model
      - Event contracts
      - Quality attribute scenarios
      - Threat model
  ↓
OpenSpec Proposal / Design / Tasks
  ↓
Copilot Implementation
```

## Principle

Keep these artifacts optional and conditional.

Use the smallest set of artifacts that reduces ambiguity and implementation risk.

## Decision rule

| Situation | Recommended artifact |
|---|---|
| Important technical choice | `architecture-contracts/architecture-decisions.md` or `architecture-contracts/adr/ADR-xxx.md` |
| REST API change | `architecture-contracts/api-contract.md` and optionally `architecture-contracts/openapi.yaml` |
| Complex business rules, workflows, state transitions | `architecture-contracts/domain-model.md` |
| Database changes | `architecture-contracts/data-model.md` |
| Event-driven integration or audit/event messages | `architecture-contracts/event-contracts.md` |
| Important NFRs | `architecture-contracts/quality-attribute-scenarios.md` |
| Security-sensitive change | `architecture-contracts/threat-model.md` |
| Infrastructure / CI-CD / operations | Use the Enablement Track |

## Recommended priority

```text
1. Architecture decisions / ADRs
2. API contract / OpenAPI
3. Data model
4. Event contracts
5. Domain model / DDD
6. Threat model
7. Quality attribute scenarios
```

DDD is useful when there is real domain complexity. It should not be used as ceremony.

OpenAPI is useful when REST APIs are created or changed and gives immediate value for frontend/backend alignment, testing, mocking, and implementation.

## Inputs

Typical inputs:

```text
input/brs-original.md
input/architecture-draft.md
business-intake/requirements.md
business-intake/brs-architecture-alignment.md
business-intake/epics-and-features.md
business-intake/user-stories.md
engineering-contracts/technical-spec.md
enablement/* if relevant
```

## Outputs

Outputs live under:

```text
features/<feature-name>/architecture-contracts/
```

Common outputs:

```text
artifact-decision.md
architecture-decisions.md
adr/ADR-001-<decision>.md
api-contract.md
openapi.yaml
domain-model.md
data-model.md
event-contracts.md
quality-attribute-scenarios.md
threat-model.md
```

## Relationship with OpenSpec

Architecture & Contract Extensions must feed OpenSpec proposal, design, and tasks.

Do not let architecture decisions, API contracts, OpenAPI, domain model, data model, event contracts, quality scenarios, or threat model findings disappear before implementation.

## Relationship with Copilot

Copilot implementation prompts should instruct Copilot to read relevant architecture-contract files before coding.

# Relationship with Handoff

Architecture & Contract Extensions should feed the handoff package.

If architecture-contract files exist, `handoff/spec-driven-handoff.md` must summarize them and explain whether they are mandatory before implementation.
