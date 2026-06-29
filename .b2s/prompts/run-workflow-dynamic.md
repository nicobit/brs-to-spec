# `.b2s` Run Dynamic Workflow

## Purpose

This prompt is the experimental runner for `b2s-dynamic`.

It follows the same core engine contract as the normal workflow runner:

- the CLI remains the source of truth for state
- artifacts remain the source of truth for work products
- validators remain mandatory

The difference is conceptual:

- `run-workflow.md` is staged and deterministic
- `run-workflow-dynamic.md` is intended for loop-oriented orchestration

## Current Scope

This prompt currently supports the `b2s-dynamic` scaffold only.

That means:

- it is safe to load and use with the dynamic workflow type
- it does not yet introduce custom shared runtime selector behavior
- it must not change how other workflow prompts behave

## Operating Rule

For now, use the same engine discipline as the staged runner:

1. read workflow state
2. run `next-step`
3. read selected action and inputs
4. execute only the selected action
5. validate
6. update state
7. continue until stop, gate, or completion

## Dynamic Intent

When using this prompt, favor the following mindset while still obeying the
engine-selected action:

- assess unresolved gaps explicitly
- justify next-action selection clearly
- record stop or continue reasoning explicitly
- keep orchestration memory in dynamic orchestration artifacts

## Safety Rules

- Do not bypass the CLI
- Do not bypass validation
- Do not modify prompts or templates outside the selected action contract
- Do not infer that this prompt changes behavior for other workflow types

## Note

This file is intentionally narrow. The full dynamic orchestration behavior is
expected to come later through isolated engine support, not by changing shared
workflow prompts.
