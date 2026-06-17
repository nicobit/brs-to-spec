# Step 0 — Lock Design Decisions

## Purpose

Lock all target artifact names, paths, naming conventions, and compatibility choices before editing any `.brs2spec2` file. Nothing in the framework should change until this step produces a signed-off decision record.

## Run this prompt

```text
Review the business-analysis improvement package and produce a locked design decision record.

Read these design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md
- framework_enhancement/business-analysis-improvement/prompt-adoption-strategy.md
- framework_enhancement/business-analysis-improvement/prompts/README.md

Read these current framework files:
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/artifact-ownership.md
- .brs2spec2/workflow/event-templates/EVT-TPL-003-create-business-rules.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-004-create-actors-and-personas.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-005-find-gaps-and-questions.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-006-create-process-flows.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-030-create-entity-model.yaml
- .brs2spec2/artifact-templates/entity-model.md
- .brs2spec2/artifact-templates/use-case-spec.md

Produce a file at:
  framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

That file must record the following decisions explicitly:

1. Naming convention
   - Confirm all artifact names use hyphens (no underscores).
   - The AIUP reference used entity_model.md and use_cases.puml — these are NOT adopted.
   - Framework names: entity-model.md, use-cases.puml, use-cases/UC-NNN.md.

2. New canonical artifacts
   - Confirm the full path for each new artifact:
     - business-analysis/requirements.md
     - business-analysis/use-cases.puml
     - business-analysis/use-cases/UC-NNN.md
   - Confirm entity-model.md retains its existing path.

3. Deprecated artifacts
   - business-analysis/use-case-spec.md is deprecated.
   - State whether existing initiatives keep it as-is or receive a migration note.

4. Compatibility strategy
   - Decide: immediate cutover vs transitional dual-read.
   - If dual-read: define which downstream consumers must handle both old and new paths temporarily.
   - If cutover: confirm all downstream references will be updated in Step 7.

5. Architecture overlap
   - Confirm that architecture may start after:
     - business-intake/business-intake-summary.md
     - business-analysis/requirements.md
     - business-analysis/gaps-and-questions.md (draft)
   - Confirm this will be encoded in workflow-definition.yaml in Step 3.

6. Entity model classification
   - Confirm entity-model.md is promoted to first-class artifact for data-relevant initiatives.
   - Confirm it remains conditional (not hard-blocking) for non-data initiatives.

7. Process-flows position
   - Confirm process-flows.md moves from upstream generator to downstream synthesis artifact.
   - Confirm its new required inputs: use-cases/UC-*.md and actors-and-personas.md.

Do not edit any .brs2spec2 files. Only produce the decision record.
```

## Done when

- `framework_enhancement/business-analysis-improvement/plan2/00-decisions.md` exists
- All 7 decision areas above are recorded with explicit choices
- No `.brs2spec2` file has been modified

## MANUAL GATE — do not proceed to Step 1 without this

After `00-decisions.md` is produced, **you must review it yourself** before running Step 1.

Check that:
- The naming convention section explicitly confirms hyphen naming and rejects underscores
- The compatibility strategy is one of: "immediate cutover" or "transitional dual-read" — not left open
- The architecture overlap entry point lists exactly the three artifacts confirmed in the plan
- The entity model ownership decision is recorded (product-owner or architect — not left blank)

Only start Step 1 after you are satisfied with all four checks.
