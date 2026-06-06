# Prompt — Extract BRS from Word Document

Recommended environment:
- Microsoft 365 Copilot if the BRS is in Word or SharePoint
- ChatGPT or another approved LLM if the Word content is pasted or uploaded
- GitHub Copilot Chat if the converted document is already in the repository

Owner:
- Business PO / BA

Repository/code access needed:
- No

Input:
- A Word Business Requirements Specification document
- Or copied/exported Word content
- Or a document stored in SharePoint / Teams, if using Microsoft 365 Copilot

Task:
Extract the content of the Word BRS into a clean Markdown document that can be used as the stable input for the rest of the workflow.

Important rules:
- Do not summarize too aggressively.
- Do not invent or complete missing information.
- Preserve the original business intent.
- Preserve original headings and section structure where possible.
- Preserve numbered requirements if they exist.
- Preserve tables as Markdown tables.
- Preserve business rules, assumptions, constraints, dependencies, risks, and open questions.
- Preserve role names and system names exactly as written.
- If diagrams or images are present, describe them briefly and mark them as "visual content from original document".
- If content is unclear, keep it and mark it as unclear.
- Do not create epics yet.
- Do not create user stories yet.
- Do not create technical design yet.
- Do not create implementation tasks yet.

Output:
Create or update:

```text
features/<feature-name>/input/brs-original.md
```

Use this structure:

```markdown
# Original BRS — <Feature Name>

## Document Metadata
- Source document:
- Version:
- Date:
- Author:
- Business owner:
- Status:

## Extraction Notes
- Extraction date:
- Tool used:
- Manual verification needed: Yes / No

## Original Structure

Preserve the original headings and content from the Word document.

## Extracted Tables

Convert Word tables to Markdown tables.

## Visual Content / Diagrams

For each image, diagram, or embedded object:
- Location in document:
- Short description:
- Relevant business meaning:
- Needs manual review: Yes / No

## Business Rules Found in Original Document

List business rules only if they are explicitly present in the original document.

## Assumptions Found in Original Document

List assumptions only if they are explicitly present in the original document.

## Constraints Found in Original Document

List constraints only if they are explicitly present in the original document.

## Dependencies Found in Original Document

List dependencies only if they are explicitly present in the original document.

## Open Questions Found in Original Document

List open questions only if they are explicitly present in the original document.

## Unclear or Ambiguous Text

List parts of the BRS that were unclear during extraction.

## Manual Review Checklist

- [ ] Headings preserved
- [ ] Tables preserved
- [ ] Business rules preserved
- [ ] Assumptions preserved
- [ ] Constraints preserved
- [ ] Dependencies preserved
- [ ] Open questions preserved
- [ ] Diagrams/images described
- [ ] No invented requirements added
```

## Example instruction for Microsoft 365 Copilot

```text
Read this Word BRS and extract it into clean Markdown.

Preserve the original headings, numbering, tables, business rules, assumptions, constraints, dependencies, risks, and open questions.

Do not rewrite it into user stories.
Do not create epics or features.
Do not create technical design.
Do not invent missing content.

Use the structure from prompts/01-business-intake/00a-extract-brs-from-word.md.
```
