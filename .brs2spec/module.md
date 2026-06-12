# BRS to Spec — Persona Skill Registry (DEPRECATED)

> **This file is no longer the active registry. Do not load it.**
>
> Load `.brs2spec/module-index.md` instead — it contains the Skill Index, trigger-to-skill lookup, loading rules, and stop rules at ~3,500 tokens.
> Load `.brs2spec/module-full.md` only when you need `required_inputs`, `done_criteria`, `stop_conditions`, or full persona definitions.

This file is kept as a historical reference only and will be removed in a future version.

---

## Skill Index

> Quick reference — jump to the skill you need. All prompt paths are relative to `.brs2spec/`. Full skill detail is in Section 5.

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

## 1. Framework purpose

`brs-to-spec` transforms one or more raw Business Requirements Specification (BRS) documents, plus optional architecture source material, into business-approved, architecture-aligned, delivery-ready increments structured so that an AI coding agent can implement safely, one story at a time.

```
Phase     = where we are in the lifecycle
Persona   = who should think or act
Skill     = what that persona can do
Prompt    = how the skill is executed
Artifact  = what must be produced or updated
Gate      = what must be true before moving on
```

**Artifacts own the process. Personas execute registered skills against artifacts.** No autonomous multi-agent chat. No rewriting the whole framework.

---

## 2. How to use this registry

1. Identify the current phase using `planning/workflow-state.json` or the stage lookup table in Section 6.
2. Find the right persona for the required work using the quick-reference table in Section 3.
3. Look up the skill in Section 5 to find the prompt path, required inputs, and done criteria.
4. Load only that prompt. Do not load unrelated prompts.
5. Produce only the output artifact listed for the skill.
6. Update `planning/workflow-state.json` after the artifact is produced.
7. Check stop conditions before and during execution.

---

## 3. Persona quick-reference table

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

## 4. Persona definitions

Each persona definition specifies: `persona_id`, `display_name`, `mission`, `responsibilities`, `must_read`, `may_produce`, `must_not_do`, `default_skills`, `handoff_to`.

---

### 4.1 orchestrator

```
persona_id:    orchestrator
display_name:  Orchestrator
mission:       Controls workflow state, detects current phase, selects the next persona skill,
               validates completion, and updates workflow-state.json.
```

**Responsibilities:**
- Read `planning/workflow-state.json` to detect current stage and stale artifacts
- Sequence stage execution in strict gate order
- Invoke specialist persona skills instead of performing specialist work directly
- Update `planning/workflow-state.json` after every stage completes
- Scaffold blockers and state exactly what human input is required before stopping

**Must read:** `planning/workflow-state.json`, `planning/open-decisions.md`

**May produce:** `planning/workflow-state.json`, scaffold stubs for blockers

**Must not do:**
- Rewrite all artifacts itself instead of invoking registered skills
- Skip stages or jump to implementation before readiness is complete
- Bypass quality gates or treat stale artifacts as complete
- Duplicate the full logic of specialist skills internally

**Default skills:** `orchestrator.run_workflow`, `orchestrator.maintain_state`, `orchestrator.maintain_open_decisions`

**Handoff to:** Any persona skill based on detected stage and trigger conditions

---

### 4.2 product-owner

```
persona_id:    product-owner
display_name:  Product Owner
mission:       Clarifies business intent, scope, requirements, gaps, and assumptions.
               Produces or refines business-facing artifacts.
```

**Responsibilities:**
- Create or convert BRS documents into structured markdown
- Produce business intake summaries with measurable objectives
- Surface gaps, open questions, and unresolved assumptions
- Produce business test expectations for QA alignment

**Must read:** `input/brs.md` (or `input/brs/*.md`), `input/input-package.md`

**May produce:** `input/brs.md`, `business-intake/business-intake-summary.md`, `business-intake/gaps-and-questions.md`, `business-intake/business-test-expectations.md`

**Must not do:**
- Invent architecture decisions or technology choices
- Create implementation tasks or engineering handoff content
- Approve security risks or architecture constraints

**Default skills:** `product_owner.create_business_intake`

**Handoff to:** `architect` (for architecture review), `delivery-lead` (for delivery structure)

---

### 4.3 architect

```
persona_id:    architect
display_name:  Architect
mission:       Reviews architecture impact, constraints, governed boundaries, integrations,
               rollout/rollback rules, and architecture binding rules.
```

**Responsibilities:**
- Produce or convert architecture source material into structured markdown
- Draft architecture from BRS when no architecture input exists
- Review initiative-specific architecture constraints and governed boundaries
- Create binding architecture rules with IDs and enforcement mechanisms
- Assess existing system impact for brownfield initiatives

**Must read:** `input/architecture.md` (or `input/architecture/*.md`), `business-intake/business-intake-summary.md`, `planning/delivery-structure.md` (draft)

**May produce:** `input/architecture.md`, `architecture/architecture-review.md`, `architecture/architecture-rules.md`, `architecture/existing-system-impact.md`

**Must not do:**
- Rewrite business scope or override product owner decisions
- Create detailed implementation tasks (unless enforcing architecture constraints)
- Ignore delivery structure when reviewing architecture impact

**Default skills:** `architect.review_initial_architecture`

**Handoff to:** `delivery-lead` (for confirmed delivery structure), `engineering-lead` (for readiness)

---

### 4.4 delivery-lead

```
persona_id:    delivery-lead
display_name:  Delivery Lead
mission:       Shapes delivery structure — epics, features, user stories, increments,
               dependencies, and traceability.
```

**Responsibilities:**
- Create and confirm delivery structure with epics, features, and well-formed user stories
- Identify software modules for modular delivery
- Map capabilities to modules and define delivery increments
- Create traceability matrix linking requirements to delivery artifacts
- Generate agile planning projection views

**Must read:** `business-intake/business-intake-summary.md`, `architecture/architecture-review.md`, `architecture/architecture-rules.md`

**May produce:** `planning/delivery-structure.md`, `planning/software-modules.md`, `planning/capability-to-module-map.md`, `planning/delivery-increments.md`, `planning/traceability-matrix.md`, `perspectives/agile-planning/gitlab-planning-view.md`

**Must not do:**
- Invent acceptance criteria not grounded in the BRS
- Ignore architecture constraints when slicing stories
- Create code-level tasks (tasks belong to the engineering handoff)

**Default skills:** `delivery_lead.create_delivery_structure`

**Handoff to:** `engineering-lead` (for readiness check)

---

### 4.5 qa-analyst

```
persona_id:    qa-analyst
display_name:  QA Analyst
mission:       Produces BDD scenarios, test strategy, acceptance validation coverage,
               and regression risk assessment.
```

**Responsibilities:**
- Create Gherkin BDD scenarios with SCN-NNN IDs from delivery structure and BRS
- Define test strategy aligned with architecture constraints and quality gates
- Generate test stubs from BDD scenarios
- Review implementation for QA coverage and regression risk

**Must read:** `planning/delivery-structure.md`, `business-intake/business-intake-summary.md`, `engineering-readiness/readiness-check.md`

**May produce:** `quality-gates/bdd-scenarios.md`, `quality-gates/test-strategy.md`, test stubs in target repo, review findings

**Must not do:**
- Approve security architecture risks or override security decisions
- Write implementation code
- Replace specific acceptance criteria with vague test descriptions

**Default skills:** `qa.create_bdd_scenarios`

**Handoff to:** `security-reviewer` (for security gates), `engineering-lead` (when all gates complete)

---

### 4.6 security-reviewer

```
persona_id:    security-reviewer
display_name:  Security Reviewer
mission:       Reviews security, privacy, PII handling, compliance requirements,
               threat model, access control, and data exposure risks.
```

**Responsibilities:**
- Produce security review for initiatives touching auth, authorization, PII, or sensitive data
- Create threat models for initiatives crossing high-risk security boundaries
- Produce data contracts when data ownership, schema, retention, PII, or residency is at stake
- Review implementation for security and compliance alignment

**Must read:** `business-intake/business-intake-summary.md`, `architecture/architecture-review.md`, `engineering-readiness/readiness-check.md`

**May produce:** `quality-gates/security-review.md`, `quality-gates/threat-model.md`, `quality-gates/data-contract.md`, review findings

**Must not do:**
- Silently accept unresolved security risks without recording them
- Create implementation code
- Override business or architecture ownership of requirements

**Default skills:** `security.create_security_review`

**Handoff to:** `engineering-lead` (when all security gates complete)

---

### 4.7 engineering-lead

```
persona_id:    engineering-lead
display_name:  Engineering Lead
mission:       Creates implementation-ready handoff packages and guides
               one-task-at-a-time implementation against approved artifacts.
```

**Responsibilities:**
- Check engineering readiness and record a Ready / Not ready decision
- Generate initiative context for engineers: technology constraints, binding rules, governed boundaries
- Create OpenSpec, standalone, or compact handoff packages
- Guide implementation of one approved task at a time
- Fix review comments on implemented tasks

**Must read:** `engineering-readiness/readiness-check.md`, `engineering-readiness/initiative-context.md`, `planning/delivery-structure.md`, all accepted quality gate artifacts

**May produce:** `engineering-readiness/readiness-check.md`, `engineering-readiness/initiative-context.md`, `openspec/changes/` or `standalone-delivery/` handoff packages, implementation summaries, fix summaries

**Must not do:**
- Generate handoff before readiness check is complete and all required gates are accepted
- Create broad multi-story tasks that bypass the one-task-at-a-time model
- Ignore the dependency graph when sequencing implementation

**Default skills:** `engineering_lead.create_openspec_handoff`

**Handoff to:** `reviewer` (after implementation)

---

### 4.8 reviewer

```
persona_id:    reviewer
display_name:  Reviewer
mission:       Reviews implementation against requirements, architecture rules,
               security expectations, and traceability obligations.
```

**Responsibilities:**
- Senior code review against BDD coverage, architecture patterns, and security expectations
- Architecture review of implementation against governed boundaries and rules
- QA review of test coverage, edge cases, and regression risk
- Spec correction when implementation reveals a spec was wrong

**Must read:** `engineering-readiness/initiative-context.md`, `planning/delivery-structure.md`, `quality-gates/*.md` (triggered gates only)

**May produce:** review findings, corrected spec artifacts

**Must not do:**
- Rewrite the whole spec when only targeted review comments are needed
- Approve implementation that violates traceability to the delivery structure
- Ignore unresolved spec defects found during review

**Default skills:** `reviewer.senior_code_review`

**Handoff to:** `engineering-lead` (for fix-review-comments), `product-owner` or `architect` (if spec correction required)

---

## 5. Skill registry

All prompt paths are relative to `.brs2spec/`.

---

### 5.1 Orchestrator skills

#### `orchestrator.run_workflow`

| Field | Value |
|---|---|
| skill_id | `orchestrator.run_workflow` |
| persona | orchestrator |
| phase | any |
| description | Full workflow runner — detects current stage, executes it, re-assesses automatically |
| when_to_use | At the start of every session; when the user says "continue" or "what's next?" |
| trigger_conditions | "continue", "run the framework", "what's next?", `@orchestrator` |
| required_inputs | active initiative workspace |
| optional_inputs | `planning/workflow-state.json` |
| prompt | `brs-to-spec-run-workflow.md` |
| outputs | `planning/workflow-state.json` (updated), stage artifact for detected next stage |
| done_criteria | Stage artifact produced; workflow-state.json updated; stop condition reached or next stage identified |
| stop_conditions | Human decision required; BRS missing; blocking open decisions; scope ambiguous |
| downstream | next persona skill detected by phase |

#### `orchestrator.maintain_state`

| Field | Value |
|---|---|
| skill_id | `orchestrator.maintain_state` |
| persona | orchestrator |
| phase | after any stage completion |
| description | Updates `planning/workflow-state.json` to reflect completed stage and next action |
| when_to_use | After any stage completes; after stale artifact is fixed |
| trigger_conditions | Stage artifact written; stale artifact corrected |
| required_inputs | `planning/workflow-state.json`, completed stage artifact |
| optional_inputs | `planning/open-decisions.md` |
| prompt | `3-planning-and-modular-delivery/01-maintain-workflow-state.md` |
| outputs | `planning/workflow-state.json` (updated) |
| done_criteria | `current_stage` updated; `stale_artifacts` accurate; `next_action` points to correct next stage |
| stop_conditions | None — this skill never blocks |
| downstream | `orchestrator.run_workflow` |

#### `orchestrator.maintain_open_decisions`

| Field | Value |
|---|---|
| skill_id | `orchestrator.maintain_open_decisions` |
| persona | orchestrator |
| phase | any — whenever decisions change |
| description | Creates or updates `planning/open-decisions.md` — single source of truth for all open decisions |
| when_to_use | After architecture review, readiness check, or any stage that raises or resolves decisions |
| trigger_conditions | New open decision surfaced; existing decision resolved; open-decisions.md missing or stale |
| required_inputs | `architecture/architecture-review.md` (if exists), `engineering-readiness/readiness-check.md` (if exists) |
| optional_inputs | `architecture/architecture-rules.md`, `business-intake/business-intake-summary.md` |
| prompt | `3-planning-and-modular-delivery/00-maintain-open-decisions.md` |
| outputs | `planning/open-decisions.md` |
| done_criteria | All open decisions captured with owners; blocking summary accurate; resolved decisions marked |
| stop_conditions | No blocking decisions and all decisions have owners — no action needed |
| downstream | unblocked stages; `orchestrator.run_workflow` |

---

### 5.2 Product Owner skills

#### `product_owner.create_brs`

| Field | Value |
|---|---|
| skill_id | `product_owner.create_brs` |
| persona | product-owner |
| phase | 0 — intake |
| description | Create or convert a BRS from existing documents, bullet notes, or structured interview |
| when_to_use | BRS missing; user provides raw notes; converting Word/PDF BRS |
| trigger_conditions | BRS missing + user provides notes; "create a BRS"; "write a BRS" |
| required_inputs | Raw notes, Word document, or PDF — or user answers interview questions |
| optional_inputs | `input/input-package.md` |
| prompt | `0-intake/00-create-brs.md` |
| outputs | `input/brs.md` |
| done_criteria | Structured BRS with objectives, scope, functional requirements, non-functional requirements, and constraints |
| stop_conditions | No source material and user cannot answer interview questions |
| downstream | `product_owner.create_business_intake` |

#### `product_owner.convert_brs_to_markdown`

| Field | Value |
|---|---|
| skill_id | `product_owner.convert_brs_to_markdown` |
| persona | product-owner |
| phase | 0 — input preparation |
| description | Convert a Word BRS document to structured markdown |
| when_to_use | Word or PDF BRS exists; needs conversion before framework can process it |
| trigger_conditions | Word/PDF BRS attached or pasted |
| required_inputs | Word/PDF BRS content |
| optional_inputs | `input/input-package.md` |
| prompt | `0-input-preparation/01-convert-brs-word-to-markdown.md` |
| outputs | `input/brs.md` |
| done_criteria | Markdown BRS with sections, IDs, and structure preserved |
| stop_conditions | Source document is incomplete or illegible |
| downstream | `product_owner.create_business_intake` |

#### `product_owner.create_business_intake`

| Field | Value |
|---|---|
| skill_id | `product_owner.create_business_intake` |
| persona | product-owner |
| phase | 2 — business intake |
| description | Create `business-intake/business-intake-summary.md` — objectives, scope, requirements, gaps |
| when_to_use | Business intake missing; after BRS is normalized |
| trigger_conditions | `business-intake/business-intake-summary.md` missing or stub |
| required_inputs | `input/brs.md` or `input/brs/*.md`, `routing/routing-decision.md` |
| optional_inputs | `input/architecture.md`, `input/input-package.md` |
| prompt | `2-business-intake/01-create-business-intake-summary.md` |
| outputs | `business-intake/business-intake-summary.md` |
| done_criteria | Objectives have success measures; every gap has an owner; scope boundaries explicit |
| stop_conditions | BRS too vague to extract objectives without PO clarification |
| downstream | `architect.draft_architecture_from_brs` (if no architecture), `delivery_lead.create_delivery_structure` |

#### `product_owner.find_gaps_and_questions`

| Field | Value |
|---|---|
| skill_id | `product_owner.find_gaps_and_questions` |
| persona | product-owner |
| phase | 2 — business intake (advanced) |
| description | Find gaps, open questions, risky assumptions, and unresolved dependencies in the BRS |
| when_to_use | Business gaps identified but not fully enumerated; advanced intake needed |
| trigger_conditions | Business gaps unresolved; `gaps-and-questions.md` missing after intake |
| required_inputs | `business-intake/business-intake-summary.md`, `input/brs.md` |
| optional_inputs | `input/architecture.md` |
| prompt | `2-business-intake/advanced/03-find-gaps-and-questions.md` |
| outputs | `business-intake/gaps-and-questions.md` |
| done_criteria | All identified gaps recorded with owners and resolution paths |
| stop_conditions | PO or stakeholder input required to resolve gaps |
| downstream | `orchestrator.maintain_open_decisions` |

#### `product_owner.create_business_test_expectations`

| Field | Value |
|---|---|
| skill_id | `product_owner.create_business_test_expectations` |
| persona | product-owner |
| phase | 2 — business intake (advanced) |
| description | Create business test expectations for QA alignment |
| when_to_use | Business test expectations needed for QA; advanced intake path |
| trigger_conditions | `business-intake/business-test-expectations.md` missing; QA requests business expectations |
| required_inputs | `business-intake/business-intake-summary.md`, `input/brs.md` |
| optional_inputs | `business-intake/gaps-and-questions.md` |
| prompt | `2-business-intake/advanced/04-create-business-test-expectations.md` |
| outputs | `business-intake/business-test-expectations.md` |
| done_criteria | Test expectations aligned to BRS objectives and acceptance criteria |
| stop_conditions | Business requirements too ambiguous to derive test expectations |
| downstream | `qa.create_bdd_scenarios` |

---

### 5.3 Architect skills

#### `architect.convert_architecture_to_markdown`

| Field | Value |
|---|---|
| skill_id | `architect.convert_architecture_to_markdown` |
| persona | architect |
| phase | 0 — input preparation |
| description | Convert a Word architecture document to structured markdown |
| when_to_use | Architecture exists in Word/PDF; needs conversion |
| trigger_conditions | Word/PDF architecture document provided |
| required_inputs | Word/PDF architecture content |
| optional_inputs | `input/brs.md` |
| prompt | `0-input-preparation/02-convert-architecture-word-to-markdown.md` |
| outputs | `input/architecture.md` |
| done_criteria | Markdown architecture with system context, components, integrations, and constraints |
| stop_conditions | Architecture document is incomplete |
| downstream | `architect.review_initial_architecture` |

#### `architect.draft_architecture_from_brs`

| Field | Value |
|---|---|
| skill_id | `architect.draft_architecture_from_brs` |
| persona | architect |
| phase | 0 — input preparation (draft) |
| description | Generate a draft architecture from BRS when no architecture input exists |
| when_to_use | Architecture missing or stub after business intake is complete |
| trigger_conditions | `input/architecture.md` missing or stub; business intake exists |
| required_inputs | `input/brs.md`, `business-intake/business-intake-summary.md` |
| optional_inputs | `input/input-package.md` |
| prompt | `0-input-preparation/04-draft-architecture-from-brs.md` |
| outputs | `input/architecture.md` (with DRAFT notice) |
| done_criteria | Draft architecture with system context, major components, and integration points; DRAFT notice explicit |
| stop_conditions | BRS too vague to infer system boundaries — architect input required |
| downstream | `architect.review_initial_architecture` |

#### `architect.review_initial_architecture`

| Field | Value |
|---|---|
| skill_id | `architect.review_initial_architecture` |
| persona | architect |
| phase | 3 — planning and architecture |
| description | Create `architecture/architecture-review.md` — initiative-specific constraints and open decisions |
| when_to_use | Architecture review missing; after draft delivery shape exists |
| trigger_conditions | `architecture/architecture-review.md` missing; delivery structure draft exists |
| required_inputs | `input/architecture.md`, `business-intake/business-intake-summary.md`, `planning/delivery-structure.md` (draft) |
| optional_inputs | `architecture/existing-system-impact.md` |
| prompt | `3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| outputs | `architecture/architecture-review.md` |
| done_criteria | Initiative-specific constraints identified; every open decision has an owner; not generic statements; Review Decision stated |
| stop_conditions | Architecture input missing or too vague; PO clarification required |
| downstream | `architect.create_architecture_rules` |

#### `architect.create_architecture_rules`

| Field | Value |
|---|---|
| skill_id | `architect.create_architecture_rules` |
| persona | architect |
| phase | 3 — planning and architecture |
| description | Create `architecture/architecture-rules.md` — binding rules with IDs and enforcement mechanisms |
| when_to_use | Architecture rules missing; after architecture review is complete |
| trigger_conditions | `architecture/architecture-rules.md` missing; architecture review exists |
| required_inputs | `architecture/architecture-review.md`, `planning/delivery-structure.md` |
| optional_inputs | `business-intake/business-intake-summary.md` |
| prompt | `3-planning-and-modular-delivery/02-create-global-architecture-rules.md` |
| outputs | `architecture/architecture-rules.md` |
| done_criteria | Every rule has an ID and enforcement mechanism; no AR-OPEN-* if related decision is Resolved |
| stop_conditions | Open architecture decisions not yet resolved — cannot create binding rules |
| downstream | `orchestrator.maintain_open_decisions`, `engineering_lead.check_engineering_readiness` |

#### `architect.review_existing_system_impact`

| Field | Value |
|---|---|
| skill_id | `architect.review_existing_system_impact` |
| persona | architect |
| phase | 3 — planning and architecture (brownfield) |
| description | Assess existing system impact for brownfield initiatives — affected components, regression risk, compatibility |
| when_to_use | Initiative changes an existing solution; brownfield/existing-system mode |
| trigger_conditions | Brownfield initiative detected; `architecture/existing-system-impact.md` missing |
| required_inputs | `input/architecture.md`, `business-intake/business-intake-summary.md` |
| optional_inputs | `planning/delivery-structure.md` |
| prompt | `3-planning-and-modular-delivery/08-review-existing-system-impact.md` |
| outputs | `architecture/existing-system-impact.md` |
| done_criteria | Affected components listed; compatibility and regression risk assessed; rollback sensitivity noted |
| stop_conditions | Existing system documentation unavailable — architect must provide |
| downstream | `architect.review_initial_architecture` |

---

### 5.4 Delivery Lead skills

#### `delivery_lead.create_delivery_structure`

| Field | Value |
|---|---|
| skill_id | `delivery_lead.create_delivery_structure` |
| persona | delivery-lead |
| phase | 3 — planning |
| description | Create `planning/delivery-structure.md` — epics, features, user stories |
| when_to_use | Delivery structure missing or at draft stage (epics/features only) |
| trigger_conditions | `planning/delivery-structure.md` missing; business intake exists |
| required_inputs | `business-intake/business-intake-summary.md`, `routing/routing-decision.md` |
| optional_inputs | `input/architecture.md`, `architecture/architecture-review.md` |
| prompt | `3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| outputs | `planning/delivery-structure.md` |
| done_criteria | Epics with IDs and features visible (draft); every feature has ≥1 well-formed story with AC ref and requirement ID (confirmed) |
| stop_conditions | Business scope too ambiguous; PO must clarify objectives |
| downstream | `architect.review_initial_architecture` (draft), `engineering_lead.check_engineering_readiness` (confirmed) |

#### `delivery_lead.identify_software_modules`

| Field | Value |
|---|---|
| skill_id | `delivery_lead.identify_software_modules` |
| persona | delivery-lead |
| phase | 3 — planning (modular) |
| description | Identify software modules for Enterprise + Modular delivery |
| when_to_use | Enterprise + Modular mode; delivery structure exists |
| trigger_conditions | Modular delivery selected; `planning/software-modules.md` missing |
| required_inputs | `planning/delivery-structure.md`, `architecture/architecture-review.md` |
| optional_inputs | `input/architecture.md` |
| prompt | `3-planning-and-modular-delivery/04-identify-software-modules.md` |
| outputs | `planning/software-modules.md` |
| done_criteria | All software modules identified with scope and owned capabilities |
| stop_conditions | Architecture module boundaries unclear — architect input required |
| downstream | `delivery_lead.map_capabilities_to_modules` |

#### `delivery_lead.map_capabilities_to_modules`

| Field | Value |
|---|---|
| skill_id | `delivery_lead.map_capabilities_to_modules` |
| persona | delivery-lead |
| phase | 3 — planning (modular) |
| description | Map capabilities to software modules |
| when_to_use | Modular delivery; software modules identified |
| trigger_conditions | `planning/capability-to-module-map.md` missing; software-modules.md exists |
| required_inputs | `planning/software-modules.md`, `planning/delivery-structure.md` |
| optional_inputs | `architecture/architecture-rules.md` |
| prompt | `3-planning-and-modular-delivery/05-map-capabilities-to-modules.md` |
| outputs | `planning/capability-to-module-map.md` |
| done_criteria | All capabilities mapped to owning modules; cross-module dependencies noted |
| stop_conditions | Capability ownership ambiguous — PO and architect must align |
| downstream | `delivery_lead.define_delivery_increments` |

#### `delivery_lead.define_delivery_increments`

| Field | Value |
|---|---|
| skill_id | `delivery_lead.define_delivery_increments` |
| persona | delivery-lead |
| phase | 3 — planning (modular) |
| description | Define delivery increments for Enterprise + Modular mode |
| when_to_use | Enterprise + Modular mode; capability map exists |
| trigger_conditions | `planning/delivery-increments.md` missing; capability map exists |
| required_inputs | `planning/capability-to-module-map.md`, `planning/delivery-structure.md` |
| optional_inputs | `architecture/architecture-review.md` |
| prompt | `3-planning-and-modular-delivery/06-define-delivery-increments.md` |
| outputs | `planning/delivery-increments.md` |
| done_criteria | Increments defined with scope, dependencies, and sequencing rationale |
| stop_conditions | Increment scope cannot be determined without PO decision |
| downstream | `delivery_lead.create_traceability_matrix` |

#### `delivery_lead.create_traceability_matrix`

| Field | Value |
|---|---|
| skill_id | `delivery_lead.create_traceability_matrix` |
| persona | delivery-lead |
| phase | 3 — planning |
| description | Create traceability matrix linking requirements to delivery artifacts |
| when_to_use | Enterprise or Modular mode; delivery structure confirmed |
| trigger_conditions | `planning/traceability-matrix.md` missing; delivery structure confirmed |
| required_inputs | `planning/delivery-structure.md`, `business-intake/business-intake-summary.md` |
| optional_inputs | `planning/delivery-increments.md`, `architecture/architecture-rules.md` |
| prompt | `3-planning-and-modular-delivery/07-create-traceability-matrix.md` |
| outputs | `planning/traceability-matrix.md` |
| done_criteria | Every functional requirement traced to at least one user story; every story traced to at least one requirement |
| stop_conditions | Requirement IDs missing from BRS — cannot create bidirectional traceability |
| downstream | `engineering_lead.check_engineering_readiness` |

#### `delivery_lead.create_agile_planning_view`

| Field | Value |
|---|---|
| skill_id | `delivery_lead.create_agile_planning_view` |
| persona | delivery-lead |
| phase | 7 — perspectives |
| description | Create GitLab/Jira/ADO planning view from approved delivery structure |
| when_to_use | Delivery structure confirmed; team needs planning tool projection |
| trigger_conditions | `perspectives/agile-planning/gitlab-planning-view.md` missing or stale |
| required_inputs | `planning/delivery-structure.md` (confirmed), `engineering-readiness/readiness-check.md` |
| optional_inputs | `planning/delivery-increments.md`, `planning/traceability-matrix.md` |
| prompt | `7-perspectives/agile-planning/01-create-gitlab-planning-view.md` |
| outputs | `perspectives/agile-planning/gitlab-planning-view.md` |
| done_criteria | Projection covers all epics, features, and stories; engineering notes and enablement needs present |
| stop_conditions | Delivery structure not yet confirmed; readiness not complete |
| downstream | None — this is a read-only projection |

---

### 5.5 QA Analyst skills

#### `qa.create_bdd_scenarios`

| Field | Value |
|---|---|
| skill_id | `qa.create_bdd_scenarios` |
| persona | qa-analyst |
| phase | 4 — quality gates |
| description | Create `quality-gates/bdd-scenarios.md` — Gherkin scenarios with SCN-NNN IDs |
| when_to_use | BDD gate triggered by readiness check |
| trigger_conditions | BDD gate triggered; `quality-gates/bdd-scenarios.md` missing or stub |
| required_inputs | `planning/delivery-structure.md`, `business-intake/business-intake-summary.md`, `engineering-readiness/readiness-check.md` |
| optional_inputs | `business-intake/business-test-expectations.md`, `architecture/architecture-review.md` |
| prompt | `4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| outputs | `quality-gates/bdd-scenarios.md` |
| done_criteria | Every user story covered; scenarios have SCN-NNN IDs; Status: Accepted |
| stop_conditions | Acceptance criteria not defined; story scope ambiguous |
| downstream | `qa.create_test_strategy`, `engineering_lead.create_openspec_handoff` |

#### `qa.create_test_strategy`

| Field | Value |
|---|---|
| skill_id | `qa.create_test_strategy` |
| persona | qa-analyst |
| phase | 4 — quality gates |
| description | Create `quality-gates/test-strategy.md` — test approach, coverage, and risk |
| when_to_use | Always — every initiative requires a test strategy before handoff |
| trigger_conditions | `quality-gates/test-strategy.md` missing or not Accepted — always required, not conditional on readiness check |
| required_inputs | `planning/delivery-structure.md`, `engineering-readiness/readiness-check.md` |
| optional_inputs | `quality-gates/bdd-scenarios.md`, `architecture/architecture-rules.md` |
| prompt | `4-engineering-readiness/quality-gates/create-test-strategy.md` |
| outputs | `quality-gates/test-strategy.md` |
| done_criteria | Test approach defined; coverage levels stated; risk areas identified; Status: Accepted |
| stop_conditions | Architecture constraints not yet known |
| downstream | `engineering_lead.create_openspec_handoff` |

#### `qa.generate_test_stubs_from_bdd`

| Field | Value |
|---|---|
| skill_id | `qa.generate_test_stubs_from_bdd` |
| persona | qa-analyst |
| phase | 8 — implementation |
| description | Generate runnable failing test stubs from BDD scenarios |
| when_to_use | BDD scenarios accepted; engineer needs test stubs to implement against |
| trigger_conditions | `quality-gates/bdd-scenarios.md` has Status: Accepted; engineer requests test stubs |
| required_inputs | `quality-gates/bdd-scenarios.md`, `engineering-readiness/initiative-context.md` |
| optional_inputs | `quality-gates/test-strategy.md` |
| prompt | `8-copilot-implementation/03-generate-test-stubs-from-bdd.md` |
| outputs | test stubs in target repo (pytest-bdd, Cucumber, or SpecFlow format) |
| done_criteria | One failing test stub per BDD scenario; stubs are runnable |
| stop_conditions | BDD scenarios not yet accepted |
| downstream | `engineering_lead.implement_one_task` |

#### `qa.review_qa`

| Field | Value |
|---|---|
| skill_id | `qa.review_qa` |
| persona | qa-analyst |
| phase | 9 — review |
| description | QA review — test coverage, edge cases, regression risk |
| when_to_use | Implementation complete; QA review required |
| trigger_conditions | Implementation complete; QA coverage review needed |
| required_inputs | Implementation artifacts, `quality-gates/bdd-scenarios.md` (if triggered) |
| optional_inputs | `quality-gates/test-strategy.md`, `planning/delivery-structure.md` |
| prompt | `9-reviewers/02-qa-review.md` |
| outputs | QA review findings |
| done_criteria | Coverage assessed; regression risks identified; finding IDs assigned |
| stop_conditions | Implementation not yet provided |
| downstream | `engineering_lead.fix_review_comments` (if findings require fixes) |

---

### 5.6 Security Reviewer skills

#### `security.create_security_review`

| Field | Value |
|---|---|
| skill_id | `security.create_security_review` |
| persona | security-reviewer |
| phase | 4 — quality gates |
| description | Create `quality-gates/security-review.md` — OWASP, auth, PII, data exposure |
| when_to_use | Security gate triggered by readiness check |
| trigger_conditions | PII/auth/authorization/secrets/exposure risk detected; security gate triggered |
| required_inputs | `business-intake/business-intake-summary.md`, `architecture/architecture-review.md`, `engineering-readiness/readiness-check.md` |
| optional_inputs | `architecture/architecture-rules.md`, `engineering-readiness/initiative-context.md` |
| prompt | `4-engineering-readiness/quality-gates/create-security-review.md` |
| outputs | `quality-gates/security-review.md` |
| done_criteria | OWASP risks assessed; auth/authorization model explicit; PII handling documented; Status: Accepted |
| stop_conditions | Security requirements not defined; PO or security officer input required |
| downstream | `security.create_threat_model` (if high-risk boundary), `engineering_lead.create_openspec_handoff` |

#### `security.create_threat_model`

| Field | Value |
|---|---|
| skill_id | `security.create_threat_model` |
| persona | security-reviewer |
| phase | 4 — quality gates |
| description | Create `quality-gates/threat-model.md` — STRIDE threat model for high-risk boundaries |
| when_to_use | High-risk security boundary identified; threat model gate triggered |
| trigger_conditions | High-risk security boundary detected; `quality-gates/threat-model.md` missing |
| required_inputs | `quality-gates/security-review.md`, `architecture/architecture-review.md` |
| optional_inputs | `engineering-readiness/initiative-context.md` |
| prompt | `4-engineering-readiness/quality-gates/create-threat-model.md` |
| outputs | `quality-gates/threat-model.md` |
| done_criteria | STRIDE threats assessed; mitigations recorded; residual risk documented; Status: Accepted |
| stop_conditions | Security boundary not yet defined |
| downstream | `engineering_lead.create_openspec_handoff` |

#### `security.create_data_contract`

| Field | Value |
|---|---|
| skill_id | `security.create_data_contract` |
| persona | security-reviewer |
| phase | 4 — quality gates |
| description | Create `quality-gates/data-contract.md` — data ownership, schema, retention, PII, residency |
| when_to_use | Data ownership, schema change, PII, or residency risk detected; data contract gate triggered |
| trigger_conditions | Data ownership/schema/retention/PII/residency change detected; `quality-gates/data-contract.md` missing |
| required_inputs | `business-intake/business-intake-summary.md`, `architecture/architecture-review.md` |
| optional_inputs | `quality-gates/security-review.md` |
| prompt | `4-engineering-readiness/quality-gates/create-data-contract.md` |
| outputs | `quality-gates/data-contract.md` |
| done_criteria | Data ownership explicit; PII fields identified; retention policy documented; Status: Accepted |
| stop_conditions | Data ownership unclear — PO and data owner must agree |
| downstream | `engineering_lead.create_openspec_handoff` |

#### `security.review_security`

| Field | Value |
|---|---|
| skill_id | `security.review_security` |
| persona | security-reviewer |
| phase | 9 — review |
| description | Security review of implementation — OWASP, secrets, auth, data exposure |
| when_to_use | Implementation touches security/PII; security review required post-implementation |
| trigger_conditions | Implementation touches security or PII boundary |
| required_inputs | Implementation artifacts, `quality-gates/security-review.md` (if triggered) |
| optional_inputs | `quality-gates/threat-model.md`, `architecture/architecture-rules.md` |
| prompt | `9-reviewers/04-security-review.md` |
| outputs | security review findings |
| done_criteria | OWASP risks assessed; auth and PII handling verified; finding IDs assigned |
| stop_conditions | Implementation not yet provided |
| downstream | `engineering_lead.fix_review_comments` (if findings require fixes) |

---

### 5.7 Engineering Lead skills

#### `engineering_lead.check_engineering_readiness`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.check_engineering_readiness` |
| persona | engineering-lead |
| phase | 4 — engineering readiness |
| description | Create `engineering-readiness/readiness-check.md` — Ready / Not ready decision and triggered gates |
| when_to_use | Architecture review and rules complete; delivery structure confirmed |
| trigger_conditions | `engineering-readiness/readiness-check.md` missing; architecture review and rules exist |
| required_inputs | `architecture/architecture-review.md`, `architecture/architecture-rules.md`, `planning/open-decisions.md`, `planning/delivery-structure.md` |
| optional_inputs | `architecture/existing-system-impact.md` |
| prompt | `4-engineering-readiness/01-check-engineering-readiness.md` |
| outputs | `engineering-readiness/readiness-check.md` |
| done_criteria | Explicit Ready / Not ready decision; every triggered gate listed with rationale; no placeholder owners |
| stop_conditions | Open blocking decisions unresolved; architecture review missing |
| downstream | `engineering_lead.generate_initiative_context`, triggered quality gate skills |

#### `engineering_lead.generate_initiative_context`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.generate_initiative_context` |
| persona | engineering-lead |
| phase | 4 — engineering readiness |
| description | Create `engineering-readiness/initiative-context.md` — technology constraints, binding rules, governed boundaries |
| when_to_use | Readiness check complete and decision = Ready; initiative context missing |
| trigger_conditions | `engineering-readiness/initiative-context.md` missing or has empty rows; readiness = Ready |
| required_inputs | `engineering-readiness/readiness-check.md`, `architecture/architecture-rules.md`, `architecture/architecture-review.md` |
| optional_inputs | `input/architecture.md`, `planning/delivery-structure.md` |
| prompt | `4-engineering-readiness/02-generate-initiative-context.md` |
| outputs | `engineering-readiness/initiative-context.md` |
| done_criteria | Technology constraints, binding rules, and governed boundaries all populated with real content — no empty rows |
| stop_conditions | Readiness = Not ready |
| downstream | triggered quality gate skills, `engineering_lead.create_openspec_handoff` |

#### `engineering_lead.create_openspec_handoff`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.create_openspec_handoff` |
| persona | engineering-lead |
| phase | 5 — handoff |
| description | Create full OpenSpec handoff — dependency graph + one folder per user story |
| when_to_use | Readiness complete; all triggered gates accepted; execution mode = OpenSpec |
| trigger_conditions | Readiness complete + OpenSpec mode; all gates with Status: Accepted |
| required_inputs | `engineering-readiness/readiness-check.md`, `engineering-readiness/initiative-context.md`, `planning/delivery-structure.md`, all triggered gate artifacts |
| optional_inputs | `input/repositories/` (for multi-repo handoff), `planning/traceability-matrix.md` |
| prompt | `5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| outputs | `openspec/changes/dependency-graph.md` + one story folder per user story |
| done_criteria | dependency-graph.md wave-ordered; every story folder has proposal, design, and tasks; all tasks traceable to stories |
| stop_conditions | Any triggered gate not yet Accepted; blocking open decisions exist |
| downstream | `engineering_lead.implement_one_task` |

#### `engineering_lead.create_standalone_handoff`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.create_standalone_handoff` |
| persona | engineering-lead |
| phase | 5 — handoff |
| description | Create standalone delivery package when OpenSpec is not used |
| when_to_use | Readiness complete; all triggered gates accepted; execution mode = Standalone |
| trigger_conditions | Readiness complete + Standalone mode; all gates with Status: Accepted |
| required_inputs | `engineering-readiness/readiness-check.md`, `engineering-readiness/initiative-context.md`, `planning/delivery-structure.md` |
| optional_inputs | `planning/traceability-matrix.md`, all triggered gate artifacts |
| prompt | `5-handoff/02-create-standalone-delivery-package.md` |
| outputs | `standalone-delivery/<deliverable-name>/` |
| done_criteria | Delivery spec, tasks, and validation plan present; all tasks traceable to stories |
| stop_conditions | Any triggered gate not yet Accepted; blocking open decisions exist |
| downstream | `engineering_lead.implement_one_task` |

#### `engineering_lead.create_compact_handoff`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.create_compact_handoff` |
| persona | engineering-lead |
| phase | 5 — handoff |
| description | Create a compact handoff for Fast Path or small changes |
| when_to_use | Fast Path routing confirmed; small change with narrow, well-understood scope |
| trigger_conditions | Small change + Fast Path routing; compact handoff needed |
| required_inputs | `routing/routing-decision.md` (Fast Path confirmed), `input/brs.md` |
| optional_inputs | `engineering-readiness/readiness-check.md`, `business-intake/business-intake-summary.md` |
| prompt | `5-handoff/03-create-compact-handoff-package.md` |
| outputs | compact handoff artifact |
| done_criteria | Scope, tasks, and constraints in a single artifact; traceable to BRS |
| stop_conditions | Routing score not Fast Path; scope too large for compact format |
| downstream | `engineering_lead.implement_one_task` |

#### `engineering_lead.implement_one_task`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.implement_one_task` |
| persona | engineering-lead |
| phase | 8 — implementation |
| description | Implement one approved task — reads initiative context, implements, produces summary |
| when_to_use | Approved task exists in handoff package; engineer ready to implement |
| trigger_conditions | Approved implementation task selected from handoff package |
| required_inputs | `engineering-readiness/initiative-context.md`, one approved task from `openspec/changes/.../tasks.md` or `standalone-delivery/.../tasks.md` |
| optional_inputs | `quality-gates/bdd-scenarios.md`, architecture and security gate artifacts |
| prompt | `8-copilot-implementation/01-implement-one-task.md` |
| outputs | code changes + implementation summary |
| done_criteria | Task implemented; implementation summary produced; BDD scenarios referenced |
| stop_conditions | No approved task available; initiative context missing |
| downstream | `reviewer.senior_code_review` |

#### `engineering_lead.fix_review_comments`

| Field | Value |
|---|---|
| skill_id | `engineering_lead.fix_review_comments` |
| persona | engineering-lead |
| phase | 8 — implementation |
| description | Fix review comments on an implemented task |
| when_to_use | Review findings returned; engineer must fix before merge |
| trigger_conditions | Review findings returned from `reviewer.senior_code_review` or other reviewer skills |
| required_inputs | Review findings, implementation artifacts, `engineering-readiness/initiative-context.md` |
| optional_inputs | `quality-gates/bdd-scenarios.md` |
| prompt | `8-copilot-implementation/02-fix-review-comments.md` |
| outputs | code changes + fix summary |
| done_criteria | All required-fix findings addressed; fix summary produced |
| stop_conditions | Review findings ambiguous — reviewer must clarify |
| downstream | `reviewer.senior_code_review` (re-review) |

---

### 5.8 Reviewer skills

#### `reviewer.senior_code_review`

| Field | Value |
|---|---|
| skill_id | `reviewer.senior_code_review` |
| persona | reviewer |
| phase | 9 — review |
| description | Senior code review — correctness, security, patterns, BDD coverage |
| when_to_use | Implementation complete; senior review required |
| trigger_conditions | Implementation complete |
| required_inputs | Implementation artifacts, `engineering-readiness/initiative-context.md` |
| optional_inputs | `quality-gates/bdd-scenarios.md`, `architecture/architecture-rules.md` |
| prompt | `9-reviewers/01-senior-code-review.md` |
| outputs | review findings with Finding IDs |
| done_criteria | All findings have IDs; required-fix vs optional-improvement distinguished |
| stop_conditions | Implementation not yet provided |
| downstream | `engineering_lead.fix_review_comments` (if required-fix findings), merge |

#### `reviewer.architecture_review`

| Field | Value |
|---|---|
| skill_id | `reviewer.architecture_review` |
| persona | reviewer |
| phase | 9 — review |
| description | Architecture review of implementation against governed boundaries and rules |
| when_to_use | Implementation touches architecture boundary; architecture review required |
| trigger_conditions | Implementation touches architecture boundary |
| required_inputs | Implementation artifacts, `architecture/architecture-rules.md`, `architecture/architecture-review.md` |
| optional_inputs | `engineering-readiness/initiative-context.md` |
| prompt | `9-reviewers/03-architecture-review.md` |
| outputs | architecture review findings |
| done_criteria | Architecture rule compliance assessed; governed boundaries respected; finding IDs assigned |
| stop_conditions | Implementation not yet provided |
| downstream | `engineering_lead.fix_review_comments` (if required-fix findings) |

#### `reviewer.spec_correction`

| Field | Value |
|---|---|
| skill_id | `reviewer.spec_correction` |
| persona | reviewer |
| phase | 9 — review |
| description | Correct a spec artifact when implementation reveals it was wrong |
| when_to_use | Implementation reveals spec defect; spec must be corrected before implementation continues |
| trigger_conditions | Implementation reveals spec is wrong or ambiguous |
| required_inputs | Affected spec artifact (delivery-structure, BDD scenario, or gate artifact), review finding referencing the defect |
| optional_inputs | `input/brs.md`, `business-intake/business-intake-summary.md` |
| prompt | `9-reviewers/05-spec-correction.md` |
| outputs | corrected spec artifact |
| done_criteria | Spec defect corrected; change noted with rationale; traceability preserved |
| stop_conditions | Spec defect requires PO or architect decision to resolve |
| downstream | `engineering_lead.implement_one_task` (re-implement with corrected spec) |

---

## 6. Stage-to-skill lookup table

| # | Stage | Artifact | Done criteria | Skill to invoke |
|---|---|---|---|---|
| 1 | Routing | `routing/routing-decision.md` | Delivery mode, execution mode, and rationale stated | (routing prompt — no dedicated skill) |
| 2 | Business intake | `business-intake/business-intake-summary.md` | Objectives have success measures; every gap has an owner | `product_owner.create_business_intake` |
| 3 | Architecture draft (if missing) | `input/architecture.md` | Not a stub; DRAFT notice acceptable | `architect.draft_architecture_from_brs` |
| 4 | Draft delivery shape | `planning/delivery-structure.md` (epics + features only) | Epics with IDs and features visible | `delivery_lead.create_delivery_structure` |
| 5 | Architecture review | `architecture/architecture-review.md` | Initiative-specific constraints; every open decision has owner | `architect.review_initial_architecture` |
| 6 | Architecture rules | `architecture/architecture-rules.md` | Every rule has ID and enforcement; no AR-OPEN-* if decision Resolved | `architect.create_architecture_rules` |
| 7 | Open decisions | `planning/open-decisions.md` | All decisions captured with owners; blocking summary accurate | `orchestrator.maintain_open_decisions` |
| 8 | Engineering readiness | `engineering-readiness/readiness-check.md` | Explicit Ready / Not ready; every triggered gate listed | `engineering_lead.check_engineering_readiness` |
| 9 | Delivery structure confirmed | `planning/delivery-structure.md` (full stories) | Every feature has ≥1 well-formed story with AC ref | `delivery_lead.create_delivery_structure` |
| 10 | Open decisions update | `planning/open-decisions.md` | Readiness blockers recorded with owners | `orchestrator.maintain_open_decisions` |
| 11 | Initiative context | `engineering-readiness/initiative-context.md` | Technology constraints, binding rules, boundaries — no empty rows | `engineering_lead.generate_initiative_context` |
| 12 | Quality gates | `quality-gates/<gate>.md` (triggered only) | Each gate: real content, ticked checklist, Status: Accepted | see trigger-to-skill table (Section 8) |
| 13 | Handoff | `openspec/changes/` or `standalone-delivery/` | Dependency graph + all story folders; tasks traceable to stories | `engineering_lead.create_openspec_handoff` or `engineering_lead.create_standalone_handoff` |

---

## 7. Artifact-to-skill lookup table

| Artifact | Owning skill | Persona |
|---|---|---|
| `input/brs.md` | `product_owner.create_brs` or `product_owner.convert_brs_to_markdown` | product-owner |
| `input/architecture.md` | `architect.convert_architecture_to_markdown` or `architect.draft_architecture_from_brs` | architect |
| `routing/routing-decision.md` | (routing prompt) | orchestrator |
| `business-intake/business-intake-summary.md` | `product_owner.create_business_intake` | product-owner |
| `business-intake/gaps-and-questions.md` | `product_owner.find_gaps_and_questions` | product-owner |
| `business-intake/business-test-expectations.md` | `product_owner.create_business_test_expectations` | product-owner |
| `architecture/architecture-review.md` | `architect.review_initial_architecture` | architect |
| `architecture/architecture-rules.md` | `architect.create_architecture_rules` | architect |
| `architecture/existing-system-impact.md` | `architect.review_existing_system_impact` | architect |
| `planning/open-decisions.md` | `orchestrator.maintain_open_decisions` | orchestrator |
| `planning/delivery-structure.md` | `delivery_lead.create_delivery_structure` | delivery-lead |
| `planning/software-modules.md` | `delivery_lead.identify_software_modules` | delivery-lead |
| `planning/capability-to-module-map.md` | `delivery_lead.map_capabilities_to_modules` | delivery-lead |
| `planning/delivery-increments.md` | `delivery_lead.define_delivery_increments` | delivery-lead |
| `planning/traceability-matrix.md` | `delivery_lead.create_traceability_matrix` | delivery-lead |
| `planning/workflow-state.json` | `orchestrator.maintain_state` | orchestrator |
| `engineering-readiness/readiness-check.md` | `engineering_lead.check_engineering_readiness` | engineering-lead |
| `engineering-readiness/initiative-context.md` | `engineering_lead.generate_initiative_context` | engineering-lead |
| `quality-gates/bdd-scenarios.md` | `qa.create_bdd_scenarios` | qa-analyst |
| `quality-gates/test-strategy.md` | `qa.create_test_strategy` | qa-analyst |
| `quality-gates/security-review.md` | `security.create_security_review` | security-reviewer |
| `quality-gates/threat-model.md` | `security.create_threat_model` | security-reviewer |
| `quality-gates/data-contract.md` | `security.create_data_contract` | security-reviewer |
| `openspec/changes/` | `engineering_lead.create_openspec_handoff` | engineering-lead |
| `standalone-delivery/` | `engineering_lead.create_standalone_handoff` | engineering-lead |
| `perspectives/agile-planning/gitlab-planning-view.md` | `delivery_lead.create_agile_planning_view` | delivery-lead |

---

## 8. Trigger-to-skill lookup

Use this table to map natural-language triggers, artifact states, and risk signals to the correct skill to invoke.

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

## 9. Rules for loading prompts

1. **Load module.md first.** Then select the specific skill needed. Do not load every prompt.
2. **One skill per invocation.** Load only the prompt for the selected skill. Do not load upstream or downstream prompts unless explicitly required by the skill's `required_inputs`.
3. **Read required inputs before generating output.** Never generate a downstream artifact without having read every artifact listed in `required_inputs`.
4. **Respect gate order.** Do not invoke a downstream skill if its upstream gate artifact is missing, stub-only, or stale.
5. **Verify artifact quality.** An artifact is only complete when it passes its `done_criteria` — not when the file exists.
6. **Never skip a stage.** Even if the user asks to skip, note the risk and propose scaffolding instead.
7. **Persona boundary.** Only invoke skills belonging to the current persona. If a different persona's work is needed, hand off explicitly.

---

## 10. Rules for stopping and asking for human input

Stop and request human input when:

1. **BRS missing and no source material provided.** Scaffold `input/input-package.md` with questions; stop.
2. **Routing requires judgment only the user can make.** Ask the single specific question; stop.
3. **Business scope is ambiguous and unresolvable from existing artifacts.** Scaffold scope-clarification stub; stop.
4. **Blocking open decisions exist** (`planning/open-decisions.md` has `blocking_count > 0`). Report the blocking decisions; stop.
5. **Readiness = Not ready.** Scaffold collection artifacts for every blocker; stop.
6. **Quality gate requires human-produced input** (legal, vendor, compliance, PO decision). Scaffold gate artifact as questionnaire stub; stop.
7. **Multiple active initiative workspaces and it is unclear which is active.** Ask which workspace is active; stop.

**Never stop without first scaffolding.** For every blocking item requiring human input, create a stub artifact immediately with questions to answer. Then stop and state: what was scaffolded, what the human must provide, what the next stage will be once blockers are resolved.

Do not present a menu of options. Do not ask "shall I proceed?". State one specific action.

---

## Framework entry points (quick reference)

| Prompt | What it does |
|---|---|
| `00-start.md` | Interview the user (5 questions) to determine entry mode, delivery mode, and first prompt to run |
| `brs-to-spec-run-workflow.md` | Full workflow orchestrator — detects current stage, executes it, re-assesses automatically |
| `agent-instructions.md` | Behavioral rules for non-Copilot agents (Claude Code, Cursor, Codex) |

---

## Note on machine-readable registry

`module.md` is the human-readable source of truth for the persona and skill registry.
`module-registry.yaml` is the machine-readable selection aid. If they conflict, `module.md` wins until the registry is corrected.
