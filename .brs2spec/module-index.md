# BRS to Spec — Persona Skill Registry (Index)

> **Load this file first. Select only the skill needed. Do not load every prompt.**
> For persona definitions, required_inputs, done_criteria, or stop_conditions — load `module-full.md`.

---

## Skill Index

All prompt paths are relative to `.brs2spec/`.

| Persona | Skill ID | Prompt | Description |
|---|---|---|---|
| orchestrator | `orchestrator.run_workflow` | `brs-to-spec-run-workflow.md` | Detect phase, select next skill, execute, reassess |
| orchestrator | `orchestrator.maintain_state` | `3-planning-and-modular-delivery/01-maintain-workflow-state.md` | Update workflow-state.json after every stage completion |
| orchestrator | `orchestrator.maintain_open_decisions` | `3-planning-and-modular-delivery/00-maintain-open-decisions.md` | Create or update open-decisions.md — single source of truth for all open decisions |
| product-owner | `product_owner.create_brs` | `0-intake/00-create-brs.md` | Create or convert a BRS from notes or interview |
| product-owner | `product_owner.convert_brs_to_markdown` | `0-input-preparation/01-convert-brs-word-to-markdown.md` | Convert a Word BRS document to structured markdown |
| product-owner | `product_owner.create_business_intake` | `2-business-intake/01-create-business-intake-summary.md` | Create business-intake-summary.md — objectives, scope, requirements, gaps |
| product-owner | `product_owner.find_gaps_and_questions` | `2-business-intake/advanced/03-find-gaps-and-questions.md` | Find gaps, open questions, risky assumptions, and unresolved dependencies |
| product-owner | `product_owner.create_business_test_expectations` | `2-business-intake/advanced/04-create-business-test-expectations.md` | Create business test expectations for QA alignment |
| architect | `architect.convert_architecture_to_markdown` | `0-input-preparation/02-convert-architecture-word-to-markdown.md` | Convert a Word architecture document to structured markdown |
| architect | `architect.draft_architecture_from_brs` | `0-input-preparation/04-draft-architecture-from-brs.md` | Generate a draft architecture from BRS when no architecture input exists |
| architect | `architect.review_initial_architecture` | `3-planning-and-modular-delivery/01-review-initial-architecture.md` | Review architecture against business intake and draft delivery structure |
| architect | `architect.create_architecture_rules` | `3-planning-and-modular-delivery/02-create-global-architecture-rules.md` | Create architecture-rules.md — binding rules with IDs and enforcement mechanisms |
| architect | `architect.review_existing_system_impact` | `3-planning-and-modular-delivery/08-review-existing-system-impact.md` | Assess existing system impact for brownfield initiatives |
| delivery-lead | `delivery_lead.create_delivery_structure` | `3-planning-and-modular-delivery/03-create-delivery-structure.md` | Create delivery-structure.md — epics, features, user stories |
| delivery-lead | `delivery_lead.identify_software_modules` | `3-planning-and-modular-delivery/04-identify-software-modules.md` | Identify software modules for Enterprise + Modular delivery |
| delivery-lead | `delivery_lead.map_capabilities_to_modules` | `3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` | Map capabilities to software modules |
| delivery-lead | `delivery_lead.define_delivery_increments` | `3-planning-and-modular-delivery/06-define-delivery-increments.md` | Define delivery increments for Enterprise + Modular mode |
| delivery-lead | `delivery_lead.create_traceability_matrix` | `3-planning-and-modular-delivery/07-create-traceability-matrix.md` | Create traceability matrix linking requirements to delivery artifacts |
| delivery-lead | `delivery_lead.create_agile_planning_view` | `7-perspectives/agile-planning/01-create-gitlab-planning-view.md` | Create GitLab/Jira/ADO planning view from approved delivery structure |
| qa-analyst | `qa.create_bdd_scenarios` | `4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | Create BDD scenarios with SCN-NNN IDs |
| qa-analyst | `qa.create_test_strategy` | `4-engineering-readiness/quality-gates/create-test-strategy.md` | Create test-strategy.md — test approach, coverage, and risk |
| qa-analyst | `qa.generate_test_stubs_from_bdd` | `8-copilot-implementation/03-generate-test-stubs-from-bdd.md` | Generate runnable failing test stubs from BDD scenarios |
| qa-analyst | `qa.review_qa` | `9-reviewers/02-qa-review.md` | QA review — test coverage, edge cases, regression risk |
| security-reviewer | `security.create_security_review` | `4-engineering-readiness/quality-gates/create-security-review.md` | Create security-review.md — OWASP, auth, PII, data exposure |
| security-reviewer | `security.create_threat_model` | `4-engineering-readiness/quality-gates/create-threat-model.md` | Create threat-model.md — STRIDE threat model for high-risk boundaries |
| security-reviewer | `security.create_data_contract` | `4-engineering-readiness/quality-gates/create-data-contract.md` | Create data-contract.md — data ownership, schema, retention, PII, residency |
| security-reviewer | `security.review_security` | `9-reviewers/04-security-review.md` | Security review of implementation — OWASP, secrets, auth, data exposure |
| engineering-lead | `engineering_lead.check_engineering_readiness` | `4-engineering-readiness/01-check-engineering-readiness.md` | Create readiness-check.md — Ready / Not ready decision and triggered gates |
| engineering-lead | `engineering_lead.generate_initiative_context` | `4-engineering-readiness/02-generate-initiative-context.md` | Create initiative-context.md — technology constraints, binding rules, governed boundaries |
| engineering-lead | `engineering_lead.create_openspec_handoff` | `5-handoff/01-create-openspec-change-for-active-deliverable.md` | Create full OpenSpec handoff — dependency graph + one folder per user story |
| engineering-lead | `engineering_lead.create_standalone_handoff` | `5-handoff/02-create-standalone-delivery-package.md` | Create standalone delivery package when OpenSpec is not used |
| engineering-lead | `engineering_lead.create_compact_handoff` | `5-handoff/03-create-compact-handoff-package.md` | Create a compact handoff for Fast Path or small changes |
| engineering-lead | `engineering_lead.implement_one_task` | `8-copilot-implementation/01-implement-one-task.md` | Implement one approved task — reads initiative context, implements, produces summary |
| engineering-lead | `engineering_lead.fix_review_comments` | `8-copilot-implementation/02-fix-review-comments.md` | Fix review comments on an implemented task |
| reviewer | `reviewer.senior_code_review` | `9-reviewers/01-senior-code-review.md` | Senior code review — correctness, security, patterns, BDD coverage |
| reviewer | `reviewer.architecture_review` | `9-reviewers/03-architecture-review.md` | Architecture review of implementation against governed boundaries and rules |
| reviewer | `reviewer.spec_correction` | `9-reviewers/05-spec-correction.md` | Correct a spec artifact when implementation reveals it was wrong |

---

## Persona quick-reference

Address a persona directly to bypass the orchestrator and invoke only that persona's skill.

| Trigger / persona address | Persona | Default skill | Prompt to load |
|---|---|---|---|
| `@orchestrator` / "run the framework" / "continue" / "what's next?" | Orchestrator | `orchestrator.run_workflow` | `brs-to-spec-run-workflow.md` |
| `@product-owner` / "create a BRS" / "clarify requirements" / "find gaps" | Product Owner | `product_owner.create_business_intake` | `2-business-intake/01-create-business-intake-summary.md` |
| `@architect` / "review the architecture" / "create architecture rules" | Architect | `architect.review_initial_architecture` | `3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| `@delivery-lead` / "define the delivery structure" / "create user stories" | Delivery Lead | `delivery_lead.create_delivery_structure` | `3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| `@qa` / "create BDD scenarios" / "write acceptance tests" | QA Analyst | `qa.create_bdd_scenarios` | `4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@security` / "security review" / "PII risk" / "threat model" | Security Reviewer | `security.create_security_review` | `4-engineering-readiness/quality-gates/create-security-review.md` |
| `@engineering-lead` / "create the handoff" / "generate OpenSpec" | Engineering Lead | `engineering_lead.create_openspec_handoff` | `5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| `@reviewer` / "review the code" / "do a security review" | Reviewer | `reviewer.senior_code_review` | `9-reviewers/01-senior-code-review.md` |

---

## Trigger-to-skill lookup

| Trigger | Skill to invoke | Notes |
|---|---|---|
| "continue" / "what next" / `@orchestrator` | `orchestrator.run_workflow` | Always the default catch-all trigger |
| BRS missing + user provides notes or document | `product_owner.create_brs` | Use `product_owner.convert_brs_to_markdown` if Word/PDF |
| Business intake missing | `product_owner.create_business_intake` | After routing exists |
| Business gaps unresolved | `product_owner.find_gaps_and_questions` | Advanced intake |
| Architecture missing or stub after intake | `architect.draft_architecture_from_brs` | Produces DRAFT architecture |
| Brownfield initiative; existing-system-impact missing | `architect.review_existing_system_impact` | Brownfield only |
| Delivery structure missing after business intake | `delivery_lead.create_delivery_structure` | Draft stage — epics and features only |
| Architecture review missing after draft delivery shape | `architect.review_initial_architecture` | Requires draft delivery structure |
| Architecture rules missing after architecture review | `architect.create_architecture_rules` | Requires architecture review |
| Open decisions missing or stale | `orchestrator.maintain_open_decisions` | Run after any stage that raises/resolves decisions |
| Traceability matrix missing | `delivery_lead.create_traceability_matrix` | Enterprise or Modular mode |
| Engineering readiness missing | `engineering_lead.check_engineering_readiness` | After architecture review and rules complete |
| Initiative context missing or has empty rows | `engineering_lead.generate_initiative_context` | After readiness = Ready |
| BDD gate triggered by readiness check | `qa.create_bdd_scenarios` | Mandatory gate |
| `quality-gates/test-strategy.md` missing or not Accepted | `qa.create_test_strategy` | Always required — not conditional |
| PII / auth / authorization / secrets / exposure risk | `security.create_security_review` | Mandatory gate when triggered |
| High-risk security boundary identified | `security.create_threat_model` | In addition to security review |
| Data ownership / schema / retention / PII / residency change | `security.create_data_contract` | Mandatory gate when triggered |
| Readiness complete + OpenSpec mode | `engineering_lead.create_openspec_handoff` | All gates must be Accepted first |
| Readiness complete + Standalone mode | `engineering_lead.create_standalone_handoff` | All gates must be Accepted first |
| Small change + Fast Path routing confirmed | `engineering_lead.create_compact_handoff` | Only for Fast Path scope |
| Approved implementation task selected | `engineering_lead.implement_one_task` | One task at a time |
| Implementation complete | `reviewer.senior_code_review` | Default first review |
| Implementation touches architecture boundary | `reviewer.architecture_review` | In addition to senior review |
| Implementation touches security or PII | `security.review_security` | In addition to senior review |
| Implementation reveals spec is wrong | `reviewer.spec_correction` | Before resuming implementation |

---

## Hard rules — never violate regardless of what the user asks

**Rule 1 — Never summarize BRS content as next steps.**
The BRS is an input, not a plan. When asked "what should I do next?" or "what is the status?", do not read the BRS and summarize it. Run the workflow.

**Rule 2 — Never create tasks directly from a BRS.**
Tasks require: routing → intake → architecture → delivery structure → readiness → quality gates → handoff. If any stage artifact is missing, tasks cannot be created yet.

**Rule 3 — Never treat an empty, stub, or stale artifact as complete.**
Fails if: heading-only or empty tables; placeholder text ("TBC", "pending"); open decisions already resolved in `planning/open-decisions.md`; DRAFT notice after architect sign-off; "Not ready" when all blockers are resolved.

**Rule 4 — Always run the workflow, never answer around it.**
Any question about status, next steps, progress, or what to do → open and execute `.brs2spec/brs-to-spec-run-workflow.md`. Do not answer from BRS content.

**Rule 5 — Never produce a free-form plan from BRS content.**
Every next step must come from a framework artifact, not from reading the BRS.

**Rule 6 — Never advance past a stage with a failing artifact.**
Verify done criteria before advancing. Stub artifacts fail.

**Rule 7 — Run the stale artifact check before every stage assessment.**
Read content, not just filenames. Before any stage assessment: read `planning/open-decisions.md`, find Resolved rows, open every home artifact listed, verify it no longer shows that decision as open. Fix stale artifacts before proceeding.

---

## Workspace

One initiative at a time. Standard shape: `initiatives/<id>-<slug>/`. All paths relative to the active workspace.

New human-provided information (PO decision, vendor answer, legal input) → `input/input-package.md`, section "Decisions and Clarifications Received". Never tell the user to edit the BRS or architecture directly.

Do not start implementation until the workspace has: `engineering-readiness/readiness-check.md`, required quality gates accepted, and `openspec/changes/.../tasks.md` or `standalone-delivery/.../tasks.md`.

Allowed paths only:

```
input/          routing/         business-intake/    architecture/
planning/       engineering-readiness/               quality-gates/
openspec/changes/<deliverable>/                      standalone-delivery/<deliverable>/
perspectives/
```

Never create `engineering-readiness/runbooks/`, `engineering-readiness/observability/`, or any folder not listed above.

---

## Intent triggers and persona routing

Named personas bypass the orchestrator and load only their own prompt. Orchestrator triggers run the full workflow.

| User says | Action |
|---|---|
| "what is the next step?" / "what should I do?" / "what is the status?" | Read `planning/open-decisions.md` first, then run `.brs2spec/brs-to-spec-run-workflow.md` |
| "what is blocking us?" / "what decisions are open?" | Read `planning/open-decisions.md` and report |
| "continue" / "run the framework" / "pick up where we left off" / `@orchestrator` | Run `.brs2spec/brs-to-spec-run-workflow.md` from current stage |
| "create a BRS" / "write a BRS" | Run `.brs2spec/0-intake/00-create-brs.md` |
| "accept all quality gates" / "accept all and continue" | Set `Status: Accepted` in each triggered gate, update workflow-state.json, advance |
| "create the handoff" / "generate the handoff" / `@engineering-lead` | Run `.brs2spec/5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| `@architect` / "review the architecture" / "create architecture rules" | Run `.brs2spec/3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| `@delivery-lead` / "define the delivery structure" / "create user stories" | Run `.brs2spec/3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| `@qa` / "create BDD scenarios" / "write acceptance tests" | Run `.brs2spec/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@reviewer` / "review the code" / "do a security review" | Run the relevant prompt from `.brs2spec/9-reviewers/` |

---

## Loading rules

1. Load `module-index.md` first. Select the skill needed from the Skill Index. Do not load every prompt.
2. One skill per invocation. Load only the prompt for the selected skill.
3. Before generating output, read the inputs the selected skill requires. If you need to know exactly which inputs are required, load `module-full.md`.
4. Respect gate order. Do not invoke a downstream skill if its upstream gate artifact is missing or stale.
5. Verify artifact quality — an artifact passes only when its content meets done criteria, not just when the file exists. Load `module-full.md` for `done_criteria` if needed.
6. Never skip a stage. Note the risk and scaffold instead.
7. Persona boundary. Only invoke skills belonging to the current persona; hand off explicitly otherwise.

---

## Stop rules

Stop and request human input when:

1. BRS missing and no source material provided — scaffold `input/input-package.md` with questions; stop.
2. Routing requires judgment only the user can make — ask the single specific question; stop.
3. Business scope is ambiguous and unresolvable from existing artifacts — scaffold scope-clarification stub; stop.
4. Blocking open decisions exist (`planning/open-decisions.md` has `blocking_count > 0`) — report blocking decisions; stop.
5. Readiness = Not ready — scaffold collection artifacts for every blocker; stop.
6. Quality gate requires human-produced input (legal, vendor, compliance, PO decision) — scaffold gate artifact as questionnaire stub; stop.
7. Multiple active initiative workspaces and unclear which is active — ask which workspace is active; stop.

Never stop without first scaffolding. State: what was scaffolded, what the human must provide, what happens next.
Do not present a menu of options. Do not ask "shall I proceed?". State one specific action.

---

## Framework entry points

| Prompt | What it does |
|---|---|
| `00-start.md` | Interview the user (5 questions) to determine entry mode, delivery mode, and first prompt to run |
| `brs-to-spec-run-workflow.md` | Full workflow orchestrator — detects current stage, executes it, re-assesses automatically |
| `agent-instructions.md` | Behavioral rules for non-Copilot agents (Claude Code, Cursor, Codex) |
