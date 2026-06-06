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
- Canonical prompt: `prompts/01-business-intake/01-summarize-brs.md`
- Repository mapping: `business-intake/brs-summary.md`

# Prompt — Create BRS Business Summary

Read the selected BRS document and create a business summary.

Return:
1. Executive summary
2. Business context
3. Business objectives
4. In-scope areas
5. Out-of-scope areas
6. Key stakeholders
7. Key assumptions
8. Important dates or target quarters if mentioned
9. Major risks or unclear points

Rules:
- Use business language.
- Do not create technical design.
- Do not invent information.
- Mark missing information as “Not specified in the BRS”.
