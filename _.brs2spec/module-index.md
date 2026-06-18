# BRS to Spec — Persona Skill Registry (Index)

> **Load this file first. Select only the skill needed. Do not load every prompt.**
> For persona definitions, required_inputs, done_criteria, or stop_conditions — load only `module-personas/<persona>.md` for the active persona. Do not load all persona files.
> For context packaging rules, artifact precedence, and retrieval profiles by role and delivery mode — see `agent-instructions.md` sections "Artifact authority and precedence", "Context packaging for downstream AI tasks", and "Retrieval profiles by role and delivery mode".

---

## Skill Index

All prompt paths are relative to `.brs2spec/`.

| Persona | Skill ID | Prompt | Description |
|---|---|---|---|
| orchestrator | `orchestrator.run_workflow` | `brs-to-spec-run-workflow.md` | Detect phase, select next skill, execute, reassess |
| orchestrator | `orchestrator.repair_workspace_state` | `skills/0-repair/repair-workspace-state.md` | Scan artifacts, correct corrupted/inaccurate workflow-state.json, reset next_action to the correct stage |
| orchestrator | `orchestrator.maintain_state` | `skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md` | Update workflow-state.json after every stage completion |
| orchestrator | `orchestrator.maintain_open_decisions` | `skills/3-planning-and-modular-delivery/00-maintain-open-decisions.md` | Create or update open-decisions.md — single source of truth for all open decisions |
| product-owner | `product_owner.create_brs` | `skills/0-intake/00-create-brs.md` | Create or convert a BRS from notes or interview |
| product-owner | `product_owner.convert_brs_to_markdown` | `skills/0-input-preparation/01-convert-brs-word-to-markdown.md` | Convert a Word BRS document to structured markdown |
| product-owner | `product_owner.create_business_intake` | `skills/2-business-intake/01-create-business-intake-summary.md` | Create business-intake-summary.md — objectives, scope, requirements, gaps |
| product-owner | `product_owner.find_gaps_and_questions` | `skills/2-business-intake/advanced/03-find-gaps-and-questions.md` | Find gaps, open questions, risky assumptions, and unresolved dependencies |
| product-owner | `product_owner.create_business_test_expectations` | `skills/2-business-intake/advanced/04-create-business-test-expectations.md` | Create business test expectations for QA alignment |
| architect | `architect.convert_architecture_to_markdown` | `skills/0-input-preparation/02-convert-architecture-word-to-markdown.md` | Convert a Word architecture document to structured markdown |
| architect | `architect.draft_architecture_from_brs` | `skills/0-input-preparation/04-draft-architecture-from-brs.md` | Generate a draft architecture from BRS when no architecture input exists |
| architect | `architect.review_initial_architecture` | `skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` | Review architecture against business intake and draft delivery structure |
| architect | `architect.create_architecture_rules` | `skills/3-planning-and-modular-delivery/02-create-global-architecture-rules.md` | Create architecture-rules.md — binding rules with IDs and enforcement mechanisms |
| architect | `architect.review_existing_system_impact` | `skills/3-planning-and-modular-delivery/08-review-existing-system-impact.md` | Assess existing system impact for brownfield initiatives |
| product-owner | `product_owner.extract_business_rules` | `skills/2-business-intake/02-extract-business-rules.md` | Extract BR-NNN business rules from BRS into business-intake/business-rules.md |
| product-owner | `product_owner.extract_actors` | `skills/2-business-intake/03-extract-actors-and-personas.md` | Extract ACT-NNN and SYS-NNN actors from BRS into business-analysis/actors-and-personas.md |
| product-owner | `product_owner.create_process_flows` | `skills/2-business-intake/04-create-process-flows.md` | Create PF-NNN process flows into business-analysis/process-flows.md |
| product-owner | `product_owner.create_use_case_specs` | `skills/2-business-intake/05-create-use-case-specs.md` | Create UC-NNN use case specs into business-analysis/use-case-spec.md |
| architect | `architect.create_entity_model` | `skills/2-business-intake/06-create-entity-model.md` | Create domain entity model with ER diagram and attribute tables into business-analysis/entity-model.md |
| delivery-lead | `delivery_lead.create_delivery_structure` | `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` | Create delivery-structure.md — epics, features, user stories |
| delivery-lead | `delivery_lead.identify_software_modules` | `skills/3-planning-and-modular-delivery/04-identify-software-modules.md` | Identify software modules for Enterprise + Modular delivery |
| delivery-lead | `delivery_lead.map_capabilities_to_modules` | `skills/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` | Map capabilities to software modules |
| delivery-lead | `delivery_lead.define_delivery_increments` | `skills/3-planning-and-modular-delivery/06-define-delivery-increments.md` | Define delivery increments for Enterprise + Modular mode |
| delivery-lead | `delivery_lead.create_traceability_matrix` | `skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md` | Create traceability matrix linking requirements to delivery artifacts |
| delivery-lead | `delivery_lead.create_agile_planning_view` | `skills/7-perspectives/agile-planning/01-create-gitlab-planning-view.md` | Create GitLab/Jira/ADO planning view from approved delivery structure |
| qa-analyst | `qa.create_bdd_scenarios` | `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | Create BDD scenarios with SCN-NNN IDs — stage 9b (three amigos, after confirmed delivery structure) |
| qa-analyst | `qa.create_test_plan_per_story` | `skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md` | Create one F-XXX.X-test-plan.md per story — risk classification (C1–C4), TC-NNN test cases by type, minimum passing bar — stage 9f |
| qa-analyst | `qa.create_test_strategy` | `skills/4-engineering-readiness/quality-gates/create-test-strategy.md` | Create test-strategy.md — stage 10, after BDD and test plans; references SCN-NNN and TC-NNN IDs |
| qa-analyst | `qa.generate_test_stubs_from_bdd` | `skills/8-copilot-implementation/03-generate-test-stubs-from-bdd.md` | Generate BDD stubs (SCN-NNN) and unit stubs (TC-NNN) — stage 13a, automatic after handoff |
| qa-analyst | `qa.review_qa` | `skills/9-reviewers/02-qa-review.md` | QA review — test coverage, edge cases, regression risk |
| security-reviewer | `security.create_security_review` | `skills/4-engineering-readiness/quality-gates/create-security-review.md` | Create security-review.md — OWASP, auth, PII, data exposure |
| security-reviewer | `security.create_threat_model` | `skills/4-engineering-readiness/quality-gates/create-threat-model.md` | Create threat-model.md — STRIDE threat model for high-risk boundaries |
| security-reviewer | `security.create_data_contract` | `skills/4-engineering-readiness/quality-gates/create-data-contract.md` | Create data-contract.md — data ownership, schema, retention, PII, residency |
| security-reviewer | `security.review_security` | `skills/9-reviewers/04-security-review.md` | Security review of implementation — OWASP, secrets, auth, data exposure |
| engineering-lead | `engineering_lead.check_engineering_readiness` | `skills/4-engineering-readiness/01-check-engineering-readiness.md` | Create readiness-check.md — Ready / Not ready decision and triggered gates |
| engineering-lead | `engineering_lead.generate_initiative_context` | `skills/4-engineering-readiness/02-generate-initiative-context.md` | Create initiative-context.md — technology constraints, binding rules, governed boundaries |
| engineering-lead | `engineering_lead.create_openspec_handoff` | `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` | Create full OpenSpec handoff — dependency graph + one folder per user story |
| engineering-lead | `engineering_lead.create_standalone_handoff` | `skills/5-handoff/02-create-standalone-delivery-package.md` | Create standalone delivery package when OpenSpec is not used |
| engineering-lead | `engineering_lead.create_compact_handoff` | `skills/5-handoff/03-create-compact-handoff-package.md` | Create a compact handoff for Fast Path or small changes |
| engineering-lead | `engineering_lead.implement_one_task` | `skills/8-copilot-implementation/01-implement-one-task.md` | Implement one approved task — reads initiative context, implements, produces summary |
| engineering-lead | `engineering_lead.fix_review_comments` | `skills/8-copilot-implementation/02-fix-review-comments.md` | Fix review comments on an implemented task |
| reviewer | `reviewer.senior_code_review` | `skills/9-reviewers/01-senior-code-review.md` | Senior code review — correctness, security, patterns, BDD coverage |
| reviewer | `reviewer.architecture_review` | `skills/9-reviewers/03-architecture-review.md` | Architecture review of implementation against governed boundaries and rules |
| reviewer | `reviewer.spec_correction` | `skills/9-reviewers/05-spec-correction.md` | Correct a spec artifact when implementation reveals it was wrong |
| delivery-lead | `delivery_lead.create_review_package` | `skills/6-review-package/01-create-review-package.md` | Assemble review-package/ — stakeholder-friendly view of the initiative with actors, process flows, entity model, use case specs |

---

## Persona quick-reference

Address a persona directly to bypass the orchestrator and invoke only that persona's skill.

| Trigger / persona address | Persona | Default skill | Prompt to load |
|---|---|---|---|
| `@orchestrator` / "run the framework" / "continue" / "what's next?" | Orchestrator | `orchestrator.run_workflow` | `brs-to-spec-run-workflow.md` |
| `@product-owner` / "create a BRS" / "clarify requirements" / "find gaps" | Product Owner | `product_owner.create_business_intake` | `skills/2-business-intake/01-create-business-intake-summary.md` |
| `@architect` / "review the architecture" / "create architecture rules" | Architect | `architect.review_initial_architecture` | `skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| `@delivery-lead` / "define the delivery structure" / "create user stories" | Delivery Lead | `delivery_lead.create_delivery_structure` | `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| `@qa` / "create BDD scenarios" / "write acceptance tests" | QA Analyst | `qa.create_bdd_scenarios` | `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@qa` / "create test plans" / "test plan per story" / "risk-based testing" | QA Analyst | `qa.create_test_plan_per_story` | `skills/4-engineering-readiness/quality-gates/create-test-plan-per-story.md` |
| `@security` / "security review" / "PII risk" / "threat model" | Security Reviewer | `security.create_security_review` | `skills/4-engineering-readiness/quality-gates/create-security-review.md` |
| `@engineering-lead` / "create the handoff" / "generate OpenSpec" | Engineering Lead | `engineering_lead.create_openspec_handoff` | `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| `@reviewer` / "review the code" / "do a security review" | Reviewer | `reviewer.senior_code_review` | `skills/9-reviewers/01-senior-code-review.md` |

---

## Trigger-to-skill lookup

| Trigger | Skill to invoke | Notes |
|---|---|---|
| "continue" / "what next" / `@orchestrator` | `orchestrator.run_workflow` | Always the default catch-all trigger |
| "repair" / "fix the workflow state" / "reset the workflow" / "workflow is broken" / "wrong stage" | `orchestrator.repair_workspace_state` | Scan disk, correct state file, reset next_action to correct stage — run before resuming workflow |
| BRS missing + user provides notes or document | `product_owner.create_brs` | Use `product_owner.convert_brs_to_markdown` if Word/PDF |
| Business intake missing | `product_owner.create_business_intake` | After routing exists |
| Business rules missing / "extract business rules" / "business rules" | `product_owner.extract_business_rules` | After business intake; before architecture draft |
| Actors missing / "extract actors" / "actors and personas" | `product_owner.extract_actors` | After business intake |
| Process flows missing / "process flows" / "business flows" | `product_owner.create_process_flows` | Draft (stage 2d): after actors-and-personas (2c); confirmed (stage 9b): after delivery structure confirmed (9) |
| Use case specs missing / "use cases" / "use case specs" | `product_owner.create_use_case_specs` | Draft (stage 2e): after process flows draft (2d); confirmed (stage 9c): after process flows confirmed (9b) |
| Entity model missing / "entity model" / "data model" | `architect.create_entity_model` | After data-contract accepted (or BRS data requirements if gate not triggered) |
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
| BDD gate — stage 9b (three amigos) | `qa.create_bdd_scenarios` | Runs after delivery structure confirmed (stage 9) — does NOT require engineering readiness |
| Test plans missing / "create test plans" / "test plan per story" | `qa.create_test_plan_per_story` | Stage 9f — runs after BDD accepted (9b) and story enrichment (9e); produces one F-XXX.X-test-plan.md per story |
| `quality-gates/test-strategy.md` missing or not Accepted | `qa.create_test_strategy` | Stage 10 — always required; runs after BDD (9b) and test plans (9f); references SCN-NNN and TC-NNN IDs |
| PII / auth / authorization / secrets / exposure risk | `security.create_security_review` | Mandatory gate when triggered |
| High-risk security boundary identified | `security.create_threat_model` | In addition to security review |
| Data ownership / schema / retention / PII / residency change | `security.create_data_contract` | Mandatory gate when triggered |
| "create review package" / "review package" / "stakeholder view" | `delivery_lead.create_review_package` | Can run after handoff; partial run possible from business intake onward |
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
Fails if: heading-only or empty tables; placeholder text ("TBC", "pending"); open decisions already resolved in `state/open-decisions.md`; DRAFT notice after architect sign-off; "Not ready" when all blockers are resolved.

**Rule 4 — Always run the workflow, never answer around it.**
Any question about status, next steps, progress, or what to do → open and execute `.brs2spec/brs-to-spec-run-workflow.md`. Do not answer from BRS content.

**Rule 5 — Never produce a free-form plan from BRS content.**
Every next step must come from a framework artifact, not from reading the BRS.

**Rule 6 — Never advance past a stage with a failing artifact.**
Verify done criteria before advancing. Stub artifacts fail.

**Rule 7 — Run the stale artifact check before every stage assessment.**
Read content, not just filenames. Before any stage assessment: read `state/open-decisions.md`, find Resolved rows, open every home artifact listed, verify it no longer shows that decision as open. Fix stale artifacts before proceeding.

---

## Workspace

One initiative at a time. Standard shape: `initiatives/<id>-<slug>/`. All paths relative to the active workspace.

New human-provided information (PO decision, vendor answer, legal input) → `input/input-package.md`, section "Decisions and Clarifications Received". Never tell the user to edit the BRS or architecture directly.

Do not start implementation until the workspace has: `engineering-readiness/readiness-check.md`, required quality gates accepted, and `specs/.../tasks.md` or `standalone-delivery/.../tasks.md`.

Allowed paths only:

```
state/          input/           business-intake/    business-analysis/
architecture/   planning/        engineering-readiness/               quality-gates/
specs/<deliverable>/                      standalone-delivery/<deliverable>/
review-package/ perspectives/
```

Never create `engineering-readiness/runbooks/`, `engineering-readiness/observability/`, or any folder not listed above.

---

## Intent triggers and persona routing

Named personas bypass the orchestrator and load only their own prompt. Orchestrator triggers run the full workflow.

| User says | Action |
|---|---|
| "repair" / "fix the workflow" / "reset the workflow" / "workflow is broken" / "wrong stage" / "started from wrong stage" | Run `.brs2spec/skills/0-repair/repair-workspace-state.md` — scan disk, correct state file, set next_action to correct stage |
| "what is the next step?" / "what should I do?" / "what is the status?" | Read `state/open-decisions.md` first, then run `.brs2spec/brs-to-spec-run-workflow.md` |
| "what is blocking us?" / "what decisions are open?" | Read `state/open-decisions.md` and report |
| "continue" / "run the framework" / "pick up where we left off" / `@orchestrator` | Run `.brs2spec/brs-to-spec-run-workflow.md` from current stage |
| "create a BRS" / "write a BRS" | Run `.brs2spec/skills/0-intake/00-create-brs.md` |
| "accept all quality gates" / "accept all and continue" | Set `Status: Accepted` in each triggered gate, update workflow-state.json, advance |
| "create the handoff" / "generate the handoff" / `@engineering-lead` | Run `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| `@architect` / "review the architecture" / "create architecture rules" | Run `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| `@delivery-lead` / "define the delivery structure" / "create user stories" | Run `.brs2spec/skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| `@qa` / "create BDD scenarios" / "write acceptance tests" | Run `.brs2spec/skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@reviewer` / "review the code" / "do a security review" | Run the relevant prompt from `.brs2spec/skills/9-reviewers/` |

---

## Artifact-to-skill lookup

| Artifact | Owning skill | Persona file |
|---|---|---|
| `input/brs.md` | `product_owner.create_brs` or `product_owner.convert_brs_to_markdown` | `module-personas/product-owner.md` |
| `input/architecture.md` | `architect.convert_architecture_to_markdown` or `architect.draft_architecture_from_brs` | `module-personas/architect.md` |
| `state/routing-decision.md` | (routing prompt) | orchestrator |
| `business-intake/business-intake-summary.md` | `product_owner.create_business_intake` | `module-personas/product-owner.md` |
| `business-intake/business-rules.md` | `product_owner.extract_business_rules` | `module-personas/product-owner.md` |
| `business-analysis/actors-and-personas.md` | `product_owner.extract_actors` | `module-personas/product-owner.md` |
| `business-analysis/process-flows.md` | `product_owner.create_process_flows` | `module-personas/product-owner.md` |
| `business-analysis/use-case-spec.md` | `product_owner.create_use_case_specs` | `module-personas/product-owner.md` |
| `business-analysis/entity-model.md` | `architect.create_entity_model` | `module-personas/architect.md` |
| `business-intake/gaps-and-questions.md` | `product_owner.find_gaps_and_questions` | `module-personas/product-owner.md` |
| `business-intake/business-test-expectations.md` | `product_owner.create_business_test_expectations` | `module-personas/product-owner.md` |
| `architecture/architecture-review.md` | `architect.review_initial_architecture` | `module-personas/architect.md` |
| `architecture/architecture-rules.md` | `architect.create_architecture_rules` | `module-personas/architect.md` |
| `architecture/existing-system-impact.md` | `architect.review_existing_system_impact` | `module-personas/architect.md` |
| `state/open-decisions.md` | `orchestrator.maintain_open_decisions` | `module-personas/orchestrator.md` |
| `planning/delivery-structure/` (folder: overview.md + epic subfolders) | `delivery_lead.create_delivery_structure` | `module-personas/delivery-lead.md` |
| `planning/software-modules.md` | `delivery_lead.identify_software_modules` | `module-personas/delivery-lead.md` |
| `planning/capability-to-module-map.md` | `delivery_lead.map_capabilities_to_modules` | `module-personas/delivery-lead.md` |
| `planning/delivery-increments.md` | `delivery_lead.define_delivery_increments` | `module-personas/delivery-lead.md` |
| `planning/traceability-matrix.md` | `delivery_lead.create_traceability_matrix` | `module-personas/delivery-lead.md` |
| `state/workflow-state.json` (repair) | `orchestrator.repair_workspace_state` | `module-personas/orchestrator.md` |
| `state/workflow-state.json` (maintain) | `orchestrator.maintain_state` | `module-personas/orchestrator.md` |
| `engineering-readiness/readiness-check.md` | `engineering_lead.check_engineering_readiness` | `module-personas/engineering-lead.md` |
| `engineering-readiness/initiative-context.md` | `engineering_lead.generate_initiative_context` | `module-personas/engineering-lead.md` |
| `quality-gates/bdd/` (folder) | `qa.create_bdd_scenarios` | `module-personas/qa-analyst.md` |
| `quality-gates/test-plans/` (folder — one F-XXX.X-test-plan.md per story) | `qa.create_test_plan_per_story` | `module-personas/qa-analyst.md` |
| `quality-gates/test-strategy.md` | `qa.create_test_strategy` | `module-personas/qa-analyst.md` |
| `quality-gates/security-review.md` | `security.create_security_review` | `module-personas/security-reviewer.md` |
| `quality-gates/threat-model.md` | `security.create_threat_model` | `module-personas/security-reviewer.md` |
| `quality-gates/data-contract.md` | `security.create_data_contract` | `module-personas/security-reviewer.md` |
| `review-package/status.md` | `delivery_lead.create_review_package` | `module-personas/delivery-lead.md` |
| `specs/` | `engineering_lead.create_openspec_handoff` | `module-personas/engineering-lead.md` |
| `standalone-delivery/` | `engineering_lead.create_standalone_handoff` | `module-personas/engineering-lead.md` |
| `perspectives/agile-planning/gitlab-planning-view.md` | `delivery_lead.create_agile_planning_view` | `module-personas/delivery-lead.md` |

---

## Loading rules

1. Load `module-index.md` first. Select the skill needed from the Skill Index. Do not load every prompt.
2. One skill per invocation. Load only the prompt for the selected skill.
3. Before generating output, load only `module-personas/<persona>.md` for the active persona — do not load `module-full.md` or all persona files.
4. Respect gate order. Do not invoke a downstream skill if its upstream gate artifact is missing or stale.
5. Verify artifact quality — an artifact passes only when its content meets done criteria, not just when the file exists. Done criteria are in the relevant `module-personas/<persona>.md` file.
6. Never skip a stage. Note the risk and scaffold instead.
7. Persona boundary. Only invoke skills belonging to the current persona; hand off explicitly otherwise.

---

## Stop rules

Stop and request human input when:

1. BRS missing and no source material provided — scaffold `input/input-package.md` with questions; stop.
2. Routing requires judgment only the user can make — ask the single specific question; stop.
3. Business scope is ambiguous and unresolvable from existing artifacts — scaffold scope-clarification stub; stop.
4. Blocking open decisions exist (`state/open-decisions.md` has `blocking_count > 0`) — report blocking decisions; stop.
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
