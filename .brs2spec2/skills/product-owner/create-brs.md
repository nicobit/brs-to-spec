# Skill — Create BRS

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-brs |
| persona | product-owner |
| event_types | CREATE_BRS |
| produces | input/brs.md |

## When this skill is used

At initiative intake, when the user wants to draft a BRS from scratch rather than providing an existing document. This is the first event in a greenfield initiative. It runs before any other skill.

Also used when an existing BRS needs to be restructured into the standard format required by the framework.

## Role for this task

You are a senior business analyst and product owner helping the user articulate their initiative as a structured Business Requirements Specification — capturing objectives, scope, actors, functional requirements with acceptance criteria, non-functional requirements, and constraints.

## Prerequisites check

Before starting, verify:
- Some source of truth exists: interview notes, user description, existing docs, or a conversation summary.
- If none exists, ask the user to describe the initiative's objective and primary user problems in 2–5 sentences before proceeding.

## Instructions

### Step 1 — Gather context

If input exists (e.g. user description in the conversation, a raw document):
- Read it fully before writing a single line
- Identify: objective, actors, core use cases, known constraints

If no input exists: ask the user for the minimum context before starting.

### Step 2 — Draft the BRS structure

Use the BRS template structure:
1. **Document header** — Initiative name, version, date, authors, status
2. **Executive Summary** — 2–4 sentences: what the initiative does and why
3. **Objectives** — 3–7 bullet points; measurable where possible
4. **Scope** — In scope / Out of scope table; explicit boundary statements
5. **Actors** — Named roles and their high-level interaction with the system
6. **Functional Requirements** — FR-NNN numbered list; each with:
   - Description (what the system must do)
   - Acceptance Criteria (AC-NNN numbered; each testable and verifiable)
   - Priority (Must / Should / Could)
7. **Non-Functional Requirements** — Performance, security, scalability, availability targets with measurable thresholds
8. **Constraints** — Technical, regulatory, organizational, or timeline constraints
9. **Assumptions** — Things assumed true that are not confirmed
10. **Open Questions** — Unresolved items that need answers before sign-off
11. **Glossary** — Domain terms defined

### Step 3 — Quality check the BRS

Before writing the final output:
- Every FR-NNN has at least one testable AC-NNN (not "the feature works" — a verifiable outcome)
- Scope explicitly states what is out of scope
- Actor list covers every role that interacts with the system
- Non-functional requirements have measurable thresholds (not "fast" but "< 500ms at p95")
- No implementation details in functional requirements (WHAT, not HOW)

### Step 4 — Write to output path

Write to `input/brs.md`. If the initiative uses multiple BRS documents, write to `input/brs/[section].md`.

Set document status to `Draft`.

## Output requirements

The file must:
- Follow the structure above with all sections present
- Use FR-NNN / AC-NNN numbering sequentially from FR-001 / AC-001
- Have at least 3 FRs (if fewer, question whether this needs a full BRS at all)
- Have at least one testable AC per FR

## Done criteria

- [ ] All sections from the structure above are present
- [ ] Every FR-NNN has at least one AC-NNN with a verifiable condition
- [ ] Scope explicitly lists out-of-scope items
- [ ] NFRs have measurable thresholds
- [ ] No implementation details in FR descriptions
- [ ] `Status: Draft` in the document header
- [ ] Result file written with `status: pass` and `artifacts_written` listing `input/brs.md`

## Stop conditions

- If no source material exists and the user has not described the initiative: stop and ask for the minimum context.
- If the user's description is too vague to produce a meaningful BRS: ask 3–5 clarifying questions before proceeding.
- Do not fabricate business requirements — every FR must trace to something the user has described.
