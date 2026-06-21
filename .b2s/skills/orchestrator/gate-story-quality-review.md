# Skill - Story Quality Review Gate

## Purpose

This action represents the human review gate for `quality/story-quality-review.md`.

## Instructions

Do not rewrite the artifact. Present the story quality review results for human review.

When presenting the gate, you MUST prominently surface the pass/fail summary before asking for a decision:

> **Story Quality Summary:**
> - Total stories reviewed: N
> - Passed: N
> - Failed: N
> - High risk: N
>
> **Most common failure reasons:** (list the top 2-3)

If all stories failed, explicitly warn:
> **Warning:** No stories passed all quality checks. Approving will proceed to BDD generation for all stories regardless of failures.

Then wait for one of these outcomes:

- **approve** — accept the review and proceed to BDD generation for all stories (including failed ones)
- **reject** — record what must be corrected before re-review

## Rules

- Human approval is authoritative
- Do not self-accept on behalf of the reviewer
- If feedback is provided, keep it specific and tied to the artifact content
- Approving means ALL stories proceed to BDD — there is no partial approval

## Notes for the staged engine

- State changes for gate approval or rejection are handled outside this prompt
