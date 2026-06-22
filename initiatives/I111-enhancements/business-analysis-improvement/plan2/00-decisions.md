# Business Analysis Improvement — Locked Design Decisions

Produced by Step 0 execution. No `.brs2spec2` files were modified.
This file is the authoritative design anchor for Steps 1–9.

---

## Decision 1 — Naming Convention

**Confirmed: all artifact names use hyphens. Underscores are rejected.**

The AIUP reference design used `entity_model.md`, `use_cases.puml`, and `use_cases/UC-*.md`.
These forms are **not adopted**. The framework naming standard is hyphen-separated throughout,
consistent with every existing artifact in `.brs2spec2/artifact-templates/` and `artifact-ownership.md`.

| AIUP reference (rejected) | Framework name (adopted) |
|---|---|
| `entity_model.md` | `entity-model.md` |
| `use_cases.puml` | `use-cases.puml` |
| `use_cases/UC-*.md` | `use-cases/UC-*.md` |

All source prompts under `framework_enhancement/business-analysis-improvement/prompts/` have been
corrected to use hyphen naming before execution of Step 1.

---

## Decision 2 — New Canonical Artifacts

The following new artifacts are introduced by this improvement:

| Artifact | Full path in initiative workspace | Status |
|---|---|---|
| Requirements catalog | `business-analysis/requirements.md` | New — does not exist yet |
| Use-case diagram (PlantUML) | `business-analysis/use-cases.puml` | New — does not exist yet |
| Use-case diagram (Mermaid/markdown) | `business-analysis/use-cases.md` | New — does not exist yet |
| Use-case specs (per file) | `business-analysis/use-cases/UC-NNN.md` | New — replaces monolithic file |

The following existing artifact retains its path unchanged:

| Artifact | Full path | Status |
|---|---|---|
| Entity model | `business-analysis/entity-model.md` | Existing — inputs and classification change; path unchanged |

**Note on `use-cases.md`:** this file is produced in parallel with `use-cases.puml` by the same event.
It contains the same diagram as a Mermaid `graph LR` block embedded in markdown, for GitLab Pages
rendering and IDE preview. Both files must carry identical `UC-NNN` IDs. The `.puml` file is for
tooling; the `.md` file is for human review.

---

## Decision 3 — Deprecated Artifacts

`business-analysis/use-case-spec.md` is **deprecated**.

Disposition for existing initiatives:

- Existing initiatives that already have `use-case-spec.md` **keep it as-is**. It is not deleted or split automatically.
- A migration note will be added to each such initiative workspace in Step 8, stating that
  `use-case-spec.md` is deprecated and that future UC work should use `use-cases/UC-NNN.md`.
- No automatic splitting of existing monolithic files. Manual or initiative-level step only.

---

## Decision 4 — Compatibility Strategy

**Chosen: immediate cutover.**

Rationale:
- The current framework has no production initiatives that depend on `use-case-spec.md` as a hard input
  to a running event. The monolithic file is an end-state artifact consumed by downstream templates,
  not a mid-workflow dependency.
- Dual-read adds complexity in every downstream event template indefinitely. A clean cutover
  is easier to maintain and removes the risk of inconsistent reads.

Consequence:
- All downstream event template references to `business-analysis/use-case-spec.md` must be updated
  in Step 7 before any initiative attempts to use the redesigned flow end to end.
- Step 8 adds migration notes to existing workspaces but does not change the framework to support both.

---

## Decision 5 — Architecture Overlap

**Confirmed: architecture may start after the following minimum baseline:**

1. `business-intake/business-intake-summary.md` — complete
2. `business-analysis/requirements.md` — complete
3. `business-analysis/gaps-and-questions.md` — draft state acceptable

This is a change from the current workflow where `REVIEW_INITIAL_ARCHITECTURE` (EVT-TPL-008)
is `blocked_by_stage: "2b-business-analysis"` — which means it currently waits for ALL
business-analysis events to complete.

The new dependency will be encoded in `workflow-definition.yaml` in **Step 3**, after Steps 1 and 2
have wired `requirements.md` and `use-cases.puml` into the workflow.

Current state observed in `workflow-definition.yaml`:
```yaml
- template: EVT-TPL-008-review-initial-architecture
  blocked_by_stage: "2b-business-analysis"
```

Target state after Step 3:
```yaml
- template: EVT-TPL-008-review-initial-architecture
  blocked_by_event:
    - EVT-TPL-043-create-requirements
    - EVT-TPL-005-find-gaps-and-questions
```

---

## Decision 6 — Entity Model Classification

**Confirmed: `entity-model.md` is promoted to a first-class business-analysis artifact.**

Current state: `EVT-TPL-030` lives in stage `2c-optional-business-analysis` with condition
`"ENTITY_MODEL in optional_artifacts_requested or DATA_CONTRACT in quality_gates_triggered"`.
This makes it purely opt-in.

Target state:
- Entity model moves to stage `2b-business-analysis`, running in parallel with `use-cases.puml`,
  `business-rules.md`, and `gaps-and-questions.md` after `requirements.md` is complete.
- It remains **conditional (not hard-blocking)** for non-data initiatives — it does not block
  architecture review or planning when the initiative has no meaningful domain data.
- It becomes a **hard prerequisite for `data-contract.md`** regardless of initiative type.

**Ownership decision:** remains with **architect** persona, consistent with current
`artifact-ownership.md` entry. The entity model is business-level (not a database schema) but its
structural analysis is an architect-led activity in this framework. No ownership change.

---

## Decision 7 — Process-Flows Position

**Confirmed: `process-flows.md` moves from upstream generator to downstream synthesis artifact.**

Current state: `EVT-TPL-006` is triggered by `CREATE_ACTORS_AND_PERSONAS` (`on_success`), and
`EVT-TPL-007` (use-case specs) is triggered by `CREATE_PROCESS_FLOWS` (`on_success`). This means
process flows currently run before use-case specs — they are an upstream input to UC creation.

Target state:
- Process flows run **after** `use-cases/UC-*.md` and `actors-and-personas.md` are complete.
- New required inputs: `business-analysis/use-cases/UC-*.md` and `business-analysis/actors-and-personas.md`.
- Process flows become cross-UC journey synthesis, not BRS-derived swimlanes.
- This removes the `on_success` chain: `CREATE_ACTORS_AND_PERSONAS` → `CREATE_PROCESS_FLOWS` → `CREATE_USE_CASE_SPECS`.
- The new chain is: `CREATE_USE_CASE_DIAGRAM` → `CREATE_USE_CASE_SPECS` (and `CREATE_ACTORS_AND_PERSONAS`) → `CREATE_PROCESS_FLOWS`.

---

## Summary Table — New Event Dependencies

| Event | New blocked_by | Notes |
|---|---|---|
| `CREATE_REQUIREMENTS_CATALOG` (EVT-TPL-043) | `CREATE_BUSINESS_INTAKE_SUMMARY` | New event |
| `CREATE_USE_CASE_DIAGRAM` (EVT-TPL-044) | `CREATE_REQUIREMENTS_CATALOG` | New event, produces both `.puml` and `.md` |
| `CREATE_ENTITY_MODEL` (EVT-TPL-030) | `CREATE_REQUIREMENTS_CATALOG` | Moved from stage 2c to 2b |
| `CREATE_BUSINESS_RULES` (EVT-TPL-003) | `CREATE_REQUIREMENTS_CATALOG` | Was blocked by stage 2-business-intake |
| `FIND_GAPS_AND_QUESTIONS` (EVT-TPL-005) | `CREATE_REQUIREMENTS_CATALOG` | Was blocked by stage 2-business-intake |
| `CREATE_ACTORS_AND_PERSONAS` (EVT-TPL-004) | `CREATE_USE_CASE_DIAGRAM` | Was blocked by stage 2-business-intake |
| `CREATE_USE_CASE_SPECS` (EVT-TPL-007) | `CREATE_USE_CASE_DIAGRAM` | Was triggered by CREATE_PROCESS_FLOWS |
| `CREATE_PROCESS_FLOWS` (EVT-TPL-006) | `CREATE_USE_CASE_SPECS` + `CREATE_ACTORS_AND_PERSONAS` | Moved downstream |
| `REVIEW_INITIAL_ARCHITECTURE` (EVT-TPL-008) | `CREATE_REQUIREMENTS_CATALOG` + `FIND_GAPS_AND_QUESTIONS` | Was blocked by full stage 2b |
| Planning events (EVT-TPL-011 etc.) | `CREATE_USE_CASE_SPECS` + `REVIEW_INITIAL_ARCHITECTURE` | No change to planning gate logic |

---

## Files Confirmed Not Modified

- `.brs2spec2/workflow/workflow-definition.yaml` — unchanged by this step
- `.brs2spec2/workflow/artifact-ownership.md` — unchanged by this step
- `.brs2spec2/workflow/event-templates/*` — all unchanged by this step
- `.brs2spec2/artifact-templates/*` — all unchanged by this step
