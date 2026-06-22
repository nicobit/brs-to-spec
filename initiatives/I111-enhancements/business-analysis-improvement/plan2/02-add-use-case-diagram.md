# Step 2 — Add the Use-Case Diagram Artifact

## Purpose

Introduce two parallel outputs from the same event:

- `business-analysis/use-cases.puml` — PlantUML source, for tooling and CI rendering
- `business-analysis/use-cases.md` — Mermaid diagram embedded in markdown, for GitLab Pages and direct preview in IDEs / MR views

Both artifacts carry the same stable `UC-NNN` IDs and actor relationships. The Mermaid file is the human-readable version; the PUML file is the machine-readable version. They must stay in sync.

## Why both

The `.brs2spec2` framework already uses Mermaid embedded in markdown for all other diagram artifacts (`entity-model.md` uses `erDiagram`, `process-flows.md` uses `flowchart`). Producing only a `.puml` file would make the use-case diagram the only artifact not natively renderable in GitLab Pages or IDE markdown preview.

Mermaid does not have a native use-case diagram type. The equivalent is a `graph LR` (or `graph TD`) with actor shapes and use-case shapes connected by labeled edges. This is consistent and readable.

## Prerequisite

Step 1 must be complete. `business-analysis/requirements.md` must be wired into the workflow before this step adds a dependency on it.

## Run this prompt

```text
Implement support for business-analysis/use-cases.puml AND business-analysis/use-cases.md in .brs2spec2.
Both files are produced by the same event. They must carry the same UC-NNN IDs and actor relationships.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/prompts/03-create-use-case-diagram.md
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md

Read the current framework pattern for Mermaid-in-markdown:
- .brs2spec2/artifact-templates/entity-model.md       (uses ```mermaid erDiagram)
- .brs2spec2/artifact-templates/process-flows.md      (uses ```mermaid flowchart)

Read the current framework context:
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/artifact-ownership.md
- .brs2spec2/workflow/event-templates/EVT-TPL-043-create-requirements.yaml  (the file created in Step 1)

Make the following changes:

1. Create a new skill prompt:
   .brs2spec2/skills/product-owner/create-use-case-diagram.md
   Base the content on framework_enhancement/business-analysis-improvement/prompts/03-create-use-case-diagram.md.
   Adapt it to use initiative-local paths and framework skill prompt conventions.

   The prompt must instruct production of BOTH outputs in one pass:

   Output A — business-analysis/use-cases.puml
   PlantUML use case diagram.
   Use standard PlantUML syntax: @startuml/@enduml, left to right direction,
   actor declarations, rectangle system boundary, usecase declarations with UC-NNN aliases.

   Output B — business-analysis/use-cases.md
   Markdown file with metadata table (same format as other artifact templates) followed by
   a Mermaid diagram block using graph LR.
   Use this shape convention to match standard use-case notation:
     - Actors: person shape  actor_name([Actor Name])
     - Use cases: rounded rectangle  UC001(UC-001 Do Something)
     - Connections: actor --> UC001
   Include a UC catalog table below the diagram listing UC-NNN, title, primary actor(s), and FR sources.
   This file is the GitLab Pages / IDE-renderable version.

   Both files must use identical UC-NNN IDs and identical actor names.

2. Create an artifact template for use-cases.md:
   .brs2spec2/artifact-templates/use-cases.md
   Model the structure after entity-model.md and process-flows.md.
   Include:
   - Metadata table (Initiative ID, Created at, Created by event, Status)
   - Mermaid graph LR block with actor and UC-NNN nodes
   - UC Catalog table: UC-NNN | Title | Primary Actor(s) | FR Sources

3. Create a new event template:
   .brs2spec2/workflow/event-templates/EVT-TPL-044-create-use-case-diagram.yaml
   (EVT-TPL-043 is assigned to Step 1 — 044 is pre-assigned for this step.)
   Set:
   - type: CREATE_USE_CASE_DIAGRAM
   - persona: product-owner
   - inputs.required: business-analysis/requirements.md
   - outputs.primary: business-analysis/use-cases.puml
   - outputs.secondary: business-analysis/use-cases.md
   - on_success:
       mark both artifacts as ai_validated
       trigger CREATE_USE_CASE_SPECS and CREATE_ACTORS_AND_PERSONAS as next events
   - validation:
       file_exists: business-analysis/use-cases.puml
       file_exists: business-analysis/use-cases.md
       both contain at least one UC-NNN
       UC-NNN IDs in both files must match

4. Update .brs2spec2/workflow/workflow-definition.yaml:
   - Add CREATE_USE_CASE_DIAGRAM to stage 2b.
   - Set it as blocked_by CREATE_REQUIREMENTS_CATALOG.
   - Set CREATE_USE_CASE_SPECS and CREATE_ACTORS_AND_PERSONAS as blocked_by CREATE_USE_CASE_DIAGRAM.
   - Do not yet update CREATE_USE_CASE_SPECS event template internals — that is Step 4.

5. Update .brs2spec2/workflow/artifact-ownership.md:
   - Add business-analysis/use-cases.puml owned by product-owner.
   - Add business-analysis/use-cases.md owned by product-owner.
   - Add a note that these two artifacts are co-produced and must stay in sync.

Note on naming:
- use-cases.puml and use-cases.md both use hyphens.
- The UC-NNN IDs are the stable identifiers used by all downstream artifacts.
  Do not invent a separate ID scheme for either file.
- Mermaid graph LR is preferred over graph TD for use-case diagrams — horizontal layout
  matches the PlantUML "left to right direction" convention.
```

## Done when

- `.brs2spec2/skills/product-owner/create-use-case-diagram.md` instructs production of both `use-cases.puml` and `use-cases.md`
- `.brs2spec2/artifact-templates/use-cases.md` exists with Mermaid graph LR template
- `EVT-TPL-044-create-use-case-diagram.yaml` lists both files as outputs and validates both
- `workflow-definition.yaml` shows `CREATE_USE_CASE_DIAGRAM` blocked by `CREATE_REQUIREMENTS_CATALOG`
- `artifact-ownership.md` includes both `use-cases.puml` and `use-cases.md`
- No existing event templates broken
