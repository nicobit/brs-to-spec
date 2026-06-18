# Skill — Define Delivery Increments

## Identity

| Field | Value |
|---|---|
| skill_id | dl-define-delivery-increments |
| persona | delivery-lead |
| event_types | DEFINE_DELIVERY_INCREMENTS |
| produces | planning/delivery-increments.md |

## When this skill is used

Only in Enterprise+Modular execution mode. After `CREATE_DELIVERY_STRUCTURE` and optionally `MAP_CAPABILITIES_TO_MODULES` complete. Defines the formal D1, D2, D3... delivery increment groupings with their scope, dependencies, and acceptance gates.

FastPath and Standard execution modes skip this skill.

## Role for this task

You are a senior delivery lead defining the formal delivery increment plan — breaking the initiative's story set into sequenced, independently deployable increments with clear entry criteria, exit criteria, and inter-increment dependencies.

## Prerequisites check

Before starting, verify:
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs and increment assignments
- [ ] `routing/routing-decision.md` confirms execution mode is Enterprise+Modular
- [ ] `architecture/architecture-review.md` exists

If execution mode is not Enterprise+Modular: stop and state that this skill applies only to Enterprise+Modular mode.

## Instructions

### Step 1 — Confirm increment groupings from delivery structure

From `planning/delivery-structure.md`, read the increment assignments (D1, D2, ...) for each story. If they are not yet assigned, assign them now following these rules:
- D1: must-have stories required for the minimum viable state (all Must-priority stories that unblock other increments)
- D2+: should/could stories, optional capabilities, or extensions
- Stories with cross-increment dependencies must be ordered: the dependency must be in an earlier increment than the dependent story

### Step 2 — For each increment, document

1. **Increment ID** — D1, D2, D3, ...
2. **Name** — short descriptive name (e.g. "Core intake capability")
3. **Scope** — list of F-XXX.X stories included
4. **Entry criteria** — what must be true before this increment begins (previous increment accepted, specific gates passed, decisions resolved)
5. **Exit criteria** — what must be true for this increment to be accepted (all stories done, BDD scenarios passing, gates accepted)
6. **Dependencies** — which increments or external deliverables this depends on
7. **Estimated team effort** — rough indication (small / medium / large) not binding commitment
8. **Quality gate requirements** — which gates are triggered within this increment

### Step 3 — Validate increment ordering

Check:
- No story in increment Dn depends on a story in increment Dn+1 or later
- The D1 scope is genuinely minimum viable (not a copy of the full scope)
- Cross-module dependencies within an increment are feasible (if MOD-NNN mapping exists)

### Step 4 — Write the artifact

Use `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, execution mode, creation date
- Increment summary table: ID, Name, Story Count, Must/Should/Could breakdown, Key Dependencies
- Full increment definition per D-N with all required fields
- Cross-increment dependency graph (Mermaid `graph LR`)

## Done criteria

- [ ] Every F-XXX.X story is assigned to exactly one increment
- [ ] Increment ordering is consistent (no forward dependencies)
- [ ] Entry and exit criteria are explicit for each increment
- [ ] D1 is minimum viable (not gold-plated)
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `planning/delivery-increments.md`

## Stop conditions

- If execution mode is not Enterprise+Modular: stop immediately.
- If delivery structure has no increment assignments and none can be derived: assign all Must stories to D1 and flag for review.
