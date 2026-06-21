# Skill - Create Elaboration Plan

## Identity

```text
skill_id:    delivery-lead.create-elaboration-plan
persona:     delivery-lead
action_id:   create-elaboration-plan
produces:    planning/elaboration-plan.md
```

## When this skill is used

Run after the delivery skeleton is created and before epic packages are elaborated. This skill reads the high-level skeleton (epic/feature/story IDs) together with architecture risk and impact data, then proposes an elaboration order — which epics to detail first, which can be done in parallel, and the dependency rationale.

## Role for this task

You are a senior delivery lead deciding the elaboration sequence for a progressive decomposition initiative. You must balance business priority, architecture risk, dependency chains, and parallel elaboration opportunities to propose the most effective order for detailed epic and story elaboration.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If a required input is missing, stop and report the blocker.

## Hard constraints

- Every epic in the delivery skeleton must appear in the elaboration plan
- Every epic must be assigned to exactly one wave
- Dependencies must be valid — no epic can depend on an epic in a later wave
- The Mermaid diagram must include every epic with correct dependency edges
- At least one parallel group must be identified (or explicitly state none exist with justification)
- Risk levels must be derived from architecture-risks.md or architecture-review.md, not invented

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Extract epic list and dependency information

From `delivery-skeleton.md`, extract all epics with their features, story counts, and priority breakdown (Must/Should/Could). From `architecture-impact-map.md`, extract which epics have cross-cutting system impacts or shared component dependencies. From `architecture-risks.md`, extract which epics carry the most risk.

### Step 3 - Analyse inter-epic dependencies

For each epic, determine:
1. Which other epics it depends on (shared data models, shared APIs, shared infrastructure components, upstream events)
2. Which other epics depend on it (downstream consumers)
3. Whether it has cross-cutting architectural concerns (touches the same components as other epics)
4. Its risk level from architecture-risks.md

### Step 4 - Propose wave ordering

Assign each epic to a wave (Wave 1, Wave 2, etc.) based on these prioritisation factors:
1. **Foundation-first**: Epics that others depend on go in earlier waves
2. **Risk-first**: Higher-risk epics go earlier (fail fast, learn early)
3. **Business-priority**: Must-have epics before Should/Could
4. **Independence**: Standalone epics with no dependencies can fill capacity in any wave

### Step 5 - Identify parallel opportunities

Within each wave, identify which epics can be elaborated in parallel:
- No mutual dependencies
- No shared cross-cutting concerns that would cause conflicting design decisions
- Document the constraint that prevents parallelisation where applicable

### Step 6 - Build the Mermaid diagram

Create a Mermaid `graph TD` diagram showing:
- Subgraphs for each wave (labelled "Wave 1", "Wave 2", etc.)
- Every epic as a node with format `ENNN["E-NNN: Epic Title"]`
- Directed edges for dependencies (A --> B means A must be elaborated before B)
- Risk-based color classes using `classDef`:
  - `highRisk fill:#f96,stroke:#333`
  - `medRisk fill:#ff9,stroke:#333`
  - `lowRisk fill:#9f9,stroke:#333`
- Apply the appropriate class to each epic node

### Step 7 - Populate prioritisation criteria

Document the weighting factors used and explain the rationale for each weight assignment. The rationale must reference specific findings from the architecture inputs, not generic statements.

### Step 8 - Document risks to the elaboration order

Identify risks that could invalidate the proposed order. Examples:
- "If ADR-003 is resolved differently, E-002 may need to precede E-001"
- "If the external API contract changes, Wave 2 may need to be reordered"

### Step 9 - Write recommendations

Summarise the recommended elaboration sequence in 2-3 sentences, highlighting the key driver for the proposed order and any constraints the delivery lead should consider when reviewing.

## Output requirements

Write `planning/elaboration-plan.md` using `.b2s/artifact-templates/elaboration-plan.md`.

## Done criteria

- [ ] Every epic from delivery-skeleton.md appears in the elaboration plan
- [ ] Every epic is assigned to exactly one wave
- [ ] No dependency points forward (no epic depends on an epic in a later wave)
- [ ] Mermaid diagram includes all epics with correct dependency edges
- [ ] Mermaid diagram uses risk-based color classes
- [ ] At least one parallel group identified (or justified absence)
- [ ] Risk levels sourced from architecture-risks.md or architecture-review.md
- [ ] Prioritisation criteria documented with specific rationale
- [ ] Epic Dependency Analysis table is fully populated
- [ ] Risks and Mitigations table has at least one entry
- [ ] Recommendations section is populated
- [ ] No placeholder text remains

## Stop conditions

- If any file in `{resolved_required_inputs}` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
