---
description: Create the engineering readiness check for the active deliverable.
---

# Create Engineering Readiness Check

Work inside the active initiative workspace.

Use:

```text
.brs2spec/4-engineering-readiness/01-check-engineering-readiness.md
templates/engineering-readiness/readiness-check.md
```

Create `engineering-readiness/readiness-check.md` inside that initiative workspace.

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
