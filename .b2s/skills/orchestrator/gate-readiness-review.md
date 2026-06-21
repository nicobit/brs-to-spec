# Skill - Readiness Review Gate

## Purpose

This action represents the human review gate for `review/readiness-report.md`.

## Instructions

Do not rewrite the artifact. Present the readiness report, ready stories, and blocked stories for human review and wait for one of these outcomes:

- approve the readiness assessment and allow progression to dispatch
- reject the assessment and record what must be corrected
- approve partially (accept some stories, block others)

## Rules

- Human approval is authoritative
- Do not self-accept on behalf of the reviewer
- If feedback is provided, keep it specific and tied to the artifact content
- Blocked stories must have clear resolution paths before proceeding

## Notes for the staged engine

- State changes for gate approval or rejection are handled outside this prompt
