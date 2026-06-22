# Scope and Boundaries

## Script-owned responsibilities

Scripts should own:

- workspace root resolution
- event-template loading and runtime instantiation
- `read_from` resolution and glob expansion
- machine-written `read_evidence`
- queue transitions across `pending`, `processing`, `done`, and `failed`
- integrity checks for orphan event/result combinations
- result-file contract checks
- count and placeholder checks for selected artifact types
- workflow-state and event-log updates
- repair and reset mechanics

## Prompt-owned responsibilities

Prompts should own:

- reading the machine-prepared input bundle
- writing the target artifact content
- explaining genuine semantic gaps
- making business-analysis judgments
- creating natural-language summaries of mechanical failures

## Anti-goals

This phase should not:

- replace artifact generation with scripts
- push business reasoning into code
- add a monolithic engine before the small commands are proven
- rely on prompts to reconstruct queue or state truth from prose

## Key enforcement rule

If a question can be answered by reading files and applying deterministic rules,
the answer should come from a script, not from the model.
