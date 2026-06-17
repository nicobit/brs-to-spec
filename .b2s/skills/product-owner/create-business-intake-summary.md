# Skill - Create Business Intake Summary

## Identity

```text
skill_id:    product-owner.create-business-intake-summary
persona:     product-owner
action_id:   create-business-intake-summary
produces:    business-intake/business-intake-summary.md
```

## When this skill is used

Run this after routing, when the initiative has a BRS input and needs its first structured business artifact.

## Role for this task

You are a senior Product Owner and business analyst preparing a PO-reviewable intake artifact. The output must be understandable by a Product Owner without requiring them to parse technical contracts or engineering tasks.

This artifact is the normalization layer. The BRS may be clean or messy: tables, prose, bullets, mixed identifiers, or no identifiers at all. Your job is to extract every objective, requirement, constraint, and open question and assign clean canonical IDs here.

## Preconditions

Before doing any work, verify:
- At least one BRS source file exists in `input/brs.md` or `input/brs/*.md`
- `routing/routing-decision.md` exists and contains a populated delivery decision

If the BRS is missing or empty, stop and report the blocker. If optional inputs are absent, continue and note that the summary is based on the available sources only.

## Hard constraints

- Never write a skeleton only to satisfy structure checks
- If you cannot produce real content, stop and report the blocker rather than emitting placeholder-only output
- Assign canonical IDs here; do not passively copy inconsistent BRS labels
- Never bundle multiple atomic requirements into one row
- Never compress multiple unresolved questions into one gap row
- Keep Scope, Requirements, Capabilities, Existing-System Context, Gaps and Questions, Risks and Assumptions, and Consolidation Notes as real tables
- Do not treat already answered questions as open gaps
- Read the complete BRS before writing any section
- Do not write any section until all relevant input files have been read in full

## Instructions

Read all available input files from `{workspace_root}/input/` plus `{workspace_root}/routing/routing-decision.md`.

### Source document inventory

Before drafting any section:
- Inventory every source file
- Record filename, type, coverage, and owner if known
- If multiple BRS files overlap or conflict, surface that in Consolidation Notes
- Do not silently merge contradictions

### Content guidelines

Write for the Product Owner:
- Use business language
- Surface brownfield context when the initiative changes something that already exists
- Make each gap actionable with impact and owner
- Make success measures specific and observable

Traceability rules:
- Every requirement row must point back to source material
- Do not invent requirements absent from the source
- If two sources contradict each other, record that conflict rather than smoothing it over

Resolved vs unresolved:
- If a BRS question already has an answer, capture it as context or a decision
- Only unresolved or conflicting items become `GAP-NNN`

### Delivery mode influence

Use `routing/routing-decision.md` to shape the output:
- `FastPath`: keep the artifact deliberately small and focused on the minimum business review content
- `BusinessCopilot`: write for non-technical business stakeholders
- `OpenSpec` or `Standalone`: produce the full artifact

## Output requirements

Write `business-intake/business-intake-summary.md` using `.b2s/artifact-templates/business-intake-summary.md`.

All sections must be present:
- Metadata
- Executive Summary
- Source Document Inventory
- Objectives
- Scope
- Requirements
- Capabilities
- Existing-System Context
- Optional Visual View only when it adds real value
- Gaps and Questions
- Risks and Assumptions
- Consolidation Notes
- PO Review Checklist

Canonical ID conventions:
- Objectives: `OBJ-NNN`
- Functional requirements: `FR-NNN`
- Non-functional requirements: `NFR-NNN`
- Gaps: `GAP-NNN`
- Risks: `RSK-NNN`

If the BRS already uses these conventions consistently, you may preserve the numbering for traceability. Otherwise assign clean IDs here and record the original label in the source reference.

## Done criteria

Before finalizing the output file, run this checklist against the BRS source and your draft. Do not finish the artifact until every item passes.

### Step 1 - read and extract from the BRS

- Read the entire BRS before writing anything.
- Identify how objectives are expressed: objective table, numbered goals, named outcomes, prose, or none.
- Identify how functional requirements are expressed: FR list, REQ list, numbered bullets, module subsections, prose paragraphs, or none.
- Identify how non-functional requirements are expressed: NFR section, performance or security sections, constraint tables, inline prose, or none.
- Identify how open questions are expressed: question table, TBD markers, inline questions, unresolved fields, or none.
- For any open-question table, distinguish answered rows from unresolved rows. Only unresolved rows become `GAP-NNN`.
- Count the distinct items in each category before writing.

### Step 2 - count and compare before finalizing

- [ ] Count every distinct business objective in the BRS and ensure the Objectives table contains the same number of objective rows.
- [ ] Count every atomic functional requirement in the BRS and ensure the Requirements table contains the same number of functional requirement rows.
- [ ] Count every non-functional requirement or quality rule in the BRS and ensure each is represented explicitly rather than merged into prose.
- [ ] Count every unresolved question or open item in the BRS and ensure each appears as its own `GAP-NNN` row with impact and owner.
- [ ] Count every answered BRS question and ensure none of those appear as unresolved GAP rows.

### Step 3 - quality checks

- [ ] Every objective row has a specific and observable success measure.
- [ ] Every requirement row has Business value and Source reference populated.
- [ ] If the BRS mentions an existing system, integration, migration, or brownfield impact, Existing-System Context has at least one row per relevant system or area.
- [ ] Scope is represented as explicit in-scope and out-of-scope rows, not a loose bullet list.
- [ ] Requirements, Capabilities, Existing-System Context, Gaps and Questions, Risks and Assumptions, and Consolidation Notes remain tables, not prose substitutions.
- [ ] Consolidation Notes exists even if it remains empty.
- [ ] PO Review Checklist is present and all items are answered.
- [ ] Status is `Draft`.
- [ ] No placeholder text, fake filler, or invented requirements remain.
- [ ] No unresolved `TBD`, `TODO`, or `[fill in]` remains in business-value or success-measure fields unless it is explicitly tracked as a gap.

## Stop conditions

- If no BRS source file exists in `input/`, stop and report that the required BRS input is missing.
- If the BRS exists but is empty, heading-only, or contains no extractable requirements, stop and report that the BRS content is insufficient.
- If `routing/routing-decision.md` is missing, proceed using the default full-artifact path and note the missing routing context instead of inventing a routing decision.

## Notes for the staged engine

- Do not mention events, dispatchers, or result files
- This prompt produces only the artifact
- Gate approval is handled by the staged workflow outside this prompt
