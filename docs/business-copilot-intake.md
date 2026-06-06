# Business Copilot Intake

This folder contains a parallel, business-facing prompt set for Microsoft 365 Copilot and Copilot Studio.

These prompts are **wrappers** of the canonical framework prompts. They do not replace the repository prompts.

## Purpose

Business users can run the early BRS intake using:

```text
Microsoft 365 Copilot
Microsoft 365 Copilot Agent Builder
Copilot Studio
Word
SharePoint
Teams
```

The outputs are business-readable documents and tables that can be stored in SharePoint and later mapped into the repository framework artifacts.

## Prompt mapping

| Business Copilot prompt | Canonical framework prompt |
|---|---|
| `01-create-brs-business-summary.md` | `prompts/01-business-intake/01-summarize-brs.md` |
| `02-extract-business-objectives.md` | `prompts/01-business-intake/04-create-delivery-structure.md` |
| `03-extract-business-requirements-for-review.md` | `prompts/01-business-intake/02-extract-requirements.md` |
| `04-identify-business-gaps-and-questions.md` | `prompts/01-business-intake/06-find-gaps-and-questions.md` |
| `05-create-business-delivery-slicing.md` | `prompts/06-planning/01-create-delivery-slicing-and-roadmap.md` |
| `06-select-next-increment-for-business-review.md` | `prompts/06-planning/02-select-next-increment-scope.md` |
| `07-create-business-acceptance-expectations.md` | `prompts/01-business-intake/07-create-business-test-expectations.md` |
| `08-create-business-approval-checklist.md` | handoff readiness / approval quality gate |

## Important rule

The business-facing prompts must not drift from the canonical framework prompts.

Each business prompt includes:
- source framework mapping,
- Microsoft 365 / Copilot Studio execution context,
- SharePoint output target,
- repository mapping.

## Ownership

Business owns the BRS interpretation, business objectives, requirements review, priorities, initial slicing, and approval.

IT/engineering owns architecture alignment, technical spec, architecture contracts, enablement, handoff, and downstream execution.
