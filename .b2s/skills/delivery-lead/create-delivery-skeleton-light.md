# Skill - Create Delivery Skeleton (Light)

## Identity

```text
skill_id:    delivery-lead.create-delivery-skeleton-light
persona:     delivery-lead
action_id:   create-delivery-skeleton
produces:    planning/delivery-skeleton.md
```

## When this skill is used

Run after architecture rules are created. This skill produces a high-level delivery hierarchy — epics and features only. Stories are NOT produced at this stage; they come later during epic elaboration.

## Role for this task

You are a senior delivery lead defining the shape of the delivery. At this stage you decide how many epics and features exist, what each covers, and how they depend on each other. You do NOT define stories, story IDs, or story counts.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If a required input is missing, stop and report the blocker.

## Hard constraints

- Do NOT create stories, story IDs, or story counts — only epics and features
- Every requirement (FR/REQ) from `atomic-requirements.md` must appear in the Requirement Coverage table mapped to a feature
- Every feature must cover at least one requirement
- Epic dependencies must be explicit (which epic depends on which)
- Risk levels must be derived from the architecture review, not invented
- Keep the file compact — no multi-paragraph descriptions

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Count and list ALL requirements

Count total requirements in `atomic-requirements.md`. List every requirement ID (FR-NNN, REQ-NNN, NFR-NNN) before proceeding. You will need this list in Step 5 — do NOT skip any.

**Write down the count:** "Total requirements: N. IDs: FR-001, FR-002, ..., FR-NNN."

This count determines the minimum scope — EVERY requirement must be covered by at least one feature. The validator will check this. If you cover less than 90%, validation will fail.

### Step 2b - Identify application layers

Before defining epics, determine what application layers this initiative requires. Check the BRS and architecture review for:

- **Frontend / UI** — does the initiative include user-facing screens, portals, dashboards? (e.g., applicant portal, underwriter dashboard, admin panel)
- **Backend / API** — does it include services, APIs, business logic?
- **Infrastructure / Deployment** — does it require new infrastructure setup, CI/CD, environments?
- **Integrations** — does it call external APIs or receive events from external systems?

Document the layers in the skeleton under a `## Application Layers` section:

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes / No | {{portal, dashboard, etc.}} | {{framework, hosting}} |
| Backend API | Yes / No | {{services}} | {{tech stack}} |
| Infrastructure | Yes / No | {{CI/CD, environments}} | {{cloud provider}} |
| Integrations | Yes / No | {{external APIs}} | {{providers}} |

Each layer that is present MUST be covered by at least one epic or feature. Do NOT collapse frontend into backend API stories — a form submission is NOT the same as a POST endpoint.

### Step 2c - Incorporate solution decisions (when available)

If `architecture/solution-decisions.md` exists in `{resolved_optional_inputs}`:

1. Read the Repository Summary table — it lists every repository (new and existing) and the decisions targeting each.
2. Note which requirements are linked to `create-new` decisions. Ensure those requirements are assigned to an epic — do not leave new-component decisions orphaned.
3. Flag any epic that will need infrastructure or scaffolding stories during elaboration (because it contains requirements linked to `create-new` decisions).
4. Do NOT assign repositories at the epic level — repository assignment happens at the story level during epic elaboration, since a single story can touch multiple repositories.

If `architecture/solution-decisions.md` does NOT exist, skip this step.

### Step 3 - Define epics

Group related requirements into epics. Each epic should represent a major business capability or delivery milestone.

Rules:
- Epics must be meaningful business outcomes, not technical layers
- However, if the initiative has a frontend layer, ensure there are epics or features that cover the UI/UX (forms, screens, navigation, error states) — not just the backend APIs they call
- If the initiative requires infrastructure setup (project scaffolding, CI/CD, deployment), include a foundation epic or feature for it
- Each epic has: ID (E-001, E-002, ...), title, one-line objective, priority, risk level
- Identify inter-epic dependencies (e.g. "E-003 depends on E-001 for applicant data")
- Derive risk from the architecture review (integration complexity, regulatory exposure, unknowns)
- Every requirement must belong to at least one epic — do not leave orphan requirements

### Step 4 - Define features per epic

Each feature is a coherent sub-capability within an epic. Assign IDs F-001, F-002, etc., sequential across the whole artifact.

For each feature:
- Title (business capability name, not technical component)
- Which requirements (FR/REQ) it covers — list every FR/REQ explicitly
- Priority (Must/Should/Could)

**Cross-check:** after defining all features, verify that every requirement from Step 2 appears in at least one feature's "Requirements Covered" column. If any are missing, add features or expand existing features to cover them.

### Step 5 - Build coverage table

Keep inferred requirement visibility explicit in this table. Add a `Basis`
column for every row:

- `direct` when the requirement is a direct source requirement from the atomic catalog
- `inferred` when the requirement is an inferred decomposition child

Do not hide inferred requirements inside a generic covered row. Their inferred
status must remain visible in the coverage table so downstream planning and
epic/story generation do not treat them as original source requirements.

Create the Requirement Coverage table. Take the complete list from Step 2 and map EVERY ID to a feature and epic. Do NOT truncate this table — it must contain exactly as many rows as there are requirements.

Mark any genuinely uncovered requirements as **Not Covered** with a note — but this should be rare. If more than 10% are Not Covered, go back to Step 4 and add features.

### Step 6 - Build epic dependency summary

Create the Epic Dependency Summary table showing which epics depend on which and their risk levels.

## Output requirements

Write `planning/delivery-skeleton.md` using `.b2s/artifact-templates/delivery-skeleton-light.md`.

## Done criteria

- [ ] Every requirement from atomic-requirements.md appears in the coverage table
- [ ] Every requirement maps to at least one feature
- [ ] Every coverage row includes a correct `Basis` value (`direct` or `inferred`)
- [ ] Every feature belongs to an epic
- [ ] Epic dependencies are documented
- [ ] Risk levels are derived from architecture review
- [ ] No story IDs, story counts, or story detail included
- [ ] If solution decisions exist, no `create-new` decision is left without an owning epic
- [ ] File is compact
- [ ] No placeholder text remains

## Stop conditions

- If any required input is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
