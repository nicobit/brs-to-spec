# E-002 — AI Scoring & Risk Decisions

## Business Objective

Deliver automated scoring with explainability exports so underwriting and automated routing can make consistent risk decisions.

## Scope

In scope:
- Scoring service with model interface and explainability exporter
- Experian adapter for credit lookups (transient)

Out of scope:
- Model training lifecycle

## High-Level Acceptance Criteria

- Scores are produced deterministically for a given model version and inputs; explainability metadata is available for each score.

## Stories

| Story ID | Title | Layers | Priority |
|---|---|---|---|
| F-003.1 | Score pipeline - happy path | Backend, Integration | Must |
| F-003.2 | Explainability export | Backend | Must |
| F-004.1 | Experian adapter | Integration, Backend | Should |
