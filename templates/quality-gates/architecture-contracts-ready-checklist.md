# Architecture & Contract Extensions Ready Checklist

## Artifact decision

- [ ] Artifact decision file exists.
- [ ] Optional artifacts are justified.
- [ ] Skipped artifacts have a reason.
- [ ] Mandatory-before-implementation artifacts are clear.

## ADRs

- [ ] Important architecture decisions are documented.
- [ ] Missing decisions are assigned to an owner.
- [ ] Blocking decisions are resolved before implementation.

## API / OpenAPI

- [ ] API contract exists for API changes.
- [ ] OpenAPI exists when contract-first implementation is needed.
- [ ] Authorization is defined.
- [ ] Error responses are defined.
- [ ] Breaking changes are assessed.

## Domain model / DDD

- [ ] Domain model is used only when domain complexity justifies it.
- [ ] Business terms are defined.
- [ ] Business invariants are documented.
- [ ] State transitions are clear.

## Data model

- [ ] Database changes are documented.
- [ ] Migration strategy is clear.
- [ ] Backward compatibility is assessed.

## Event contracts

- [ ] Produced and consumed events are documented.
- [ ] Event versioning is considered.
- [ ] Idempotency and retry handling are considered.

## Quality attributes

- [ ] Vague NFRs are converted into measurable scenarios.

## Threat model

- [ ] Assets and trust boundaries are identified.
- [ ] Threats and mitigations are documented.
- [ ] Security validation tasks are defined.

## OpenSpec handoff

- [ ] Architecture-contract findings are reflected in OpenSpec proposal/design/tasks.
