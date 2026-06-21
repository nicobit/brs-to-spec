# Skill - Requirements Review Gate

## Purpose

This action represents the human review gate for requirements artifacts:

- `requirements/atomic-requirements.md`
- `requirements/open-questions.md`
- `requirements/assumptions.md`

## Instructions

Do not rewrite the artifacts. Present the existing requirements, open questions, and assumptions for human review and wait for one of these outcomes:

- approve the artifacts and allow progression to domain analysis
- reject the artifacts and record what must be corrected

## Rules

- Human approval is authoritative
- Do not self-accept on behalf of the reviewer
- If feedback is provided, keep it specific and tied to the artifact content

## Notes for the staged engine

- State changes for gate approval or rejection are handled outside this prompt
