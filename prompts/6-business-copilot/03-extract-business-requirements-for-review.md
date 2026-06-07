# Business Copilot Prompt

Execution environment:
- Microsoft 365 Copilot
- Microsoft 365 Copilot Agent Builder
- Copilot Studio

Output target:
- Word / SharePoint / Teams / business review document

Important:
This is a business-facing wrapper of a canonical framework prompt. It does not replace the repository prompt.


Framework mapping:
- Canonical prompt: `prompts/01-business-intake/02-extract-requirements.md`
- Repository mapping: `business-intake/requirements.md`

# Prompt — Extract Business Requirements for Review

Read the selected BRS document and extract the business requirements.

Return a table with:
- Requirement ID
- Requirement statement
- Requirement type: functional, non-functional, regulatory, data, reporting, operational, process, security, audit
- Business priority if mentioned
- Source section or evidence from the BRS
- Ambiguity or clarification needed
- Suggested owner for clarification

Rules:
- Do not invent requirements.
- Split combined requirements if they contain multiple obligations.
- Mark duplicates.
- Mark contradictions.
- Use clear business language.
