# How to Run Business Intake in Microsoft 365 Copilot

## Goal

Let business users process the BRS in Microsoft 365 and save reviewed outputs in SharePoint.

## SharePoint structure

```text
<initiative-name>/
  00-source/
    BRS-original.docx
    Architecture-draft.docx optional
  01-business-intake/
  02-planning/
  03-approval/
  04-it-handoff/
```

## Prompt order

Use:

```text
prompts/6-business-copilot/
```

Recommended order:
1. `01-create-brs-business-summary.md`
2. `02-extract-business-objectives.md`
3. `03-extract-business-requirements-for-review.md`
4. `04-identify-business-gaps-and-questions.md`
5. `05-create-business-delivery-slicing.md`
6. `06-select-next-increment-for-business-review.md`
7. `07-create-business-acceptance-expectations.md`
8. `08-create-business-approval-checklist.md`

## IT handoff

IT later maps approved SharePoint outputs to:
- `input/brs.md`,
- `business-intake/business-intake-summary.md`,
- `planning/delivery-increments.md`,
- OpenSpec handoff.
