# Prompt 1 — Strategic Refactoring

You are working on my `brs-to-spec` / `.b2s` framework.

Current problem:

The framework already contains many useful enterprise artifacts such as business intake, requirements, business rules, architecture review, readiness checks, traceability, BDD, test strategy, OpenSpec handoff, and review package.

However, the core delivery output is not strong enough.

The framework gives the feeling that it creates many governance artifacts, but the most important output for AI-assisted implementation is not yet central enough:

- clear Epics
- clear Features
- high-quality User Stories
- strong Acceptance Criteria
- BDD scenarios
- implementation tasks
- coding-agent prompts
- traceability from BRS/business rules/architecture to each story

The objective is to refactor the framework so that the main output becomes AI-ready delivery packages.

Do not remove the existing enterprise governance artifacts unless they are clearly duplicated or unused. Instead, make those artifacts feed into stronger story packages.

Target positioning:

`brs-to-spec` transforms raw enterprise BRS documents into AI-ready story packages with business traceability, architecture context, acceptance criteria, BDD scenarios, implementation tasks, and coding prompts.

Expected outcome:

1. Analyze the current `.b2s` structure.
2. Identify where Epics, Features, Stories, Acceptance Criteria, BDD, Tasks, and Coding Prompts are currently generated.
3. Identify gaps where the current output is too shallow, too table-based, or not suitable for AI coding agents.
4. Propose concrete changes to templates, skills, workflow actions, and validators.
5. Implement the changes.
6. Add or update tests/fixtures to prove the new story package output is generated correctly.

Important principle:

The story package must become the atomic unit of implementation.

Each story package should include:

- story title and ID
- user story
- business goal
- source traceability
- linked requirements
- linked business rules
- linked architecture constraints
- acceptance criteria
- BDD scenarios
- impacted components
- data/API/UI impact where applicable
- dependencies
- non-goals
- implementation tasks
- test expectations
- definition of done
- coding-agent prompt

Do not produce generic stories. Every story must be specific, traceable, testable, and implementation-ready.
