---
description: Correct a spec artifact when implementation or review reveals it was wrong — traces the fix back through affected artifacts.
---

# Spec Correction

Use this when a code review or implementation session reveals that an approved spec artifact (delivery-spec, tasks, architecture-rules, readiness-check) is wrong, incomplete, or inconsistent with what the code actually requires.

Follow:

```text
.brs2spec/9-reviewers/05-spec-correction.md
```

## Preconditions

You need:

```text
the finding ID from the review that triggered this correction
the review artifact that contains the finding (reviews/implementation/<file>.md)
```

## Output

```text
reviews/corrections/spec-correction-<finding-id>.md
```

Plus in-place updates to each affected artifact.

## Rule

Do not create shadow copies of corrected artifacts.

Update the originals and record what changed, why, and what downstream stages are affected.
