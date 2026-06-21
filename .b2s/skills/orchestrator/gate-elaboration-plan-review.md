# Skill - Elaboration Plan Review Gate

## Purpose

This action represents the human review gate for `planning/elaboration-plan.md`.

## Instructions

Do not rewrite the artifact. Present the elaboration plan for human review, highlighting:

- The proposed wave ordering and rationale
- Parallel elaboration opportunities
- The Mermaid dependency diagram
- Any risks to the proposed order

Wait for one of these outcomes:

- approve the plan and allow progression to epic and story elaboration
- reject the plan and record what must be adjusted (wave ordering, dependencies, parallel groups)

## Rules

- Human approval is authoritative
- Do not self-accept on behalf of the reviewer
- If feedback is provided, keep it specific and tied to the elaboration plan content
- The human may request reordering of waves, different parallel groupings, or additional analysis

## Notes for the staged engine

- State changes for gate approval or rejection are handled outside this prompt
