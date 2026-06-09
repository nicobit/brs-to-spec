---
description: Create standalone delivery package when OpenSpec is not used.
---

# Create Standalone Delivery Package

Work inside the active initiative workspace.

Use:

```text
.brs2spec/5-handoff/02-create-standalone-delivery-package.md
templates/standalone-delivery/
```

## Preconditions

Before creating standalone handoff, verify:

```text
engineering-readiness/readiness-check.md exists
required quality gates are completed or explicitly accepted as risk
active deliverable is clear
```

## Output

Create:

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

Standalone mode must not be lower quality than OpenSpec mode.
