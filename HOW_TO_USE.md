# How to Use This Framework

Practical, step-by-step usage. Run only the steps your delivery mode needs.

## Step 0 — Prepare inputs

If your sources are Word, SharePoint, Confluence, or unstructured text, normalize
them first.

```text
prompts/0-input-preparation/01-convert-brs-word-to-markdown.md
prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md
prompts/0-input-preparation/03-normalize-input-package.md
```

Outputs:

```text
input/brs.md
input/initial-architecture.md
input/input-package.md
```

If there is no architecture document, create `input/initial-architecture.md` and
mark it `No initial architecture document provided.`

## Step 1 — Select delivery mode (and execution mode)

```text
prompts/1-routing/01-select-delivery-mode.md
```

Pick a **delivery mode** (Fast / Standard / Enterprise / Enterprise + Modular)
and an **execution mode**:

```text
Execution Mode A — OpenSpec   (default)
Execution Mode B — Standalone (no OpenSpec)
Execution Mode C — Business Copilot (business users in M365)
```

## Step 2 — Create business intake summary

```text
prompts/2-business-intake/01-create-business-intake-summary.md
→ business-intake/business-intake-summary.md
```

This is the single artifact the Product Owner reviews.

## Step 3 — Review initial architecture

```text
prompts/3-planning-and-modular-delivery/02-review-initial-architecture.md
prompts/3-planning-and-modular-delivery/03-create-global-architecture-rules.md
→ architecture/initial-architecture-review.md
→ architecture/global-architecture-rules.md
```

## Step 4 — Plan delivery (modular only if needed)

```text
prompts/3-planning-and-modular-delivery/01-create-delivery-structure.md
```

Add modular delivery only for large initiatives:

```text
prompts/3-planning-and-modular-delivery/04-identify-software-modules.md
prompts/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md
prompts/3-planning-and-modular-delivery/06-define-delivery-increments.md
prompts/3-planning-and-modular-delivery/07-create-traceability-matrix.md
```

## Step 5 — Check engineering readiness

```text
prompts/4-engineering-readiness/01-check-engineering-readiness.md
→ engineering-readiness/readiness-check.md
```

The readiness check fills the **Conditional Quality Gates** table and decides
which gates are triggered.

## Step 6 — Run required conditional quality gates

Run only the gates the readiness check marked **Triggered** (then they are
mandatory):

```text
prompts/4-engineering-readiness/02-identify-required-quality-gates.md
prompts/4-engineering-readiness/quality-gates/<gate>.md
→ quality-gates/<gate>.md
```

## Step 7A — Create OpenSpec change (Execution Mode A)

```text
prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md
→ openspec/changes/D1-<deliverable-name>/
    proposal.md
    design.md
    tasks.md
```

## Step 7B — Or create standalone delivery package (Execution Mode B)

```text
prompts/5-handoff/03-create-standalone-delivery-package.md
→ standalone-delivery/D1-<deliverable-name>/
    delivery-spec.md
    implementation-plan.md
    tasks.md
    validation-plan.md
    review-checklist.md
```

Use exactly one of 7A or 7B per deliverable.

## Step 8 — Implement / validate / review

Implement the active deliverable only, run the validation defined in tasks, and
satisfy every triggered quality gate before merge or release.

## Delivery modes at a glance

### Fast Path
Already engineering-ready. Go straight to Step 7A or 7B.

### Standard Path
Run Step 0 (if needed), Step 2, then Step 7A/7B.

### Enterprise Path
Run Steps 0–3, Step 5, required gates (Step 6), then Step 7A/7B.

### Enterprise + Modular Delivery
Run Steps 0–7 in full, including modular planning in Step 4.

## Execution Mode C — Business Copilot

Business users can run the early intake in Microsoft 365 Copilot / SharePoint /
Word / Teams / Copilot Studio:

```text
prompts/6-business-copilot/
docs/04-business-copilot/
```

This feeds the same planning, then engineering continues in Mode A or Mode B.

## Product Owner experience

Review one artifact:

```text
business-intake/business-intake-summary.md
```

POs do not manage module technical specs, API contracts, implementation tasks,
OpenSpec tasks, or low-level test automation.

## Engineering experience

Engineering receives a compact package:

```text
input/brs.md
input/initial-architecture.md
business-intake/business-intake-summary.md
architecture/initial-architecture-review.md
architecture/global-architecture-rules.md
planning/delivery-increments.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
```

Then engineering creates the OpenSpec change (7A) or the standalone package (7B).

## Scaffold a workspace

```text
python tools/scripts/new_feature.py my-feature --mode standard --execution-mode openspec
python tools/scripts/new_feature.py my-feature --mode enterprise --execution-mode standalone
python tools/scripts/new_feature.py my-feature --mode enterprise-modular --execution-mode openspec
```

## Important rules

- Do not generate tasks for all deliverables at once.
- Do not create both an OpenSpec change and a standalone package for the same
  deliverable.
- Do not ignore the initial architecture document.
- Do not use Modular Delivery for small changes.
- Conditional Quality Gates are not optional once triggered.
