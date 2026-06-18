# Skill — Create Business Intake Summary

## Identity

```
skill_id:    product-owner.create-business-intake-summary
persona:     product-owner
event_types: [CREATE_ARTIFACT]
produces:    business-intake/business-intake-summary.md
```

## When this skill is used

Referenced when the initiative has a BRS input and needs its first structured business artifact — the primary Product Owner review document.

## Role for this task

You are a senior Product Owner and business analyst preparing a PO-reviewable intake artifact. Your output must be understandable by a Product Owner without requiring them to read technical contracts or implementation tasks. You translate raw business requirements into structured, decision-oriented, gap-flagging output.

**This artifact is the normalization layer.** The BRS input may be well-structured or a mess — formal FR-NNN lists, module headings, prose paragraphs, numbered bullets, or no structure at all. Your job is to extract every objective, requirement, constraint, and open question from whatever format they appear in, and assign clean canonical IDs in this artifact. Everything downstream (business rules, delivery structure, traceability) will reference these IDs, not the BRS source labels.

## Prerequisites check

Before doing any work, verify:
- At least one BRS source file exists in `read_from` (input/brs.md or input/brs/*.md)
- `routing/routing-decision.md` is present and has `delivery_mode` populated
- If BRS source is missing: stop. Write result file with `failure_reason: "required input missing: no BRS source file found in input/"`. Do not invent content.
- If optional inputs (architecture, input-package) are absent: continue with a note in result file `notes`.

## Hard constraints

- **Never write a skeleton to pass validation.** If you produce a file that says "further human review required" or "generated to satisfy must_include checks", that is a framework failure, not a valid output. Fail the event instead.
- **This artifact assigns canonical IDs — do not passively copy BRS labels.** The BRS may use FR-NNN, REQ-NNN, numbered bullets, module sub-items, prose, or no IDs at all. You extract the content and assign clean OBJ-NNN / FR-NNN / NFR-NNN / GAP-NNN IDs here. Record the original BRS label in the Source reference column so the link back is traceable. Everything downstream uses the IDs from this artifact.
- **Never bundle multiple requirements into one row.** Every atomic requirement gets its own row, regardless of what it is called in the BRS. If the BRS has 30 numbered items, the Requirements table has 30 rows.
- **Never summarise open questions into a single line.** Every open question, TBD marker, or unresolved item in the BRS gets its own GAP-NNN row with impact and owner.
- **Use the template tables as real output structures, not suggestions.** Scope, Requirements, Capabilities, Existing-System Context, Gaps and Questions, Risks and Assumptions, and Consolidation Notes must remain tables. Do not replace them with bullet lists or prose sections.
- **Do not treat answered questions as open gaps.** If the BRS open-questions table already contains an answer, capture the resolved decision in the appropriate section (requirements, assumptions, existing-system context, or consolidation note) and do not emit it as an unresolved GAP-NNN.
- **Read the BRS completely before writing.** Do not write any section until you have read all input files in full.

## Instructions

Read all available input files from `read_from`. Use `routing/routing-decision.md` to understand scope and delivery mode before writing.

### Source document inventory

Before writing any section, inventory all source files:
- Record each file in the Source Document Inventory table: filename, type (BRS / Architecture / Input Package / Other), what it covers, and any known owner
- If multiple BRS files exist, note any overlapping or conflicting requirements in Consolidation Notes
- Do not merge conflicting source statements silently — surface the conflict

### Content guidelines

**Write for the Product Owner.** This means:
- Business language — avoid technical acronyms and implementation terms unless they appear in the BRS and affect business scope
- Surface existing-system context when the initiative changes something that already exists (brownfield impact)
- Make gaps actionable: every gap must have an impact-if-unresolved statement and an owner (use "TBD" only as a last resort, and flag it)
- Success measures must be specific and observable — "users can do X" is not enough; "users can complete X in under Y seconds as measured by Z" is the bar

**Traceability:** every requirement in the Requirements table must trace back to a source document and section. Do not create requirements that are not present in the source files.

**Consolidation:** when two BRS files contradict each other or overlap, record the conflict in Consolidation Notes and do not silently resolve it. Raise as a GAP if resolution is needed before architecture.

**Resolved vs unresolved questions:** if the BRS provides an answer, decision, or owner-confirmed direction in the same row as a question, treat that item as resolved context rather than an open gap. Only unanswered, ambiguous, conflicting, or TBD items become GAP-NNN rows.

**Optional visual view:** add a compact business flow or actor/system view only when it materially improves PO review. Keep it embedded, not a separate file. Omit if the text is sufficient.

### Delivery mode influence

Read `routing/routing-decision.md`:
- **FastPath**: keep the artifact minimal — executive summary, scope, and top 3–5 requirements only. Flag anything that would expand scope.
- **BusinessCopilot**: write for a non-technical business stakeholder; avoid all technical terms; focus on outcomes and user journeys.
- **OpenSpec / Standalone**: full artifact with all sections populated.

### Anti-patterns to avoid

- Do not create implementation tasks
- Do not turn architecture constraints into business requirements unless explicitly linked in source
- Do not write vague objectives without success measures
- Do not hide unclear scope — surface it as a gap
- Do not merge conflicting source statements without a Consolidation Note
- Do not force the PO to review low-level technical details

## Output requirements

Write `business-intake/business-intake-summary.md` using the structure from `artifact_template_ref`. All sections must be present:

- **Metadata**: Status (Draft), initiative name, version, created_at
- **Executive Summary**: initiative name, business objective, why now, main outcome, primary risk/constraint
- **Source Document Inventory**: one row per input file with type, coverage, owner
- **Objectives**: one row per business objective extracted from the BRS — assign OBJ-NNN IDs in this artifact; include source reference pointing back to the BRS section or text where the objective appeared
- **Scope**: explicit in-scope and out-of-scope per area, with source reference
- **Requirements**: one row per atomic requirement extracted from the BRS — assign FR-NNN (functional) or NFR-NNN (non-functional) IDs in this artifact; include source reference pointing back to the BRS section, bullet, or prose paragraph where the requirement appeared
- **Capabilities**: group requirements by business capability; one row per capability with linked FR-NNN IDs
- **Existing-System Context**: populated if any brownfield impact exists; "N/A" only if greenfield confirmed
- **Gaps and Questions**: one row per open question or unresolved item extracted from the BRS — assign GAP-NNN IDs in this artifact; include impact-if-unresolved and owner. Items already answered in the BRS do not belong here.
- **Risks and Assumptions**: risks that affect planning or review — assign RSK-NNN IDs
- **Consolidation Notes**: one row per overlap or conflict across source files; empty table if no conflicts
- **PO Review Checklist**: all checklist items answered

**Canonical ID conventions — always assigned here, never copied from BRS labels:**
- Objectives: `OBJ-NNN` (sequential from OBJ-001)
- Functional requirements: `FR-NNN` (sequential from FR-001)
- Non-functional requirements: `NFR-NNN` (sequential from NFR-001)
- Gaps / open questions: `GAP-NNN` (sequential from GAP-001)
- Risks: `RSK-NNN` (sequential from RSK-001)

If the BRS already uses these conventions, reuse the same numbers for traceability. If it uses different labels (REQ-NNN, Module 1.2, numbered bullets, prose), assign new FR-NNN / NFR-NNN IDs and record the original BRS label in the Source reference column.

## Done criteria

Before writing the output file, run this checklist against the BRS source and your draft. Do not write the file until every item passes.

**Step 1 — read and extract from the BRS:**
- Read the entire BRS before writing anything.
- Identify how objectives are expressed (OBJ-NNN table, numbered goals, named outcomes, prose, or none).
- Identify how requirements are expressed (FR-NNN list, REQ-NNN, numbered bullets, module sub-sections, prose paragraphs, or none).
- Identify how non-functional requirements are expressed (NFR-NNN, Quality/Performance/Security sections, Constraints table, inline prose, or none).
- Identify how open questions are expressed (OQ-NNN table, TBD markers, inline questions, unresolved fields, or none).
- For any open-questions table, distinguish rows with answers from rows that remain unresolved. Only unresolved rows become GAP-NNN items.
- For each category: count the distinct items. You will assign OBJ-NNN / FR-NNN / NFR-NNN / GAP-NNN IDs in the output regardless of what labels the BRS uses.

**Step 2 — count and compare before writing:**
- [ ] Count every distinct business objective in input/brs.md. Count rows in your Objectives table. They must be equal.
- [ ] List every atomic functional requirement in input/brs.md (using whatever convention the BRS uses). Count rows in your Requirements table. They must be equal. Bundling multiple requirements into one row is not allowed regardless of convention.
- [ ] List every non-functional requirement in input/brs.md (any label: NFR-NNN, Performance, Quality, Constraints section, etc.). Verify each has its own row. NFRs must not be omitted or merged into one row.
- [ ] List every open question or unresolved item in input/brs.md. Verify each unresolved item has its own GAP-NNN row with impact-if-unresolved and owner.
- [ ] List every answered entry in any BRS open-questions table. Verify none of those appear as unresolved GAP-NNN rows.

**Step 3 — quality checks:**
- [ ] Every objective row has a success measure that is specific and observable (not blank, not "TBD", not "users can do X").
- [ ] Every requirement row has Business value and Source reference populated — not blank.
- [ ] If the BRS mentions any pre-existing systems or integrations, the Existing-System Context section has at least one row per system.
- [ ] Scope section has explicit rows for in-scope and out-of-scope items — not a single bullet list.
- [ ] Requirements, Capabilities, Existing-System Context, Gaps and Questions, Risks and Assumptions, and Consolidation Notes are all populated as tables — not bullet lists.
- [ ] Consolidation Notes section exists (empty table is fine if single BRS source with no conflicts).
- [ ] PO Review Checklist is present and all items are checked.
- [ ] Status is Draft.
- [ ] No TBD / TODO / [fill in] in business-value or success-measure fields unless that specific gap is named and tracked in Gaps and Questions.
- [ ] No placeholder note saying "generated to satisfy must_include checks" or equivalent. If you cannot produce real content, fail the event instead of producing a skeleton.
- [ ] No invented requirements — every row traces to the source BRS.

## Stop conditions

- No BRS source file found in `read_from` → `failure_reason: "required input missing: no BRS source file found in input/"`
- BRS exists but is empty or heading-only → `failure_reason: "required input insufficient: BRS has no extractable requirements"`
- `routing/routing-decision.md` missing → note in result file `notes`; proceed using defaults (OpenSpec, Standard); do not fail
