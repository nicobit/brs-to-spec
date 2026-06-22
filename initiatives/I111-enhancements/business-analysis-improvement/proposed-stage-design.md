# Proposed Business Analysis Stage Design For `.brs2spec2`

## Objective

Redesign the business-analysis phase so it follows an AIUP-style artifact spine while preserving the framework's stronger governance and support artifacts.

## Target Production Order

This should not be treated as a hard waterfall.

The recommended model is:

- early business analysis to establish the business and behavioral baseline
- early architecture starting before business analysis is fully complete
- a refinement loop between architecture and business analysis
- planning only after both are sufficiently mature

### Stage 2 — Business Intake

1. `business-intake/business-intake-summary.md`

Reason:

- Keeps the current PO-readable normalization layer
- Provides source inventory, scope, and early gaps
- Remains useful for business review before deeper analysis starts

### Stage 2b — Core Analysis Spine

2. `business-analysis/requirements.md`

Reason:

- This becomes the canonical analysis entry point
- Everything else in the AIUP-inspired model derives from this artifact

3. In parallel after `requirements.md`:

- `business-analysis/entity-model.md`
- `business-analysis/use-cases.puml`
- `business-analysis/business-rules.md`
- `business-analysis/gaps-and-questions.md`

Reason:

- These artifacts all benefit from a normalized requirements catalog
- They do not all need to wait on each other
- This produces fast convergence on the core analysis picture

4. After `use-cases.puml`:

- `business-analysis/actors-and-personas.md`

Reason:

- Actor extraction should align to the use-case map, not run independently from it
- This reduces actor drift and keeps `ACT-NNN` IDs closer to behavioral usage

5. After `requirements.md` and `use-cases.puml`:

- `business-analysis/use-cases/UC-*.md`

Reason:

- AIUP treats the diagram and requirements as the direct precursors to detailed use-case specs
- One-file-per-UC should be preserved

6. After `use-cases/UC-*.md` and `actors-and-personas.md`:

- `business-analysis/process-flows.md`

Reason:

- Process flows should be synthesized from stable use cases and actors
- They should show cross-use-case and end-to-end journeys, not compete with UC specs

## What Must Exist Before Architecture Starts

Architecture should not wait for the full business-analysis package.

Recommended minimum inputs before architecture review begins:

- `business-intake/business-intake-summary.md`
- `business-analysis/requirements.md`
- `business-analysis/gaps-and-questions.md` in an early draft state
- optionally `business-analysis/use-cases.puml` if it is quick to produce

Why this is enough:

- The architecture team can already see the initiative scope, actors, main required behaviors, constraints, and open risks.
- Integration-heavy or brownfield initiatives often need architecture input early to surface existing-system boundaries, external-system dependencies, and platform constraints that are not explicit in business artifacts.

## What Can Be Completed After Architecture Has Started

These artifacts do not need to be final before architecture begins:

- `business-analysis/entity-model.md`
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`
- `business-analysis/use-cases/UC-*.md`
- `business-analysis/process-flows.md`

These should instead be refined with architecture feedback where useful.

Examples:

- architecture may identify external systems or contracts that should be added to `actors-and-personas.md`
- architecture may reveal missing integration rules that should be reflected in `business-rules.md`
- architecture may expose new exception paths or boundary conditions that should be added to `UC-*.md`
- architecture may highlight data ownership and persistence concerns that improve `entity-model.md`

## Recommended Overlap Model

The target flow should be:

1. `business-intake/business-intake-summary.md`
2. `business-analysis/requirements.md`
3. `business-analysis/gaps-and-questions.md` initial draft
4. early architecture review starts
5. in parallel:
   - `entity-model.md`
   - `use-cases.puml`
   - `business-rules.md`
   - `actors-and-personas.md`
6. architecture feedback loop into business-analysis artifacts
7. `use-cases/UC-*.md`
8. `process-flows.md`
9. delivery structure and planning

This means architecture is neither first nor last.
It starts after the business problem is clear enough, and before analysis has been elaborated to the final level of detail.

## Recommended Dependency Graph

```text
business-intake-summary.md
  -> requirements.md

requirements.md
  -> entity-model.md
  -> use-cases.puml
  -> business-rules.md
  -> gaps-and-questions.md

use-cases.puml
  -> actors-and-personas.md
  -> use-cases/UC-*.md

business-rules.md
  -> use-cases/UC-*.md (enrichment)
  -> process-flows.md (decision references)

actors-and-personas.md
  -> process-flows.md

use-cases/UC-*.md
  -> process-flows.md
  -> delivery-structure.md
  -> bdd/*
  -> test-strategy.md
  -> handoff artifacts

gaps-and-questions.md
  -> open decisions
  -> readiness blocking
  -> planning confidence
```

## Architecture Entry Point

Architecture should begin after the minimum business-analysis baseline exists, not after the entire business-analysis phase is finalized.

Recommended architecture entry artifacts:

- `business-intake/business-intake-summary.md`
- `business-analysis/requirements.md`
- `business-analysis/gaps-and-questions.md`

Recommended architecture outputs that should feed back into business analysis:

- integration candidates and external system boundaries
- brownfield constraints and existing-system impacts
- technical or compliance constraints that should be represented as business constraints or open decisions
- architectural assumptions that require clarification in use cases or rules

## Recommended Blocking Behavior

### Hard blockers

These should block downstream work if missing or materially weak:

- `business-intake/business-intake-summary.md`
- `business-analysis/requirements.md`
- `business-analysis/use-cases.puml`
- `business-analysis/use-cases/UC-*.md`

Why:

- These four define the minimum coherent analysis contract
- Without them, planning and testable handoff generation become much weaker

### Conditional blockers

These should block only when the initiative characteristics make them critical:

- `business-analysis/entity-model.md`
  Block data-contract and data-heavy architecture work when the initiative has meaningful domain data.

- `business-analysis/business-rules.md`
  Block validation-heavy, policy-heavy, or compliance-heavy downstream work when missing.

- `business-analysis/gaps-and-questions.md`
  Block planning and readiness only when blocking gaps exist.

### Informing but non-blocking artifacts

- `business-analysis/actors-and-personas.md`
- `business-analysis/process-flows.md`

These should normally inform and enrich, but not stop all progress unless the initiative is actor-complex or process-centric.

## Downstream Consumption Model

### Planning

Primary readers:

- `requirements.md`
- `use-cases/UC-*.md`
- `architecture/architecture-review.md`

Secondary readers:

- `gaps-and-questions.md`
- `business-rules.md`
- `use-cases.puml`

### Architecture

Primary readers:

- `requirements.md`
- `gaps-and-questions.md`
- `business-intake/business-intake-summary.md`

Secondary readers:

- `entity-model.md`
- `process-flows.md`
- `business-rules.md`
- `use-cases/UC-*.md`

### Readiness and quality gates

Primary readers:

- `use-cases/UC-*.md`
- `entity-model.md`
- `business-rules.md`
- `gaps-and-questions.md`

### Handoff

Primary readers:

- `use-cases/UC-*.md`
- `requirements.md`
- `business-rules.md`

Secondary readers:

- `entity-model.md`
- `process-flows.md`
- `actors-and-personas.md`

## Main Changes Compared With Current `.brs2spec2`

1. `requirements.md` becomes explicit and canonical.
2. `entity-model.md` moves from optional side path to a first-class business-analysis artifact, at least for data-relevant initiatives.
3. `use-case-spec.md` changes from one monolithic file to `use-cases/UC-*.md`.
4. `use-cases.puml` is added as a first-class diagram artifact.
5. `process-flows.md` shifts from upstream generator to downstream synthesis artifact.
6. `actors-and-personas.md` is aligned to the use-case diagram rather than extracted independently from raw BRS alone.
7. architecture starts earlier, after a minimum business-analysis baseline, and feeds back into the refinement of analysis artifacts before planning.

## Suggested Minimal Event Set

If the business-analysis phase is redesigned, the minimum event set should look like this:

1. `CREATE_BUSINESS_INTAKE_SUMMARY`
2. `CREATE_REQUIREMENTS_CATALOG`
3. `CREATE_ENTITY_MODEL`
4. `CREATE_USE_CASE_DIAGRAM`
5. `CREATE_BUSINESS_RULES`
6. `FIND_GAPS_AND_QUESTIONS`
7. `CREATE_ACTORS_AND_PERSONAS`
8. `CREATE_USE_CASE_SPECS`
9. `CREATE_PROCESS_FLOWS`

This keeps the phase understandable while preserving room for later conditional logic.
