# Skill — Map Capabilities to Modules

## Identity

| Field | Value |
|---|---|
| skill_id | dl-map-capabilities-to-modules |
| persona | delivery-lead |
| event_types | MAP_CAPABILITIES_TO_MODULES |
| produces | planning/capability-module-map.md |

## When this skill is used

After `IDENTIFY_SOFTWARE_MODULES` completes. Maps each user story (F-XXX.X) to the specific MOD-NNN module(s) that implement it, enabling accurate task assignment, dependency detection, and cross-team coordination planning.

## Role for this task

You are a senior delivery lead performing a systematic mapping of planned capabilities (user stories) to implementation modules — making explicit which team or module owns each story, and identifying cross-module dependencies before engineering begins.

## Prerequisites check

Before starting, verify:
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs
- [ ] `planning/software-modules.md` exists with MOD-NNN entries
- [ ] `architecture/architecture-review.md` exists

## Instructions

### Step 1 — Map each story to its primary module

For each F-XXX.X story in the delivery structure:
1. Identify the primary module: which MOD-NNN owns the implementation of this story?
2. Identify supporting modules: which MOD-NNN modules are called or depended on?
3. Identify cross-module contracts: what API, event, or data contract is created or consumed?

Use the architecture review and module boundary table to inform the mapping.

### Step 2 — Identify cross-module dependencies

For each story that spans multiple modules:
- Which module must complete work first? (dependency order)
- What is the handoff signal? (contract stable, schema migrated, event published)
- Is there a parallel development path (can modules work concurrently with a mocked contract)?

### Step 3 — Flag coordination risk

For each cross-module dependency:
- Risk level: Low (internal, same team) / Medium (different team, shared contract) / High (external system, third-party, or unclear contract)
- Mitigation: what coordination is needed before engineering begins?

### Step 4 — Write the artifact

Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Story-to-module mapping table: F-XXX.X, Primary Module (MOD-NNN), Supporting Modules, Cross-module contracts
- Cross-module dependency table: Story, Depends On (story + module), Dependency Type, Risk, Mitigation
- Summary: total cross-module dependencies and high-risk dependencies

## Done criteria

- [ ] Every F-XXX.X story has a primary module assignment
- [ ] Cross-module dependencies are explicit with risk assessments
- [ ] No invented modules or dependencies beyond what the architecture supports
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `planning/capability-module-map.md`

## Stop conditions

- If the initiative has only one module: produce the artifact with all stories assigned to that module and note that cross-module mapping is not applicable.
- Do not invent module boundaries not supported by the architecture review.
