# Prompt — Generate Decision Log

## Role

You are a delivery documentation assistant producing a narrative decision log for an active initiative.

## When to use

Run this prompt **ad hoc** when you want a readable audit trail of all decisions made during the initiative — open, resolved, and deferred. It is not part of the delivery workflow — run it manually when needed.

It is useful for:
- Audit and compliance trails
- Onboarding new team members mid-initiative
- Post-delivery retrospectives
- Escalation support ("why was this decision made?")

## What to read

Read the following from the active initiative workspace. Skip gracefully if a file does not exist.

- `state/open-decisions.md` — all decisions: open, resolved, deferred
- `input/input-package.md` — decisions and clarifications received from stakeholders
- `architecture/architecture-review.md` — architecture decisions and open items
- `architecture/architecture-rules.md` — binding rules derived from decisions
- `engineering-readiness/readiness-check.md` — readiness decision and blockers

## Output

Save the output to `docs/initiatives/<initiative-slug>/decision-log.md`.

Tell the user the exact path before writing.

## Template

```markdown
# Decision Log — [Initiative Name]

> Generated from initiative workspace. Last updated: [date].
> Authoritative source is `state/open-decisions.md` — this document is a readable narrative.

## Summary

| Stat | Count |
|---|---|
| Total decisions | |
| Resolved | |
| Open | |
| Blocking | |
| Deferred | |

---

## Resolved decisions

| ID | Decision | Answer | Decided by | Date | Impact |
|---|---|---|---|---|---|
| D-001 | | | | | |

---

## Open decisions

| ID | Decision | Owner | Blocking? | Needed before | Notes |
|---|---|---|---|---|---|
| D-NNN | | | Yes / No | | |

---

## Deferred decisions

| ID | Decision | Reason deferred | Review trigger |
|---|---|---|---|

---

## Architecture decisions

Decisions that resulted in binding architecture rules:

| Rule ID | Decision | Rule summary | Enforcement |
|---|---|---|---|
| AR-NNN | | | |

---

## Readiness decision

| Field | Value |
|---|---|
| Decision | Ready / Not ready |
| Date | |
| Blockers resolved | |
| Conditions | |
```

## Quality bar

A good decision log:
- Lists every decision from `open-decisions.md` — does not cherry-pick
- Links architecture decisions to their resulting AR-NNN rules
- States the impact of each resolved decision in plain language
- Clearly flags any decisions that are still blocking
- Does not invent decisions — only records what is in the source artifacts

## After producing the log

Tell the user:
1. The file has been saved to `docs/initiatives/<slug>/decision-log.md`
2. Re-run this prompt at any time to refresh — decisions change as the initiative progresses
3. This file is documentation only — editing it does not affect `state/open-decisions.md`
4. If this is a new initiative, add its nav block to `mkdocs.yml` under `Initiative Samples:` — see `generate-initiative-summary.md` for the exact block to add.
