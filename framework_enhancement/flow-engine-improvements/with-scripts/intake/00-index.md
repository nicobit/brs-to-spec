# Scripts-Based Validation — Index

## Problem summary

Three layered problems cause LLM-operated dispatch to produce stub artifacts
that pass validation:

| Layer | Problem | Current state | Fix |
|---|---|---|---|
| 1 | Dispatcher bypass — LLM writes artifacts freehand without going through Steps 6–19 | Detectable after the fact (orphan result file in done/) | `check-integrity.py` blocks the next dispatch if bypass detected |
| 2 | Self-validation — same LLM produces artifact and validates it in same context window | No fix available without breaking automation or using a second agent | Partially mitigated by count-anchored must_include (Layer 3 fix) |
| 3 | Fabricated counts — validation_notes claim "FR-001..FR-027 present" when artifact has 9 rows | count-gate enforces entry count, not entry honesty | `validate-artifact-counts.py` + count-anchored must_include |

## Documents in this folder

| File | What it covers |
|---|---|
| `problem-and-proposal.md` | Full problem analysis, why instruction-only fixes don't work, proposed approach |
| `01-validation-scripts-spec.md` | Spec for 4 Python scripts: validate-result-file, validate-artifact-counts, validate-no-placeholders, check-integrity |
| `02-integrity-check-spec.md` | Deep spec for check-integrity.py — how it detects bypasses, dispatcher integration, limitations |
| `03-must-include-anchoring-spec.md` | How to replace vague must_include items with count-anchored items that force explicit ID enumeration |

## Implementation order

1. `check-integrity.py` — highest value, catches bypasses on the next dispatch
2. `validate-result-file.py` — catches schema violations (status: done, wrong fields)
3. Count-anchored must_include in EVT-TPL-002 and EVT-TPL-003 — improves LLM validation honesty
4. `validate-artifact-counts.py` — mechanical enforcement of count checks
5. `validate-no-placeholders.py` — lowest priority, already partially covered by natural_language rules

## What is NOT in scope here

- Splitting dispatch-next into persona turn + orchestrator turn (rejected: reduces
  automation without solving self-validation in dispatch-all)
- Second AI agent as independent validator (future — requires agent orchestration
  infrastructure not currently available)
- Preventing Copilot from running autonomously between dispatch-all stop signals
  (behavioral, not addressable by framework changes)
