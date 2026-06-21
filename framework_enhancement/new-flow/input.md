# BRS-to-Spec SDLC Workflow: Architecture-Aware Artifact Pipeline

This document defines a practical workflow for transforming a Business Requirements Specification (BRS) into architecture-aware, testable, AI-ready delivery artifacts.

The goal is **not** to generate everything in one generic prompt.  
The goal is to use **progressive decomposition**, with clear inputs, reusable artifacts, review gates, and AI-safe implementation handoff.

---

## Core Principle

Avoid this:

```text
BRS → Generate Epics + Features + User Stories + BDD in one shot
```

Prefer this:

```text
BRS + Architecture + Repository Context
        ↓
Atomic Requirements
        ↓
Capability Map
        ↓
Architecture Context Pack
        ↓
Architecture Impact Map
        ↓
Epics
        ↓
Features per Epic
        ↓
Stories per Feature
        ↓
Story Quality Gate
        ↓
BDD
        ↓
AI Implementation Handoff
        ↓
Dispatch Next Action
```

---

## Recommended Artifact Structure

```text
.brs2spec/
  00-governance/
    delivery-constitution.md

  01-requirements/
    atomic-requirements.md
    open-questions.md
    assumptions.md

  02-domain/
    capability-map.md
    domain-model.md
    business-rules.md
    traceability-matrix.md

  03-architecture/
    architecture-context-pack.md
    architecture-impact-map.md
    required-adrs.md
    architecture-risks.md

  04-delivery/
    epics.md
    features/
      EPIC-001-features.md
    stories/
      FEATURE-001-stories.md
    delivery-waves.md
    dependency-graph.md

  05-quality/
    story-quality-review.md
    bdd/
      STORY-001-bdd.md
    test-strategy.md
    test-data.md

  06-handoff/
    stories/
      STORY-001/
        story.md
        business-context.md
        acceptance-criteria.md
        bdd-scenarios.md
        architecture-context.md
        implementation-guidance.md
        test-guidance.md
        constraints.md
        open-questions.md
        ai-agent-prompt.md

  07-review/
    readiness-report.md
    ready-stories.md
    blocked-stories.md
    fix-recommendations.md

  08-dispatch/
    next-action.md
    dispatch-log.md
    persona-message.md
```

---

# Phase 0 — Delivery Constitution

## Purpose

Create reusable delivery rules for the initiative or repository.

This is the governance artifact that later phases must respect.

## Inspired by

- GitHub Spec Kit constitution concept
- Enterprise SDLC governance
- AI-safe implementation controls

## Inputs

| Input | Source |
|---|---|
| BRS | Original business requirement document |
| Architecture documentation | Existing C4, arc42, ADRs, diagrams, repository docs |
| Repository context | Existing codebase structure, services, modules, APIs |
| Organization standards | Security, compliance, QA, documentation, release rules |

## Output Artifact

```text
.brs2spec/00-governance/delivery-constitution.md
```

## Creation Prompt

```markdown
# Phase 0 — Create Delivery Constitution

You are the SDLC Governance Architect for an enterprise AI-assisted delivery framework.

Input:
- Business Requirements Source: {{BRS_PATH}}
- Architecture Source: {{ARCHITECTURE_PATH}}
- Repository Context: {{REPOSITORY_CONTEXT_PATH}}
- Organization Standards: {{ORG_STANDARDS_PATH}}

Goal:
Create a Delivery Constitution that defines the non-negotiable rules for transforming business requirements into AI-ready implementation artifacts.

Produce:
1. Delivery principles
2. Story quality rules
3. Architecture alignment rules
4. BDD and testability rules
5. Security/compliance rules
6. Documentation rules
7. AI implementation safety rules
8. Definition of Ready
9. Definition of Done
10. Conditions that block implementation

Rules:
- Do not generate implementation tasks yet.
- Do not invent requirements.
- If information is missing, create explicit assumptions and open questions.
- The constitution must be reusable across all later phases.
- Every later phase must be validated against this constitution.

Output file:
{{OUTPUT_ROOT}}/00-governance/delivery-constitution.md
```

## Template

```markdown
# Delivery Constitution

## 1. Purpose

## 2. Delivery Principles

## 3. Requirement Handling Rules

## 4. Architecture Alignment Rules

## 5. Story Quality Rules

## 6. BDD and Testability Rules

## 7. Security and Compliance Rules

## 8. Documentation Rules

## 9. AI Implementation Safety Rules

## 10. Definition of Ready

## 11. Definition of Done

## 12. Blocking Conditions

## 13. Human Review Checkpoints
```

---

# Phase 1 — Atomic Requirements Extraction

## Purpose

Extract precise, traceable, atomic requirements from the BRS.

This phase prevents generic epics and stories later.

## Inputs

| Input | Source |
|---|---|
| BRS | Original document |
| Delivery Constitution | Phase 0 |
| Architecture source | Existing architecture docs, diagrams, ADRs |
| Repository context | Existing codebase and module structure |

## Output Artifacts

```text
.brs2spec/01-requirements/atomic-requirements.md
.brs2spec/01-requirements/open-questions.md
.brs2spec/01-requirements/assumptions.md
```

## Creation Prompt

```markdown
# Phase 1 — Extract Atomic Requirements

You are a Business Requirements Analyst.

Input:
- BRS document: {{BRS_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}
- Architecture context: {{ARCHITECTURE_PATH}}
- Repository context: {{REPOSITORY_CONTEXT_PATH}}

Goal:
Extract atomic, traceable requirements from the BRS.

For each requirement, produce:
- Requirement ID
- Requirement text
- Requirement type: functional / non-functional / data / integration / security / operational / reporting
- Source section
- Business actor
- Business object
- Trigger/event
- Expected outcome
- Dependencies
- Ambiguities
- Assumptions
- Blocking questions

Rules:
- Do not create epics, features, or stories.
- Do not merge unrelated requirements.
- Do not invent missing behavior.
- Mark unclear requirements explicitly.
- Keep each requirement atomic and traceable.
- Validate the extraction against the Delivery Constitution.

Output files:
{{OUTPUT_ROOT}}/01-requirements/atomic-requirements.md
{{OUTPUT_ROOT}}/01-requirements/open-questions.md
{{OUTPUT_ROOT}}/01-requirements/assumptions.md
```

## Template

```markdown
# Atomic Requirements

## Summary

## Requirement Catalogue

### REQ-001 — <Requirement Title>

| Field | Value |
|---|---|
| Type | Functional / Non-functional / Data / Integration / Security / Operational / Reporting |
| Source Section | |
| Actor | |
| Business Object | |
| Trigger/Event | |
| Expected Outcome | |
| Dependencies | |
| Ambiguities | |
| Assumptions | |
| Blocking Questions | |

#### Requirement Text

#### Notes

---

## Open Questions

## Assumptions

## Traceability Notes
```

---

# Phase 2 — Business Capability and Domain Model

## Purpose

Group requirements into business capabilities and domain concepts before generating delivery artifacts.

This prevents random epics and helps keep business logic separated from technical solution design.

## Inputs

| Input | Source |
|---|---|
| Atomic requirements | Phase 1 |
| Open questions | Phase 1 |
| Assumptions | Phase 1 |
| Delivery Constitution | Phase 0 |
| BRS | Original document, if needed for clarification |

## Output Artifacts

```text
.brs2spec/02-domain/capability-map.md
.brs2spec/02-domain/domain-model.md
.brs2spec/02-domain/business-rules.md
.brs2spec/02-domain/traceability-matrix.md
```

## Creation Prompt

```markdown
# Phase 2 — Build Business Capability and Domain Model

You are the Enterprise Business Analyst.

Input:
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Open Questions: {{OPEN_QUESTIONS_PATH}}
- Assumptions: {{ASSUMPTIONS_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}
- Original BRS: {{BRS_PATH}}

Goal:
Create a structured business capability model and domain model that can be used for architecture review, epic generation, feature generation, and story slicing.

Produce:
1. Business capability map
2. Capability descriptions
3. Domain entities
4. Entity relationships
5. Business events
6. Business rules
7. State transitions
8. User roles and permissions
9. Process flow summary
10. Capability-to-requirement traceability matrix

Rules:
- Do not create epics, features, or stories yet.
- A capability must describe a business ability, not a technical component.
- Do not invent domain concepts not supported by the BRS.
- Every requirement must map to at least one capability.
- If a requirement does not fit, place it in "Unclassified Requirements" and explain why.
- Highlight capabilities that require architecture review.

Output files:
{{OUTPUT_ROOT}}/02-domain/capability-map.md
{{OUTPUT_ROOT}}/02-domain/domain-model.md
{{OUTPUT_ROOT}}/02-domain/business-rules.md
{{OUTPUT_ROOT}}/02-domain/traceability-matrix.md
```

## Template

```markdown
# Business Capability Map

## Summary

## Capability Map

### CAP-001 — <Capability Name>

| Field | Value |
|---|---|
| Business Purpose | |
| Related Requirements | |
| Actors | |
| Business Objects | |
| Business Events | |
| Business Rules | |
| Dependencies | |
| Ambiguities | |
| Delivery Risk | |

---

# Domain Model

## Domain Entities

### <Entity Name>

| Field | Value |
|---|---|
| Description | |
| Key Attributes | |
| Relationships | |
| Lifecycle / States | |
| Related Requirements | |

## Business Events

## State Transitions

## Roles and Permissions

---

# Business Rules

### BR-001 — <Rule Name>

| Field | Value |
|---|---|
| Rule | |
| Applies To | |
| Related Requirements | |
| Exceptions | |
| Open Questions | |

---

# Traceability Matrix

| Requirement ID | Capability | Entity | Business Rule | Notes |
|---|---|---|---|---|
```

---

# Phase 3 — Architecture Context Pack

## Purpose

Create a compact architecture context artifact that later phases can use.

Architecture must not only be reviewed at the end. It must constrain epic, feature, story, BDD, and AI handoff generation.

## Inputs

| Input | Source |
|---|---|
| Architecture documentation | C4, arc42, ADRs, diagrams, README files |
| Repository context | Codebase, services, modules, folders, APIs |
| Atomic requirements | Phase 1 |
| Capability map | Phase 2 |
| Domain model | Phase 2 |
| Delivery Constitution | Phase 0 |

## Output Artifact

```text
.brs2spec/03-architecture/architecture-context-pack.md
```

## Creation Prompt

```markdown
# Phase 3 — Build Architecture Context Pack

You are the Architecture Context Analyst.

Input:
- Existing architecture documentation: {{ARCHITECTURE_PATH}}
- Repository context: {{REPOSITORY_CONTEXT_PATH}}
- Atomic requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Capability map: {{CAPABILITY_MAP_PATH}}
- Domain model: {{DOMAIN_MODEL_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Create a compact architecture context pack that can be reused by all later SDLC phases.

Produce:
1. System overview
2. Main systems
3. Main containers/components
4. Component responsibilities
5. API boundaries
6. Data ownership
7. Integration points
8. Authentication/authorization model
9. Security zones
10. Deployment model
11. Observability/logging model
12. Known constraints
13. Known technical debt
14. Existing architecture decisions
15. Missing architecture information
16. Architecture assumptions

Rules:
- Do not invent architecture.
- If architecture is missing, mark it explicitly.
- Keep the output compact and reusable.
- Focus only on architecture elements relevant to the BRS.
- Separate confirmed facts from assumptions.
- Highlight unclear architecture areas that may block delivery.

Output:
{{OUTPUT_ROOT}}/03-architecture/architecture-context-pack.md
```

## Template

```markdown
# Architecture Context Pack

## 1. System Overview

## 2. Relevant Systems

| System | Responsibility | Notes |
|---|---|---|

## 3. Containers / Components

| Component | Responsibility | Owner | Notes |
|---|---|---|---|

## 4. API Boundaries

| API / Contract | Producer | Consumer | Notes |
|---|---|---|---|

## 5. Data Ownership

| Data / Entity | Owner | Storage | Notes |
|---|---|---|---|

## 6. Integrations

| Integration | Direction | Protocol | Notes |
|---|---|---|---|

## 7. Security and Authorization Model

## 8. Deployment Model

## 9. Observability Model

## 10. Existing ADRs

## 11. Known Constraints

## 12. Technical Debt

## 13. Missing Architecture Information

## 14. Architecture Assumptions
```

---

# Phase 4 — Architecture Impact Map

## Purpose

Map each requirement and capability to architecture impact.

This artifact should be used before creating epics, features, and stories.

## Inputs

| Input | Source |
|---|---|
| Atomic requirements | Phase 1 |
| Capability map | Phase 2 |
| Domain model | Phase 2 |
| Architecture context pack | Phase 3 |
| Existing architecture documentation | Original architecture source |
| Delivery Constitution | Phase 0 |

## Output Artifacts

```text
.brs2spec/03-architecture/architecture-impact-map.md
.brs2spec/03-architecture/required-adrs.md
.brs2spec/03-architecture/architecture-risks.md
```

## Creation Prompt

```markdown
# Phase 4 — Create Architecture Impact Map

You are the Software Architecture Reviewer.

Input:
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Capability Map: {{CAPABILITY_MAP_PATH}}
- Domain Model: {{DOMAIN_MODEL_PATH}}
- Architecture Context Pack: {{ARCHITECTURE_CONTEXT_PACK_PATH}}
- Existing Architecture Documentation: {{ARCHITECTURE_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Map each requirement and capability to architecture impact.

For each requirement/capability, identify:
- Impacted system
- Impacted container/component
- Impacted API
- Impacted database/entity
- Impacted integration
- Security impact
- Deployment impact
- Observability impact
- Performance/scalability impact
- Backward compatibility impact
- Required ADR
- Architecture risk
- Architecture readiness: READY / NEEDS CLARIFICATION / BLOCKED

Rules:
- Do not create epics, features, or stories.
- Do not invent impacted components.
- If impact is unclear, mark NEEDS CLARIFICATION.
- If an architecture decision is missing, mark BLOCKED.
- Every architecture impact must trace back to a requirement or capability.
- Produce a list of architecture decisions required before implementation.

Output files:
{{OUTPUT_ROOT}}/03-architecture/architecture-impact-map.md
{{OUTPUT_ROOT}}/03-architecture/required-adrs.md
{{OUTPUT_ROOT}}/03-architecture/architecture-risks.md
```

## Template

```markdown
# Architecture Impact Map

## Summary

## Impact by Requirement

### REQ-001 — <Requirement Title>

| Area | Impact |
|---|---|
| Capability | |
| Impacted System | |
| Impacted Component | |
| Impacted API | |
| Impacted Data / Entity | |
| Impacted Integration | |
| Security Impact | |
| Deployment Impact | |
| Observability Impact | |
| Performance / Scalability Impact | |
| Backward Compatibility Impact | |
| Required ADR | |
| Architecture Risk | LOW / MEDIUM / HIGH |
| Readiness | READY / NEEDS CLARIFICATION / BLOCKED |

---

# Required ADRs

| ADR ID | Topic | Reason | Blocking? |
|---|---|---|---|

# Architecture Risks

| Risk ID | Description | Impact | Mitigation | Blocking? |
|---|---|---|---|---|
```

---

# Phase 5 — Epic Generation

## Purpose

Create epics from capabilities and architecture impact.

Epics should represent meaningful business outcomes, not random groups of requirements.

## Inputs

| Input | Source |
|---|---|
| Capability map | Phase 2 |
| Atomic requirements | Phase 1 |
| Architecture impact map | Phase 4 |
| Delivery Constitution | Phase 0 |
| Business rules | Phase 2 |

## Output Artifact

```text
.brs2spec/04-delivery/epics.md
```

## Creation Prompt

```markdown
# Phase 5 — Generate Epics from Capabilities

You are a Delivery Product Owner.

Input:
- Capability Map: {{CAPABILITY_MAP_PATH}}
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Business Rules: {{BUSINESS_RULES_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Create delivery epics from the business capabilities and architecture impact.

For each epic, produce:
- Epic ID
- Epic title
- Business outcome
- Related capabilities
- Included requirements
- Excluded requirements
- Architecture impact
- Data impact
- Integration impact
- Security/compliance impact
- Main risks
- Dependencies
- Readiness status: READY / NEEDS CLARIFICATION / BLOCKED

Rules:
- Do not create features or stories yet.
- Do not create one epic per requirement.
- Do not create generic epics unless the BRS clearly supports them.
- Each epic must represent a meaningful business outcome.
- Every epic must be traceable to capabilities and requirements.
- If architecture impact is unclear, mark the epic as NEEDS CLARIFICATION or BLOCKED.
- Respect the Delivery Constitution.

Output:
{{OUTPUT_ROOT}}/04-delivery/epics.md
```

## Template

```markdown
# Epics

## Summary

## Epic Catalogue

### EPIC-001 — <Epic Title>

| Field | Value |
|---|---|
| Business Outcome | |
| Related Capabilities | |
| Included Requirements | |
| Excluded Requirements | |
| Architecture Impact | |
| Data Impact | |
| Integration Impact | |
| Security / Compliance Impact | |
| Dependencies | |
| Risks | |
| Readiness | READY / NEEDS CLARIFICATION / BLOCKED |

#### Description

#### Notes

---

## Blocked Epics

## Epic Traceability Matrix

| Epic | Capabilities | Requirements | Architecture Impact | Readiness |
|---|---|---|---|---|
```

---

# Phase 6 — Feature Generation per Epic

## Purpose

Break one epic into implementation-oriented features.

Run this phase one epic at a time.

## Inputs

| Input | Source |
|---|---|
| Selected epic | Phase 5 |
| Epics file | Phase 5 |
| Capability map | Phase 2 |
| Atomic requirements | Phase 1 |
| Architecture impact map | Phase 4 |
| Architecture context pack | Phase 3 |
| Business rules | Phase 2 |
| Delivery Constitution | Phase 0 |

## Output Artifact

```text
.brs2spec/04-delivery/features/{{EPIC_ID}}-features.md
```

## Creation Prompt

```markdown
# Phase 6 — Generate Features for One Epic

You are a Feature Planner.

Input:
- Selected Epic ID: {{EPIC_ID}}
- Epic Definition: {{EPIC_PATH}}
- Capability Map: {{CAPABILITY_MAP_PATH}}
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Business Rules: {{BUSINESS_RULES_PATH}}
- Architecture Context Pack: {{ARCHITECTURE_CONTEXT_PACK_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Break the selected epic into implementation-oriented features.

For each feature, produce:
- Feature ID
- Feature title
- Feature objective
- Included requirements
- Business value
- Actors
- Business rules
- Impacted capabilities
- Impacted architecture areas
- Data impact
- API/integration impact
- UI impact, if any
- Dependencies
- Non-functional concerns
- Readiness status

Rules:
- Generate features only for the selected epic.
- Do not generate stories yet.
- A feature must be independently understandable.
- A feature must be small enough to be delivered in one or more related stories.
- Do not group unrelated business flows into the same feature.
- Mark unclear features as NOT READY.
- If the feature crosses architecture boundaries, explain why.
- Respect the Delivery Constitution.

Output:
{{OUTPUT_ROOT}}/04-delivery/features/{{EPIC_ID}}-features.md
```

## Template

```markdown
# Features for EPIC-XXX — <Epic Title>

## Summary

## Feature Catalogue

### FEATURE-001 — <Feature Title>

| Field | Value |
|---|---|
| Objective | |
| Business Value | |
| Related Requirements | |
| Related Business Rules | |
| Actors | |
| Impacted Capabilities | |
| Impacted Components | |
| Data Impact | |
| API / Integration Impact | |
| UI Impact | |
| Non-functional Concerns | |
| Dependencies | |
| Readiness | READY / NOT READY / BLOCKED |

#### Description

#### Out of Scope

#### Notes

---

## Feature Dependency Notes

## Feature Traceability Matrix

| Feature | Requirements | Capabilities | Components | Readiness |
|---|---|---|---|---|
```

---

# Phase 7 — Story Generation per Feature

## Purpose

Create implementation-ready stories for one feature at a time.

This avoids generic one-shot story generation.

## Inputs

| Input | Source |
|---|---|
| Selected feature | Phase 6 |
| Feature file | Phase 6 |
| Atomic requirements | Phase 1 |
| Business rules | Phase 2 |
| Domain model | Phase 2 |
| Architecture context pack | Phase 3 |
| Architecture impact map | Phase 4 |
| Delivery Constitution | Phase 0 |

## Output Artifact

```text
.brs2spec/04-delivery/stories/{{FEATURE_ID}}-stories.md
```

## Creation Prompt

```markdown
# Phase 7 — Generate User Stories for One Feature

You are an Agile Story Slicing Specialist.

Input:
- Selected Feature ID: {{FEATURE_ID}}
- Feature Definition: {{FEATURE_PATH}}
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Business Rules: {{BUSINESS_RULES_PATH}}
- Domain Model: {{DOMAIN_MODEL_PATH}}
- Architecture Context Pack: {{ARCHITECTURE_CONTEXT_PACK_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Create implementation-ready user stories for the selected feature.

For each story, produce:
- Story ID
- Story title
- User story statement
- Business context
- Requirement traceability
- Acceptance criteria
- Business rules covered
- Impacted component
- Impacted API
- Impacted data/entity
- Impacted integration
- Architecture constraints
- Security/compliance constraints
- Observability requirements
- Dependencies
- Out of scope
- Open questions
- Readiness: READY / NOT READY
- Reason for readiness status

Rules:
- Generate stories only for the selected feature.
- Keep stories small and independently testable.
- Do not cross architecture boundaries unless explicitly justified.
- Do not create stories that require unresolved architecture decisions.
- If architecture impact is unknown, mark the story NOT READY.
- Every story must trace back to requirements and architecture impact.
- Every story must be suitable for later BDD generation.
- Respect the Delivery Constitution.

Output:
{{OUTPUT_ROOT}}/04-delivery/stories/{{FEATURE_ID}}-stories.md
```

## Template

```markdown
# User Stories for FEATURE-XXX — <Feature Title>

## Summary

## Story Catalogue

### STORY-001 — <Story Title>

| Field | Value |
|---|---|
| Feature | |
| User Story | As a ..., I want ..., so that ... |
| Business Context | |
| Requirement Traceability | |
| Acceptance Criteria | |
| Business Rules Covered | |
| Impacted Component | |
| Impacted API | |
| Impacted Data / Entity | |
| Impacted Integration | |
| Architecture Constraints | |
| Security / Compliance Constraints | |
| Observability Requirements | |
| Dependencies | |
| Out of Scope | |
| Open Questions | |
| Readiness | READY / NOT READY |
| Readiness Reason | |

#### Acceptance Criteria

- AC1:
- AC2:
- AC3:

#### Notes

---

## Not Ready Stories

## Story Traceability Matrix

| Story | Feature | Requirements | Components | Readiness |
|---|---|---|---|---|
```

---

# Phase 8 — Story Quality Gate

## Purpose

Validate stories before BDD and implementation handoff.

The reviewer prompt is more important than the generator prompt.

## Inputs

| Input | Source |
|---|---|
| Stories | Phase 7 |
| Atomic requirements | Phase 1 |
| Architecture impact map | Phase 4 |
| Architecture context pack | Phase 3 |
| Delivery Constitution | Phase 0 |
| Business rules | Phase 2 |

## Output Artifact

```text
.brs2spec/05-quality/story-quality-review.md
```

## Creation Prompt

```markdown
# Phase 8 — Validate Story Quality

You are a strict Agile Delivery Reviewer.

Input:
- Stories: {{STORIES_PATH}}
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Business Rules: {{BUSINESS_RULES_PATH}}
- Architecture Context Pack: {{ARCHITECTURE_CONTEXT_PACK_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Validate whether each story is ready for BDD and AI implementation handoff.

For each story, check:
- Is the business goal clear?
- Is the story small enough?
- Is it independently testable?
- Are acceptance criteria specific?
- Is requirement traceability present?
- Are dependencies explicit?
- Is architecture impact understood?
- Are data/API/UI/integration impacts clear?
- Are security and compliance concerns addressed?
- Are observability requirements clear where needed?
- Are open questions blocking?
- Could an AI coding agent implement this safely?

Return for each story:
- PASS / FAIL
- Readiness status
- Blocking issues
- Missing information
- Suggested rewrite
- Risk level: LOW / MEDIUM / HIGH

Rules:
- Be strict.
- Do not pass generic stories.
- Do not pass stories with vague acceptance criteria.
- Do not pass stories where architecture impact is unknown.
- Do not silently fix stories; report required changes.
- Respect the Delivery Constitution.

Output:
{{OUTPUT_ROOT}}/05-quality/story-quality-review.md
```

## Template

```markdown
# Story Quality Review

## Summary

| Metric | Value |
|---|---|
| Total Stories Reviewed | |
| Passed | |
| Failed | |
| Blocked | |
| High Risk | |

## Review Results

### STORY-001 — <Story Title>

| Check | Result | Notes |
|---|---|---|
| Business Goal Clear | PASS / FAIL | |
| Small Enough | PASS / FAIL | |
| Independently Testable | PASS / FAIL | |
| Acceptance Criteria Specific | PASS / FAIL | |
| Traceability Present | PASS / FAIL | |
| Dependencies Explicit | PASS / FAIL | |
| Architecture Impact Clear | PASS / FAIL | |
| Data/API/UI/Integration Impact Clear | PASS / FAIL | |
| Security/Compliance Covered | PASS / FAIL | |
| Observability Clear | PASS / FAIL | |
| AI Safe to Implement | PASS / FAIL | |

#### Final Decision

PASS / FAIL

#### Blocking Issues

#### Missing Information

#### Suggested Rewrite

#### Risk Level

LOW / MEDIUM / HIGH

---

## Ready Stories

## Failed Stories

## Recommended Fixes
```

---

# Phase 9 — BDD and Test Strategy

## Purpose

Generate BDD only for approved stories.

Do not generate BDD for vague or failed stories.

## Inputs

| Input | Source |
|---|---|
| Approved stories | Phase 8 |
| Story quality review | Phase 8 |
| Business rules | Phase 2 |
| Domain model | Phase 2 |
| Architecture impact map | Phase 4 |
| Delivery Constitution | Phase 0 |

## Output Artifacts

```text
.brs2spec/05-quality/bdd/{{STORY_ID}}-bdd.md
.brs2spec/05-quality/test-strategy.md
.brs2spec/05-quality/test-data.md
```

## Creation Prompt

```markdown
# Phase 9 — Generate BDD for Approved Stories

You are a BDD and QA Specialist.

Input:
- Approved Stories: {{APPROVED_STORIES_PATH}}
- Story Quality Review: {{STORY_QUALITY_REVIEW_PATH}}
- Business Rules: {{BUSINESS_RULES_PATH}}
- Domain Model: {{DOMAIN_MODEL_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Generate BDD scenarios only for stories that passed the story quality gate.

For each story, produce:
- Scenario title
- Given / When / Then
- Happy path
- Negative cases
- Validation cases
- Authorization/security cases
- Integration failure cases
- Audit/logging cases
- Data consistency cases
- Non-functional test notes
- Test data needs
- Mock/stub needs

Rules:
- Do not generate BDD for failed stories.
- Use business language.
- Do not include implementation code.
- Every scenario must map to acceptance criteria, business rules, or architecture risk.
- If a missing scenario is caused by unclear requirements, flag it.
- Respect the Delivery Constitution.

Output:
{{OUTPUT_ROOT}}/05-quality/bdd/{{STORY_ID}}-bdd.md
{{OUTPUT_ROOT}}/05-quality/test-strategy.md
{{OUTPUT_ROOT}}/05-quality/test-data.md
```

## Template

```markdown
# BDD Scenarios for STORY-XXX — <Story Title>

## Story Summary

## Acceptance Criteria Covered

| Acceptance Criterion | Scenario |
|---|---|

## Scenarios

### Scenario 1 — <Happy Path>

Given ...
When ...
Then ...

### Scenario 2 — <Validation Error>

Given ...
When ...
Then ...

### Scenario 3 — <Authorization / Security>

Given ...
When ...
Then ...

### Scenario 4 — <Integration Failure>

Given ...
When ...
Then ...

### Scenario 5 — <Audit / Logging>

Given ...
When ...
Then ...

## Test Data Requirements

## Mock / Stub Requirements

## Non-functional Test Notes

## Open Testing Questions
```

---

# Phase 10 — AI Implementation Handoff

## Purpose

Create self-contained story folders that an AI coding agent can safely use.

This phase prepares work for GitHub Copilot, Codex, Claude Code, OpenSpec, or similar tools.

## Inputs

| Input | Source |
|---|---|
| Approved stories | Phase 8 |
| BDD scenarios | Phase 9 |
| Architecture context pack | Phase 3 |
| Architecture impact map | Phase 4 |
| Repository context | Original repository analysis |
| Delivery Constitution | Phase 0 |
| Story quality review | Phase 8 |

## Output Folder

```text
.brs2spec/06-handoff/stories/{{STORY_ID}}/
```

## Creation Prompt

```markdown
# Phase 10 — Create AI Implementation Handoff

You are the AI Implementation Handoff Engineer.

Input:
- Approved Stories: {{APPROVED_STORIES_PATH}}
- BDD Scenarios: {{BDD_PATH}}
- Story Quality Review: {{STORY_QUALITY_REVIEW_PATH}}
- Architecture Context Pack: {{ARCHITECTURE_CONTEXT_PACK_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Repository Context: {{REPOSITORY_CONTEXT_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Create self-contained implementation handoff packages for AI coding agents.

For each READY story, create a story folder containing:
1. story.md
2. business-context.md
3. acceptance-criteria.md
4. bdd-scenarios.md
5. architecture-context.md
6. impacted-files-or-areas.md
7. implementation-guidance.md
8. test-guidance.md
9. constraints.md
10. open-questions.md
11. ai-agent-prompt.md

The ai-agent-prompt.md must include:
- Role
- Goal
- Inputs
- Expected outputs
- Files likely impacted
- Architecture constraints
- Security constraints
- Validation steps
- Do-not-do list
- Completion checklist

Rules:
- Only create handoff packages for stories marked READY.
- Do not hand off stories with blocking ambiguities.
- Do not ask the AI coding agent to make product decisions.
- Do not ask the AI coding agent to change architecture unless an ADR exists.
- Keep each handoff small enough for one focused implementation session.
- Include BDD scenarios and test expectations in every handoff.
- Respect the Delivery Constitution.

Output folder:
{{OUTPUT_ROOT}}/06-handoff/stories/{{STORY_ID}}/
```

## Template

```markdown
# AI Implementation Handoff — STORY-XXX

## 1. Story

## 2. Business Context

## 3. Acceptance Criteria

## 4. BDD Scenarios

## 5. Architecture Context

## 6. Impacted Files or Areas

| Area | Expected Impact | Confidence |
|---|---|---|

## 7. Implementation Guidance

## 8. Test Guidance

## 9. Constraints

### Architecture Constraints

### Security Constraints

### Data Constraints

### Integration Constraints

### Do Not Do

## 10. Open Questions

## 11. AI Agent Prompt

```markdown
You are an AI Coding Agent working on STORY-XXX.

Goal:
...

Inputs:
...

Expected Output:
...

Architecture Constraints:
...

Implementation Rules:
...

Validation Steps:
...

Do Not:
...

Completion Checklist:
...
```
```

---

# Phase 11 — Readiness Review

## Purpose

Validate all generated artifacts before implementation starts.

This phase decides which stories are truly ready.

## Inputs

| Input | Source |
|---|---|
| Delivery Constitution | Phase 0 |
| Atomic requirements | Phase 1 |
| Capability map | Phase 2 |
| Architecture context pack | Phase 3 |
| Architecture impact map | Phase 4 |
| Epics | Phase 5 |
| Features | Phase 6 |
| Stories | Phase 7 |
| Story quality review | Phase 8 |
| BDD | Phase 9 |
| Handoff packages | Phase 10 |

## Output Artifacts

```text
.brs2spec/07-review/readiness-report.md
.brs2spec/07-review/ready-stories.md
.brs2spec/07-review/blocked-stories.md
.brs2spec/07-review/fix-recommendations.md
```

## Creation Prompt

```markdown
# Phase 11 — Review Initiative Readiness

You are the SDLC Readiness Reviewer.

Input:
- Delivery Constitution: {{CONSTITUTION_PATH}}
- Atomic Requirements: {{ATOMIC_REQUIREMENTS_PATH}}
- Capability Map: {{CAPABILITY_MAP_PATH}}
- Architecture Context Pack: {{ARCHITECTURE_CONTEXT_PACK_PATH}}
- Architecture Impact Map: {{ARCHITECTURE_IMPACT_MAP_PATH}}
- Epics: {{EPICS_PATH}}
- Features: {{FEATURES_PATH}}
- Stories: {{STORIES_PATH}}
- Story Quality Review: {{STORY_QUALITY_REVIEW_PATH}}
- BDD Scenarios: {{BDD_PATH}}
- Handoff Packages: {{HANDOFF_ROOT}}

Goal:
Review all generated artifacts and decide whether the initiative is ready for AI-assisted implementation.

Check:
1. BRS coverage
2. Requirement traceability
3. Story quality
4. Story size
5. Architecture alignment
6. ADR completeness
7. BDD completeness
8. Testability
9. Security/compliance coverage
10. Data/integration impact
11. Operational readiness
12. AI handoff quality
13. Blocking ambiguities
14. Human approval points

For each story, return:
- READY / NOT READY
- Reason
- Blocking issues
- Missing artifacts
- Suggested fixes
- Implementation risk: LOW / MEDIUM / HIGH

Produce:
1. Overall readiness score
2. Stories ready for implementation
3. Stories blocked
4. Architecture decisions required
5. Business clarifications required
6. QA concerns
7. Recommended next action

Rules:
- Be strict.
- Do not pass vague stories.
- Do not pass stories without testable acceptance criteria.
- Do not pass stories with unresolved architecture decisions.
- Do not improve artifacts silently; report required corrections.

Output files:
{{OUTPUT_ROOT}}/07-review/readiness-report.md
{{OUTPUT_ROOT}}/07-review/ready-stories.md
{{OUTPUT_ROOT}}/07-review/blocked-stories.md
{{OUTPUT_ROOT}}/07-review/fix-recommendations.md
```

## Template

```markdown
# Readiness Report

## Overall Readiness Score

| Area | Score | Notes |
|---|---|---|
| BRS Coverage | |
| Traceability | |
| Architecture Alignment | |
| Story Quality | |
| BDD Completeness | |
| Testability | |
| Security / Compliance | |
| AI Handoff Quality | |

## Ready Stories

| Story | Risk | Notes |
|---|---|---|

## Blocked Stories

| Story | Blocking Reason | Required Action |
|---|---|---|

## Required Architecture Decisions

## Required Business Clarifications

## QA Concerns

## Recommended Next Action

## Final Decision

READY / PARTIALLY READY / NOT READY
```

---

# Phase 12 — Dispatch Next Action

## Purpose

Decide the next workflow step.

This is your unique differentiator: the framework does not just create artifacts; it routes the next action.

## Inputs

| Input | Source |
|---|---|
| Readiness report | Phase 11 |
| Ready stories | Phase 11 |
| Blocked stories | Phase 11 |
| Open questions | Phase 1 |
| Required ADRs | Phase 4 |
| Fix recommendations | Phase 11 |
| Delivery Constitution | Phase 0 |

## Output Artifacts

```text
.brs2spec/08-dispatch/next-action.md
.brs2spec/08-dispatch/dispatch-log.md
.brs2spec/08-dispatch/persona-message.md
```

## Creation Prompt

```markdown
# Phase 12 — Dispatch Next Action

You are the Workflow Dispatcher.

Input:
- Readiness Report: {{READINESS_REPORT_PATH}}
- Ready Stories: {{READY_STORIES_PATH}}
- Blocked Stories: {{BLOCKED_STORIES_PATH}}
- Open Questions: {{OPEN_QUESTIONS_PATH}}
- Required ADRs: {{REQUIRED_ADRS_PATH}}
- Fix Recommendations: {{FIX_RECOMMENDATIONS_PATH}}
- Delivery Constitution: {{CONSTITUTION_PATH}}

Goal:
Determine the next best action in the SDLC workflow.

Possible next actions:
1. REQUEST_BUSINESS_CLARIFICATION
2. REQUEST_ARCHITECTURE_DECISION
3. REFINE_REQUIREMENTS
4. REFINE_EPIC
5. REFINE_FEATURE
6. REFINE_STORY
7. GENERATE_MISSING_BDD
8. GENERATE_HANDOFF
9. READY_FOR_AI_IMPLEMENTATION
10. READY_FOR_HUMAN_REVIEW
11. STOP_BLOCKED

For each next action, produce:
- Action type
- Target artifact
- Assigned persona
- Reason
- Required input
- Expected output
- Blocking condition
- Recommended prompt to run next

Rules:
- Choose the smallest useful next action.
- Do not dispatch implementation if readiness failed.
- Do not ask for human input unless it is truly blocking.
- Prefer artifact refinement before implementation.
- Maintain auditability of why the next action was selected.

Output files:
{{OUTPUT_ROOT}}/08-dispatch/next-action.md
{{OUTPUT_ROOT}}/08-dispatch/dispatch-log.md
{{OUTPUT_ROOT}}/08-dispatch/persona-message.md
```

## Template

```markdown
# Next Action

## Recommended Action

| Field | Value |
|---|---|
| Action Type | |
| Target Artifact | |
| Assigned Persona | |
| Reason | |
| Required Input | |
| Expected Output | |
| Blocking Condition | |
| Recommended Prompt | |

## Dispatch Rationale

## Dispatch Log Entry

| Field | Value |
|---|---|
| Timestamp | |
| Previous Phase | |
| Decision | |
| Reason | |
| Next Persona | |
| Next Artifact | |

## Persona Message

### To: <Persona>

### Context

### Task

### Inputs

### Expected Output

### Constraints
```

---

# Recommended Review Gates

The workflow should include explicit gates.

```text
Gate 1 — Requirements Review
After Phase 1

Gate 2 — Domain Review
After Phase 2

Gate 3 — Architecture Review
After Phase 4

Gate 4 — Epic Review
After Phase 5

Gate 5 — Feature Review
After Phase 6

Gate 6 — Story Quality Review
After Phase 8

Gate 7 — BDD/Test Review
After Phase 9

Gate 8 — AI Handoff Review
After Phase 11
```

---

# What Not to Do

Avoid prompts like:

```markdown
Create epics, features, user stories, BDD scenarios, and implementation tasks from this BRS.
```

This creates artifacts that may look complete but are usually:

- Too generic
- Weakly traceable
- Not architecture-aware
- Too large for implementation
- Weak on dependencies
- Weak on testability
- Unsafe for AI coding agents

---

# Better Prompt Strategy

Use two families of prompts.

## Generator Prompts

These create artifacts:

```text
Extract atomic requirements
Create capability map
Build architecture context pack
Create architecture impact map
Generate epics
Generate features for one epic
Generate stories for one feature
Generate BDD for approved stories
Create AI handoff package
```

## Reviewer Prompts

These validate artifacts:

```text
Validate requirements
Validate capability map
Validate architecture impact
Validate epics
Validate features
Validate stories
Validate BDD
Validate AI handoff
Dispatch next action
```

The reviewer prompts are what prevent generic output.

---

# Final Recommended Workflow

```text
00 Delivery Constitution
   ↓
01 Atomic Requirements
   ↓
02 Capability + Domain Model
   ↓
03 Architecture Context Pack
   ↓
04 Architecture Impact Map
   ↓
05 Epics
   ↓
06 Features per Epic
   ↓
07 Stories per Feature
   ↓
08 Story Quality Gate
   ↓
09 BDD + Test Strategy
   ↓
10 AI Implementation Handoff
   ↓
11 Readiness Review
   ↓
12 Dispatch Next Action
```

---

# Final Positioning

`brs-to-spec` should not be described as a tool that simply generates epics, features, and user stories.

A stronger positioning is:

> `brs-to-spec` transforms business requirements into architecture-aware, testable, AI-ready delivery stories with explicit review gates, traceability, and controlled implementation handoff.

Or:

> `brs-to-spec` is an enterprise SDLC workflow layer that prepares BRS input for safe AI-assisted delivery by producing requirements, architecture impact, delivery decomposition, BDD, and implementation handoff artifacts.

---

# Implementation Notes for the Framework

## Keep Artifacts Compact

Do not generate too many large documents by default.  
Prefer compact artifacts with strong traceability.

## Generate Per Unit

Generate:

- Features per epic
- Stories per feature
- BDD per approved story
- Handoff per ready story

Do not generate everything in one large response.

## Use Statuses Everywhere

Use simple readiness states:

```text
READY
NOT READY
NEEDS CLARIFICATION
BLOCKED
```

## Keep Human Review Explicit

Human review should happen when:

- Business meaning is ambiguous
- Architecture decision is missing
- Security/compliance risk is high
- Story is too large
- AI implementation may be unsafe

## Make Architecture a First-Class Constraint

Architecture should be used in:

- Requirement classification
- Capability validation
- Epic generation
- Feature generation
- Story slicing
- BDD scenario creation
- AI handoff
- Readiness review

Architecture is not only a final review.
It is an input throughout the workflow.
