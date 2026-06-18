# Prompt — Extract Actors and Personas

## Role

You are a business analyst extracting every human actor and system actor from the BRS and business intake artifacts.

## When to use

After `business-intake/business-intake-summary.md` is complete. Run before architecture review so that actor-boundary decisions are grounded in named actors with explicit permissions.

## Inputs

1. `input/brs.md` or `input/brs/*.md` — roles, personas, authorization rules, integration requirements
2. `business-intake/business-intake-summary.md` — scope boundaries, requirements summary
3. `business-intake/business-rules.md` — if exists; BR-NNN rules where category = security or role-based
4. `input/architecture.md` — if exists; integration points identify system actors

## Output path

```text
business-analysis/actors-and-personas.md
```

## Template

Use:

```text
.brs2spec/templates/review-package/01-business-analysis/actors-and-personas.md
```

## Generation rules

### Human actors

- Source: BRS roles/personas section; "As a {{role}}" patterns in any user story language in the BRS; explicit authorization sections
- Assign ACT-NNN IDs sequentially in order of first appearance
- For each actor: name, one-line description, primary goals (what they want to achieve), permissions/access level
- Do not invent actors not present in the BRS — if a role is implied but unnamed, use the implied name and flag it with `<!-- inferred — confirm with PO -->`

### System actors

- Source: BRS integration requirements; `input/architecture.md` integration points
- Assign SYS-NNN IDs sequentially
- For each: name, system type (API / Queue / DB / File / IdP / etc.), direction (Inbound / Outbound / Both), protocol
- Only include systems this initiative directly integrates with — not the entire ecosystem

### Actor × feature matrix

- Leave stub rows at this stage — features are not yet confirmed
- Add a note: `<!-- Feature column to be filled after delivery-structure.md is confirmed (stage 9) -->`

### Authorization boundaries

- Derive from: BR-NNN rules where category = security or role-based; BRS "only X can", "X is not allowed to", "requires role Y" language
- If no authorization rules exist yet: leave the table with one stub row and a note

## Quality bar

- Every named role in the BRS maps to exactly one ACT-NNN row — no silently dropped roles
- Every external system mentioned in BRS integration requirements maps to a SYS-NNN row
- ACT-NNN IDs are sequential with no gaps
- No actors invented beyond what BRS content supports

## Anti-patterns to avoid

- Inventing actors from general domain knowledge ("surely there's an Admin role") not present in the BRS
- Merging two distinct roles into one actor because they seem similar
- Omitting system actors because "that's architecture's concern" — system actors are part of the business boundary

## Stop conditions

If `input/brs.md` is missing or has no roles/personas section and no "As a" language: write a stub with a note listing what is missing and what the PO must provide.

## Self-review checklist

- [ ] Every named role in the BRS appears as an ACT-NNN row
- [ ] Every external system in BRS integration requirements appears as a SYS-NNN row
- [ ] Authorization boundary table populated from BR-NNN or BRS language (not invented)
- [ ] No actors without a BRS source reference
