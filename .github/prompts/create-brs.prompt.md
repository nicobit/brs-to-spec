---
description: Create or convert a Business Requirements Specification. Works from an existing document, bullet-point notes, or a structured interview starting from just an initiative name.
---

# Create Business Requirements Specification

Use:

```text
.brs2spec/0-intake/00-create-brs.md
templates/input/brs.md
```

## Three entry points — Copilot detects which to use

| What you provide | What happens |
|---|---|
| Existing document (Word export, Confluence, PDF text, email) | **Convert** — maps to BRS structure, assigns IDs, flags gaps |
| Bullet points or short notes | **Draft** — expands into BRS structure, flags what needs confirmation |
| Initiative name or one-liner | **Interview** — Copilot asks structured questions across 3 rounds, then generates |

## Output

```text
input/brs.md
```

## What Copilot produces

- Structured `input/brs.md` ready for the brs-to-spec routing stage
- FR-NNN / NFR-NNN / AC-NNN IDs assigned sequentially
- Gap report at the end — missing ACs, NFRs without targets, open questions, sections needing input
- In interview mode: 3 rounds of questions before generating — do not skip to generation

## After the BRS is created

Run the framework workflow — routing will pick up `input/brs.md` and begin the delivery flow.
