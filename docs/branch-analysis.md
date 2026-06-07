# brs-to-spec — Branch Analysis (0.0.1 → 0.0.7) and Proposed 0.0.8

The branches form a **linear history**: `0.0.1 → 0.0.2 → 0.0.3 → 0.0.4 → 0.0.5 → 0.0.6 → 0.0.7`, and `main == 0.0.7`. File counts: 0.0.1 ≈ 70, 0.0.2 ≈ 95, 0.0.3 ≈ 130, **0.0.4 = 193**, **0.0.5 = 219** (peak complexity), then a deliberate simplification to **0.0.6 = 91** and **0.0.7 = 105**.

## Per-branch summary

### 0.0.1 — Foundation
- **Does well:** Clear linear pipeline (`00-change-assessment → 01-business-intake → 02-engineering-contracts → 03-openspec-handoff → 04-copilot-implementation → 05-reviewers`). Schemas + templates + 3 scripts present. CI workflow (`.github/workflows/validate-sdd.yml`).
- **Does poorly:** Single rigid path; no architecture input; no routing; OpenSpec implicitly mandatory.
- **Keep:** The simple numbered-stage idea, schemas, scripts skeleton.

### 0.0.2 — Detailed output quality (YOUR OBSERVATION: CONFIRMED ✔)
- Adds the rich intake chain: `00a-extract-brs-from-word`, `00b-extract-architecture-from-word`, `01-summarize-brs`, `02-extract-requirements`, `03-review-brs-and-requirements-against-architecture`, `04-create-delivery-structure`, `05-create-user-stories`, `06-find-gaps-and-questions`, `07-create-business-test-expectations`, plus engineering-contracts (technical-spec, bdd, test-strategy, test-plan, traceability) and an `08-enablement` track.
- **Does well:** Highest *intermediate output depth*. Architecture becomes an input. Good templates/schemas.
- **Does poorly:** Too heavy as a default — every change pays the full ceremony.
- **Keep:** The detailed prompts — **but only as conditional/triggered outputs**, not main flow.

### 0.0.3 — Adapters + architecture contracts
- Adds `06-planning`, `09-architecture-contracts` (ADR, API/OpenAPI, domain/data model, events, quality attributes, threat model), `10-handoff`, and `11-downstream-adapters` (gstack, kiro, openspec, spec-kit, standalone).
- **Does well:** Introduces "this framework hands off to *a* downstream", architecture contracts, traceability.
- **Does poorly:** Sprawl; many parallel concepts; hard to know the "default" path.
- **Keep:** Architecture-contract artifacts (as quality gates), the multi-downstream idea, traceability.

### 0.0.4 — Full enterprise AI-assisted delivery kit (YOUR OBSERVATION: CONFIRMED ✔)
- Adds the **Business Copilot / M365** track: `12-business-copilot-intake/*` and `docs/copilot/*` (Copilot Studio agent design, how-to-create-M365-agent, how-to-run-intake-in-M365).
- **Does well:** Most complete enterprise kit — business intake, engineering contracts, OpenSpec + Copilot impl, QA/security/architecture reviews, enablement, handoff, **Copilot path**.
- **Does poorly:** Too complex/hard to adopt as default; ~193 files; PO would drown.
- **Keep:** Business Copilot path (must not be lost), review prompts, contracts — as conditional.

### 0.0.5 — Mode A / Mode B (YOUR OBSERVATION: CONFIRMED ✔)
- Peak size (219 files). Adds `00-routing/01-select-delivery-mode`, `07-modular-delivery`, modular templates, and `business-intake/01-create-business-intake-summary` (the single PO artifact).
- **Critical concept to preserve:** `docs/framework-boundary-and-handoff.md` defines:
  - **Mode A — Handoff mode** (prepare inputs, hand to OpenSpec/Spec Kit/Kiro/…)
  - **Mode B — Standalone mode** (framework is end-to-end source of truth when no downstream is used)
- **Does poorly:** Standalone is under-built — just a README pointing back at the old prompts; massive surface area; duplicate/legacy files (`04-create-delivery-structure.legacy.md`, two `01-…` intake prompts).
- **Keep:** The **Mode A / Mode B** distinction and the standalone discipline (source-of-truth rule). **This is the main thing 0.0.7 lost.**

### 0.0.6 — Simplified architecture-aware core (YOUR OBSERVATION: CONFIRMED ✔)
- **Big reset: 219 → 91 files.** Introduces the final macro-structure: `0-input-preparation`, `1-routing`, `2-business-intake`, `3-planning-and-modular-delivery`, `4-engineering-readiness`, `5-handoff-to-openspec`, `6-business-copilot`. Normalized inputs `input/brs.md`, `input/initial-architecture.md`, `input/input-package.md`. Architecture-aware flow. OpenSpec as default downstream. Cleaner README.
- **Does well:** The right product direction — small front door, modular for AI agents, architecture as first-class input.
- **Does poorly:** Dropped the review/governance depth; standalone mode not explicit (Mode A/B lost); CI dropped.
- **Keep:** This whole structure is the base.

### 0.0.7 — Current base (YOUR OBSERVATION: CONFIRMED ✔)
- = 0.0.6 **plus** re-added review/governance prompts under `4-engineering-readiness/advanced/`: `create-bdd-scenarios`, `create-test-strategy`, `create-qa-review`, `create-architecture-review`, `create-security-review`, `create-release-readiness-review` (joining api/data/event-contract, threat-model, observability-plan) and matching `templates/advanced-governance/*`.
- **Does well:** Best current base — simple core + recovered governance depth as opt-in.
- **Does poorly / to fix in 0.0.8:**
  1. Governance is labelled **"optional advanced governance"** → should be **Conditional Quality Gates** (not always required, but **mandatory when triggered**).
  2. **OpenSpec-only** — `5-handoff-to-openspec` and the whole narrative assume OpenSpec; **standalone Mode B is not explicit** (regression from 0.0.5).
  3. No explicit **execution modes** (OpenSpec / Standalone / Business Copilot).
  4. Readiness check lists gates but has no **Triggered? / Required?** decision table.
  5. No CI; scripts don't check the newer artifacts.

## Markdown formatting note (your point #8)
On 0.0.7 no markdown file has the "everything-collapsed-on-one-line" problem (max line ~210 chars, which GitHub wraps fine). I'll keep 0.0.8 clean (normal newlines, readable headings) and avoid over-long paragraph lines.

## Proposed 0.0.8 — final structure

```text
prompts/
  0-input-preparation/        (unchanged)
  1-routing/                  (now selects delivery mode AND execution mode A/B/C)
  2-business-intake/          (single PO artifact + advanced/)
  3-planning-and-modular-delivery/
  4-engineering-readiness/
    01-check-engineering-readiness.md        (adds Conditional Quality Gates table)
    02-identify-required-quality-gates.md
    quality-gates/            (RENAMED from advanced/  — 11 gate prompts)
  5-handoff/                  (RENAMED from 5-handoff-to-openspec)
    01-create-openspec-change-for-active-deliverable.md   (Execution Mode A)
    02-create-openspec-handoff-package.md
    03-create-standalone-delivery-package.md              (Execution Mode B — NEW)
    advanced/ (adapters)
  6-business-copilot/         (Execution Mode C)
templates/
  quality-gates/              (RENAMED from advanced-governance/)
  standalone-delivery/        (NEW: delivery-spec, implementation-plan, tasks, validation-plan, review-checklist)
  engineering-readiness/readiness-check.md   (adds gates table)
  ... (openspec-handoff, business-copilot, planning, input-preparation unchanged)
docs/
  02-delivery-modes.md        (+ execution modes)
  05-handoff.md               (RENAMED; covers OpenSpec + standalone)
  06-conditional-quality-gates.md   (RENAMED from 06-advanced-governance.md)
  08-execution-modes.md       (NEW: A/B/C)
  09-migration-0.0.7-to-0.0.8.md (NEW)
  branch-analysis.md          (this analysis)
tools/scripts/
  check_program.py            (updated required-files list)
  check_prompt_sequence.py    (5-handoff path)
  new_feature.py              (--mode fast|standard|enterprise|enterprise-modular  --execution-mode openspec|standalone)
.github/workflows/validate.yml (NEW, minimal — runs the validation scripts; optional, noted in migration)
```

### Key design decisions / trade-offs
- **Delivery modes** (Fast / Standard / Enterprise / Enterprise+Modular) answer *how much ceremony*; **Execution modes** (A OpenSpec / B Standalone / C Business Copilot) answer *who builds it & with what downstream*. They are orthogonal.
- **Standalone (Mode B)** preserves the same discipline as OpenSpec (clear scope, architecture constraints, small tasks, validation, review gates) but does **not** pretend to be OpenSpec — separate `standalone-delivery/` output tree.
- **Conditional Quality Gates** replace "optional advanced governance" everywhere. The readiness check decides `Triggered?`; when triggered they are `Required?` = Yes and become mandatory before implementation/merge/release.
- **Detailed 0.0.2/0.0.4 outputs** are recovered as conditional gates/advanced prompts, never as mandatory main-flow steps.
- **PO experience** stays one artifact: `business-intake/business-intake-summary.md`.
- **Architecture** stays a first-class input and is propagated into review, rules, modules, increments, traceability, readiness, and both OpenSpec and standalone outputs.
