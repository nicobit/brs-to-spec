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
- Canonical prompt: `prompts/06-planning/01-create-delivery-slicing-and-roadmap.md`
- Repository mapping: `planning/delivery-slicing.md`

# Prompt — Create Business Delivery Slicing

Using the BRS summary, extracted requirements, and gaps/questions, propose an initial delivery slicing.

Assume the BRS may span more than one quarter.

Return:
1. MVP / first valuable increment
2. Increment 1 scope
3. Increment 2 scope
4. Future scope
5. Items that should not be started yet
6. Key dependencies
7. Open questions that block slicing
8. Recommended next increment

Rules:
- Do not create detailed user stories for the whole BRS.
- Detail only the next increment at a high level.
- Mark dependencies and blockers clearly.
