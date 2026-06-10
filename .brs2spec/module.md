# BRS to Spec — Module Index

Use this index to discover what prompts exist and what they do before loading any of them.
Load a prompt only when you need to execute it.

## Persona quick-reference

Address a persona directly to bypass the orchestrator and load only that agent's prompt.

| User says | Persona | Prompt to load |
|---|---|---|
| `@orchestrator` / "run the framework" / "continue" / "what's next?" | Orchestrator | `brs-to-spec-run-workflow.md` |
| `@architect` / "review the architecture" / "create architecture rules" | Architect | `3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| `@delivery-lead` / "define the delivery structure" / "create user stories" | Delivery Lead | `3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| `@qa` / "create BDD scenarios" / "write acceptance tests" | QA Analyst | `4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@engineering-lead` / "create the handoff" / "generate OpenSpec" | Engineering Lead | `5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| `@reviewer` / "review the code" / "do a security review" | Reviewer | `9-reviewers/` — see Phase 9 below for the specific reviewer prompt |

## Framework entry points

| Prompt | ~Tokens | What it does |
|---|---|---|
| `00-start.md` | ~1,350 | Interview the user (5 questions) to determine entry mode, delivery mode, and first prompt to run |
| `brs-to-spec-run-workflow.md` | ~6,500 | Full workflow orchestrator — detects current stage, executes it, re-assesses automatically |
| `agent-instructions.md` | ~1,100 | Behavioral rules for non-Copilot agents (Claude Code, Cursor, Codex) |

## Phase 0 — Input preparation

| Prompt | ~Tokens | What it does |
|---|---|---|
| `0-input-preparation/01-convert-brs-word-to-markdown.md` | ~600 | Convert a Word BRS document to structured markdown |
| `0-input-preparation/02-convert-architecture-word-to-markdown.md` | ~650 | Convert a Word architecture document to structured markdown |
| `0-input-preparation/03-normalize-input-package.md` | ~220 | Normalize and validate `input/input-package.md` |
| `0-input-preparation/04-draft-architecture-from-brs.md` | ~2,700 | Generate a draft architecture from BRS when no architecture input exists |
| `0-intake/00-create-brs.md` | ~1,650 | Create or convert a BRS — works from existing doc, bullet notes, or structured interview |

## Phase 1 — Routing

| Prompt | ~Tokens | What it does |
|---|---|---|
| `1-routing/01-select-delivery-and-execution-mode.md` | ~810 | Select delivery mode (Fast/Standard/Enterprise/Modular) and execution mode (OpenSpec/Standalone/Business Copilot) |

## Phase 2 — Business intake

| Prompt | ~Tokens | What it does |
|---|---|---|
| `2-business-intake/01-create-business-intake-summary.md` | ~800 | Create `business-intake/business-intake-summary.md` — objectives, scope, requirements, gaps |
| `2-business-intake/advanced/02-extract-detailed-requirements.md` | ~130 | Extract detailed requirements from BRS (advanced) |
| `2-business-intake/advanced/03-find-gaps-and-questions.md` | ~125 | Find gaps and open questions (advanced) |
| `2-business-intake/advanced/04-create-business-test-expectations.md` | ~125 | Create business test expectations (advanced) |
| `2-business-intake/advanced/05-create-user-stories-if-needed.md` | ~130 | Create user stories when delivery structure is not yet defined (advanced) |

## Phase 3 — Planning and architecture

| Prompt | ~Tokens | What it does |
|---|---|---|
| `3-planning-and-modular-delivery/00-maintain-open-decisions.md` | ~1,000 | Create or update `planning/open-decisions.md` — single source of truth for all open decisions |
| `3-planning-and-modular-delivery/01-maintain-workflow-state.md` | ~1,470 | Update `planning/workflow-state.json` after any stage completes |
| `3-planning-and-modular-delivery/01-review-initial-architecture.md` | ~1,310 | Create `architecture/architecture-review.md` — initiative-specific constraints and open decisions |
| `3-planning-and-modular-delivery/02-create-global-architecture-rules.md` | ~785 | Create `architecture/architecture-rules.md` — binding rules with IDs and enforcement mechanisms |
| `3-planning-and-modular-delivery/03-create-delivery-structure.md` | ~1,660 | Create `planning/delivery-structure.md` — epics, features, user stories |
| `3-planning-and-modular-delivery/04-identify-software-modules.md` | ~465 | Identify software modules for modular delivery |
| `3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` | ~460 | Map capabilities to software modules |
| `3-planning-and-modular-delivery/06-define-delivery-increments.md` | ~465 | Define delivery increments for Enterprise + Modular mode |
| `3-planning-and-modular-delivery/07-create-traceability-matrix.md` | ~465 | Create traceability matrix linking requirements to delivery artifacts |
| `3-planning-and-modular-delivery/advanced/08-create-module-spec.md` | ~125 | Create a module spec (advanced) |

## Phase 4 — Engineering readiness and quality gates

| Prompt | ~Tokens | What it does |
|---|---|---|
| `4-engineering-readiness/01-check-engineering-readiness.md` | ~1,775 | Create `engineering-readiness/readiness-check.md` — Ready / Not ready decision, triggered gates |
| `4-engineering-readiness/02-generate-initiative-context.md` | ~915 | Create `engineering-readiness/initiative-context.md` — technology constraints, binding rules, governed boundaries |
| `4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | ~3,940 | Create `quality-gates/bdd-scenarios.md` — Gherkin scenarios with SCN-NNN IDs |
| `4-engineering-readiness/quality-gates/create-api-contract.md` | ~545 | Create `quality-gates/api-contract.md` |
| `4-engineering-readiness/quality-gates/create-data-contract.md` | ~540 | Create `quality-gates/data-contract.md` |
| `4-engineering-readiness/quality-gates/create-event-contract.md` | ~540 | Create `quality-gates/event-contract.md` |
| `4-engineering-readiness/quality-gates/create-security-review.md` | ~490 | Create `quality-gates/security-review.md` |
| `4-engineering-readiness/quality-gates/create-threat-model.md` | ~545 | Create `quality-gates/threat-model.md` |
| `4-engineering-readiness/quality-gates/create-test-strategy.md` | ~490 | Create `quality-gates/test-strategy.md` |
| `4-engineering-readiness/quality-gates/create-observability-plan.md` | ~540 | Create `quality-gates/observability-plan.md` |
| `4-engineering-readiness/quality-gates/create-qa-review.md` | ~480 | Create `quality-gates/qa-review.md` |
| `4-engineering-readiness/quality-gates/create-release-readiness-review.md` | ~495 | Create `quality-gates/release-readiness-review.md` |
| `4-engineering-readiness/quality-gates/create-architecture-review.md` | ~500 | Create architecture review quality gate |
| `quality-gates/generate-ci-gate-config.md` | ~870 | Generate CI pipeline configuration for an accepted quality gate |

## Phase 5 — Handoff

| Prompt | ~Tokens | What it does |
|---|---|---|
| `5-handoff/01-create-openspec-change-for-active-deliverable.md` | ~4,230 | Create full OpenSpec handoff — dependency graph + one folder per user story |
| `5-handoff/02-create-standalone-delivery-package.md` | ~1,035 | Create standalone delivery package when OpenSpec is not used |
| `5-handoff/03-create-compact-handoff-package.md` | ~300 | Create a compact handoff for Fast Path or small changes |

## Phase 6 — Business Copilot (M365 / Copilot Studio)

| Prompt | ~Tokens | What it does |
|---|---|---|
| `6-business-copilot/01-analyze-brs.md` | ~810 | Analyze BRS — produces structured business summary (objectives, scope, requirements, personas) |
| `6-business-copilot/02-identify-gaps-and-questions.md` | ~965 | Identify gaps, open questions, risky assumptions, unresolved dependencies |
| `6-business-copilot/03-draft-epics-and-features.md` | ~1,200 | Draft outcome-oriented epics with capability-oriented features |

## Phase 7 — Perspectives

| Prompt | ~Tokens | What it does |
|---|---|---|
| `7-perspectives/agile-planning/01-create-gitlab-planning-view.md` | ~1,170 | Create GitLab/Jira/ADO planning view from approved delivery structure |
| `7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md` | ~1,200 | Refresh planning view after delivery structure changes |

## Phase 8 — Implementation

| Prompt | ~Tokens | What it does |
|---|---|---|
| `8-copilot-implementation/01-implement-one-task.md` | ~955 | Implement one approved task — reads initiative context, implements, produces summary |
| `8-copilot-implementation/02-fix-review-comments.md` | ~670 | Fix review comments on an implemented task |
| `8-copilot-implementation/03-generate-test-stubs-from-bdd.md` | ~1,280 | Generate runnable failing test stubs from BDD scenarios (pytest-bdd, Cucumber, SpecFlow) |

## Phase 9 — Review

| Prompt | ~Tokens | What it does |
|---|---|---|
| `9-reviewers/01-senior-code-review.md` | ~1,055 | Senior code review — correctness, security, patterns, BDD coverage |
| `9-reviewers/02-qa-review.md` | ~695 | QA review — test coverage, edge cases, regression risk |
| `9-reviewers/03-architecture-review.md` | ~970 | Architecture review — constraints, patterns, integration points |
| `9-reviewers/04-security-review.md` | ~800 | Security review — OWASP, secrets, auth, data exposure |
| `9-reviewers/05-spec-correction.md` | ~1,405 | Correct a spec artifact when implementation reveals it was wrong |

## Tools

| Prompt | ~Tokens | What it does |
|---|---|---|
| `tools/prompts/describe-repository.md` | ~1,130 | Analyse a repository and generate an `input/repositories/` descriptor file |

## Stage → prompt lookup

| Workflow stage | Prompt to load |
|---|---|
| Routing | `1-routing/01-select-delivery-and-execution-mode.md` |
| Business intake | `2-business-intake/01-create-business-intake-summary.md` |
| Architecture draft (if missing) | `0-input-preparation/04-draft-architecture-from-brs.md` |
| Delivery structure (draft) | `3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| Architecture review | `3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| Architecture rules | `3-planning-and-modular-delivery/02-create-global-architecture-rules.md` |
| Open decisions | `3-planning-and-modular-delivery/00-maintain-open-decisions.md` |
| Engineering readiness | `4-engineering-readiness/01-check-engineering-readiness.md` |
| Delivery structure (confirmed) | `3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| Initiative context | `4-engineering-readiness/02-generate-initiative-context.md` |
| Quality gates | `4-engineering-readiness/quality-gates/create-<gate>.md` |
| OpenSpec handoff | `5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| Standalone handoff | `5-handoff/02-create-standalone-delivery-package.md` |
| Workflow state update | `3-planning-and-modular-delivery/01-maintain-workflow-state.md` |
