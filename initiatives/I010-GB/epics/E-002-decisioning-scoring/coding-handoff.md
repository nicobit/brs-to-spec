# Coding Handoff - E-002 Decisioning & Scoring

## 0 - Component and Repository Map
- Component: Scoring pipeline service — repo: platform/scoring
- Explainability store: platform/explainability

## 1. Implementation Objective

Provide the scoring ingestion, job creation, model inference invocation, and persistence of explainability artifacts so that scoring results and recommendations are available to downstream systems.

## 2. Scope

In Scope:
- POST /api/scoring/jobs to create scoring jobs
- Explainability artifact persistence and retrieval

Out of Scope:
- Production model training

## 3. Data Model

See implementation contract inlined below.

## 4. Acceptance Criteria (selected)

### S-002.0 — Scoring e2e POC
```gherkin
Scenario: Scoring pipeline ingests a synthetic submission and produces score
  Given a synthetic application submission is POSTed to the Intake API
  When the Intake API publishes the submission event
  Then the scoring pipeline produces a scoring result containing `score` and `recommendation`
```

### S-002.1 — Scoring ingestion API
```gherkin
Scenario: Intake API publishes normalized scoring job event (happy path)
  Given a valid application submission
  When the submission is accepted
  Then the Intake API publishes an `application.scoring.job` event containing normalized fields required by scoring pipeline
```

### S-002.2 — Store explainability artifacts
```gherkin
Scenario: Explainability artifacts persisted and retrievable
  Given a scoring.result with explainability payload
  When the explainability service persists the artifact
  Then the artifact is retrievable via the explainability API and marked immutable
```

*This file is the self-contained coding handoff for E-002.*
