# `.brs2spec2` Business Analysis Improvement Implementation Plan

## Objective

Refactor the `.brs2spec2` business-analysis phase so that:

- the canonical artifact spine follows the AI Unified Process structure
- the existing framework support artifacts are retained where valuable
- architecture can start after a minimum business-analysis baseline
- planning, readiness, and handoff consume the new artifact model coherently

## Guiding target

Target business-analysis outputs:

- `business-analysis/requirements.md`
- `business-analysis/entity_model.md`
- `business-analysis/use_cases.puml`
- `business-analysis/use_cases/UC-*.md`
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`
- `business-analysis/process-flows.md`
- `business-analysis/gaps-and-questions.md`

## Current framework areas affected

Primary `.brs2spec2` files that will need updates:

- `.brs2spec2/workflow/workflow-definition.yaml`
- `.brs2spec2/workflow/artifact-ownership.md`
- `.brs2spec2/workflow/event-templates/EVT-TPL-003-create-business-rules.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-004-create-actors-and-personas.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-005-find-gaps-and-questions.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-006-create-process-flows.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml`
- `.brs2spec2/workflow/event-templates/EVT-TPL-030-create-entity-model.yaml`

New files likely required:

- new event template for requirements catalog
- new event template for use-case diagram
- revised artifact templates for `requirements.md`, `entity_model.md`, `use_cases.puml`
- new folder-style artifact convention for `business-analysis/use_cases/UC-*.md`

Downstream consumers that will need follow-up updates:

- planning prompts and event templates
- readiness prompts and event templates
- quality-gate prompts and event templates
- handoff prompts and event templates
- review-package prompt and template

## Recommended implementation sequence

### Phase 1 — Lock the target design

Goal:

- confirm the target artifact set and overlap model before editing `.brs2spec2`

Tasks:

1. Treat the parent-folder documents as the reference design:
   - `artifact-map.md`
   - `proposed-stage-design.md`
   - `prompt-adoption-strategy.md`
2. Confirm naming decisions:
   - `entity_model.md` versus `entity-model.md`
   - `use_cases/` folder shape
   - whether `requirements.md` lives in `business-analysis/`
3. Confirm that `business-intake-summary.md` remains as intake, not the canonical downstream requirements artifact.

Done when:

- one target artifact model is agreed and stable enough for framework edits

### Phase 2 — Add canonical business-analysis artifacts

Goal:

- introduce the AIUP-style artifact spine into `.brs2spec2`

Tasks:

1. Create a new skill/prompt for `business-analysis/requirements.md` using the draft in:
   - `../prompts/01-create-requirements.md`
2. Create a new event template for requirements catalog generation.
3. Create or revise the entity-model prompt/template based on:
   - `../prompts/02-create-entity-model.md`
4. Create a new skill/prompt and event template for:
   - `business-analysis/use_cases.puml`
   using `../prompts/03-create-use-case-diagram.md`
5. Replace monolithic `business-analysis/use-case-spec.md` generation with:
   - `business-analysis/use_cases/UC-*.md`
   using `../prompts/04-create-use-case-spec.md`

Done when:

- the framework can produce the canonical analysis spine as first-class outputs

### Phase 3 — Refactor support artifacts around the new spine

Goal:

- make existing framework-native artifacts consume the new canonical artifacts

Tasks:

1. Refactor business-rules generation to use `requirements.md` as the primary source.
2. Refactor actors-and-personas generation to use:
   - `requirements.md`
   - `use_cases.puml`
3. Refactor process-flows generation to use:
   - `use_cases/UC-*.md`
   - `actors-and-personas.md`
   instead of being primarily raw-BRS-derived.
4. Refactor gaps-and-questions to read not only intake/BRS but also:
   - `requirements.md`
   - `entity_model.md`
   - `use_cases/UC-*.md`
   - architecture findings where available

Done when:

- support artifacts reinforce the new analysis spine instead of bypassing it

### Phase 4 — Redesign stage graph and dependencies

Goal:

- encode the new overlap model in workflow definition and event dependencies

Tasks:

1. Update `workflow-definition.yaml` so:
   - `requirements.md` is generated before the rest of core analysis
   - architecture can start after a minimum business-analysis baseline
   - use-case specs no longer depend on process flows as a hard prerequisite
2. Introduce the overlap logic:
   - intake
   - requirements
   - initial gaps
   - early architecture starts
   - other analysis artifacts refine in parallel
3. Move entity model from "optional side artifact only" toward a first-class artifact, at least for data-relevant initiatives.
4. Rework `blocked_by_stage` and `blocked_by_event` chains for EVT-TPL-003..007 and EVT-TPL-030.

Done when:

- the stage graph reflects the target overlap model rather than the current quasi-linear business-analysis sequence

### Phase 5 — Update artifact ownership and templates

Goal:

- make ownership and artifact contracts match the new artifact set

Tasks:

1. Update `artifact-ownership.md` for:
   - `business-analysis/requirements.md`
   - `business-analysis/use_cases.puml`
   - `business-analysis/use_cases/*`
2. Remove or deprecate ownership entry for:
   - `business-analysis/use-case-spec.md`
3. Add or revise artifact templates for the canonical artifacts.
4. Decide and standardize filename conventions:
   - underscore vs hyphen
   - singular file vs folder outputs

Done when:

- the framework metadata matches the target artifact model

### Phase 6 — Update downstream consumers

Goal:

- make later phases read the new artifacts first

Tasks:

1. Planning:
   - update delivery-structure logic to consume `requirements.md` and `use_cases/UC-*.md`
2. Traceability:
   - update matrix logic to trace from requirements and UCs
3. Architecture:
   - confirm architecture review consumes the minimum business-analysis baseline and can feed back findings
4. Quality gates:
   - update BDD, test strategy, data contract, API contract, security review as needed
5. Handoff:
   - update handoff prompts to read `use_cases/UC-*.md` rather than monolithic `use-case-spec.md`
6. Review package:
   - update references from `use-case-spec.md` to `use_cases/*`

Done when:

- downstream phases treat the new analysis spine as the authoritative input

### Phase 7 — Migration and compatibility strategy

Goal:

- decide how old and new initiatives coexist during rollout

Tasks:

1. Define whether migration is:
   - immediate cutover
   - dual-read compatibility
   - transitional support for both old and new artifacts
2. Decide whether `use-case-spec.md` is:
   - removed
   - deprecated
   - temporarily synthesized from `use_cases/*`
3. Decide whether `entity-model.md` and `entity_model.md` need compatibility handling.
4. Add migration notes for existing initiatives.

Done when:

- the framework can be changed without creating ambiguity for existing workspaces

### Phase 8 — Validation pass

Goal:

- test the redesigned business-analysis flow end to end

Tasks:

1. Use one representative initiative to test:
   - intake
   - requirements
   - use-case diagram
   - UC files
   - business rules
   - actors
   - process flows
   - gaps
2. Check architecture starts at the intended point.
3. Check planning consumes the new outputs correctly.
4. Check handoff no longer depends on the monolithic `use-case-spec.md`.

Done when:

- the redesigned flow works on a realistic initiative without manual patching

## Recommended execution order

If doing the real work in sequence, use this order:

1. Lock design decisions
2. Add `requirements.md`
3. Add `use_cases.puml`
4. Change `use-case-spec.md` to `use_cases/UC-*.md`
5. Rework `entity_model.md`
6. Refactor support artifacts
7. Redesign stage graph
8. Update downstream consumers
9. Validate end to end

## Risks to manage

- downstream prompts still expecting `business-analysis/use-case-spec.md`
- filename inconsistency between `entity-model.md` and `entity_model.md`
- introducing too many changes at once without a compatibility strategy
- architecture overlap logic becoming unclear unless explicitly encoded in workflow definition
- planning prompts continuing to use intake-summary as the de facto requirements source

## Recommended success criteria

The improvement is successful when:

- `.brs2spec2` produces the AIUP-style canonical analysis spine
- support artifacts remain useful and do not duplicate the canonical spine
- architecture can start after a minimum business-analysis baseline
- planning reads requirements plus UC artifacts first
- handoff and quality gates no longer depend on the old monolithic use-case-spec artifact
