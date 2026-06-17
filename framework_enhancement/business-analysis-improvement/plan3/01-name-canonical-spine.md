# Step 1 — Name the Canonical Spec Spine

## Purpose

Create `.brs2spec2/spec-anchoring.md` as a named framework principle document, and update `artifact-ownership.md` to formally classify canonical vs. support artifacts.

## Prerequisites

Step 0 (`00-spec-anchoring-principles.md`) read and understood. No framework files need to be read before running this step — the content is specified below.

## Run this prompt

```text
Read the design anchor first:
- framework_enhancement/business-analysis-improvement/plan3/00-spec-anchoring-principles.md
  Focus on Principle 1 (canonical vs. support) and Principle 2 (summary vs. canonical).

Read the current framework file:
- .brs2spec2/workflow/artifact-ownership.md

Then make the following changes:

--- Create .brs2spec2/spec-anchoring.md ---

Create a new file at .brs2spec2/spec-anchoring.md with the following content and structure:

# BRS-to-Spec v2 — Spec-Anchoring Principle

## What this file is

This file defines the canonical specification spine for brs-to-spec v2.
It is a framework principle document — not an artifact template, not an event template.
The dispatcher and all persona skill prompts must treat the declarations here as authoritative.

## The Canonical Spec Spine

The following four artifact groups are the canonical specification of what an initiative must deliver.
They are execution-driving: all downstream phases must read them first and must not contradict them.

| # | Artifact | Path | Produced by | Canonical status |
|---|---|---|---|---|
| 1 | Requirements catalog | `business-analysis/requirements.md` | EVT-TPL-043 | CANONICAL |
| 2 | Entity model | `business-analysis/entity-model.md` | EVT-TPL-030 | CANONICAL |
| 3 | Use-case diagram (PlantUML) | `business-analysis/use-cases.puml` | EVT-TPL-044 | CANONICAL |
| 3 | Use-case diagram (Mermaid) | `business-analysis/use-cases.md` | EVT-TPL-044 | CANONICAL (co-produced) |
| 4 | Use-case specs (per file) | `business-analysis/use-cases/UC-NNN.md` | EVT-TPL-007 | CANONICAL |

These are the only artifacts from which implementation work may be derived without explicit justification.

## Support Artifacts

The following artifacts support the canonical spine. They are produced alongside it and consumed by
downstream phases as supplementary context. They do not drive implementation and cannot substitute
for the canonical set.

| Artifact | Path | Supports | Role |
|---|---|---|---|
| Business intake summary | `business-intake/business-intake-summary.md` | requirements.md | Source material for FR derivation; background context once requirements.md exists |
| Business rules | `business-analysis/business-rules.md` | use-cases/UC-NNN.md | Constraint annotations derived from FR-NNN; feeds exception paths in UC specs |
| Actors and personas | `business-analysis/actors-and-personas.md` | use-cases.puml, UC-NNN.md | Actor catalog derived from use-cases.puml; must not precede it |
| Process flows | `business-analysis/process-flows.md` | use-cases/UC-NNN.md | Cross-UC journey synthesis; does not replace per-UC behavioral specs |
| Gaps and questions | `business-analysis/gaps-and-questions.md` | requirements.md | Gap catalog; blocking gaps prevent delivery structure from starting |
| Business test expectations | `business-intake/business-test-expectations.md` | requirements.md | PO-level expectations; not a substitute for BDD scenarios |

## Enforcement Rules

1. Any event template that requires a canonical artifact as input must list it under `inputs.required`.
2. Any event template where a canonical artifact exists must demote `business-intake-summary.md` to `inputs.optional`.
3. No downstream event template may reference `business-intake-summary.md` as its primary requirements source when `requirements.md` is available.
4. Planning (EVT-TPL-011) must verify that no blocking gap in `gaps-and-questions.md` lacks a stated assumption before proceeding.
5. Every story in `delivery-structure.md` must cite at least one UC-NNN or FR-NNN source.
6. Every handoff task must cite at least one FR-NNN and UC-NNN source.

## Traceability Chain

The authoritative spec-to-implementation traceability chain for this framework:

```
FR-NNN (requirements.md)
  → BR-NNN (business-rules.md)          annotates constraint rules on FRs
  → UC-NNN (use-cases/UC-NNN.md)        specifies behavioral realization of FRs
  → F-NNN.X story (delivery-structure)  decomposes UC into deliverable stories
  → AC-NNN (delivery-structure)         acceptance criteria per story
  → SCN-NNN (BDD scenarios)             executable test of AC-NNN
  → TC-NNN (test plans)                 unit-level branch coverage of BR-NNN
  → tasks / coding-prompt               implementation anchored to AC-NNN + AR-NNN
```

Any artifact that skips a link in this chain must document why.

--- Update .brs2spec2/workflow/artifact-ownership.md ---

In Section 1 (Artifact ownership by persona), add a CANONICAL marker column:

Add a new column "Spec role" to the table header:
| Artifact path pattern | Owner persona | Spec role | Notes |

Then set "Spec role" values as follows for business-analysis rows:
- `business-analysis/requirements.md` → CANONICAL
- `business-analysis/entity-model.md` → CANONICAL
- `business-analysis/use-cases.puml` → CANONICAL
- `business-analysis/use-cases.md` → CANONICAL (co-produced)
- `business-analysis/use-cases/*` → CANONICAL
- `business-intake/business-intake-summary.md` → SUPPORT
- `business-analysis/business-rules.md` → SUPPORT
- `business-analysis/actors-and-personas.md` → SUPPORT
- `business-analysis/process-flows.md` → SUPPORT
- `business-analysis/gaps-and-questions.md` → SUPPORT
- `business-intake/business-test-expectations.md` → SUPPORT
- All other rows → leave Spec role blank (not business-analysis scope)

Add a note at the top of Section 1:
# CANONICAL artifacts drive implementation. SUPPORT artifacts annotate and supplement.
# See .brs2spec2/spec-anchoring.md for the full principle.
```

## Done when

- `.brs2spec2/spec-anchoring.md` exists and contains the canonical spine table, support artifact table, enforcement rules, and traceability chain
- `artifact-ownership.md` has a Spec role column with CANONICAL / SUPPORT values for all business-analysis rows
- A cross-reference note in `artifact-ownership.md` points to `spec-anchoring.md`
