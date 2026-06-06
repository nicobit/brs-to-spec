# How to Run Business Intake in Microsoft 365 Copilot

## Goal

Use Microsoft 365 Copilot to process a large BRS and produce business-reviewed outputs in SharePoint.

## SharePoint folder structure

```text
<initiative-name>/
  00-source/
    BRS-original.docx
    Architecture-draft.docx optional
  01-business-intake/
    BRS-summary.docx
    Business-objectives.docx
    Business-requirements.docx
    Gaps-and-questions.docx
  02-planning/
    Delivery-slicing.docx
    Next-increment-scope.docx
  03-approval/
    Business-acceptance-expectations.docx
    Business-approval-checklist.docx
  04-it-handoff/
```

## Prompt execution order

Run these prompts from:

```text
prompts/12-business-copilot-intake/
```

in this order:

```text
01-create-brs-business-summary.md
02-extract-business-objectives.md
03-extract-business-requirements-for-review.md
04-identify-business-gaps-and-questions.md
05-create-business-delivery-slicing.md
06-select-next-increment-for-business-review.md
07-create-business-acceptance-expectations.md
08-create-business-approval-checklist.md
```

## Step-by-step

### Step 1 — Create BRS summary

Use:

```text
01-create-brs-business-summary.md
```

Save output to:

```text
01-business-intake/BRS-summary.docx
```

### Step 2 — Extract business objectives

Use:

```text
02-extract-business-objectives.md
```

Save output to:

```text
01-business-intake/Business-objectives.docx
```

### Step 3 — Extract requirements for review

Use:

```text
03-extract-business-requirements-for-review.md
```

Save output to:

```text
01-business-intake/Business-requirements.docx
```

Business must review and correct the output.

### Step 4 — Identify gaps/questions

Use:

```text
04-identify-business-gaps-and-questions.md
```

Save output to:

```text
01-business-intake/Gaps-and-questions.docx
```

### Step 5 — Create delivery slicing

Use:

```text
05-create-business-delivery-slicing.md
```

Save output to:

```text
02-planning/Delivery-slicing.docx
```

### Step 6 — Select next increment

Use:

```text
06-select-next-increment-for-business-review.md
```

Save output to:

```text
02-planning/Next-increment-scope.docx
```

### Step 7 — Create acceptance expectations

Use:

```text
07-create-business-acceptance-expectations.md
```

Save output to:

```text
03-approval/Business-acceptance-expectations.docx
```

### Step 8 — Create approval checklist

Use:

```text
08-create-business-approval-checklist.md
```

Save output to:

```text
03-approval/Business-approval-checklist.docx
```

## Repository mapping

| SharePoint output | Repository artifact |
|---|---|
| `BRS-summary.docx` | `business-intake/brs-summary.md` |
| `Business-objectives.docx` | input to `business-intake/epics-and-features.md` |
| `Business-requirements.docx` | `business-intake/requirements.md` |
| `Gaps-and-questions.docx` | `business-intake/gaps-and-questions.md` |
| `Delivery-slicing.docx` | `planning/delivery-slicing.md` |
| `Next-increment-scope.docx` | `planning/next-increment-scope.md` |
| `Business-acceptance-expectations.docx` | `business-intake/business-test-expectations.md` |
| `Business-approval-checklist.docx` | input to `handoff/spec-driven-handoff.md` |

## Rules

- Copilot output is draft until business reviews it.
- Do not create technical design in the business step.
- Do not create OpenAPI, DDD, infrastructure, CI/CD, or implementation tasks.
- For large BRS documents, detail only the next increment.
- Store approved outputs in SharePoint.
