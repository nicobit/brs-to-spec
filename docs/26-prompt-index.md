# Prompt Index

All framework prompts live inside `.brs2spec/`. This page lists every prompt with its purpose and relative loading size when brought into working context.

> Agents use `.brs2spec/module-index.md` (Skill Index + routing tables, compact startup entry point) to discover which prompt to load. `.brs2spec/module-full.md` provides per-skill detail when needed. `.brs2spec/module-registry.yaml` is the machine-readable companion used only by the validator scripts.

---

## Framework entry points

| Prompt | Relative Size | What it does |
|---|---|---|
| `00-start.md` | Medium | Interview the user (5 questions) to determine entry mode, delivery mode, and first prompt to run |
| `brs-to-spec-run-workflow.md` | Large | Full workflow orchestrator — detects current stage, executes it, re-assesses automatically |

---

## Phase 0 — Input preparation

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/0-input-preparation/01-convert-brs-word-to-markdown.md` | Small | Convert a Word BRS document to structured markdown |
| `skills/0-input-preparation/02-convert-architecture-word-to-markdown.md` | Small | Convert a Word architecture document to structured markdown |
| `skills/0-input-preparation/03-normalize-input-package.md` | Small | Normalize and validate `input/input-package.md` |
| `skills/0-input-preparation/04-draft-architecture-from-brs.md` | Large | Generate a draft architecture from BRS when no architecture input exists |
| `skills/0-intake/00-create-brs.md` | Medium | Create or convert a BRS — from existing doc, bullet notes, or structured interview |

---

## Phase 1 — Routing

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/1-routing/01-select-delivery-and-execution-mode.md` | Small | Select delivery mode (Fast/Standard/Enterprise/Modular) and execution mode (OpenSpec/Standalone/Business Copilot) |

---

## Phase 2 — Business intake

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/2-business-intake/01-create-business-intake-summary.md` | Small | Create `business-intake/business-intake-summary.md` — objectives, scope, requirements, gaps |
| `skills/2-business-intake/advanced/02-extract-detailed-requirements.md` | Small | Extract detailed requirements from BRS (advanced) |
| `skills/2-business-intake/advanced/03-find-gaps-and-questions.md` | Small | Find gaps and open questions (advanced) |
| `skills/2-business-intake/advanced/04-create-business-test-expectations.md` | Small | Create business test expectations (advanced) |
| `skills/2-business-intake/advanced/05-create-user-stories-if-needed.md` | Small | Create user stories when delivery structure is not yet defined (advanced) |

---

## Phase 3 — Planning and architecture

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/3-planning-and-modular-delivery/00-maintain-open-decisions.md` | Medium | Create or update `planning/open-decisions.md` |
| `skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md` | Medium | Update `planning/workflow-state.json` after any stage completes |
| `skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` | Medium | Create `architecture/architecture-review.md` |
| `skills/3-planning-and-modular-delivery/02-create-global-architecture-rules.md` | Small | Create `architecture/architecture-rules.md` |
| `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` | Medium | Create `planning/delivery-structure.md` — epics, features, user stories |
| `skills/3-planning-and-modular-delivery/04-identify-software-modules.md` | Small | Identify software modules for modular delivery |
| `skills/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` | Small | Map capabilities to software modules |
| `skills/3-planning-and-modular-delivery/06-define-delivery-increments.md` | Small | Define delivery increments for Enterprise + Modular mode |
| `skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md` | Small | Create traceability matrix |

---

## Phase 4 — Engineering readiness and quality gates

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/4-engineering-readiness/01-check-engineering-readiness.md` | Medium | Create `readiness-check.md` — Ready / Not ready decision, triggered gates |
| `skills/4-engineering-readiness/02-generate-initiative-context.md` | Small | Create `initiative-context.md` — technology constraints, binding rules |
| `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | Large | Create BDD scenarios with Gherkin and SCN-NNN IDs |
| `skills/4-engineering-readiness/quality-gates/create-api-contract.md` | Small | Create API contract gate |
| `skills/4-engineering-readiness/quality-gates/create-data-contract.md` | Small | Create data contract gate |
| `skills/4-engineering-readiness/quality-gates/create-event-contract.md` | Small | Create event contract gate |
| `skills/4-engineering-readiness/quality-gates/create-security-review.md` | Small | Create security review gate |
| `skills/4-engineering-readiness/quality-gates/create-threat-model.md` | Small | Create threat model gate |
| `skills/4-engineering-readiness/quality-gates/create-test-strategy.md` | Small | Create test strategy gate |
| `skills/4-engineering-readiness/quality-gates/create-observability-plan.md` | Small | Create observability plan gate |
| `skills/4-engineering-readiness/quality-gates/create-qa-review.md` | Small | Create QA review gate |
| `skills/4-engineering-readiness/quality-gates/create-release-readiness-review.md` | Small | Create release readiness review gate |
| `quality-gates/generate-ci-gate-config.md` | Small | Generate CI pipeline config for an accepted quality gate |

---

## Phase 5 — Handoff

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` | Large | Create full OpenSpec handoff — dependency graph + one folder per user story |
| `skills/5-handoff/02-create-standalone-delivery-package.md` | Medium | Create standalone delivery package |
| `skills/5-handoff/03-create-compact-handoff-package.md` | Small | Create compact handoff for Fast Path or small changes |

---

## Phase 6 — Business Copilot

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/6-business-copilot/01-analyze-brs.md` | Small | Analyze BRS — structured business summary |
| `skills/6-business-copilot/02-identify-gaps-and-questions.md` | Medium | Identify gaps, questions, risky assumptions |
| `skills/6-business-copilot/03-draft-epics-and-features.md` | Medium | Draft epics and features |

---

## Phase 7 — Perspectives

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/7-perspectives/agile-planning/01-create-gitlab-planning-view.md` | Medium | Create GitLab / Jira / ADO planning view |
| `skills/7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md` | Medium | Refresh planning view after changes |

---

## Phase 8 — Implementation

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/8-copilot-implementation/01-implement-one-task.md` | Small | Implement one approved task |
| `skills/8-copilot-implementation/02-fix-review-comments.md` | Small | Fix review comments on an implemented task |
| `skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md` | Medium | Generate failing test stubs from BDD scenarios |

---

## Phase 9 — Review

| Prompt | Relative Size | What it does |
|---|---|---|
| `skills/9-reviewers/01-senior-code-review.md` | Medium | Senior code review |
| `skills/9-reviewers/02-qa-review.md` | Small | QA review |
| `skills/9-reviewers/03-architecture-review.md` | Medium | Architecture review |
| `skills/9-reviewers/04-security-review.md` | Small | Security review |
| `skills/9-reviewers/05-spec-correction.md` | Medium | Correct a spec artifact when implementation reveals it was wrong |

---

## Tools

All tool prompts are ad-hoc utilities — not part of the delivery workflow. Run manually when needed.

### When to run the documentation generators

The `generate-*` prompts write readable snapshot pages to `docs/initiatives/<slug>/`. They are never triggered automatically — run them whenever you want the documentation site updated.

| Good moment to run | Which prompts |
|---|---|
| After business intake is complete | `generate-initiative-summary` |
| After architecture review and rules are finalised | `generate-architecture-summary`, `generate-architecture-diagrams` |
| After delivery structure and increments are defined | `generate-delivery-overview` |
| After any open decision is resolved or added | `generate-decision-log` |
| After a quality gate is accepted or updated | `generate-quality-gates-summary` |
| Before a sprint review or stakeholder demo | All five `generate-*` docs to get a fresh snapshot |
| Before a stage gate or handoff | All five `generate-*` docs — gives reviewers a readable package |
| Any time architecture diagrams look stale | `generate-architecture-diagrams` (standalone, no need to re-run the full review) |

Each prompt reads the current workspace artifacts and overwrites the matching doc file. Running them multiple times is safe — the output is always a fresh snapshot of the current state.

To add a new initiative to the documentation nav, follow the instructions at the bottom of `generate-initiative-summary.md`.

### Tool prompt reference

| Prompt | Relative Size | What it does |
|---|---|---|
| `tools/prompts/describe-repository.md` | Medium | Analyse a repository and generate an `input/repositories/` descriptor |
| `tools/prompts/generate-architecture-diagrams.md` | Small | Regenerate `architecture/diagrams/component.mmd` and `deployment.mmd` independently of the review |
| `tools/prompts/generate-initiative-summary.md` | Small | Generate `docs/initiatives/<slug>/initiative-summary.md` — one-page readable brief |
| `tools/prompts/generate-decision-log.md` | Small | Generate `docs/initiatives/<slug>/decision-log.md` — full decision audit trail |
| `tools/prompts/generate-delivery-overview.md` | Small | Generate `docs/initiatives/<slug>/delivery-overview.md` — epics, features, stories with status |
| `tools/prompts/generate-architecture-summary.md` | Small | Generate `docs/initiatives/<slug>/architecture-summary.md` — constraints and rules for developers |
| `tools/prompts/generate-quality-gates-summary.md` | Small | Generate `docs/initiatives/<slug>/quality-gates-summary.md` — gate status and audit trail |

---

## Stage → prompt quick reference

| Workflow stage | Prompt |
|---|---|
| Routing | `skills/1-routing/01-select-delivery-and-execution-mode.md` |
| Business intake | `skills/2-business-intake/01-create-business-intake-summary.md` |
| Architecture draft | `skills/0-input-preparation/04-draft-architecture-from-brs.md` |
| Delivery structure | `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| Architecture review | `skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| Architecture rules | `skills/3-planning-and-modular-delivery/02-create-global-architecture-rules.md` |
| Open decisions | `skills/3-planning-and-modular-delivery/00-maintain-open-decisions.md` |
| Engineering readiness | `skills/4-engineering-readiness/01-check-engineering-readiness.md` |
| Initiative context | `skills/4-engineering-readiness/02-generate-initiative-context.md` |
| Quality gates | `skills/4-engineering-readiness/quality-gates/create-<gate>.md` |
| OpenSpec handoff | `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| Standalone handoff | `skills/5-handoff/02-create-standalone-delivery-package.md` |
| Workflow state update | `skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md` |
