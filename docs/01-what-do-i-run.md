# What Do I Run?

> **If unsure, run the workflow.** Load `.brs2spec/brs-to-spec-run-workflow.md` in your AI assistant, say "run the workflow", and it handles everything else. Return to this page only when you want to invoke a specific persona skill directly.

---

## Lookup table

| Need | Persona | Skill | Prompt to load | Output artifact |
|---|---|---|---|---|
| Continue workflow / what's next? | Orchestrator | `orchestrator.run_workflow` | `.brs2spec/brs-to-spec-run-workflow.md` | `planning/workflow-state.json` (updated) + next stage artifact |
| Create or convert a BRS from notes | Product Owner | `product_owner.create_brs` | `.brs2spec/skills/0-intake/00-create-brs.md` | `input/brs.md` |
| Convert a Word/PDF BRS to markdown | Product Owner | `product_owner.convert_brs_to_markdown` | `.brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md` | `input/brs.md` |
| Create business intake summary | Product Owner | `product_owner.create_business_intake` | `.brs2spec/skills/2-business-intake/01-create-business-intake-summary.md` | `business-intake/business-intake-summary.md` |
| Find gaps and open questions in BRS | Product Owner | `product_owner.find_gaps_and_questions` | `.brs2spec/skills/2-business-intake/advanced/03-find-gaps-and-questions.md` | `business-intake/gaps-and-questions.md` |
| Draft architecture when none exists | Architect | `architect.draft_architecture_from_brs` | `.brs2spec/skills/0-input-preparation/04-draft-architecture-from-brs.md` | `input/architecture.md` (DRAFT) |
| Review initiative architecture | Architect | `architect.review_initial_architecture` | `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md` | `architecture/architecture-review.md` |
| Create architecture binding rules | Architect | `architect.create_architecture_rules` | `.brs2spec/skills/3-planning-and-modular-delivery/02-create-global-architecture-rules.md` | `architecture/architecture-rules.md` |
| Assess brownfield/existing system impact | Architect | `architect.review_existing_system_impact` | Use template at `.brs2spec/templates/planning-and-modular-delivery/existing-system-impact.md` | `architecture/existing-system-impact.md` |
| Create delivery structure (epics, features, stories) | Delivery Lead | `delivery_lead.create_delivery_structure` | `.brs2spec/skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` | `planning/delivery-structure.md` |
| Create traceability matrix | Delivery Lead | `delivery_lead.create_traceability_matrix` | `.brs2spec/skills/3-planning-and-modular-delivery/07-create-traceability-matrix.md` | `planning/traceability-matrix.md` |
| Create agile planning view | Delivery Lead | `delivery_lead.create_agile_planning_view` | `.brs2spec/skills/7-perspectives/agile-planning/01-create-gitlab-planning-view.md` | `perspectives/agile-planning/gitlab-planning-view.md` |
| Check engineering readiness | Engineering Lead | `engineering_lead.check_engineering_readiness` | `.brs2spec/skills/4-engineering-readiness/01-check-engineering-readiness.md` | `engineering-readiness/readiness-check.md` |
| Generate initiative context for engineers | Engineering Lead | `engineering_lead.generate_initiative_context` | `.brs2spec/skills/4-engineering-readiness/02-generate-initiative-context.md` | `engineering-readiness/initiative-context.md` |
| Create OpenSpec handoff | Engineering Lead | `engineering_lead.create_openspec_handoff` | `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` | `openspec/changes/` |
| Create standalone handoff (no OpenSpec) | Engineering Lead | `engineering_lead.create_standalone_handoff` | `.brs2spec/skills/5-handoff/02-create-standalone-delivery-package.md` | `standalone-delivery/` |
| Create compact handoff (Fast Path) | Engineering Lead | `engineering_lead.create_compact_handoff` | `.brs2spec/skills/5-handoff/03-create-compact-handoff-package.md` | compact handoff artifact |
| Create BDD scenarios | QA Analyst | `qa.create_bdd_scenarios` | `.brs2spec/skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` | `quality-gates/bdd-scenarios.md` |
| Create test strategy | QA Analyst | `qa.create_test_strategy` | `.brs2spec/skills/4-engineering-readiness/quality-gates/create-test-strategy.md` | `quality-gates/test-strategy.md` |
| Create security review | Security Reviewer | `security.create_security_review` | `.brs2spec/skills/4-engineering-readiness/quality-gates/create-security-review.md` | `quality-gates/security-review.md` |
| Create data contract | Security Reviewer | `security.create_data_contract` | `.brs2spec/skills/4-engineering-readiness/quality-gates/create-data-contract.md` | `quality-gates/data-contract.md` |
| Implement one approved task | Engineering Lead | `engineering_lead.implement_one_task` | `.brs2spec/skills/8-copilot-implementation/01-implement-one-task.md` | code changes + summary |
| Fix review comments | Engineering Lead | `engineering_lead.fix_review_comments` | `.brs2spec/skills/8-copilot-implementation/02-fix-review-comments.md` | code changes + fix summary |
| Senior code review of implementation | Reviewer | `reviewer.senior_code_review` | `.brs2spec/skills/9-reviewers/01-senior-code-review.md` | review findings |
| Architecture review of implementation | Reviewer | `reviewer.architecture_review` | `.brs2spec/skills/9-reviewers/03-architecture-review.md` | architecture review findings |
| QA review of implementation | QA Analyst | `qa.review_qa` | `.brs2spec/skills/9-reviewers/02-qa-review.md` | QA review findings |

---

## Persona quick addresses

You can address a persona directly to bypass the orchestrator and invoke only that persona's skill:

| Say | Persona invoked |
|---|---|
| `@orchestrator` | Orchestrator — run or continue the workflow |
| `@product-owner` | Product Owner — business intake, BRS, gaps |
| `@architect` | Architect — architecture review, rules, brownfield |
| `@delivery-lead` | Delivery Lead — delivery structure, traceability, planning view |
| `@qa` | QA Analyst — BDD scenarios, test strategy |
| `@security` | Security Reviewer — security review, data contract, threat model |
| `@engineering-lead` | Engineering Lead — readiness, initiative context, handoff, implementation |
| `@reviewer` | Reviewer — senior code review, architecture review |

---

## Workflow state is always the authority

The workflow state file tracks where you are:

```text
<initiative-workspace>/planning/workflow-state.json
```

The orchestrator reads and updates it after every stage. You can read it at any time to see the current stage, triggered quality gates, blocking decisions, and what comes next.

---

> **If unsure, run the workflow.** Load `.brs2spec/brs-to-spec-run-workflow.md` in your AI assistant and say "continue" or "what's next?" The orchestrator will detect the current state and execute the correct next skill automatically.
