# Prompt — Extract Architecture Draft from Word Document

Recommended environment:
- Microsoft 365 Copilot if the architecture document is in Word or SharePoint
- ChatGPT or another approved LLM if the Word content is pasted or uploaded
- GitHub Copilot Chat if the converted document is already in the repository

Owner:
- Architect / Tech Lead
- Business PO / BA can run the extraction, but an architect or tech lead must review it

Repository/code access needed:
- No for extraction
- Yes later for validation against existing implementation

Input:
- A Word architecture document
- Or copied/exported Word content
- Or a document stored in SharePoint / Teams, if using Microsoft 365 Copilot

Task:
Extract the content of the Word architecture document into a clean Markdown document that can be used as architecture input for the rest of the workflow.

Important rules:
- Do not summarize too aggressively.
- Do not invent architecture.
- Preserve original headings and section structure where possible.
- Preserve tables as Markdown tables.
- Preserve component names, system names, integration names, environment names, and technology names exactly as written.
- Preserve architecture decisions, assumptions, constraints, dependencies, risks, NFRs, security notes, data notes, deployment notes, and open questions.
- If diagrams or images are present, describe them briefly and mark them as "visual content from original document".
- If architecture diagrams are present, describe components, relationships, data flows, integrations, security boundaries, and environments.
- If content is unclear, keep it and mark it as unclear.
- Do not create requirements yet.
- Do not create user stories yet.
- Do not create implementation tasks yet.
- Do not convert the architecture into a final design; this is extraction only.

Output:
Create or update:

```text
features/<feature-name>/input/architecture-draft.md
```

Use this structure:

```markdown
# Architecture Draft — <Feature Name>

## Document Metadata
- Source document:
- Version:
- Date:
- Author:
- Architecture owner:
- Status:

## Extraction Notes
- Extraction date:
- Tool used:
- Manual architecture review needed: Yes / No

## Original Structure

Preserve the original headings and content from the Word document.

## Extracted Tables

Convert Word tables to Markdown tables.

## Visual Content / Diagrams

For each image, diagram, or embedded object:
- Location in document:
- Short description:
- Components shown:
- Relationships / flows shown:
- Security boundaries shown:
- Data stores shown:
- Needs manual review: Yes / No

## Components / Systems Mentioned

## Integrations Mentioned

## Data / Storage Notes

## Security / Authorization Notes

## Audit / Logging / Observability Notes

## Deployment / Environment Notes

## Architecture Decisions Found in Original Document

## Architecture Assumptions Found in Original Document

## Architecture Constraints Found in Original Document

## Architecture Risks Found in Original Document

## Open Questions Found in Original Document

## Unclear or Ambiguous Architecture Text

## Manual Review Checklist

- [ ] Headings preserved
- [ ] Tables preserved
- [ ] Components/systems preserved
- [ ] Integrations preserved
- [ ] Diagrams/images described
- [ ] Security notes preserved
- [ ] Data/storage notes preserved
- [ ] Deployment/environment notes preserved
- [ ] Architecture assumptions preserved
- [ ] Architecture constraints preserved
- [ ] Architecture risks preserved
- [ ] Open questions preserved
- [ ] No invented architecture added
```
