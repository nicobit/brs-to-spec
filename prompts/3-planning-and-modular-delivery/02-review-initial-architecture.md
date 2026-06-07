# Prompt — Review Initial Architecture

## Purpose

Review the initial architecture document against the BRS and business intake summary.

This creates the bridge between the given architecture and all downstream planning.

## Inputs

Use:
- `input/brs.md`
- `input/initial-architecture.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md` if available.

## Output file

```text
architecture/initial-architecture-review.md
```

## Output structure

```markdown
# Initial Architecture Review

## 1. Architecture Source Summary

## 2. Architecture Constraints Identified

| Constraint ID | Constraint | Source section | Applies to | Notes |
|---|---|---|---|---|

## 3. Architecture Decisions Already Taken

| Decision ID | Decision | Source | Impact |
|---|---|---|---|

## 4. BRS Alignment

| BRS area / requirement | Architecture support | Gap / conflict | Owner |
|---|---|---|---|

## 5. Missing Architecture Information

| Missing item | Why it matters | Owner | Blocking? |
|---|---|---|---|

## 6. Conflicts Between BRS and Architecture

| Conflict ID | Description | Impact | Decision needed |
|---|---|---|---|

## 7. Constraints to Propagate

List the constraints that must be inherited by global architecture rules, modules, deliverables, engineering readiness, and OpenSpec.

## 8. Open Architecture Decisions
```

## Rules

- Do not invent architecture.
- Preserve explicit constraints.
- If there is no initial architecture document, mark architecture review as incomplete.
- If the initial architecture defines a constraint, do not override it unless marked as conflict or open decision.
