# Overview

This framework is an adaptive enterprise BRS-to-delivery-readiness framework. It
transforms a raw BRS plus an initial architecture document into
business-approved, architecture-aligned delivery increments.

OpenSpec is the **default** engineering downstream, but standalone execution is
fully supported when OpenSpec is not used.

## Problem

OpenSpec works well when the engineering change is clear.

But enterprise BRS documents are often:
- business-heavy,
- ambiguous,
- multi-stakeholder,
- multi-system,
- architecture-sensitive,
- too large for one AI coding context.

## Solution

The framework converts:

```text
BRS + initial architecture
```

into:

```text
business-approved, architecture-aligned, OpenSpec-ready delivery increments
```

## Output

The final engineering output depends on the execution mode.

Execution Mode A — OpenSpec (default):

```text
openspec/changes/<active-deliverable>/
  proposal.md
  design.md
  tasks.md
```

Execution Mode B — Standalone (when OpenSpec is not used):

```text
standalone-delivery/<active-deliverable>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

See `docs/08-execution-modes.md`.
