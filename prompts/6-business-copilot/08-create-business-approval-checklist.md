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
- Canonical artifacts: handoff readiness and quality gates
- Repository mapping: input to `handoff/spec-driven-handoff.md`

# Prompt — Create Business Approval Checklist

Create a business approval checklist for this BRS intake.

Return:
1. Business summary approved? Yes/No
2. Requirements reviewed? Yes/No
3. Priorities confirmed? Yes/No
4. Out-of-scope items confirmed? Yes/No
5. MVP / first increment confirmed? Yes/No
6. Open business questions assigned? Yes/No
7. Blocking questions resolved? Yes/No
8. Ready for IT architecture alignment? Yes/No
9. Approval owners
10. Approval date

Rules:
- Use a table format suitable for Word or SharePoint.
- Do not claim approval unless explicitly provided by the business owner.
