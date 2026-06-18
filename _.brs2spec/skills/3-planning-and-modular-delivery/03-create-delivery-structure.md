# Prompt - Create Delivery Structure

## Role

You are a delivery architect structuring business scope into deliverable units.

## Context

This prompt is the early delivery-shaping step. It should create enough planning structure to make later architecture refinement initiative-specific. It must not create implementation tasks for the whole BRS.

## Purpose

Create an early delivery structure connecting objectives, epics, features, user stories, candidate increments, and the known high-level architecture context.

## Inputs

Required:
- `input/brs.md` or `input/brs/*.md` — functional requirements (FR-NNN) and acceptance criteria (AC-NNN)
- `business-intake/business-intake-summary.md` — objectives, scope, requirements summary

Required before confirmed stage (must exist before stories can be confirmed — stubs or draft epics are fine without them):
- `business-intake/business-rules.md` — BR-NNN rules; confirmed stories must reference the rules that constrain them
- `business-analysis/actors-and-personas.md` — ACT-NNN IDs; confirmed story actors must use these IDs, not free-text role names

Optional:
- `input/architecture.md` or `input/architecture/*.md` — system components and integration context

## Output structure

The delivery structure is a **folder**, not a single file:

```
planning/delivery-structure/
  overview.md                              ← initiative scope, governed boundaries, slices, traceability rules
  E-NNN-<epic-slug>/
    epic.md                                ← epic description, objectives, source FRs, candidate modules
    F-NNN.N-<feature-slug>.md              ← feature description + all its user stories
    F-NNN.N-<feature-slug>.md
  E-NNN-<epic-slug>/
    epic.md
    F-NNN.N-<feature-slug>.md
```

**Output rules:**
- Always write the full folder structure. Never produce a single flat `planning/delivery-structure.md` file.
- If `planning/delivery-structure/` already exists, overwrite each file completely — never append.
- If a legacy flat `planning/delivery-structure.md` file exists, ignore it. The folder is authoritative.
- Epic folder names: `E-NNN-<kebab-case-epic-title>` (e.g. `E-001-loan-application-intake`)
- Feature file names: `F-NNN.N-<kebab-case-feature-name>.md` (e.g. `F-001.1-application-submission-form.md`)

## Templates

Use these templates:

```text
.brs2spec/templates/planning-and-modular-delivery/delivery-structure-overview.md   → planning/delivery-structure/overview.md
.brs2spec/templates/planning-and-modular-delivery/delivery-structure-epic.md       → planning/delivery-structure/E-NNN-<slug>/epic.md
.brs2spec/templates/planning-and-modular-delivery/delivery-structure-feature.md    → planning/delivery-structure/E-NNN-<slug>/F-NNN.N-<slug>.md
```

Keep each file structurally rich but text-light. Use tables and short rules rather than long narrative sections.
Use the initial architecture input as high-level solution context when it exists; do not wait for later architecture refinement to shape the first delivery view.
Add an optional compact slice/dependency view in `overview.md` only when it materially improves planning or review clarity.

## Story hierarchy rule

Every feature must have at least one well-formed user story.

If a feature has only one story, the artifact must include a one-line justification for why further splitting is not useful or not yet needed (e.g. "single atomic capability — no meaningful split available at this stage"). Do not force artificial stories.

Derive multiple stories per feature where the scope warrants it by asking:

- Are there different personas who interact with this feature differently?
- Are there distinct scenarios — happy path, failure path, edge case — that represent separate deliverable behaviors?
- Are there different entry points, states, or contexts that a user experiences separately?
- Is there a support or admin view that is distinct from the customer-facing view?

A feature covering a complex capability may have three or more stories. A feature covering a single atomic action may legitimately have one.

Do not write stories that merely restate the feature name with "As a user, I want to..." wrapper text. Each story must represent a distinct, independently testable behavior.

**Draft vs confirmed:**
- **Draft stage** (before architecture review): epics and features are the primary output. User stories may be stubs. `F-XXX.X` IDs are optional but recommended.
- **Confirmed stage** (after readiness = Ready): all stories must be fully formed. Every story MUST have:
  - An `F-XXX.X` ID (assign sequentially if not yet present)
  - An actor reference using the `ACT-NNN` ID from `business-analysis/actors-and-personas.md` — free-text role names are not accepted at confirmed stage
  - A verbatim "As a `ACT-NNN <persona>`, I want `<capability>`, so that `<business value>`." statement
  - At least one `AC-NNN` acceptance criterion reference pointing to a specific row in `input/brs.md`; the AC text must be copied verbatim from the BRS — do not paraphrase or summarise. A testable statement describes an observable outcome: a specific value, a named state, a measurable SLA, or a named failure mode. "The system works correctly" or "the feature behaves as expected" are not acceptance criteria.
  - **AC coverage rule:** a story covering a complex or regulated capability (compliance, security, SLA, external integration, error handling) must have at least three `AC-NNN` entries. A story covering a single atomic UI action may have one. When in doubt, read every sentence in the corresponding FR section of `input/brs.md` — each testable sentence is a candidate AC. Do not stop at one AC unless the FR has only one testable statement.
  - A `FR-NNN` requirement ID
  - At least one `BR-NNN` link from `business-intake/business-rules.md` — or an explicit inline note: `Business rules: none apply — [reason]`
  - A story that lacks any of these is still a stub — expand it before marking delivery-structure as confirmed.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- define Epic / Feature / User Story structure early enough to guide later architecture review and downstream handoff
- produce at least one well-formed user story per feature; features with one story must include a justification for why splitting is not needed
- write stories that represent distinct, independently testable behaviors — not restatements of the feature name
- derive stories from different personas, scenarios, failure paths, and edge cases present in the BRS
- use classic Agile user story wording: `As a <persona>, I want <capability>, so that <business value>.`
- make clear that stories are planning parents and tasks are engineering children
- surface existing-system impact where it affects slicing, validation, compatibility, or rollout
- make governed service/API, data, and event boundaries explicit where they exist
- mark conflicts instead of resolving them silently
- assign owners for gaps and decisions
- avoid creating low-level implementation tasks
- avoid repeating acceptance detail or architecture rationale that belongs in source artifacts
- avoid over-explaining candidate modules or slices when a concise summary is enough
- avoid pretending initiative-specific architecture refinement is already complete at this stage
- keep any optional visual as orientation support, not as a second planning artifact

## Anti-patterns to avoid

Do not produce outputs that:

- have a feature with one story and no justification for why splitting is not needed
- write stories that restate the feature name with a user story wrapper
- write stories only for the happy path — failure paths, retry flows, and support views are stories too
- invent architecture not present in the inputs
- slice work only by technical layer
- leave user stories until the later planning projection step
- create tasks for all future deliverables
- ignore impacted components or regression-sensitive behaviors when the initiative changes an existing system
- hide governed boundary changes inside generic capability names
- ignore architecture conflicts
- produce a table without evidence or owner

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.
- If `business-intake/business-rules.md` is missing and stories are being confirmed (not just drafted at epics/features level): stop. Business rules must be extracted before stories can be confirmed. Run `skills/2-business-intake/02-extract-business-rules.md` first.
- If `business-analysis/actors-and-personas.md` is missing and stories are being confirmed: stop. Actors must be extracted before stories can be confirmed. Run `skills/2-business-intake/03-extract-actors-and-personas.md` first.

## Self-review checklist

Before finalizing, verify:

- [ ] Architecture constraints are referenced.
- [ ] Business requirements remain traceable.
- [ ] Epic / Feature / User Story structure is defined and traceable.
- [ ] Every feature has at least one well-formed user story — features with only one story include a justification for why splitting is not needed.
- [ ] Each story represents a distinct, independently testable behavior — not a restatement of the feature name.
- [ ] Stories cover multiple personas, failure paths, and edge cases where the BRS implies them.
- [ ] User stories use `As a <persona>, I want <capability>, so that <business value>.`
- [ ] **Confirmed stage only:** every story has an `F-XXX.X` ID, a FR-NNN reference, and AC-NNN references. Stories missing any of these are stubs — do not mark delivery-structure as confirmed.
- [ ] **Confirmed stage only:** AC text is copied verbatim from `input/brs.md` — not paraphrased. Stories for complex/regulated/SLA/integration capabilities have at least three ACs. Stories with only one AC: verified the corresponding FR section has only one testable statement.
- [ ] **Confirmed stage only:** every story actor uses an `ACT-NNN` ID from `business-analysis/actors-and-personas.md` — free-text role names are not accepted at confirmed stage.
- [ ] **Confirmed stage only:** every story has at least one `BR-NNN` link from `business-intake/business-rules.md`, or an explicit `Business rules: none apply — [reason]` note. Stories with no BR link and no explicit note are stubs.
- [ ] **Confirmed stage only:** every `AC-NNN` acceptance criterion describes an observable, testable outcome — not "the system handles X correctly" or similar vague language.
- [ ] Story entries point to acceptance / validation references.
- [ ] Existing-system impact is visible where it changes slicing or validation expectations.
- [ ] Governed service/API, data, and event boundaries are visible where relevant.
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] The output gives later architecture review a concrete initiative shape to assess.
- [ ] The artifact is specific enough for readiness and handoff shaping, not just structurally complete.
