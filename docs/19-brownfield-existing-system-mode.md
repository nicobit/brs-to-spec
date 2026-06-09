# Brownfield / Existing-System Mode

## Purpose

Use this mode when the initiative changes an existing solution rather than creating a largely new one.

This is not a second framework.

It is a stronger way to surface existing-system risk early inside the current initiative workflow.

## What this mode emphasizes

Brownfield work often needs earlier visibility on:

```text
current architecture constraints
affected components or modules
compatibility and regression risk
data migration or schema sensitivity
API contract impact
deployment or rollback impact
existing operational dependencies
existing behavior that must remain stable
```

## Recommended artifact

When existing-system impact is material, create:

```text
architecture/existing-system-impact.md
```

Use:

```text
templates/planning-and-modular-delivery/existing-system-impact.md
```

This artifact is lightweight.

It exists to summarize brownfield impact, not to create a second architecture process.

## Recommended sequence

1. Normalize inputs.
2. Create business intake.
3. Create `architecture/existing-system-impact.md` when existing-system impact is meaningful.
4. Review architecture.
5. Create delivery structure.
6. Run readiness with explicit brownfield evidence.

## What should become visible early

At minimum, surface:

- existing-system context summary
- affected components or modules
- compatibility and regression risk
- contract and schema impact
- existing behavior that must remain stable
- rollout / rollback sensitivity
- operational dependencies

## Important rule

Do not use brownfield mode to make the framework heavier for every initiative.

Use it when existing-system impact is real enough that ignoring it would create delivery or operational risk.
