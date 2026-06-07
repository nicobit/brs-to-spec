---
description: Create the engineering readiness check for the active deliverable.
---

# Create Engineering Readiness Check

Use:

```text
prompts/4-engineering-readiness/01-check-engineering-readiness.md
templates/engineering-readiness/readiness-check.md
```

Create `engineering-readiness/readiness-check.md`.

You must decide:

```text
Ready
Ready with risks
Not ready
```

You must also decide which Conditional Quality Gates are triggered.

For each triggered gate include:

```text
trigger evidence
risk if skipped
owner
required-before stage
output path
```

Do not call quality gates optional.
