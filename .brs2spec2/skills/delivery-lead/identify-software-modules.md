# Skill — Identify Software Modules

## Identity

| Field | Value |
|---|---|
| skill_id | dl-identify-software-modules |
| persona | delivery-lead |
| event_types | IDENTIFY_SOFTWARE_MODULES |
| produces | planning/software-modules.md |

## When this skill is used

After `CREATE_DELIVERY_STRUCTURE` completes and `architecture/architecture-review.md` is available. Used in Enterprise and Enterprise+Modular execution modes to identify the software modules that will implement the stories, and to set up the capability-to-module mapping.

FastPath initiatives skip this skill unless they have a clear multi-module architecture.

## Role for this task

You are a senior delivery lead and architect collaborating to identify the software modules that will implement the initiative's stories — mapping capabilities to implementation units, making handoff boundaries explicit.

## Prerequisites check

Before starting, verify:
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs
- [ ] `architecture/architecture-review.md` exists
- [ ] `input/architecture.md` (or `input/architecture/*.md`) is readable

If the initiative is confirmed to be a single-module delivery, produce the artifact with one module and note that capability mapping is trivial.

## Instructions

### Step 1 — Identify modules from architecture

From the architecture review and architecture document:
- List every service, microservice, module, or deployment unit that will be changed or created
- Assign module IDs: MOD-001, MOD-002, ...
- For each module: name, type (new / existing), primary responsibility, technology stack

### Step 2 — Identify module boundaries

For each pair of modules:
- What is the contract between them? (API, event, shared database — avoid shared DB if architecture rules prohibit)
- Who owns the contract? (producer or consumer — pick one)
- Is the boundary synchronous or asynchronous?

### Step 3 — Map modules to functional areas

Create a mapping from functional area (BRS section or epic) to the module(s) responsible for implementing it:
- Primary module: the module that owns the implementation
- Supporting modules: modules that the primary depends on

### Step 4 — Identify team ownership

If the initiative involves multiple teams:
- Assign each module to a team or domain
- Identify cross-team dependencies

### Step 5 — Write the artifact

Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Module catalog: MOD-NNN ID, Name, Type (new/existing), Responsibility, Technology, Team
- Module boundary table: Module pair, Contract type, Owner, Sync/Async
- Functional area to module mapping table

## Done criteria

- [ ] Every component from the architecture review has a MOD-NNN entry
- [ ] Module boundaries have explicit contract types and owners
- [ ] Functional areas from the delivery structure map to at least one module
- [ ] No modules invented beyond what the architecture supports
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `planning/software-modules.md`

## Stop conditions

- If the architecture review has no identifiable module boundaries: produce a single-module artifact.
- Do not invent modules or boundaries not derivable from the architecture inputs.
