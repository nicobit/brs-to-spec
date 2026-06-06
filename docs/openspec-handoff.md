# OpenSpec Handoff

This project deliberately separates business intake from engineering execution.

## Source of truth rule

Before engineering starts:

```text
Business Intake = source of business truth
```

During implementation:

```text
OpenSpec Change = source of implementation truth
```

Business intake should not be maintained as a second competing implementation spec.

## Handoff mapping

| Business / contract artifact | OpenSpec artifact |
|---|---|
| `business-intake/requirements.md` | `proposal.md` and `specs/` |
| `business-intake/user-stories.md` | `proposal.md` / scenarios |
| `business-intake/gaps-and-questions.md` | resolved before `tasks.md` |
| `engineering-contracts/technical-spec.md` | `design.md` |
| `engineering-contracts/bdd-scenarios.md` | `specs/` and tests |
| `engineering-contracts/test-strategy.md` | `design.md` test section |
| `engineering-contracts/traceability-matrix.md` | governance evidence |
| `openspec-change/tasks.md` | Copilot implementation tasks |

## Handoff checklist

- Business PO approved the user stories.
- Critical gaps are resolved.
- Technical design has been reviewed.
- Security and audit rules are clear.
- Tasks are small and testable.
- OpenSpec `proposal.md`, `design.md`, and `tasks.md` are aligned.
