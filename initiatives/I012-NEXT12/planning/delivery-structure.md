# Delivery Structure

## Purpose

Capture the recommended delivery organisation, cadence, milestones, and artefacts for initiative I012-NEXT12. This is a planning-level view to support delivery planning, traceability, and engineering readiness.

## Summary

- Delivery lead: Delivery Lead (role: delivery-lead)
- Suggested cadence: 2-week sprints with monthly architecture checkpoints
- Initial teams: Frontend (Portal), API/Integration, AI/Scoring, Data & Platform, QA/Automation
- Key milestones: Discovery complete, MVP ready for UAT, Production readiness

## Workstreams and Responsibilities

- Product/PO: Prioritise backlog, acceptance criteria, UAT coordination
- Delivery Lead: Plan increments, manage dependencies, reporting
- Engineering Lead: Technical delivery plan, CI/CD, environment hygiene
- Security/Compliance: Gate approvals for PII flows and auditability
- Ops: Environments, monitoring, runbooks

## Delivery Increments (Suggested)

1. Increment 0 — Discovery & Foundations
   - Finalise requirements, finalize architecture rules, environments, CI/CD skeleton
   - Deliverables: `requirements.md`, `architecture-rules.md`, basic IaC skeleton

2. Increment 1 — Core Applicant Flow (MVP)
   - Applicant Portal, basic eligibility checks, application submission, audit logging
   - Deliverables: UC-001..UC-004 implemented end-to-end, basic E2E tests

3. Increment 2 — Scoring & Decisioning
   - AI scoring integration, Experian call, decision rules, underwriter referrals
   - Deliverables: AI scoring service, integration adapters, performance tests

4. Increment 3 — Underwriting & Offer
   - DocuSign flow, offer generation, T24 integration for decision persistence
   - Deliverables: Integration adapters, integration test suite

5. Increment 4 — Hardening & Production Readiness
   - Observability, DR runbook, performance tuning, security hardening
   - Deliverables: runbooks, production IaC, final compliance signoffs

## Environments

- `dev` — feature branches, short-lived test deployments
- `int` — integration environment for cross-team testing
- `pre-prod` — release candidate validation with production-like data controls
- `prod` — UK South primary, UK West DR

## Artefacts & Traceability

- Delivery backlog in chosen tool (use-case IDs linked to backlog items)
- `planning/delivery-structure.md` (this file)
- `planning/traceability-matrix.md` (to be generated)
- Test plans and performance test scripts

## CI/CD and Quality Gates

- Use IaC linting and security scanning in PR pipelines. Enforce `AR-001`, `AR-002`, `AR-004` via policy checks.
- Automated unit, integration, and E2E tests run in `int` with gating to `pre-prod`.

## Risks & Assumptions

- Assumes architecture rules accepted and integrations have defined SLAs.
- Risk: External vendor SLAs may require fallback manual processes.

---

Status: Draft (workflow will assign `ai_validated` on pass)
