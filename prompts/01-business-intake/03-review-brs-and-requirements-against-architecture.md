# Prompt 03 — Review BRS and Requirements Against Architecture Draft

Recommended environment:
- VS Code Copilot Chat if the repository and architecture context are available
- ChatGPT or another approved LLM if the BRS, requirements, and architecture Markdown are provided
- Microsoft 365 Copilot can be used if both source documents are in Word/SharePoint, but engineering must review the output

Owner:
- Architect / Tech Lead
- Business PO / BA can support
- QA should review the resulting gaps for testability

Repository/code access needed:
- No for document-level alignment
- Yes if validating against existing codebase or current architecture

Input files:
- `features/<feature-name>/input/brs-original.md`
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/input/architecture-draft.md`

Task:
Compare the original BRS and the extracted requirements against the architecture draft.

Purpose:
The BRS is the primary source of business intent.  
The extracted requirements are the structured interpretation of the BRS.  
The architecture draft is used as a constraint, feasibility, dependency, and risk input.

Important rules:
- Do not invent business requirements from architecture.
- Do not let the architecture document override the BRS silently.
- Check whether the requirements correctly represent the BRS.
- Check whether the architecture supports, contradicts, constrains, or leaves unclear each major requirement.
- If the BRS and architecture conflict, create a contradiction or question.
- If the requirements missed something important from the BRS, flag it.
- Use the architecture document to identify constraints, dependencies, risks, NFR implications, security implications, data implications, integration implications, deployment implications, and audit/logging implications.
- Mark whether each question is for Business, Architecture, QA, Security, Delivery, Platform, or SRE.
- Mark whether each issue blocks implementation.

Output:
Create:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Use this structure:

```markdown
# BRS, Requirements, and Architecture Alignment Review

## 1. Summary

Short summary of whether the BRS, extracted requirements, and architecture draft appear aligned.

## 2. BRS Items Potentially Missing from Requirements

| ID | BRS item | Missing or weak requirement coverage | Why it matters | Owner |
|---|---|---|---|---|

## 3. Architecture Constraints Relevant to Requirements

| ID | Constraint | Source in architecture | Affected BRS / requirement | Impact |
|---|---|---|---|---|

## 4. Requirements Supported by Architecture

| Requirement | Architecture support | Notes |
|---|---|---|

## 5. Requirements Not Clearly Supported by Architecture

| Requirement | Missing or unclear architecture support | Why it matters | Owner |
|---|---|---|---|

## 6. Contradictions Between BRS / Requirements and Architecture

| ID | BRS or requirement says | Architecture says | Why it matters | Severity | Owner |
|---|---|---|---|---|---|

## 7. Missing Architecture Decisions

| ID | Missing decision | Why it matters | Affected requirement/story | Owner | Blocks implementation? |
|---|---|---|---|---|---|

## 8. Data / Integration Gaps

| ID | Gap | Affected requirement | Impact | Owner |
|---|---|---|---|---|

## 9. Security / Authorization Gaps

| ID | Gap | Affected requirement | Impact | Owner |
|---|---|---|---|---|

## 10. Audit / Logging / Observability Gaps

| ID | Gap | Affected requirement | Impact | Owner |
|---|---|---|---|---|

## 11. NFR / Performance / Availability Implications

| ID | Implication | Source | Impact | Owner |
|---|---|---|---|---|

## 12. Deployment / Environment / Configuration Gaps

| ID | Gap | Impact | Owner |
|---|---|---|---|

## 13. Questions for Business

| ID | Question | Why it matters | Related requirement | Severity |
|---|---|---|---|---|

## 14. Questions for Architecture / Tech Lead

| ID | Question | Why it matters | Related requirement | Severity |
|---|---|---|---|---|

## 15. Questions for QA / Testing

| ID | Question | Why it matters | Related acceptance criteria or test area | Severity |
|---|---|---|---|---|

## 16. Questions for Platform / SRE / Deployment

| ID | Question | Why it matters | Related enablement area | Severity |
|---|---|---|---|---|

## 17. Recommended Updates

List recommended updates to:
- `requirements.md`
- `epics-and-features.md`
- `user-stories.md`
- `gaps-and-questions.md`
- `technical-spec.md`
- enablement artifacts, if needed
```

When to run:
Run this after:

```text
00a-extract-brs-from-word.md
00b-extract-architecture-from-word.md
01-summarize-brs.md
02-extract-requirements.md
```

and before:

```text
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
```

For small changes, this step can be lightweight.  
For medium and large/risky changes, it is strongly recommended.

## Position in the sequence

Run this prompt after:

```text
02-extract-requirements.md
```

and before:

```text
04-create-delivery-structure.md
```

Required core order:

```text
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
```
