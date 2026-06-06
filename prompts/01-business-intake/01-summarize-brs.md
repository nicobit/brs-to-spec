# Prompt 01 — Summarize BRS for Business Intake

Recommended environment:
- Microsoft 365 Copilot if the BRS is in Word or SharePoint
- ChatGPT or another approved LLM if the BRS is exported as text
- GitHub Copilot Chat if the BRS already exists in the repository

Owner:
- Business PO / BA

Input:
- `features/<feature-name>/input/brs-original.md`
- Or the Word BRS content provided in the approved business tool

Task:
Create a concise business summary of the BRS.

Rules:
- Do not invent missing content.
- Preserve business wording where useful.
- Highlight unclear or contradictory parts.
- Identify the main business outcome.
- Identify the main users and processes.
- Identify potential regulatory, audit, reporting, or approval aspects.

Output:
Create `features/<feature-name>/business-intake/brs-summary.md`.

Structure:

```markdown
# BRS Summary

## Source
- Original document:
- Version/date:
- Author/owner:

## Business Context

## Business Objective

## Process Summary

## Key Users / Roles

## Key Business Rules

## Main Functional Areas

## Main Non-Functional Expectations

## Data Involved

## Integrations / Dependencies

## Audit / Reporting / Compliance Notes

## Assumptions

## Open Questions

## Items That Need Business Confirmation
```

## Prerequisite

If the source is a Word document, first run:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

This creates:

```text
features/<feature-name>/input/brs-original.md
```

Then use this prompt to summarize the extracted BRS.
