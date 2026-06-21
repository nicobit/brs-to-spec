# Skill — Create Epic Packages

## Identity

```text
skill_id:    delivery-lead.create-epic-packages
persona:     delivery-lead
action_id:   create-epic-packages
produces:    planning/epics/
```

## When this skill is used

Run after the delivery skeleton is created. Creates one standalone epic file per epic defined in the delivery skeleton.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable. The delivery skeleton or delivery structure must contain epic definitions.

If a required input is missing, stop and report the blocker.

## Step 1 — Read all inputs

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all available inputs are read completely.

## Step 2 — Extract epic list

From the delivery skeleton (or delivery structure), extract all epics in order. Each epic has an ID (`E-NNN`) and a name. Record the features listed under each epic.

Count epics. The number of files you create must equal this count exactly.

## Step 3 — Create one file per epic

For each epic, create `planning/epics/E-NNN-<slug>.md` where `<slug>` is a lowercase hyphenated version of the epic name.

Follow the structure in `.b2s/artifact-templates/epic-package.md` exactly. Populate every section with specific content derived from the inputs. Do not leave placeholder text.

**Business Objective:** Write 2–4 sentences explaining what business capability this epic delivers, why it matters, and the business risk of not delivering it. Derive from the BRS and delivery constitution objectives.

**Business Capabilities Delivered:** List the specific capabilities, not generic phrases. Derive from the features under this epic and the capability map if available.

**Scope:** Be explicit. In scope must list the concrete deliverables. Out of scope must name things a developer might assume are included but are not.

**Source Traceability:** Link to the BRS sections and FR-NNN requirements that this epic covers. Derive from the requirements artifact by matching FR-NNN to the stories under each epic's features.

**Impacted Business Processes:** Derive from `architecture-review.md` or `architecture-impact-map.md`. Name real processes, not generic labels.

**Impacted Systems and Modules:** Extract from `architecture-review.md`. Name real systems (e.g. "Experian connector", "Temenos T24 adapter"), not generic labels like "backend" or "system".

**Features:** List every feature under this epic with its ID, priority, and increment from `delivery-structure.md`.

**Risks:** Derive from `architecture-review.md` open decisions, known unknowns, and blast radius entries. At least one risk per epic.

**Success Metrics:** Define measurable criteria for this epic. Derive from BRS objectives or business intake summary.

## Done criteria

- [ ] One file per epic in the delivery skeleton / delivery structure
- [ ] Every epic file has all sections from `epic-package.md` populated
- [ ] Business objective is specific (not generic)
- [ ] Impacted systems name real systems, not "backend" or "system"
- [ ] Source traceability links to real FR-NNN references
- [ ] At least one risk per epic
- [ ] Status is `Draft`
