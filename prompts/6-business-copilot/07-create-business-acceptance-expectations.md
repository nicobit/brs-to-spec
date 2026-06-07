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
- Canonical prompt: `prompts/01-business-intake/07-create-business-test-expectations.md`
- Repository mapping: `business-intake/business-test-expectations.md`

# Prompt — Create Business Acceptance Expectations

Based on the BRS, requirements, and next increment scope, create business acceptance expectations.

Return:
- Acceptance expectation ID
- Related requirement
- Business scenario
- Expected outcome
- Negative / exception cases
- Evidence expected
- Business owner
- Priority

Rules:
- Keep this business-readable.
- Do not create technical test automation.
- Mark unclear acceptance expectations as questions.
