# Migration — 0.0.7 → 0.0.8

0.0.8 keeps the simplified, architecture-aware core of 0.0.6/0.0.7 and adds
explicit execution modes, a standalone path, and Conditional Quality Gates.

## Renames (paths)

| 0.0.7 | 0.0.8 |
|---|---|
| `prompts/5-handoff-to-openspec/` | `prompts/5-handoff/` |
| `prompts/4-engineering-readiness/advanced/` | `prompts/4-engineering-readiness/quality-gates/` |
| `prompts/4-engineering-readiness/02-identify-required-advanced-contracts.md` | `.../02-identify-required-quality-gates.md` |
| `templates/advanced-governance/` | `templates/quality-gates/` |
| `docs/05-openspec-handoff.md` | `docs/05-handoff.md` |
| `docs/06-advanced-governance.md` | `docs/06-conditional-quality-gates.md` |
| `examples/enterprise-modular-path/advanced-governance/` | `examples/enterprise-modular-path/quality-gates/` |

History is preserved (the moves were done with `git mv`).

## Concept changes

- **"Optional advanced governance" → "Conditional Quality Gates".** Gates are not
  always required, but when **triggered** by the readiness check they are
  **mandatory**. The readiness check now contains a
  `Quality Gate | Triggered? | Required? | Reason | Owner | Output` table.
- **Execution modes are now explicit:** Mode A — OpenSpec (default), Mode B —
  Standalone, Mode C — Business Copilot. Delivery mode and execution mode are
  orthogonal. (Mode A/B recovers the lost 0.0.5 handoff/standalone concept.)
- **Routing** (`prompts/1-routing/01-select-delivery-mode.md`) now selects both a
  delivery mode and an execution mode.

## New files

- `prompts/5-handoff/03-create-standalone-delivery-package.md`
- `templates/standalone-delivery/{delivery-spec,implementation-plan,tasks,validation-plan,review-checklist}.md`
- `docs/08-execution-modes.md`
- `docs/09-migration-0.0.7-to-0.0.8.md`
- `docs/branch-analysis.md`
- `.github/workflows/validate.yml` (runs the validation scripts; remove if you
  prefer no CI, as 0.0.6/0.0.7 had none)

## Script changes

- `tools/scripts/new_feature.py` now takes
  `--mode fast|standard|enterprise|enterprise-modular` and
  `--execution-mode openspec|standalone`, and scaffolds the matching output tree
  (`openspec/changes/...` or `standalone-delivery/...`).
- `tools/scripts/check_program.py` checks input-prep prompts, architecture review
  + traceability prompts, OpenSpec + standalone handoff prompts, all conditional
  quality gates, the business Copilot prompt, and key templates.
- `tools/scripts/check_prompt_sequence.py` uses `5-handoff` and requires both
  execution-mode handoff prompts.

## What did NOT change

- The macro prompt structure (`0`…`6`).
- Normalized inputs (`input/brs.md`, `input/initial-architecture.md`,
  `input/input-package.md`).
- The single Product Owner artifact (`business-intake/business-intake-summary.md`).
- OpenSpec remains the default downstream.

## Action for existing workspaces

- Update any references from the renamed paths above.
- If you used `advanced-governance/...` outputs, they are now `quality-gates/...`.
- No content in your generated workspaces needs to move; only framework paths
  changed.
