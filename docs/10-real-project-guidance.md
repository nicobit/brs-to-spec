# Real Project Guidance

## Recommended baseline

Use this version as the baseline for real enterprise projects.

## How to avoid over-processing

Do not run every prompt.

Start with routing. Run only what the selected delivery mode requires.

## How to avoid shallow output

Do not skip engineering readiness.

The readiness check is the control point that decides whether extra gates are required.

## How to use without OpenSpec

Select execution mode:

```text
Standalone
```

Then create:

```text
standalone-delivery/D1-<deliverable-name>/
```

The standalone package must include scope, implementation plan, tasks, validation, and review.

## How to use with OpenSpec

Select execution mode:

```text
OpenSpec
```

Then create:

```text
openspec/changes/D1-<deliverable-name>/
```

## How to use with business users

Use Business Copilot mode only for intake and review.

Engineering execution should still be OpenSpec or standalone.
