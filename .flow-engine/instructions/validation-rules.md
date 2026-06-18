# Flow Engine — Validation Rules
# Version: 1.0
#
# Defines how Claude applies the two validation layers from the event schema.
# Applied during dispatch steps 14 (must_include) and 16 (natural_language).

---

## 1. When validation runs

Validation runs in orchestrator mode — after the result file is written (step 15), before deciding done/ or failed/ (step 17).

Validation is always performed by Claude in orchestrator mode. Never in persona mode.
The persona produces the artifact. The orchestrator validates it.

Two-pass sequence:
1. `must_include` — structural presence checks (Step 14, orchestrator mode — reads artifact from disk after persona has written it)
2. `validation_rules.natural_language` — content quality checks (Step 16, orchestrator mode)

Both passes run in orchestrator mode. The persona writes the artifact (Step 11); the orchestrator validates it (Steps 14 and 16). The mode boundary is the result file (Step 15).

If must_include fails, skip natural_language validation — the artifact is already failed.

---

## 2. must_include validation

`must_include` entries are evaluated first. Each entry is a plain-English assertion about structural presence.

**How to evaluate:**
- Read each entry as a yes/no question about the produced artifact.
- Read the artifact(s) in `write_to`.
- For each entry: answer yes (present and non-empty) or no (absent, empty, or stub-only).

**Pass/fail rule:**
- All entries must be true for must_include to pass.
- If any entry is false: set result `status: fail`. Populate `failure_reason` with prefix `"Required content missing: "` followed by the specific failing entries.

**Example must_include entries and how to check them:**

| Entry | Check |
|---|---|
| `"every objective has a measurable success criterion"` | Read objectives section — each objective must have at least one criterion that can be measured |
| `"Status field in Metadata"` | Scan artifact for a `Status:` line in a Metadata table or header section |
| `"every gap has an owner"` | Read gaps section — each gap entry must have a named owner (not "TBD" or blank) |
| `"delivery_mode field is present"` | Scan artifact for `delivery_mode:` or `**Delivery Mode:**` field with a non-empty value |

---

## 3. natural_language validation

`validation_rules.natural_language` entries are evaluated after must_include passes.

**How to evaluate:**
- Read each rule as a plain-English assertion about artifact content.
- Read the artifact(s) in `write_to` (already in context from execution).
- For each rule: determine pass or fail based on actual content.
- Record each result in `validation_notes` in the result file.

**Pass/fail rule:**
- All rules must pass for validation to pass.
- If any rule fails: set result `status: fail`. Populate `failure_reason` with the specific failing rule(s) and what was found vs what was expected.

**Common rule patterns and how to evaluate:**

| Rule pattern | How to evaluate |
|---|---|
| `"no placeholder text (TBD / TODO / [fill in]) in output"` | Scan full artifact text for strings: TBD, TODO, [fill in], PLACEHOLDER, [TBD], [INSERT] |
| `"every BR-NNN maps to at least one FR-NNN"` | For each BR-NNN ID in the artifact, check that at least one FR-NNN ID appears in the same row or linked section |
| `"Status in Metadata is one of: Draft, Accepted, Rejected"` | Find the Status field value; check it is exactly one of the allowed values (case-sensitive) |
| `"delivery_mode is one of the four allowed values"` | Find the delivery_mode value; check it is exactly: OpenSpec, Standalone, FastPath, or BusinessCopilot |
| `"every user story has acceptance criteria"` | For each F-NNN.N story entry, check that at least one AC-NNN or acceptance criterion text is present |

**Specificity rule:** failure_reason must name the specific items that failed, not just the rule.
Bad: `"BR-NNN traceability check failed"`
Good: `"Validation failed: 'every BR-NNN maps to at least one FR-NNN' — BR-004, BR-007, BR-012 have no FR-NNN link"`

---

## 3b. Folder-output validation (applies when any `write_to` entry ends with `/`)

When a `write_to` path ends with `/`, the output is a folder of files, not a single file.

**Dispatcher Step 13 (verify write_to) for folder outputs:**
- Check that the folder exists on disk and contains at least one file matching the pattern from `validation_rules.machine.folder_contains_at_least_one` (e.g. `UC-*.md`).
- If the folder does not exist OR contains no matching files → result status is `fail`. `failure_reason: "folder output missing: <folder-path> does not exist or contains no <pattern> files. The persona must write one file per entity inside this folder, not a single monolithic file."`
- Never accept a flat file (e.g. `use-case-specs.md`) as a substitute for a folder output.

**must_include evaluation for folder outputs:**
- Evaluate each `must_include` assertion against the set of files in the folder, not a single file.
- An assertion like "every UC-NNN from use-cases.puml has exactly one file in use-cases/" is evaluated by listing the folder contents and cross-referencing the source diagram.
- If the folder contains a single monolithic file with all content merged, treat this as a fail — one file per entity is a structural requirement, not a style preference.

---

## 4. machine validators (v2.1 — not executed in v2.0)

Machine validators are defined in event files under `validation_rules.machine`. They are not executed in v2.0 (chat-operated). A future deterministic dispatcher (v2.1) will implement them.

In v2.0: list each machine validator in `validation_notes` with `result: skipped (v2.0)`.

**Defined validators and what they will check in v2.1:**

| Validator | What it checks |
|---|---|
| `no_placeholders` | Scans artifact for strings: TBD, TODO, [fill in], PLACEHOLDER, [TBD], [INSERT] |
| `id_pattern` | Checks that at least one ID matching `args.pattern` regex appears in the artifact |
| `traceability_links` | For every ID matching `args.from` pattern, checks that at least one `args.to` pattern ID appears in the same row or linked section |
| `markdown_table_required` | Checks that at least one markdown table (`|---|`) is present in the artifact |
| `status_field_required` | Checks that a field named by `args.field` (default: `Status`) has a value from `args.allowed` list |

---

## 4b. Enforcement rule — natural_language validation must be explicitly recorded

This rule prevents silent validation skip. The most common failure mode is: the orchestrator writes `validation_notes` with only `must_include` results, skips the `natural_language` step, and the check passes because `validation_notes` is technically non-empty.

**When `validation_rules.natural_language` is defined in the event, the orchestrator MUST:**

1. Evaluate the natural_language rule against the produced artifact(s) — reading the rule text and the artifact content.
2. Write one `validation_notes` entry whose `rule:` field contains the natural_language rule text (or a clear excerpt of it if it is long).
3. Set `result: pass` or `result: fail` on that entry, with a specific `detail`.

**Enforcement check (Step 16, orchestrator mode):**

After writing the preliminary result file (Step 15), before moving to Step 17:

- If `validation_rules.natural_language` is defined in the event AND no entry in `validation_notes` has a `rule:` value that references or quotes the natural_language rule text → treat this as a validation failure:
  - Set result `status: fail`.
  - Set `failure_reason: "natural_language validation skipped: validation_rules.natural_language is defined but no validation_notes entry records its evaluation. must_include results alone are not sufficient — the orchestrator must evaluate and record the natural_language check separately."`.
  - Move event and result file to `failed/`.
  - Do NOT mark the artifact as `ai_validated`.

**A `validation_notes` entry that only records a `must_include` check does NOT satisfy this requirement**, even if `validation_notes` is non-empty.

**Format for the natural_language validation_notes entry:**

```yaml
validation_notes:
  - rule: "<quote or clear excerpt of the natural_language rule text>"
    result: pass   # or fail
    detail: "<specific: what was counted, compared, or verified — e.g. 'requirements.md has 20 FR-NNN rows; BRS has ~20 FRs; no domain-mismatched rows found; all NFRs have measurable thresholds'>"
```

**Specificity requirement for `detail`:** a passing entry must state concrete evidence (counts, names, comparisons). A detail that only says "passed", "looks good", or "checked" is not acceptable and must be treated as if the check was not performed — re-evaluate and rewrite.

---

## 5. Validation failure handling

When validation fails (must_include or natural_language):

- **Do not delete the artifact.** Leave it on disk — it may be partially useful for debugging or repair.
- Set result file `status: fail`.
- Populate `failure_reason` with specific rule names and what was found vs expected.
- Move event and result file to `failed/`.
- Set artifact status in workflow-state.json to `"failed"`.
- Execute `on_failure` actions (decision raising, chaining).

**The artifact on disk with status `failed` in workflow-state.json** means: the file exists but is not trusted. Downstream events that have this artifact in `blocked_by` will remain blocked until a REPAIR_ARTIFACT or RETRY_FAILED_TASK event re-produces it and passes validation.

---

## 6. Suspicious failure detection (read_evidence cross-check)

This section defines how the orchestrator uses `read_evidence` to detect fabricated
or lazy failure reasons before accepting a `status: fail` result.

**When this rule applies:**
- The event result has `status: fail`
- The `failure_reason` makes a claim about input content quality (not about a missing
  file, schema error, or must_include failure)

This rule applies whether or not `read_evidence` is present. If `read_evidence` is
absent the check is stricter, not skipped — see step 4 below.

**Content-quality failure phrases that trigger this check:**
- "no extractable requirements"
- "BRS has no content" / "BRS is empty" / "insufficient BRS content"
- "no extractable content"
- "no requirements found"
- "source file does not contain"
- "input is insufficient"
- Any phrase claiming a file is empty, minimal, or lacks substantive content

**Check procedure:**

1. Find the `read_evidence` entry for the input file referenced in the failure reason.

2. Check `exists` and `lines`:
   - If `exists: false` → the file was genuinely missing. Failure is plausible. Accept.
   - If `exists: true` AND `lines <= 20` → short file. Failure may be plausible, but
     `failure_reason` must quote at least one specific line from the file explaining
     why the content is insufficient. A generic claim is still not acceptable.
   - If `exists: true` AND `lines > 20` → file has substantial content.
     A generic emptiness claim is invalid. Reject with:
     `failure_reason: "generic emptiness claim rejected: [original reason] —
     read_evidence shows [path] has [lines] lines. This does not prove the file is
     semantically sufficient, but it does prove it is not empty. The failure_reason
     must quote specific sections found and explain exactly what was missing.
     Re-run with a specific failure_reason."`

3. Check `first_nonempty_line` contradiction:
   - If `read_evidence` shows a meaningful `first_nonempty_line`
     (e.g. `"# Business Requirements Specification"`) AND `failure_reason` claims
     the file was empty or had no content:
     - this is a direct contradiction — reject with:
       `failure_reason: "contradictory failure: read_evidence shows
       first_nonempty_line '[value]' for [path] but failure_reason claims the file
       was empty. These cannot both be true. Re-run with honest failure evidence."`

4. If `read_evidence` is absent entirely when `read_from` is non-empty:
   - **Hard reject — this blocks the result regardless of `failure_reason` text.**
   - A result with a content-quality failure claim and no `read_evidence` means
     Step 10 was never executed. The model declared failure without reading the inputs.
   - Set `status: fail` (keep fail).
   - Set `failure_reason: "fabricated failure: read_evidence is absent but read_from
     is non-empty. The failure was declared without reading the input files — Step 10
     was not executed. Move the event back to pending/ and re-run dispatch-next."`
   - Move event and result to `failed/`. Do not proceed to Step 17 as pass.

**Critical distinction:** this rule rejects **generic emptiness claims** on non-empty
files. It does NOT prevent genuine semantic failures. A file with 100 lines can still
be a stub, placeholder content, or domain-irrelevant. In that case, the `failure_reason`
must quote the specific content found and explain precisely why it is insufficient.
Line count rules out "empty file" — it does not rule out "wrong content".
