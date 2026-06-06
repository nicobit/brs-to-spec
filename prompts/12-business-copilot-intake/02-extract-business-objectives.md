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
- Canonical prompt: `prompts/01-business-intake/04-create-delivery-structure.md`
- Repository mapping: input to `business-intake/epics-and-features.md`

# Prompt — Extract Business Objectives

Read the selected BRS and extract the business objectives.

Return a table with:
- Objective ID
- Business objective
- Business value
- Stakeholder / beneficiary
- Related BRS section
- Priority if mentioned
- Notes / assumptions

Rules:
- Do not invent objectives.
- Separate objectives from implementation details.
- Mark unclear objectives as questions.
