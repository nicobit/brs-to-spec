# Prompt Index

All framework prompts live inside `.brs2spec/`. This page lists every prompt with its purpose and approximate token cost when loaded into context.

> Agents use `.brs2spec/module-index.md` (Skill Index + routing tables, ~3,500 tokens) to discover which prompt to load. `.brs2spec/module-full.md` provides per-skill detail when needed. `.brs2spec/module-registry.yaml` is the machine-readable companion used only by the validator scripts.

---

## Framework entry points

| Prompt | ~Tokens | What it does |
|---|---|---|
| `00-start.md` | ~1,350 | Interview the user (5 questions) to determine entry mode, delivery mode, and first prompt to run |
| `brs-to-spec-run-workflow.md` | ~6,500 | Full workflow orchestrator — detects current stage, executes it, re-assesses automatically |

---

## Phase 0 — Input preparation

| Prompt | ~Tokens | What it does |
|---|---|---|
| `0-input-preparation/01-convert-brs-word-to-markdown.md` | ~600 | Convert a Word BRS document to structured markdown |
| `0-input-preparation/02-convert-architecture-word-to-markdown.md` | ~650 | Convert a Word architecture document to structured markdown |
| `0-input-preparation/03-normalize-input-package.md` | ~220 | Normalize and validate `input/input-package.md` |
| `0-input-preparation/04-draft-architecture-from-brs.md` | ~2,700 | Generate a draft architecture from BRS when no architecture input exists |
| `0-intake/00-create-brs.md` | ~1,650 | Create or convert a BRS — from existing doc, bullet notes, or structured interview |

---

## Phase 1 — Routing

| Prompt | ~Tokens | What it does |
|---|---|---|
| `1-routing/01-select-delivery-and-execution-mode.md` | ~810 | Select delivery mode (Fast/Standard/Enterprise/Modular) and execution mode (OpenSpec/Standalone/Business Copilot) |

---

## Phase 2 — Business intake

| Prompt | ~Tokens | What it does |
|---|---|---|
| `2-business-intake/01-create-business-intake-summary.md` | ~800 | Create `business-intake/business-intake-summary.md` — objectives, scope, requirements, gaps |
| `2-business-intake/advanced/02-extract-detailed-requirements.md` | ~130 | Extract detailed requirements from BRS (advanced) |
| `2-business-intake/advanced/03-find-gaps-and-questions.md` | ~125 | Find gaps and open questions (advanced) |
| `2-business-intake/advanced/04-create-business-test-expectations.md` | ~125 | Create business test expectations (advanced) |
| `2-business-intake/advanced/05-create-user-stories-if-needed.md` | ~130 | Create user stories when delivery structure is not yet defined (advanced) |

---

## Phase 3 — Planning and architecture

| Prompt | ~Tokens | What it does |
|---|---|---|
| `3-planning-and-modular-delivery/00-maintain-open-decisions.md` | ~1,000 | Create or update `planning/open-decisions.md` |
| `3-planning-and-modular-delivery/01-maintain-workflow-state.md` | ~1,470 | Update `planning/workflow-state.json` after any stage completes |
| `3-planning-and-modular-delivery/01-review-initial-architecture.md` | ~1,310 | Create `architecture/architecture-review.md` |
| `3-planning-and-modular-delivery/02-create-global-architecture-rules.md` | ~785 | Create `architecture/architecture-rules.md` |
| `3-planning-and-modular-delivery/03-create-delivery-structure.md` | ~1,660 | Create `planning/delivery-structure.md` — epics, features, user stories |
| `3-planning-and-modular-delivery/04-identify-software-modules.md` | ~465 | Identify software modules for modular delivery |
| `3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` | ~460 | Map capabilities to software modules |
| `3-planning-and-modular-delivery/06-define-delivery-increments.md` | ~465 | Define delivery increments for Enterprise + Modular mode |
| `3-planning-and-modular-delivery/07-create-traceability-matrix.md` | ~465 | Create traceability matrix |

---

## Phase 4 — Engineering readiness and quality gates

| Prompt | ~Tokens | What it does |
|---|---|---|
| `4-engineering-readiness/01-check-engineering-readiness.md` | ~1,775 | Create `readiness-check.md` — Ready / Not ready decision, triggered gates |
| `4-engineering-readiness/02-generate-initiative-context.md` | ~915 | Create `initiative-context.md` — technology constraints, binding rules |
| `4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | ~3,940 | Create BDD scenarios with Gherkin and SCN-NNN IDs |
| `4-engineering-readiness/quality-gates/create-api-contract.md` | ~545 | Create API contract gate |
| `4-engineering-readiness/quality-gates/create-data-contract.md` | ~540 | Create data contract gate |
| `4-engineering-readiness/quality-gates/create-event-contract.md` | ~540 | Create event contract gate |
| `4-engineering-readiness/quality-gates/create-security-review.md` | ~490 | Create security review gate |
| `4-engineering-readiness/quality-gates/create-threat-model.md` | ~545 | Create threat model gate |
| `4-engineering-readiness/quality-gates/create-test-strategy.md` | ~490 | Create test strategy gate |
| `4-engineering-readiness/quality-gates/create-observability-plan.md` | ~540 | Create observability plan gate |
| `4-engineering-readiness/quality-gates/create-qa-review.md` | ~480 | Create QA review gate |
| `4-engineering-readiness/quality-gates/create-release-readiness-review.md` | ~495 | Create release readiness review gate |
| `quality-gates/generate-ci-gate-config.md` | ~870 | Generate CI pipeline config for an accepted quality gate |

---

## Phase 5 — Handoff

| Prompt | ~Tokens | What it does |
|---|---|---|
| `5-handoff/01-create-openspec-change-for-active-deliverable.md` | ~4,230 | Create full OpenSpec handoff — dependency graph + one folder per user story |
| `5-handoff/02-create-standalone-delivery-package.md` | ~1,035 | Create standalone delivery package |
| `5-handoff/03-create-compact-handoff-package.md` | ~300 | Create compact handoff for Fast Path or small changes |

---

## Phase 6 — Business Copilot

| Prompt | ~Tokens | What it does |
|---|---|---|
| `6-business-copilot/01-analyze-brs.md` | ~810 | Analyze BRS — structured business summary |
| `6-business-copilot/02-identify-gaps-and-questions.md` | ~965 | Identify gaps, questions, risky assumptions |
| `6-business-copilot/03-draft-epics-and-features.md` | ~1,200 | Draft epics and features |

---

## Phase 7 — Perspectives

| Prompt | ~Tokens | What it does |
|---|---|---|
| `7-perspectives/agile-planning/01-create-gitlab-planning-view.md` | ~1,170 | Create GitLab / Jira / ADO planning view |
| `7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md` | ~1,200 | Refresh planning view after changes |

---

## Phase 8 — Implementation

| Prompt | ~Tokens | What it does |
|---|---|---|
| `8-copilot-implementation/01-implement-one-task.md` | ~955 | Implement one approved task |
| `8-copilot-implementation/02-fix-review-comments.md` | ~670 | Fix review comments on an implemented task |
| `8-copilot-implementation/03-generate-test-stubs-from-bdd.md` | ~1,280 | Generate failing test stubs from BDD scenarios |

---

## Phase 9 — Review

| Prompt | ~Tokens | What it does |
|---|---|---|
| `9-reviewers/01-senior-code-review.md` | ~1,055 | Senior code review |
| `9-reviewers/02-qa-review.md` | ~695 | QA review |
| `9-reviewers/03-architecture-review.md` | ~970 | Architecture review |
| `9-reviewers/04-security-review.md` | ~800 | Security review |
| `9-reviewers/05-spec-correction.md` | ~1,405 | Correct a spec artifact when implementation reveals it was wrong |

---

## Tools

All tool prompts are ad-hoc utilities — not part of the delivery workflow. Run manually when needed.

| Prompt | ~Tokens | What it does |
|---|---|---|
| `tools/prompts/describe-repository.md` | ~1,130 | Analyse a repository and generate an `input/repositories/` descriptor |
| `tools/prompts/generate-architecture-diagrams.md` | ~800 | Regenerate `architecture/diagrams/component.mmd` and `deployment.mmd` independently of the review |
| `tools/prompts/generate-initiative-summary.md` | ~800 | Generate `docs/initiatives/<slug>/initiative-summary.md` — one-page readable brief |
| `tools/prompts/generate-decision-log.md` | ~750 | Generate `docs/initiatives/<slug>/decision-log.md` — full decision audit trail |
| `tools/prompts/generate-delivery-overview.md` | ~850 | Generate `docs/initiatives/<slug>/delivery-overview.md` — epics, features, stories with status |
| `tools/prompts/generate-architecture-summary.md` | ~800 | Generate `docs/initiatives/<slug>/architecture-summary.md` — constraints and rules for developers |
| `tools/prompts/generate-quality-gates-summary.md` | ~900 | Generate `docs/initiatives/<slug>/quality-gates-summary.md` — gate status and audit trail |

---

## Stage → prompt quick reference

| Workflow stage | Prompt |
|---|---|
| Routing | `1-routing/01-select-delivery-and-execution-mode.md` |
| Business intake | `2-business-intake/01-create-business-intake-summary.md` |
| Architecture draft | `0-input-preparation/04-draft-architecture-from-brs.md` |
| Delivery structure | `3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| Architecture review | `3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| Architecture rules | `3-planning-and-modular-delivery/02-create-global-architecture-rules.md` |
| Open decisions | `3-planning-and-modular-delivery/00-maintain-open-decisions.md` |
| Engineering readiness | `4-engineering-readiness/01-check-engineering-readiness.md` |
| Initiative context | `4-engineering-readiness/02-generate-initiative-context.md` |
| Quality gates | `4-engineering-readiness/quality-gates/create-<gate>.md` |
| OpenSpec handoff | `5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| Standalone handoff | `5-handoff/02-create-standalone-delivery-package.md` |
| Workflow state update | `3-planning-and-modular-delivery/01-maintain-workflow-state.md` |
