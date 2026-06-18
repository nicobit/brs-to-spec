# Skill — Create Feature Packages

## Identity

```text
skill_id:    delivery-lead.create-feature-packages
persona:     delivery-lead
action_id:   create-feature-packages
produces:    planning/features/
```

## When this skill is used

Run after `create-epic-packages` completes. Creates one standalone feature file per feature defined in `delivery-structure.md`. Only runs when delivery mode is `OpenSpec` or `Standalone`.

## Preconditions

Before starting, verify:
- `planning/delivery-structure.md` exists with feature definitions
- `planning/epics/` exists with at least one epic file
- `business-analysis/requirements.md` exists
- `architecture/architecture-review.md` exists

If a required input is missing, stop and report the blocker.

## Step 1 — Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/planning/delivery-structure.md`
- All files under `{workspace_root}/planning/epics/`
- `{workspace_root}/business-analysis/requirements.md`
- `{workspace_root}/architecture/architecture-review.md`

If present, also read:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/actors-and-personas.md`
- `{workspace_root}/business-analysis/use-cases/`

Do not start writing until all available inputs are read completely.

## Step 2 — Extract feature list

From `delivery-structure.md`, extract all features in order. Each feature has an ID (`F-NNN`), a name, a parent epic ID, and a list of stories. Count features. The number of files you create must equal this count exactly.

## Step 3 — Create one file per feature

For each feature, create `planning/features/F-NNN-<slug>.md` where `<slug>` is a lowercase hyphenated version of the feature name.

Follow the structure in `.b2s/artifact-templates/feature-package.md` exactly. Populate every section with specific content derived from the inputs. Do not leave placeholder text.

**Parent Epic:** Link to the epic file in `planning/epics/`. Populate the epic name from that file.

**Feature Goal:** Write 2–3 sentences explaining what coherent business capability this feature delivers and how it relates to the parent epic. Derive from `delivery-structure.md` and the epic file.

**Business Value:** State why this feature matters to the business. What breaks or fails if this feature is not built? Derive from `business-intake-summary.md` and the FR-NNN requirements this feature covers.

**Scope:** In scope must list the stories and their specific capabilities. Out of scope must name related functionality that is explicitly not part of this feature.

**Source Traceability:** Link to every FR-NNN from `requirements.md` that at least one story in this feature covers.

**Business Rules:** Extract every BR-NNN from `business-rules.md` that constrains any story in this feature. State the impact on the feature concretely.

**Impacted Components:** Derive from `architecture-review.md`. Name real components — do not use "backend", "frontend", or "system". Every feature must name at least one specific component.

**Stories:** List every story under this feature with its ID, title, priority, and increment from `delivery-structure.md`.

**Acceptance Criteria Summary:** State what "done" looks like for this feature as a whole — not for individual stories. What must be true for the feature to ship?

**BDD Coverage Expectations:** For each story in the feature, list which scenario types are expected (happy path, negative, authorization, state transition, integration failure, audit). Derive from the story detail blocks in `delivery-structure.md` and business rules.

**Implementation Notes:** Include any architecture rule (AR-NNN) from `architecture-review.md` that applies to this feature. Include any known integration risk or brownfield constraint.

**Test Strategy Summary:** State what test types are needed, coverage target, and who signs off.

## Done criteria

- [ ] One file per feature in `delivery-structure.md`
- [ ] Every feature file links back to its parent epic
- [ ] Every feature lists all its stories with IDs
- [ ] Impacted components are named specifically (no "backend" or "system")
- [ ] BDD coverage expectations are stated per story
- [ ] At least one AR-NNN or constraint in Implementation Notes per feature
- [ ] Status is `Draft`
