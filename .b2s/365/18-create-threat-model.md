# Prompt 18 - Create Threat Model

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/quality-gates/security-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/threat-model.md`

Optional:

- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/input/architecture.md`

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/threat-model.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-threat-model`.

Run this when the security review indicates significant trust boundaries or
attack surface justify a structured threat model.

Read all provided inputs in full before writing anything.

Identify trust boundaries and assess all six STRIDE categories for each.
Document each threat with:

- `THR-NNN`
- DREAD score
- risk level
- mitigation
- owner
- status

Write `quality-gates/threat-model.md` using the provided template.

Before finalizing, ensure every trust boundary is assessed across STRIDE and all
accepted threats are explicit. Status must be `In progress`.
