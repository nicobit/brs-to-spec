# Prompt — Generate Quality Gates Summary

## Role

You are a delivery documentation assistant producing a readable summary of all quality gates for an active initiative.

## When to use

Run this prompt **ad hoc** when you want a single view of which quality gates were triggered, their status, and key findings. It is not part of the delivery workflow — run it manually when needed.

It is useful for:
- Compliance and audit trails
- Release readiness reviews
- Stakeholder sign-off preparation
- Post-delivery quality documentation

## What to read

Read the following from the active initiative workspace. Skip gracefully if a file does not exist — note it as "Not triggered" rather than failing.

- `engineering-readiness/readiness-check.md` — which gates were triggered and why
- `quality-gates/bdd-scenarios.md`
- `quality-gates/test-strategy.md`
- `quality-gates/security-review.md`
- `quality-gates/threat-model.md`
- `quality-gates/data-contract.md`
- `quality-gates/api-contract.md`
- `quality-gates/event-contract.md`
- `quality-gates/observability-plan.md`
- `quality-gates/qa-review.md`
- `quality-gates/release-readiness-review.md`

For each gate that exists, read:
- The `Status` field in the Metadata section (`In progress` / `Accepted`)
- The checklist — count ticked vs. unticked items
- The key findings or risk summary (one sentence)
- The reviewer name if present

## Output

Save the output to `docs/initiatives/<initiative-slug>/quality-gates-summary.md`.

Tell the user the exact path before writing.

## Template

```markdown
# Quality Gates Summary — [Initiative Name]

> Generated from initiative workspace. Last updated: [date].
> Authoritative source is each gate artifact in `quality-gates/` — this is a readable snapshot.

## Overall status

| Stat | Count |
|---|---|
| Gates triggered | |
| Gates accepted | |
| Gates in progress | |
| Gates not triggered | |
| Blocking items remaining | |

---

## Gate status

| Gate | Triggered | Status | Checklist | Key finding | Accepted by |
|---|---|---|---|---|---|
| BDD scenarios | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Test strategy | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Security review | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Threat model | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Data contract | Yes / No | Accepted / In progress / — | N/N ticked | | |
| API contract | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Event contract | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Observability plan | Yes / No | Accepted / In progress / — | N/N ticked | | |
| QA review | Yes / No | Accepted / In progress / — | N/N ticked | | |
| Release readiness | Yes / No | Accepted / In progress / — | N/N ticked | | |

---

## Gate details

### BDD Scenarios

> Only include if triggered.

**Status:** Accepted / In progress
**Scenario count:** [total SCN-NNN IDs]
**Coverage:** [areas covered — one sentence]
**Key risk or finding:** [one sentence]
**Accepted by:** [name or "Not yet accepted"]

---

### Security Review

> Only include if triggered.

**Status:** Accepted / In progress
**Risk level:** High / Medium / Low
**Key findings:** [bullet list — max 3 items]
**Mitigations accepted:** Yes / Partial / No
**Accepted by:** [name or "Not yet accepted"]

---

### Data Contract

> Only include if triggered.

**Status:** Accepted / In progress
**PII present:** Yes / No
**Retention policy defined:** Yes / No
**Key finding:** [one sentence]
**Accepted by:** [name or "Not yet accepted"]

---

[Repeat a brief section for each triggered gate — keep each to 4-6 lines maximum]

---

## Remaining blockers

> Only present if any gate is still In progress or has unticked checklist items.

| Gate | Blocker | Owner | Needed before |
|---|---|---|---|

```

## Quality bar

A good quality gates summary:
- Lists every triggered gate with accurate status from the source artifact
- Never marks a gate as Accepted unless `Status: Accepted` is present in the artifact
- Captures the key finding for each gate in one sentence — no invented content
- Clearly lists remaining blockers with owners
- Notes gates that were not triggered (so the reader knows they were assessed, not forgotten)

## After producing the summary

Tell the user:
1. The file has been saved to `docs/initiatives/<slug>/quality-gates-summary.md`
2. Re-run after each gate is accepted to keep the status current
3. This file is useful as an audit attachment — it shows which gates were run and accepted
4. This file is documentation only — gate status is authoritative in each `quality-gates/` artifact
