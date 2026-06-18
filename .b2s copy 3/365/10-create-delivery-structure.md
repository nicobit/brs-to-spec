# Prompt 10 - Create Delivery Structure

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/routing/routing-decision.md`
- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/business-analysis/use-cases/` contents
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/delivery-structure.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/business-analysis/actors-and-personas.md`

## Output file to create

- `initiatives/<id>-<slug>/planning/delivery-structure.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-delivery-structure`.

Read all provided inputs fully before writing anything.

Use `routing/routing-decision.md` to determine:

- delivery mode
- execution mode

Apply these rules:

- `FastPath`: keep the structure deliberately minimal
- `Enterprise+Modular`: assign stories to delivery increments such as `D1`,
  `D2`, and so on

Define:

- epics with IDs `E-001`, `E-002`, and so on
- features with IDs `F-001`, `F-002`, and so on, sequential across the whole
  artifact
- user stories with IDs `F-XXX.X`

User story rules:

- every story must be independently implementable, testable, and reviewable
- use the format `As a [actor], I want [action], so that [outcome].`
- each story must have acceptance criteria, priority, and increment assignment
  where applicable
- stories should be sized for one engineer and one sprint
- do not create placeholder implementation tasks

After each feature story table, add a story detail block for every story row.

For each story detail block, record:

- actor name, using `actors-and-personas.md` if present
- linked `FR-NNN` references
- linked `BR-NNN` references when business rules exist
- primary impacted component derived from `architecture-review.md`
- one explicit out-of-scope statement

Write `planning/delivery-structure.md` using the provided template.

The artifact must contain:

- metadata with `Status: Draft`
- epic -> feature -> story hierarchy
- story count assertion
- FR coverage table with one row per `FR-NNN`

Before finalizing, verify:

- epic count reflects the major BRS capability areas
- every `FR-NNN` has its own row in the coverage table
- story count assertion matches the actual story rows
- every story has complete user story phrasing
- every story has at least one acceptance criterion reference
- every story detail block has FR links
- every story detail block has an explicit out-of-scope statement
- increment assignments are present and consistent when required
- status is `Draft`

Do not self-accept the artifact. This step creates the planning hierarchy only.
