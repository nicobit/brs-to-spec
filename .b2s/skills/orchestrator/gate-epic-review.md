# Skill - Epic Review Gate

## Purpose

This action represents the human review gate for the epic folders under `epics/`.

## Instructions

Do not rewrite the artifacts. Present the epic folder structure for human review.

When presenting the gate, you MUST surface:

> **Epic Elaboration Summary:**
> - Total epics: N
> - Total stories: N
> - Stories with 2+ acceptance criteria: N
> - Stories with open questions: N
> - Not Ready stories: N
> - Unknown requirement references: N
> - Requirement title mismatches: N
> - Coverage gaps or semantic drift warnings: N

For each epic, summarise: title, wave, story count, and any blocking dependencies or open questions.

Then wait for one of these outcomes:

- **approve** — accept the epic folders and mark the workflow complete
- **reject** — record what must be corrected (missing stories, weak AC, unresolved dependencies)

## Rules

- Human approval is authoritative
- Do not self-accept on behalf of the reviewer
- If feedback is provided, keep it specific and tied to the artifact content

## Notes for the staged engine

- State changes for gate approval or rejection are handled outside this prompt
