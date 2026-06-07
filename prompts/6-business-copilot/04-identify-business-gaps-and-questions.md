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
- Canonical prompt: `prompts/01-business-intake/06-find-gaps-and-questions.md`
- Repository mapping: `business-intake/gaps-and-questions.md`

# Prompt — Identify Business Gaps and Questions

Review the BRS and the extracted requirements.

Create a list of gaps, assumptions, contradictions, and open questions.

Return a table with:
- ID
- Type: gap, assumption, contradiction, missing information, decision needed
- Description
- Why it matters
- Owner: Business, IT, Architecture, QA, Legal/Compliance, Operations
- Blocks delivery? Yes/No
- Suggested next action

Rules:
- Focus on business clarification.
- Do not create implementation tasks.
