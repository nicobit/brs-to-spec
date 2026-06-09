# Proposal — D3: Regional Hardening and Ops Readiness

> OpenSpec change proposal. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder (`openspec/changes/D3-regional-hardening/`) into the target code repository before applying.
> **Depends on D1 and D2 being deployed.**

## Why

D1 and D2 deliver a working onboarding flow for the internal pilot. D3 makes it production-ready for the Italian market: enforcing data residency, hardening availability to 99.9%, completing observability (runbooks, alert hardening, dashboard links), and enabling CRM sync if Legal has signed off. Without D3, the service cannot go to external users.

## What changes

- Data residency enforcement — confirmed `eu-south` deployment, cross-region replication policy locked
- Subject deletion endpoint `DELETE /profiles/{profile_id}` — GDPR compliance
- CRM sync — profile and consent data shared with CRM (pending Legal sign-off on OD-004)
- Observability hardening — runbooks tested, alert thresholds tuned to production traffic, dashboard links attached
- Availability hardening — AKS multi-AZ confirmed, chaos/load testing completed
- Legal residency sign-off attached to `input/input-package.md`

## Scope

### In scope

| Feature | User story summary | Requirement |
|---|---|---|
| F-005.2 Runbooks and alerting | SRE has tested runbooks and hardened alert thresholds | NFR-005 |
| GDPR deletion | Subject access / deletion endpoint operational | Legal requirement, `quality-gates/data-contract.md` |
| Data residency enforcement | Italy residency confirmed in production, Legal sign-off attached | OD-001, `quality-gates/data-contract.md` |
| CRM sync | Profile and consent data synced to CRM | OD-004 — conditional on Legal sign-off |
| Availability hardening | AKS multi-AZ, load test, chaos test | NFR-002 |

### Out of scope (explicitly)

- Core onboarding flow changes — D1
- Support UI changes — D2
- New integrations not in BRS scope

## Success criteria

| Criterion | Target | Source |
|---|---|---|
| Service availability | ≥ 99.9% monthly in production | BRS NFR-002 |
| Runbooks tested by SRE | All P1 scenarios exercised in staging | `quality-gates/observability-plan.md` |
| Data residency confirmed | Legal sign-off document attached | OD-001, data-contract.md |
| GDPR deletion operational | `DELETE /profiles/{id}` deletes profile and triggers purge schedule | Legal requirement |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| D1 and D2 must be deployed before D3 starts | D1/D2 handoff checklists |
| CRM sync requires Legal sign-off on data-sharing contract | OD-004 resolution |
| Italy residency: no cross-region replication without Legal approval | `quality-gates/data-contract.md` |
| Retention and deletion policies confirmed with Legal | `quality-gates/data-contract.md` |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Data contract | `quality-gates/data-contract.md` | Residency, retention, deletion, CRM sharing scope |
| Observability plan | `quality-gates/observability-plan.md` | Runbook content, alert rules to harden |
| Open decisions | `planning/open-decisions.md` | OD-001 (residency), OD-004 (CRM sync) resolutions |
| Architecture | `input/architecture.md` | AKS multi-AZ topology |
