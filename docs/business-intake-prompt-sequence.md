# Business Intake Prompt Sequence

The canonical business intake sequence is:

```text
00a-extract-brs-from-word.md
00b-extract-architecture-from-word.md
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
07-create-business-test-expectations.md
```

## What each step does

| Step | Prompt | Purpose | Output |
|---:|---|---|---|
| 00a | `00a-extract-brs-from-word.md` | Extract Word BRS into Markdown | `input/brs-original.md` |
| 00b | `00b-extract-architecture-from-word.md` | Extract Word architecture into Markdown | `input/architecture-draft.md` |
| 01 | `01-summarize-brs.md` | Summarize the BRS | `business-intake/brs-summary.md` |
| 02 | `02-extract-requirements.md` | Extract structured requirements from the BRS | `business-intake/requirements.md` |
| 03 | `03-review-brs-and-requirements-against-architecture.md` | Compare original BRS + extracted requirements against the architecture draft | `business-intake/brs-architecture-alignment.md` |
| 04 | `04-create-delivery-structure.md` | Create business objectives, epics, features/capabilities | `business-intake/epics-and-features.md` |
| 05 | `05-create-user-stories.md` | Create user stories and acceptance criteria | `business-intake/user-stories.md` |
| 06 | `06-find-gaps-and-questions.md` | Consolidate business, requirement, architecture, delivery, QA, and enablement gaps | `business-intake/gaps-and-questions.md` |
| 07 | `07-create-business-test-expectations.md` | Create business-level UAT/test expectations | `business-intake/business-test-expectations.md` |

## Critical rule

Run the architecture alignment step before creating the delivery structure:

```text
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
```

## Why step 03 must run before step 04

Step 03 produces:

```text
business-intake/brs-architecture-alignment.md
```

This artifact identifies BRS items missing from extracted requirements, requirements not supported by architecture, architecture constraints, contradictions, missing architecture decisions, security/data/integration/audit gaps, deployment/environment gaps, and questions for business, architecture, QA, platform, SRE, and deployment.

Step 04 must use those findings before creating epics/features/capabilities.

## When can step 03 be skipped?

Only when all of these are true:

```text
There is no architecture draft.
The change is small.
There is no infrastructure, integration, data, security, deployment, or NFR impact.
The skip is explicitly documented in gaps-and-questions.md or the change-size assessment.
```

If there is an architecture draft, run step 03 before step 04.
