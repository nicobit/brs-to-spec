# Skill — Create Review Package

## Identity

| Field | Value |
|---|---|
| skill_id | dl-create-review-package |
| persona | delivery-lead |
| event_types | CREATE_REVIEW_PACKAGE |
| produces | review-package/ (folder) |

## When this skill is used

After handoff is complete (`specs/` exists with all story folders, or `standalone-delivery/` exists), or on demand when a stakeholder-friendly view of current initiative state is needed. May also be run earlier with partial artifacts — sections not yet available are marked as stubs.

## Role for this task

You are a senior business analyst and delivery lead assembling a complete, human-readable review package from all artifacts produced by the workflow — suitable for business stakeholders, architects doing governance sign-off, QA planning, and new team members onboarding.

The review package is a read-only presentation layer assembled from existing artifacts. Do not invent content not already present in source artifacts.

## Prerequisites check

Before starting, verify:
- [ ] `business-intake/business-intake-summary.md` exists (required — if missing, stop)
- [ ] `planning/delivery-structure.md` exists (required — if missing, stop)
- [ ] `architecture/architecture-review.md` exists (required for governance sign-off usecase)

Read ALL available inputs before writing any file.

## Instructions

### Step 1 — Read all available artifacts

Load in order:
1. `.flow/state/workflow-state.json` — determines which sections can be populated
2. `business-intake/business-intake-summary.md`
3. `business-analysis/requirements.md` (if exists)
4. `business-analysis/use-cases.md` (if exists — Mermaid diagram for readable rendering)
5. `business-analysis/use-cases/` (if exists — read all UC-NNN.md files)
6. `business-analysis/entity-model.md` (if exists)
7. `business-analysis/business-rules.md` (if exists)
8. `business-analysis/actors-and-personas.md` (if exists)
9. `business-analysis/process-flows.md` (if exists)
10. `input/brs.md` or `input/brs/*.md` (fallback context)
9. `planning/delivery-structure.md`
10. `.flow/state/open-decisions.md`
11. `architecture/architecture-review.md`
12. `architecture/architecture-rules.md`
13. `engineering-readiness/readiness-check.md` (if exists)
14. `quality-gates/data-contract.md`, `api-contract.md`, `security-review.md` (if exist)
15. `planning/traceability-matrix.md` (if exists)
16. All `specs/*/story.md` files (if specs/ exists)

### Step 2 — Generate output folder structure

```
review-package/
├── 00-intake/source-summary.md
├── 01-business-analysis/
│   ├── business-rules.md
│   ├── actors-and-personas.md
│   └── process-flows.md
├── 02-solution-analysis/
│   ├── entity-model.md
│   ├── architecture-impact.md
│   └── non-functional-requirements.md
├── 03-delivery-structure/
│   ├── use-cases.md
│   └── story-map.md
├── 04-specs/
│   ├── api-specification.md
│   ├── data-specification.md
│   └── security-specification.md
├── 05-validation/
│   ├── traceability-matrix.md
│   └── bdd-coverage.md
└── status.md
```

For each file:
- If the source artifact exists: copy verbatim (for gate artifacts) or generate from evidence (for assembled views)
- If the source artifact does not exist: write a stub with `<!-- Not yet available — requires: [stage] -->`
- Add header comment to copied artifacts identifying the source

### Step 3 — Generate unique files

Files that are assembled (not copied):
- `00-intake/source-summary.md` — business context, scope in/out, assumptions, glossary
- `03-delivery-structure/story-map.md` — epic → feature → story table from delivery-structure.md
- `02-solution-analysis/non-functional-requirements.md` — NFRs extracted and categorized
- `05-validation/bdd-coverage.md` — coverage table from specs/*/story.md BDD sections
- `status.md` — which sections are Complete / Partial / Stub

### Step 4 — Write status.md last

After all files are written, generate `status.md` reflecting actual completeness.

## Output requirements

All files in the review-package/ folder structure. Each file is either:
- **Complete**: populated from real source artifacts
- **Partial**: some sections filled, others stubbed due to missing upstream artifacts
- **Stub**: source artifact not yet available

## Done criteria

- [ ] All 12+ output files created (as Complete, Partial, or Stub)
- [ ] `status.md` exists and accurately reflects each section's completeness
- [ ] Copied artifacts have header comments but are otherwise verbatim
- [ ] Story-map.md derives exactly from delivery-structure.md (no added or removed stories)
- [ ] No content invented beyond source artifacts
- [ ] Result file written with `status: pass` and `artifacts_written` listing `review-package/` folder

## Stop conditions

- If both `business-intake-summary.md` and `delivery-structure.md` are missing: stop — the package cannot be assembled.
- Do not invent business context, actors, or requirements.
