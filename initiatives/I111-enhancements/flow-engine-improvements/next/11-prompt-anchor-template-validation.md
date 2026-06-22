# Prompt 11 - Anchor Template Validation Rules

## Goal

Strengthen template-level `must_include` items so prompts must explicitly reason
about counts and identifiers, while scripts later verify those claims.

## Files to review and modify

Review the event templates that create:

- business-intake summaries
- requirements catalogs
- other artifacts where row or ID completeness matters

## Required changes

Replace vague rules such as:

- "requirements section has one row per atomic requirement"
- "covers non-functional requirements"
- "no placeholder text in output"

with anchored rules such as:

- enumerate all FR IDs in the output, enumerate all FR IDs in the source, compare counts, list missing IDs
- enumerate all NFR IDs in the output, enumerate all NFR IDs in the source, compare counts, list missing IDs
- quote any line containing placeholder markers, or state explicitly that none were found

## Important constraint

Do not treat this template change as sufficient by itself. It complements script
validation; it does not replace it.

## Verification

Verify:

1. the updated `must_include` items are explicit and count-anchored
2. they name the source artifact that acts as truth
3. they do not reduce the existing schema clarity
