# Skill — Create Epic Packages

## Identity

```text
skill_id:    delivery-lead.create-epic-packages
persona:     delivery-lead
action_id:   create-epic-packages
produces:    planning/epics/
```

## When this skill is used

Run after `create-delivery-structure` completes. Creates one standalone epic file per epic defined in `delivery-structure.md`. Only runs when delivery mode is `OpenSpec` or `Standalone`.

## Preconditions

Before starting, verify:
- `planning/delivery-structure.md` exists and contains epic definitions
- `business-intake/business-intake-summary.md` exists
- `business-analysis/requirements.md` exists
- `architecture/architecture-review.md` exists

If a required input is missing, stop and report the blocker.

## Step 1 — Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/business-intake/business-intake-summary.md`
- `{workspace_root}/business-analysis/requirements.md`
- `{workspace_root}/architecture/architecture-review.md`

If present, also read:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/process-flows.md`

Do not start writing until all available inputs are read completely.

## Step 2 — Extract epic list

From `delivery-structure.md`, extract all epics in order. Each epic has an ID (`E-NNN`) and a name. Record the features listed under each epic.

Count epics. The number of files you create must equal this count exactly.

## Step 3 — Create one file per epic

For each epic, create `planning/epics/E-NNN-<slug>.md` where `<slug>` is a lowercase hyphenated version of the epic name.

Follow the structure in `.b2s/artifact-templates/epic-package.md` exactly. Populate every section with specific content derived from the inputs. Do not leave placeholder text.

**Business Objective:** Write 2–4 sentences explaining what business capability this epic delivers, why it matters, and the business risk of not delivering it. Derive from `business-intake-summary.md` and the BRS objectives.

**Business Capabilities Delivered:** List the specific capabilities, not generic phrases. Derive from the features under this epic.

**Scope:** Be explicit. In scope must list the concrete deliverables. Out of scope must name things a developer might assume are included but are not.

**Source Traceability:** Link to the BRS sections and FR-NNN requirements that this epic covers. Derive from `requirements.md` by matching FR-NNN to the stories under each epic's features.

**Impacted Business Processes:** Derive from `process-flows.md` if present, otherwise from `architecture-review.md`. Name real processes, not generic labels.

**Impacted Systems and Modules:** Extract from `architecture-review.md`. Name real systems (e.g. "Experian connector", "Temenos T24 adapter"), not generic labels like "backend" or "system".

**Features:** List every feature under this epic with its ID, priority, and increment from `delivery-structure.md`.

**Risks:** Derive from `architecture-review.md` open decisions, known unknowns, and blast radius entries. At least one risk per epic.

**Success Metrics:** Define measurable criteria for this epic. Derive from BRS objectives or business intake summary.

## Done criteria

- [ ] One file per epic in `delivery-structure.md`
- [ ] Every epic file has all sections from `epic-package.md` populated
- [ ] Business objective is specific (not generic)
- [ ] Impacted systems name real systems, not "backend" or "system"
- [ ] Source traceability links to real FR-NNN references
- [ ] At least one risk per epic
- [ ] Status is `Draft`
