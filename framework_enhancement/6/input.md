# BRS-to-Spec Framework Analysis and Improvement Plan

## 1. Executive Summary

The current **BRS-to-Spec** workflow is already a strong foundation for converting a Business Requirements Specification into structured delivery artifacts. It is particularly suitable for **large initiatives**, where governance, traceability, architecture alignment, quality gates, and stakeholder review are important.

However, the target has evolved beyond simple specification generation. The intended output is not only a specification, but a package that can be used by autonomous or semi-autonomous AI coding tools such as **GitHub Copilot, Claude Code, Codex, Cursor, Devin, or similar agents**.

The correct target should therefore be:

```text
BRS → governed specification → repository-aware delivery split → AI implementation package
```

The framework does **not** need full source-code access during specification generation. Instead, it should consume repository metadata from a `repositories/` folder. That metadata should describe technologies, services, deployment units, repository ownership, module boundaries, validation commands, and constraints. This allows the framework to split stories and tasks by repository before the package is handed off to an AI coding agent running inside the real repository.

The main recommendation is to evolve the framework from:

```text
BRS-to-Spec
```

into:

```text
BRS-to-AI-Implementation-Package
```

or, more generally:

```text
BRS-to-Agentic-Delivery
```

The current flow works, but it should be improved by adding:

1. Repository intelligence as a formal input phase.
2. Capability-to-repository mapping.
3. Repository-level task splitting.
4. Candidate implementation guidance instead of pretending to know exact files.
5. By-story and by-repository output packages.
6. Repository execution guard for AI agents running later in the actual codebase.
7. Implementation feedback loop.

---

## 2. Current Workflow Assessment

The current workflow contains the following important stages:

- BRS normalisation.
- Architecture draft if missing.
- Input package normalisation.
- Routing decision.
- Business intake summary.
- Business rules.
- Actors and personas.
- Draft process flows.
- Draft use cases.
- Draft delivery structure.
- Architecture review.
- Architecture rules.
- Open decisions.
- Engineering readiness.
- Confirmed delivery structure.
- Confirmed process flows.
- Confirmed use cases.
- Story enrichment check.
- Initiative context.
- Quality gates.
- Entity model.
- AI-oriented handoff with `coding-prompt.md`.
- Review package.

This is a strong workflow for large initiatives because it separates business understanding, architectural reasoning, delivery planning, quality validation, and engineering handoff.

The latest improvements are particularly valuable:

- Draft process flows are created before confirmed stories.
- Draft use cases are created after process flows.
- Architecture review uses business intake, draft delivery shape, and draft process flows.
- Confirmed process flows and use cases enrich existing drafts instead of recreating them.
- Story enrichment verifies actor, business rule, acceptance criteria, and process-flow linkage.
- Handoff includes `coding-prompt.md` with business rules, architecture rules, acceptance criteria, scenarios, validation commands, and definition of done.

These changes make the process much more reliable than a simple BRS-to-user-stories generator.

### Current rating

| Dimension | Rating | Comment |
|---|---:|---|
| BRS-to-specification | 8.5 / 10 | Strong and governed |
| BRS-to-engineering handoff | 8 / 10 | Good, especially with `coding-prompt.md` |
| BRS-to-autonomous AI coding | 7 / 10 | Good direction, but needs repository-aware packaging |
| Large-initiative governance | 8.5 / 10 | Good gates and artifact discipline |
| Repository-level execution readiness | 6.5 / 10 | Needs formal repository intelligence and repo-level output packages |

---

## 3. Key Clarification: The Framework Does Not Need the Full Codebase

The framework does not need to read the actual source code. That is acceptable and even desirable if the framework is intended to run before implementation.

The model should be:

```text
BRS-to-Spec framework
    ↓
Consumes BRS, architecture input, and repository metadata
    ↓
Produces AI implementation package
    ↓
Package is copied into target repository or repositories
    ↓
Copilot / Claude / Codex / other agent runs there with real codebase access
```

This means the framework should not claim to know exact implementation details unless they are provided in repository metadata. Instead, it should produce **candidate implementation guidance**.

For example:

- Candidate repositories.
- Candidate services.
- Candidate modules.
- Candidate files or folders to inspect.
- Candidate validation commands.
- Candidate task split.

The final confirmation must happen inside the target repository when the coding agent has real access to the source code.

---

## 4. Role of the `repositories/` Folder

The `repositories/` folder should become a first-class input to the framework.

Its purpose is not to contain source code. Its purpose is to provide **repository intelligence**.

The framework should use it to understand:

- Which repositories exist.
- Which technologies they use.
- Which type of service each repository contains.
- Which business or technical capabilities each repository owns.
- Which deployment unit each repository represents.
- Which APIs, jobs, events, database schemas, or integrations each repository exposes or consumes.
- Which validation commands should be used later.
- Which coding standards and architectural constraints apply to each repository.

This allows the framework to split features, stories, and tasks across repositories before the AI coding agent runs inside the actual codebase.

---

## 5. Recommended `repositories/` Structure

The following structure is recommended:

```text
repositories/
  repository-inventory.md
  technology-service-classification.md
  repository-constraints.md
  repo-001/
    repository-profile.md
    technology-stack.md
    service-catalog.md
    module-map.md
    api-surface.md
    data-surface.md
    integration-surface.md
    build-test-commands.md
    coding-standards.md
    deployment-profile.md
  repo-002/
    repository-profile.md
    technology-stack.md
    service-catalog.md
    module-map.md
    api-surface.md
    data-surface.md
    integration-surface.md
    build-test-commands.md
    coding-standards.md
    deployment-profile.md
```

The structure can be simplified at first, but the following artifacts should become the minimum expected set.

---

## 6. Minimum Repository Metadata Artifacts

### 6.1 `repositories/repository-inventory.md`

Purpose: provide the list of repositories that may be involved in the initiative.

Suggested table:

```markdown
| Repo ID | Repository | Type | Main technology | Owns capability | Deployment unit |
|---|---|---|---|---|---|
| REPO-001 | client-advisor-api | Backend API | .NET 8 | Client onboarding | Azure App Service |
| REPO-002 | client-advisor-ui | Frontend SPA | React / TypeScript | Advisor UI | Static Web App |
| REPO-003 | onboarding-worker | Worker | .NET Worker | Async onboarding processing | Container App |
| REPO-004 | database | Database | SQL Server | Schema and migrations | DACPAC / migration scripts |
```

This is the high-level map used by the framework to decide where work may belong.

---

### 6.2 `repositories/repo-XXX/repository-profile.md`

Purpose: describe the responsibility and boundaries of a specific repository.

Example:

```markdown
# Repository Profile — REPO-001

## Basic Information

- Repo ID: REPO-001
- Name: client-advisor-api
- Type: Backend API
- Primary language: C#
- Framework: ASP.NET Core
- Deployment unit: Azure App Service

## Owns

- Onboarding API
- Validation orchestration
- Audit logging

## Does Not Own

- Frontend rendering
- Database schema ownership
- External KYC provider implementation

## Notes

- Controllers must remain thin.
- Business rules belong in application services or domain layer.
- No direct database access from controllers.
```

---

### 6.3 `repositories/repo-XXX/technology-stack.md`

Purpose: identify technology stack and runtime model.

Example:

```markdown
# Technology Stack — REPO-001

| Area | Value |
|---|---|
| Language | C# |
| Runtime | .NET 8 |
| Framework | ASP.NET Core Web API |
| API style | REST |
| Authentication | OAuth2 / JWT / Azure AD |
| Database access | Entity Framework Core |
| Testing | xUnit |
| Build | dotnet build |
| Test | dotnet test |
| Deployment | Azure App Service |
```

---

### 6.4 `repositories/repo-XXX/service-catalog.md`

Purpose: identify services or deployable units represented by the repository.

Example:

```markdown
# Service Catalog — REPO-001

| Service ID | Service Name | Type | Responsibility |
|---|---|---|---|
| SVC-001 | Onboarding API | REST API | Receives onboarding requests |
| SVC-002 | Audit API | REST API | Records audit events |
```

---

### 6.5 `repositories/repo-XXX/module-map.md`

Purpose: provide enough structural guidance without exposing full source code.

Example:

```markdown
# Module Map — REPO-001

| Module ID | Module | Responsibility | Notes |
|---|---|---|---|
| MOD-001 | API Controllers | Expose REST endpoints | Thin controllers only |
| MOD-002 | Application Services | Business orchestration | Main logic here |
| MOD-003 | Domain | Domain rules and entities | No infrastructure dependencies |
| MOD-004 | Infrastructure | DB and external API access | Adapter pattern |
| MOD-005 | Tests | Unit and integration tests | xUnit |
```

This helps the framework generate repository-specific implementation tasks.

---

### 6.6 `repositories/repo-XXX/api-surface.md`

Purpose: describe relevant API capabilities.

Example:

```markdown
# API Surface — REPO-001

| API ID | Method | Path | Responsibility | Notes |
|---|---|---|---|---|
| API-001 | POST | /api/onboarding | Create onboarding request | Existing endpoint |
| API-002 | GET | /api/onboarding/{id} | Read onboarding status | Existing endpoint |
```

This does not need full OpenAPI detail, but the more structured it is, the better the generated tasks will be.

---

### 6.7 `repositories/repo-XXX/data-surface.md`

Purpose: identify data ownership and persistence responsibilities.

Example:

```markdown
# Data Surface — REPO-004

| Data ID | Entity / Table | Owner Repo | Description | Notes |
|---|---|---|---|---|
| DATA-001 | OnboardingRequest | REPO-004 | Stores onboarding request state | SQL Server |
| DATA-002 | AuditEvent | REPO-004 | Stores audit trail | Append-only |
```

---

### 6.8 `repositories/repo-XXX/integration-surface.md`

Purpose: describe external and internal dependencies.

Example:

```markdown
# Integration Surface — REPO-003

| Integration ID | Type | Direction | System | Purpose |
|---|---|---|---|---|
| INT-001 | REST | Outbound | KYC Provider | Validate customer identity |
| INT-002 | Queue | Inbound | Service Bus | Receive onboarding events |
| INT-003 | Database | Outbound | SQL Server | Update onboarding state |
```

---

### 6.9 `repositories/repo-XXX/build-test-commands.md`

Purpose: provide candidate commands for the AI coding agent.

Example:

```markdown
# Build and Test Commands — REPO-001

| Purpose | Command | Expected Result |
|---|---|---|
| Restore | dotnet restore | Dependencies restored |
| Build | dotnet build | Build succeeds without errors |
| Test | dotnet test | All tests pass |
| Format | dotnet format --verify-no-changes | No formatting violations |
```

These should be copied into the AI handoff package as candidate validation commands.

---

### 6.10 `repositories/repo-XXX/coding-standards.md`

Purpose: define repository-specific rules for AI coding.

Example:

```markdown
# Coding Standards — REPO-001

## Rules

- Keep controllers thin.
- Put business orchestration in application services.
- Put domain invariants in the domain layer.
- Do not call the database directly from controllers.
- Use existing logging abstractions.
- Add or update tests for all new behavior.
- Do not introduce new dependencies without explicit approval.

## Forbidden Patterns

- Business logic in API controllers.
- Duplicated validation rules across layers.
- Direct HTTP calls without using existing integration adapters.
- Silent exception swallowing.
```

---

## 7. Recommended Workflow Changes

The current workflow should be modified by adding a formal repository intelligence phase after business analysis and before draft delivery planning.

### Current simplified flow

```text
0   BRS normalisation
0b  Architecture draft if missing
0c  Input package normalisation
1   Routing decision
2   Business intake summary
2b  Business rules
2c  Actors and personas
2d  Draft process flows
2e  Draft use cases
4   Draft delivery structure
5   Architecture review
6   Architecture rules
7   Open decisions
8   Engineering readiness
9   Delivery structure confirmed
9b  Process flows confirmed
9c  Use cases confirmed
9d  Story enrichment check
12  Quality gates
13  Handoff
14  Review package
```

### Recommended improved flow

```text
0   BRS normalisation
0b  Architecture draft if missing
0c  Input package normalisation

1   Routing decision

2   Business intake summary
2b  Business rules
2c  Actors and personas
2d  Draft process flows
2e  Draft use cases

3   Repository intelligence
3a  Repository inventory
3b  Technology and service classification
3c  Capability-to-repository map
3d  Repository constraints

4   Draft delivery structure

5   Architecture review
6   Architecture rules
7   Open decisions
8   Engineering readiness

9   Delivery structure confirmed
9b  Process flows confirmed
9c  Use cases confirmed
9d  Story enrichment check

10  Open decisions update
11  Initiative context

12  Quality gates
12b Entity model

13  AI implementation handoff
13a By-story package
13b By-repository package
13c Cross-repository dependency graph
13d Repository execution guard

14  Review package
15  Implementation feedback loop
```

This preserves the strength of the current workflow while making the final output much more useful for AI-assisted implementation.

---

## 8. New Repository Intelligence Phase

### 8.1 Stage 3 — Repository Intelligence

**Persona:** Engineering Lead / Repository Analyst

**Purpose:** understand the repository landscape enough to split stories, tasks, validation, and coding prompts by repository.

**Inputs:**

- `input/brs.md`
- `input/input-package.md`
- `business-intake/business-intake-summary.md`
- `business-intake/business-rules.md`
- `business-analysis/actors-and-personas.md`
- `business-analysis/process-flows.md` draft
- `business-analysis/use-case-spec.md` draft
- `repositories/` metadata

**Outputs:**

- `repositories/repository-inventory.md`
- `repositories/technology-service-classification.md`
- `planning/capability-to-repository-map.md`
- `repositories/repository-constraints.md`

---

### 8.2 Stage 3a — Repository Inventory

**Artifact:** `repositories/repository-inventory.md`

Purpose: identify candidate repositories involved in the initiative.

The framework should determine:

- Which repositories may be impacted.
- Which repositories are definitely not impacted.
- Which repositories are uncertain and need confirmation.
- Which repository owns which capability.

---

### 8.3 Stage 3b — Technology and Service Classification

**Artifact:** `repositories/technology-service-classification.md`

Purpose: classify each repository by technology and service type.

Recommended service types:

```text
backend-api
frontend-spa
frontend-mobile
worker
batch-job
database
integration-service
library
infrastructure
pipeline
documentation
configuration
```

Suggested table:

```markdown
| Repo ID | Repo Name | Service Type | Technology | Runtime | Deployment Unit | Validation Profile |
|---|---|---|---|---|---|---|
| REPO-001 | client-advisor-api | backend-api | .NET 8 | ASP.NET Core | Azure App Service | dotnet |
| REPO-002 | client-advisor-ui | frontend-spa | React / TypeScript | Node.js | Static Web App | npm |
| REPO-003 | onboarding-worker | worker | .NET 8 | Worker Service | Container App | dotnet |
| REPO-004 | database | database | SQL Server | SQL | DACPAC | sql |
```

---

### 8.4 Stage 3c — Capability-to-Repository Map

**Artifact:** `planning/capability-to-repository-map.md`

Purpose: map business capabilities, process flows, use cases, and features to repositories.

Suggested table:

```markdown
| Capability | PF | UC | Repo ID | Service | Responsibility | Confidence |
|---|---|---|---|---|---|---|
| Submit onboarding request | PF-001 | UC-001 | REPO-002 | Advisor UI | Capture form | High |
| Submit onboarding request | PF-001 | UC-001 | REPO-001 | Onboarding API | Validate and persist request | High |
| Process onboarding async | PF-002 | UC-002 | REPO-003 | Onboarding Worker | Execute async checks | Medium |
| Store onboarding state | PF-001 | UC-001 | REPO-004 | Client DB | Persist request state | High |
```

This artifact is essential because it drives repository-aware story splitting.

---

### 8.5 Stage 3d — Repository Constraints

**Artifact:** `repositories/repository-constraints.md`

Purpose: define repo-specific implementation boundaries.

Example:

```markdown
# Repository Constraints

## REPO-001 — client-advisor-api

- Controllers must remain thin.
- Business rules must be implemented in application services or domain layer.
- No direct database calls from controllers.
- New endpoints must use existing authentication and authorization mechanisms.
- All changes require unit tests.

## REPO-002 — client-advisor-ui

- API calls must go through the existing API client layer.
- Do not duplicate backend business validation in the UI except for simple field validation.
- Reuse existing form components when possible.
- All new UI behavior requires component or integration tests.

## REPO-004 — database

- Schema changes require migration and rollback scripts.
- New tables require ownership and retention classification.
- PII fields must be explicitly classified.
```

---

## 9. How Story Splitting Should Change

The confirmed delivery structure should become repository-aware.

Every story should include:

- Story ID.
- Actor.
- Requirement links.
- Business rule links.
- Acceptance criteria.
- Process-flow reference.
- Primary repository.
- Secondary repositories.
- Impacted service or module.
- Repository-specific implementation slices.
- Candidate validation commands.

### Example story structure

```markdown
# Story F-001.1 — Submit onboarding request

## User Story

As an advisor, I want to submit an onboarding request so that the client onboarding process can start.

## Traceability

| Type | IDs |
|---|---|
| Functional requirements | FR-001, FR-002 |
| Business rules | BR-001, BR-003 |
| Actor | ACT-001 Advisor |
| Process flow | PF-001 |
| Use case | UC-001 |

## Repository Allocation

| Role | Repo ID | Repository | Responsibility |
|---|---|---|---|
| Primary | REPO-002 | client-advisor-ui | Capture onboarding form |
| Secondary | REPO-001 | client-advisor-api | Validate and persist request |
| Secondary | REPO-004 | database | Store onboarding request state |

## Implementation Slices

1. REPO-004: Add or update onboarding request persistence model.
2. REPO-001: Add API endpoint, command, validation, and tests.
3. REPO-002: Add UI form, API integration, validation messages, and tests.

## Candidate Validation

| Repo ID | Commands |
|---|---|
| REPO-001 | `dotnet build`, `dotnet test` |
| REPO-002 | `npm run build`, `npm test`, `npm run lint` |
| REPO-004 | migration validation command |
```

This structure is much more useful for autonomous implementation than a story that only contains business text.

---

## 10. Handoff Package Design

The handoff should be split in two complementary ways:

```text
standalone-delivery/
  by-story/
  by-repository/
  cross-repository/
  review-package/
```

### Why both views are needed

The by-story package preserves business traceability.

The by-repository package is what an AI coding agent actually needs when it runs inside one repository.

Most coding agents work best when focused on one repository at a time. Therefore, the repository-level package is critical.

---

## 11. By-Story Package

Recommended structure:

```text
standalone-delivery/by-story/F-001.1/
  story.md
  design.md
  tasks.md
  acceptance-criteria.md
  bdd-scenarios.md
  repository-split.md
  cross-repo-dependencies.md
  coding-prompt.md
```

### Purpose of each file

| File | Purpose |
|---|---|
| `story.md` | Business story and traceability |
| `design.md` | Story-level design notes |
| `tasks.md` | Implementation tasks across repos |
| `acceptance-criteria.md` | Testable AC list |
| `bdd-scenarios.md` | Related Gherkin scenarios |
| `repository-split.md` | How the story is split by repo/service |
| `cross-repo-dependencies.md` | Sequencing and dependencies |
| `coding-prompt.md` | AI-ready story prompt |

The story package should answer:

```text
What business behavior must be delivered, and which repositories participate?
```

---

## 12. By-Repository Package

Recommended structure:

```text
standalone-delivery/by-repository/REPO-001/
  repo-context.md
  stories-in-scope.md
  implementation-plan.md
  tasks.md
  candidate-files-to-touch.md
  validation-commands.md
  repository-execution-guard.md
  coding-prompt.md
  implementation-feedback-template.md
```

### Purpose of each file

| File | Purpose |
|---|---|
| `repo-context.md` | Repository profile, technology, service type, constraints |
| `stories-in-scope.md` | Stories or story slices allocated to this repo |
| `implementation-plan.md` | Sequenced repo-level implementation approach |
| `tasks.md` | Concrete repo-specific tasks |
| `candidate-files-to-touch.md` | Candidate files, folders, or modules to inspect or modify |
| `validation-commands.md` | Candidate build, test, lint, migration commands |
| `repository-execution-guard.md` | Mandatory checks before coding in the real repo |
| `coding-prompt.md` | AI-ready prompt for the repo-level coding agent |
| `implementation-feedback-template.md` | Template for reporting blockers, mismatches, and completed changes |

The repository package should answer:

```text
What should be done in this repository, in what order, with which constraints, and how should it be validated?
```

---

## 13. Cross-Repository Package

Recommended structure:

```text
standalone-delivery/cross-repository/
  dependency-graph.md
  implementation-sequence.md
  integration-contracts.md
  release-coordination.md
  rollback-considerations.md
```

### Purpose

Large initiatives often span multiple repositories. The framework should explicitly manage cross-repo dependencies.

The cross-repository package should answer:

- Which repository must be changed first?
- Which repository depends on another?
- Which API or data contract must be agreed before implementation?
- Which changes must be released together?
- Which changes can be released independently?
- What is the rollback strategy if one repository fails?

---

## 14. Repository Execution Guard

This is one of the most important additions.

Because the framework does not have full source-code access, the AI agent running inside the target repository must verify the repository reality before changing code.

Recommended file:

```text
standalone-delivery/by-repository/REPO-XXX/repository-execution-guard.md
```

Recommended content:

```markdown
# Repository Execution Guard

You are now running inside the target repository.

Before modifying code, you must:

1. Inspect the repository structure.
2. Identify the actual modules, folders, and existing implementation patterns.
3. Confirm or revise the candidate files-to-touch list.
4. Confirm build, test, lint, and migration commands.
5. Check whether the repository matches the repository profile provided in this package.
6. Check whether architecture rules and repository constraints are still valid.
7. Identify any missing technical information.
8. Report mismatches before implementation.

Do not implement if:

- The expected repository type does not match the actual repository.
- Required modules or services cannot be located.
- Validation commands cannot be identified.
- The requested change conflicts with architecture rules.
- The requested change requires a decision that is still open.
- The package assigns responsibilities to the wrong repository.

If a mismatch is found, update `implementation-feedback.md` and stop unless explicitly instructed to continue.
```

This guard makes the package safe for autonomous AI coding.

---

## 15. Candidate vs Confirmed Implementation Guidance

The framework should distinguish between candidate guidance and confirmed guidance.

Because the framework does not have full codebase access, it should use names such as:

| Use this | Avoid this when codebase is not available |
|---|---|
| `candidate-files-to-touch.md` | `files-to-touch.md` |
| `candidate-validation-commands.md` | `validation-commands.md` without caveat |
| `candidate-module-impact.md` | `module-impact.md` as if confirmed |
| `repository-execution-guard.md` | no guard |

This distinction is important. It prevents the framework from overclaiming.

The coding agent inside the real repository should turn candidate guidance into confirmed guidance.

---

## 16. Updated Stage 13 — AI Implementation Handoff

Stage 13 should be expanded.

### Current Stage 13

```text
13 · OpenSpec / Standalone handoff
One folder per F-XXX.X story:
story.md + design.md + tasks.md + coding-prompt.md
```

### Recommended Stage 13

```text
13 · AI implementation handoff
Produce by-story and by-repository implementation packages.
Generate cross-repository dependency graph and repository execution guards.
Each coding prompt must include business rules, architecture rules, acceptance criteria, BDD scenarios, candidate repo/module impact, validation commands, DoD, and execution guard.
```

### Recommended outputs

```text
standalone-delivery/
  by-story/
  by-repository/
  cross-repository/
  implementation-feedback/
  review-package/
```

### Blocking rules

Stage 13 should be blocked by:

- Story enrichment passed.
- All triggered quality gates accepted.
- Zero blocking open decisions.
- Repository intelligence available or explicitly marked unavailable.
- Capability-to-repository map produced.
- Repository execution guard generated.

---

## 17. Updated Hard Gate Rules

Recommended hard gate rules:

1. Stage 2d requires business rules and actors.
2. Stage 2e requires draft process flows.
3. Repository intelligence phase requires at least repository inventory or an explicit statement that repository metadata is unavailable.
4. Draft delivery structure requires business rules, actors, and repository intelligence.
5. Architecture review requires draft process flows and repository intelligence.
6. Confirmed stories require readiness, business rules, actors, and capability-to-repository map.
7. Story enrichment requires confirmed process flows.
8. BDD requires confirmed and enriched stories.
9. Handoff requires story enrichment passed, all triggered gates accepted, zero blocking decisions, and repository execution guard generated.
10. Repository-level coding prompts must not treat candidate files as confirmed.
11. If repository metadata is missing, handoff must include a repository discovery task and explicit uncertainty warning.

---

## 18. Updated Artifact List

### Input artifacts

```text
input/brs.md
input/architecture.md
input/input-package.md
repositories/repository-inventory.md
repositories/*/repository-profile.md
repositories/*/technology-stack.md
repositories/*/service-catalog.md
repositories/*/module-map.md
repositories/*/api-surface.md
repositories/*/data-surface.md
repositories/*/integration-surface.md
repositories/*/build-test-commands.md
repositories/*/coding-standards.md
```

### Business artifacts

```text
business-intake/business-intake-summary.md
business-intake/business-rules.md
business-analysis/actors-and-personas.md
business-analysis/process-flows.md
business-analysis/use-case-spec.md
business-analysis/entity-model.md
```

### Planning artifacts

```text
planning/delivery-structure.md
planning/capability-to-repository-map.md
planning/delivery-increments.md
planning/traceability-matrix.md
```

### Architecture artifacts

```text
architecture/architecture-review.md
architecture/architecture-rules.md
architecture/integration-dependency-map.md
architecture/decisions/ADR-001.md
architecture/decisions/ADR-002.md
```

### Readiness and quality artifacts

```text
state/open-decisions.md
engineering-readiness/readiness-check.md
engineering-readiness/initiative-context.md
quality-gates/test-strategy.md
quality-gates/security-review.md
quality-gates/data-contract.md
quality-gates/api-contract.md
quality-gates/observability-plan.md
quality-gates/non-functional-requirements.md
quality-gates/bdd/
```

### AI implementation handoff artifacts

```text
standalone-delivery/by-story/
standalone-delivery/by-repository/
standalone-delivery/cross-repository/
standalone-delivery/implementation-feedback/
review-package/status.md
```

---

## 19. Recommended `coding-prompt.md` Structure

Each `coding-prompt.md` should be directly usable by an AI coding agent.

Recommended structure:

```markdown
# Coding Prompt — REPO-001 / F-001.1

## Execution Context

You are running inside the target repository. Before modifying code, execute the repository execution guard.

## Goal

Describe the business and technical goal.

## Stories in Scope

List story IDs and summaries.

## Business Rules

List BR-NNN rules relevant to this repository.

## Architecture Rules

List AR-NNN rules relevant to this repository.

## Repository Constraints

List repository-specific constraints.

## Acceptance Criteria

List AC-NNN acceptance criteria relevant to this repository.

## BDD Scenarios

List scenario IDs and scenario summaries.

## Candidate Implementation Areas

List candidate modules, folders, or files to inspect.

## Tasks

List sequenced tasks.

## Validation Commands

List candidate validation commands.

## Definition of Done

- Repository execution guard completed.
- Candidate files confirmed or revised.
- Implementation completed.
- Tests added or updated.
- Validation commands run.
- No unrelated files changed.
- Architecture rules respected.
- Business rules respected.
- Implementation feedback completed.

## Stop Conditions

Stop and report if:

- Repository profile does not match actual repository.
- Required modules cannot be found.
- Commands cannot be run.
- Architecture rules conflict with requested implementation.
- Open decisions block implementation.
```

---

## 20. Implementation Feedback Loop

The framework should generate feedback templates that the coding agent completes after attempting implementation.

Recommended file:

```text
standalone-delivery/by-repository/REPO-XXX/implementation-feedback-template.md
```

Recommended content:

```markdown
# Implementation Feedback — REPO-XXX

## Repository Reality Check

| Check | Result | Notes |
|---|---|---|
| Repository matches expected profile | Yes / No |  |
| Candidate files confirmed | Yes / No |  |
| Validation commands confirmed | Yes / No |  |
| Architecture rules applicable | Yes / No |  |

## Changes Implemented

| Story | Task | Status | Notes |
|---|---|---|---|

## Files Changed

| File | Change Type | Reason |
|---|---|---|

## Tests Added or Updated

| Test | Purpose | Result |
|---|---|---|

## Validation Results

| Command | Result | Notes |
|---|---|---|

## Blockers

| Blocker | Type | Required Decision |
|---|---|---|

## Deviations from Package

| Package Assumption | Actual Repository Reality | Action Taken |
|---|---|---|

## Follow-up Required

List follow-up actions.
```

This closes the loop between specification generation and real implementation.

---

## 21. What Should Be Removed or Reduced

### 21.1 Fast Path in the main flow

Since the framework is mainly for big initiatives, Fast Path should not be emphasized in the main workflow.

Recommendation:

- Move Fast Path to an appendix.
- Keep Standard, Enterprise, and Enterprise + Modular in the main model.

### 21.2 Stale readiness as a special case

The current stale readiness rule is useful but too specific.

Instead of only checking whether `readiness-check.md` is stale, use a general consistency rule:

```text
Before every phase transition, the orchestrator validates that all upstream artifacts are current, non-empty, and consistent with the latest accepted decisions.
```

### 21.3 Overconfident files-to-touch

Do not generate final `files-to-touch.md` unless the framework has actual codebase metadata precise enough to justify it.

Prefer:

```text
candidate-files-to-touch.md
```

Then ask the coding agent to confirm or revise it inside the repository.

---

## 22. Proposed Final Workflow Table

| # | Phase | Stage | Main Artifact | Purpose |
|---|---|---|---|---|
| 0 | Input | BRS normalisation | `input/brs.md` | Normalize BRS and assign requirement IDs |
| 0b | Input | Architecture draft if missing | `input/architecture.md` | Create initial architecture context |
| 0c | Input | Input package normalisation | `input/input-package.md` | Consolidate source inputs and assumptions |
| 1 | Routing | Routing decision | `state/routing-decision.md` | Classify initiative complexity and mode |
| 2 | Business | Business intake | `business-intake/business-intake-summary.md` | Extract scope, objectives, requirements |
| 2b | Business | Business rules | `business-intake/business-rules.md` | Extract BR-NNN rules |
| 2c | Business | Actors/personas/systems | `business-analysis/actors-and-personas.md` | Identify actors and external systems |
| 2d | Business | Draft process flows | `business-analysis/process-flows.md` | Model process before final stories |
| 2e | Business | Draft use cases | `business-analysis/use-case-spec.md` | Model use cases from process flows |
| 3 | Repository | Repository inventory | `repositories/repository-inventory.md` | Identify candidate repositories |
| 3b | Repository | Technology/service classification | `repositories/technology-service-classification.md` | Classify technology and service type |
| 3c | Repository | Capability-to-repository map | `planning/capability-to-repository-map.md` | Map business scope to repos |
| 3d | Repository | Repository constraints | `repositories/repository-constraints.md` | Define repo-specific rules |
| 4 | Planning | Draft delivery structure | `planning/delivery-structure.md` | Draft epics, features, story stubs |
| 5 | Architecture | Architecture review | `architecture/architecture-review.md` | Validate business/process/repo alignment |
| 6 | Architecture | Architecture rules | `architecture/architecture-rules.md` | Define enforceable AR-NNN rules |
| 7 | Decisions | Open decisions | `state/open-decisions.md` | Track blockers and owners |
| 8 | Readiness | Engineering readiness | `engineering-readiness/readiness-check.md` | Decide whether detailed planning can proceed |
| 9 | Planning | Confirmed delivery structure | `planning/delivery-structure.md` | Expand stories with AC, FR, BR, repo allocation |
| 9b | Business | Confirmed process flows | `business-analysis/process-flows.md` | Add story and AC references |
| 9c | Business | Confirmed use cases | `business-analysis/use-case-spec.md` | Add story and AC coverage |
| 9d | Planning | Story enrichment check | `planning/delivery-structure.md` | Validate story completeness |
| 10 | Decisions | Decision consistency update | `state/open-decisions.md` | Update blockers from confirmed planning |
| 11 | Engineering | Initiative context | `engineering-readiness/initiative-context.md` | Document constraints and governed boundaries |
| 12 | Quality | Quality gates | `quality-gates/*` | Test, security, data, API, observability, BDD |
| 12b | Business/Data | Entity model | `business-analysis/entity-model.md` | Model entities and relationships |
| 13 | Handoff | AI implementation handoff | `standalone-delivery/*` | Produce by-story and by-repository packages |
| 13a | Handoff | By-story package | `standalone-delivery/by-story/` | Preserve story-level traceability |
| 13b | Handoff | By-repository package | `standalone-delivery/by-repository/` | Provide repo-level coding package |
| 13c | Handoff | Cross-repository dependency graph | `standalone-delivery/cross-repository/` | Coordinate multi-repo implementation |
| 13d | Handoff | Repository execution guard | per repo | Force repo validation before coding |
| 14 | Review | Review package | `review-package/status.md` | Stakeholder-facing package |
| 15 | Feedback | Implementation feedback loop | `implementation-feedback.md` | Capture execution findings |

---

## 23. Final Recommendation

The current framework is on the right path. It should not be simplified. It should be made more explicit about what it produces and what it does not know.

The main conceptual change is this:

```text
The framework does not generate final codebase-specific implementation instructions.
It generates a governed, repository-aware, candidate implementation package.
The final codebase confirmation happens later inside the target repository.
```

The most important practical change is this:

```text
Do not only split work by epic, feature, and story.
Also split it by repository, service, and module.
```

The final output should therefore include both:

```text
by-story packages for traceability
by-repository packages for AI coding execution
```

This gives you the best of both worlds:

- Business and governance traceability.
- Practical implementation guidance for autonomous coding agents.
- Clear repository ownership.
- Safer AI execution.
- Better multi-repository coordination.
- A feedback loop when the real codebase differs from the assumptions.

With these changes, the framework becomes a strong candidate for real enterprise usage.

---

## 24. Short Final Verdict

The current version works as a BRS-to-specification framework.

With the recommended repository intelligence phase and AI implementation handoff changes, it can become a strong BRS-to-agentic-delivery framework.

Recommended final positioning:

```text
BRS-to-Agentic-Delivery is a framework that transforms business requirements into governed, traceable, repository-aware implementation packages for AI-assisted software delivery.
```

