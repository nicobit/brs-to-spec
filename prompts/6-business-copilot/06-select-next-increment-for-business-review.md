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
- Canonical prompt: `prompts/06-planning/02-select-next-increment-scope.md`
- Repository mapping: `planning/next-increment-scope.md`

# Prompt — Select Next Increment for Business Review

Based on the delivery slicing, define the next increment scope.

Return:
1. Increment name
2. Increment goal
3. Business value
4. Included requirements
5. Excluded/deferred requirements
6. Candidate user stories to create later
7. Key acceptance expectations
8. Open questions
9. Risks
10. Ready for IT review? Yes / No / Yes with risks

Rules:
- Do not create technical design.
- Do not create implementation tasks.
- Keep scope realistic.
