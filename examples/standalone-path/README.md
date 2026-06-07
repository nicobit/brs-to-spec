# Standalone Path Example (Execution Mode B)

Same discipline as the OpenSpec path, but OpenSpec is not used. The framework's
`standalone-delivery/` tree is the source of truth for execution.

```text
input/brs.md
input/initial-architecture.md
business-intake/business-intake-summary.md
architecture/initial-architecture-review.md
architecture/global-architecture-rules.md
planning/delivery-increments.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
standalone-delivery/D1-create-onboarding-request/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

Scaffold it with:

```text
python tools/scripts/new_feature.py onboarding --mode enterprise --execution-mode standalone
```
