# How to Use This Framework

## Recommended first prompt

Run:

```text
.github/prompts/brs-to-spec-run-workflow.prompt.md
```

Use it at the start of every working session. The workflow runner detects the active initiative workspace, checks content (not just file existence), identifies stale artifacts, and executes the next required stage automatically.

## Workspace rule

Work inside one initiative workspace at a time.

The standard workspace shape is:

```text
initiatives/<initiative-id>-<slug>/
```

Create a new workspace with:

```bash
python .brs2spec/tools/scripts/new_initiative.py onboarding-request --initiative-id I001 --mode enterprise --execution-mode openspec
```

## Workflow status rule

At every point, be able to answer:

```text
What stage am I in?
What artifact is already complete?
What artifact is missing?
What must exist before I proceed?
What is the next prompt to run?
```

## Artifact use rule

For every major artifact, be clear about:

```text
who consumes it
what decision or purpose it serves
what artifact or workflow step depends on it next
what should be referenced instead of duplicated into it
```

Quick guide:

| Artifact | Primary consumer | Next dependency | Do not duplicate |
|---|---|---|---|
| `business-intake/business-intake-summary.md` | PO / delivery lead | Architecture review and planning | Engineering task detail |
| `architecture/architecture-review.md` | Architect / tech lead | Architecture rules, planning, readiness | Rewritten business intake |
| `planning/delivery-structure.md` | Delivery lead / architect / PO | Readiness, handoff, planning projection | Full acceptance text or implementation steps |
| `engineering-readiness/readiness-check.md` | Delivery lead / QA / architect | Triggered quality gates and handoff decision | Handoff package details |
| `quality-gates/*.md` | Gate owner role | Handoff, merge, or release approval | Full copies of source artifacts |
| `delivery-spec.md` or `design.md` | Engineers / reviewers | Implementation tasks | Backlog projection content |
| `tasks.md` | Engineers / coding agents | Implementation and implementation review | A second business-planning hierarchy |
| `gitlab-planning-view.md` | Delivery team / PO | Agile tool projection and coordination | Source-of-truth scope or engineering contract |

Some artifacts may also include an optional embedded visual view when it materially improves understanding:

- `business-intake-summary.md` -> business flow or actor/system view
- `architecture-review.md` -> context, container, or integration flow
- `delivery-structure.md` -> slice/dependency or capability-to-module orientation view
- `design.md` or `delivery-spec.md` -> focused interaction or sequence flow for the active deliverable

Prefer lightweight markdown-friendly visuals such as Mermaid.
Do not add a diagram when text is already clear enough.
Reference an existing authoritative diagram instead of regenerating one when that source is already the system of record.
Add a visual only when it materially improves clarity for the primary consumer.
Do not treat the absence of a non-critical visual as a workflow blocker by itself.

## Planning density rule

For the two largest planning artifacts:

```text
planning/delivery-structure.md
perspectives/agile-planning/gitlab-planning-view.md
```

apply this split:

- `delivery-structure.md` carries planning structure, story hierarchy, governed boundaries, and traceability expectations
- `gitlab-planning-view.md` carries only the coordination projection the team needs for GitLab or similar tools

Keep detailed:

- epic / feature / user story structure
- governed boundaries
- slice logic that changes handoff, readiness, or validation

Keep summary-level:

- business capability overviews
- candidate modules when they are only orientation aids
- candidate slices when they are not yet selected active deliverables
- Engineering Notes and Enablement Needs that do not change coordination

Reference instead of repeat:

- acceptance definitions
- architecture rationale
- readiness detail
- quality-gate content
- implementation-task detail

## Default input mode

Start simple unless the same initiative clearly has multiple source documents:

```text
input/brs.md
input/architecture.md
input/input-package.md
```

At this stage, architecture input is often high-level solution architecture context rather than initiative-specific design detail.

## Expanded input mode

If the same initiative is described by more than one BRS or more than one architecture source, expand only that input family:

```bash
python .brs2spec/tools/scripts/add_brs.py initiatives/I001-onboarding-request compliance
python .brs2spec/tools/scripts/add_architecture.py initiatives/I001-onboarding-request security-constraints
```

After expansion, the workspace can look like:

```text
input/brs/
  main.md
  compliance.md
input/architecture/
  main.md
  security-constraints.md
input/input-package.md
```

All prompt input and output paths are relative to the current initiative workspace, not the repository root.

## Choose an entry mode first

Before you think about delivery mode or execution mode, choose the starting pattern that best matches the initiative:

```text
BRS-first
existing-system enhancement
small change / bug fix
large modular initiative
```

Use:

```text
docs/18-entry-modes.md
```

If the entry mode is `existing-system enhancement`, also review:

```text
docs/19-brownfield-existing-system-mode.md
```

If the entry mode is `small change / bug fix`, also review:

```text
docs/20-small-change-paths.md
```

This does not replace routing.

It helps you choose the right entry point before running:

```text
.brs2spec/1-routing/01-select-delivery-and-execution-mode.md
```

## Step 0 - Prepare inputs

Inside the initiative workspace, maintain either:

```text
input/brs.md
input/architecture.md
input/input-package.md
```

or, when needed:

```text
input/brs/*.md
input/architecture/*.md
input/input-package.md
```

Run:

```text
.brs2spec/0-input-preparation/01-convert-brs-word-to-markdown.md
.brs2spec/0-input-preparation/02-convert-architecture-word-to-markdown.md
.brs2spec/0-input-preparation/03-normalize-input-package.md
```

Use `input/input-package.md` to record:

```text
source inventory
completeness
overlap
conflicts
assumptions
consolidation notes
```

Transition to Step 1 only when:

- the source inputs are normalized enough to route the initiative
- conflicts and assumptions are visible

## Step 1 - Select delivery and execution mode

Run:

```text
.brs2spec/1-routing/01-select-delivery-and-execution-mode.md
```

Output:

```text
routing/routing-decision.md
```

Transition to Step 2 only when:

- the likely delivery mode is clear enough
- the likely execution mode is clear enough
- small-change applicability is explicit when scope is narrow

## Step 2 - Create business intake summary

Run:

```text
.brs2spec/2-business-intake/01-create-business-intake-summary.md
```

Output:

```text
business-intake/business-intake-summary.md
```

This is the main Product Owner review artifact for the current initiative workspace.

For brownfield work, make sure the intake also surfaces existing-system context and what behavior must remain stable.

If existing-system impact is material, create:

```text
architecture/existing-system-impact.md
```

using:

```text
.brs2spec/templates/planning-and-modular-delivery/existing-system-impact.md
```

Transition to Step 3 only when:

- business scope is understandable
- major gaps and questions are visible
- brownfield context is visible when relevant

## Step 3 - Create early delivery shape

Run:

```text
.brs2spec/3-planning-and-modular-delivery/03-create-delivery-structure.md
```

For Enterprise + Modular Delivery, you may also continue later with:

```text
.brs2spec/3-planning-and-modular-delivery/04-identify-software-modules.md
.brs2spec/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md
.brs2spec/3-planning-and-modular-delivery/06-define-delivery-increments.md
```

`planning/delivery-structure.md` should define the initiative's Epic / Feature / User Story structure early enough to guide later architecture refinement.

At this point, use the architecture input mainly as early solution context:

- system landscape
- software systems
- containers
- integrations
- major platform boundaries
- high-level constraints

Transition to Step 4 only when:

- delivery structure exists
- the initial slices and story structure are understandable
- the architecture review can now assess a concrete initiative shape

## Step 4 - Review and refine architecture

Run:

```text
.brs2spec/3-planning-and-modular-delivery/01-review-initial-architecture.md
.brs2spec/3-planning-and-modular-delivery/02-create-global-architecture-rules.md
```

Outputs:

```text
architecture/architecture-review.md
architecture/architecture-rules.md
```

For brownfield work, use `architecture/existing-system-impact.md` as an explicit input to architecture review and readiness.

This is the point where high-level architecture context becomes initiative-specific architecture refinement.

The goal is not to restate the whole solution architecture.

The goal is to refine what that architecture means for this initiative's:

- slices and impacted components
- boundaries and contract implications
- validation implications
- rollout / rollback constraints
- readiness and handoff rules

Transition to Step 5 only when:

- architecture constraints are visible
- major conflicts and open decisions are explicit

## Step 5 - Complete delivery planning

For Enterprise Path, run:

```text
.brs2spec/3-planning-and-modular-delivery/07-create-traceability-matrix.md
```

For Enterprise + Modular Delivery, also run:

```text
.brs2spec/3-planning-and-modular-delivery/04-identify-software-modules.md when still needed
.brs2spec/3-planning-and-modular-delivery/05-map-capabilities-to-modules.md when still needed
.brs2spec/3-planning-and-modular-delivery/06-define-delivery-increments.md
```

Use this step to refine the planning set after architecture review, not to postpone initial delivery shape until late in the flow.

Transition to Step 6 only when:

- delivery structure exists
- active deliverable slicing is understandable
- traceability can be created or completed

## Step 6 - Check engineering readiness

Run:

```text
.brs2spec/4-engineering-readiness/01-check-engineering-readiness.md
```

Output:

```text
engineering-readiness/readiness-check.md
```

The readiness check decides whether the active deliverable is ready and which quality gates are triggered.

Readiness should consume:

- approved delivery shape from `planning/delivery-structure.md`
- initiative-specific architecture refinement from `architecture/architecture-review.md`
- initiative-specific architecture rules from `architecture/architecture-rules.md`
- traceability from `planning/traceability-matrix.md` when that artifact exists

Readiness is not the place to reconstruct vague planning or unresolved architecture.
It is also not the place to block progress only because an optional visual is absent when the text evidence is already clear enough.

If delivery shape or architecture refinement is still weak, improve those artifacts before treating readiness as authoritative.

Transition to Step 7 only when:

- readiness decision is explicit
- triggered gates are visible
- required-before stages are clear

For genuinely small and clearly safe changes, keep the path light.

For risky small changes, do not skip this step.

## Step 7 - Run required Conditional Quality Gates

Run only gates where:

```text
Triggered = Yes
Required = Yes
```

Quality gates are not optional. They are conditional.

These gate artifacts are pre-implementation or pre-release governance artifacts.

They are not the same as downstream implementation review prompts.

If the initiative creates or changes a governed boundary, the corresponding contract gate should normally be triggered:

- governed service or API boundary -> `API contract`
- governed data ownership or schema boundary -> `Data contract`
- governed asynchronous event boundary -> `Event contract`

Transition to Step 8 only when:

- required gates are complete
- or the remaining risks are explicitly accepted

## Step 8A - OpenSpec handoff

Run:

```text
.brs2spec/5-handoff/01-create-openspec-change-for-active-deliverable.md
```

Output:

```text
openspec/changes/
  dependency-graph.md
  F-XXX.X-<slug>/
    proposal.md
    design.md
    tasks.md
    specs/
```

The generated tasks are the engineering implementation contract for OpenSpec mode.

### Multi-repository handoff (optional)

If the initiative spans multiple repositories owned by different teams, you can tell the framework which repos are involved before generating the handoff. Create one descriptor file per repository in:

```text
input/repositories/
  api.md        ← becomes the "api" subfolder in each story folder
  ui.md         ← becomes the "ui" subfolder
  db.md         ← becomes the "db" subfolder
```

Use `.brs2spec/templates/repositories/_template.md` as the starting point for each file. The file name (without `.md`) becomes the subfolder name inside every story folder in the handoff output.

When descriptors are present the output structure becomes:

```text
openspec/changes/
  dependency-graph.md
  F-XXX.X-<slug>/
    api/
      proposal.md   ← API repo changes for this story only
      design.md
      tasks.md
      specs/
    ui/
      proposal.md   ← UI repo changes for this story only
      design.md
      tasks.md
      specs/
```

Each repo subfolder is self-contained — a team picks up their subfolder and implements without opening the other repos' folders. The `dependency-graph.md` at the root shows both story-to-story ordering and intra-story repo sequencing.

If `input/repositories/` does not exist, the workflow runner will ask once before generating the handoff whether you need multi-repo structure. Answering no proceeds with the flat structure above.

They should preserve traceability back to requirements, user stories when available, acceptance sources, architecture constraints, and quality gates.

They should be derived from planned user stories, not created independently from them.

Do not proceed with OpenSpec handoff from vague delivery structure or weak architecture refinement.

Handoff should consume:

- approved delivery shape
- initiative-specific architecture refinement and rules
- readiness decisions
- triggered quality gates
- traceability evidence

Missing optional visuals should not block handoff by default.

Only stop if the boundary, interaction, or contract is still too unclear for engineering without clearer visual support.

## Step 8B - Standalone handoff

Run:

```text
.brs2spec/5-handoff/02-create-standalone-delivery-package.md
```

Output:

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

The generated tasks are the engineering implementation contract for Standalone mode.

They should preserve traceability back to requirements, user stories when available, acceptance sources, architecture constraints, and quality gates.

They should be derived from planned user stories, not created independently from them.

Do not proceed with standalone handoff from vague delivery structure or weak architecture refinement.

Handoff should consume:

- approved delivery shape
- initiative-specific architecture refinement and rules
- readiness decisions
- triggered quality gates
- traceability evidence

Missing optional visuals should not block handoff by default.

Only stop if the boundary, interaction, or contract is still too unclear for engineering without clearer visual support.

Transition to Step 9 or Step 10 only when:

- implementation tasks are approved
- scope, validation, and constraints are clear enough for engineering

## Step 9 - Optional ready-for-Copilot gate

Before asking a coding agent to implement, you may complete:

```text
.brs2spec/templates/quality-gates/ready-for-copilot-checklist.md
```

Use it to confirm the active deliverable, implementation source, readiness state, and required quality gates.

## Step 10 - Implement one task

Use a coding-agent environment such as VS Code Copilot Agent mode only after the handoff artifacts exist.

Run:

```text
.brs2spec/8-copilot-implementation/01-implement-one-task.md
```

If review findings come back, use:

```text
.brs2spec/8-copilot-implementation/02-fix-review-comments.md
```

Do not implement from user stories alone.

Use user stories for business context and traceability.

Use one approved OpenSpec or standalone task as the implementation unit.

Transition to Step 11 only when:

- the selected task is implemented
- tests or validation evidence are available
- assumptions and residual risks are recorded

## Step 11 - Review implemented work

Run the review prompts that match the change:

```text
.brs2spec/9-reviewers/01-senior-code-review.md
.brs2spec/9-reviewers/02-qa-review.md
.brs2spec/9-reviewers/03-architecture-review.md
.brs2spec/9-reviewers/04-security-review.md
```

These prompts review actual code and tests after implementation.

They do not replace the quality-gate artifacts created earlier in the workflow.

## Step 12 - Review artifact quality

For every generated artifact, check:

```text
Decision clear?
Evidence included?
Risk stated?
Owner assigned?
Required-before stage clear?
Traceability preserved?
```

If an artifact does not answer these questions, regenerate it using the same prompt and the template as a stricter quality bar.

Also use:

```text
docs/21-artifact-quality-review.md
```

to review whether the artifact is actually useful for the next step, not just formally complete.

## Important rules

Do not generate tasks for the whole initiative at once.

Do not skip architecture constraints.

Do not call triggered quality gates optional.

Do not force Product Owners to review low-level engineering details.

Do not use standalone mode as a lower-quality version of OpenSpec.

Do not mix outputs from different initiatives in the same workspace.

## Step 13 - Create GitLab Planning View

Use this only when the delivery team plans and tracks work in GitLab, Jira, Azure DevOps or a similar planning tool.

Run after delivery increments and preferably after readiness check:

```text
.brs2spec/7-perspectives/agile-planning/01-create-gitlab-planning-view.md
```

Output:

```text
perspectives/agile-planning/gitlab-planning-view.md
```

This file is a planning projection, not the source of truth.

It is also not the engineering contract.

It should project the Epic / Feature / User Story structure already defined in `planning/delivery-structure.md`.

Do not edit the planning view to change scope, requirements, architecture constraints, quality gates, or implementation tasks.

Use the planning view to show Agile breakdown, Engineering Notes, Enablement Needs, and GitLab mapping in one place.

User stories in this view provide business context and traceability.

Implementation still happens from approved OpenSpec or standalone tasks.

If something changes, update the source artifacts and regenerate the view.

To refresh the view after readiness or quality gates change, run:

```text
.brs2spec/7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md
```

## Using GitHub Copilot / VS Code

This repository includes repository-level Copilot instructions:

```text
.github/copilot-instructions.md
```

Useful prompt files:

```text
.github/prompts/brs-to-spec-run-workflow.prompt.md   ← recommended entry point
.github/prompts/create-engineering-readiness.prompt.md
.github/prompts/create-openspec-handoff.prompt.md
.github/prompts/create-standalone-handoff.prompt.md
.github/prompts/create-gitlab-planning-view.prompt.md
.github/prompts/implement-one-task.prompt.md
.github/prompts/spec-correction.prompt.md
.github/prompts/describe-repository.prompt.md         ← run inside a target repo to generate input/repositories/ descriptor
```

Utility prompts (run standalone, not part of the delivery workflow):

```text
.brs2spec/tools/prompts/describe-repository.md   ← analyse a repository and produce a descriptor file for multi-repo handoff
```

Recommended first Copilot request:

```text
Based on .github/copilot-instructions.md, identify the active initiative workspace, the current workflow stage, and the next artifact to create.
```

Do not ask Copilot to implement directly from raw BRS sources.
