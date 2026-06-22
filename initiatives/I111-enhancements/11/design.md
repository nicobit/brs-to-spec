# Enhancement 11 — Artifact Digests (Token Reduction)

## Status: DESIGN ONLY — not implemented

---

## 1. Problem statement

Each dispatch event reloads the full content of every artifact listed in `read_from` — BRS, prior artifacts, skill files, persona files — from scratch, because each dispatch runs in a fresh context window. As a workflow progresses, the cumulative re-read cost compounds: an artifact produced at EVT-00002 may be re-read at EVT-00003, EVT-00004, EVT-00005, and beyond, each time consuming its full token weight.

On a typical OpenSpec + Enterprise+Modular run (10–15 events), a 3,000-token `business-intake-summary.md` may be re-read 8 times = 24,000 tokens for a single artifact. Multiply across all artifacts in the chain and per-event token cost grows faster than the workflow itself.

The persona executing the skill is the unavoidable cost. The re-reading of prior artifacts is not.

---

## 2. Design goal

Allow downstream events to read a **compact digest** of a prior artifact instead of its full content, when the full content is not needed for the current task. The digest is produced automatically alongside the full artifact by the same event that created it. No new event types, no changes to the dispatch sequence, no breaking changes.

---

## 3. What is a digest

A digest is a short structured summary of an artifact, written to `<artifact-path-stem>-digest.md` at the same time the full artifact is written.

**Properties:**
- Maximum 300 tokens (enforced by the producing skill)
- Contains only facts needed by downstream events: IDs, counts, key decisions, named entities
- Does NOT contain prose, rationale, or content that only humans need to read
- Written by the same persona that produced the full artifact, as a second `write_to` entry
- Structured as a flat list or small table — no headings, no paragraphs

**Example — digest for `business-intake-summary.md`:**

```markdown
initiative: I006-my-app
delivery_mode: OpenSpec
execution_mode: Enterprise+Modular
fr_count: 23
fr_ids: FR-001..FR-023
ac_count: 41
ac_ids: AC-001..AC-041
key_constraints: HMRC API dependency, GDPR data residency UK, 12-week timeline
out_of_scope: mobile app, payment processing, admin portal
```

**Example — digest for `business-analysis/actors-and-personas.md`:**

```markdown
act_count: 5
act_ids: ACT-001..ACT-005
act_names: Applicant, Underwriter, Compliance Officer, System Administrator, External Auditor
sys_count: 3
sys_ids: SYS-001..SYS-003
sys_names: HMRC API, CRM Platform, Document Storage
```

---

## 4. How events declare digest usage

### 4.1 Producing a digest (in the event template)

The producing event adds the digest path as a second `outputs` entry and adds a `digest_rules` block:

```yaml
outputs:
  primary: "business-intake/business-intake-summary.md"
  digest: "business-intake/business-intake-summary-digest.md"

digest_rules:
  max_tokens: 300
  include:
    - "initiative id and slug"
    - "delivery_mode and execution_mode values"
    - "all FR-NNN IDs as a compact range or list"
    - "all AC-NNN IDs as a compact range or list"
    - "key constraints named in the BRS"
    - "explicit out-of-scope items"
  exclude:
    - "prose descriptions"
    - "rationale or justification"
    - "table formatting"
```

At runtime the dispatcher maps `outputs.digest` → second entry in `write_to`. The skill instruction file gains a standard closing section: "After writing the full artifact, write a digest to `write_to[1]` following the event's `digest_rules`."

### 4.2 Consuming a digest (in downstream event templates)

Downstream events declare which inputs they need in full vs. digest only:

```yaml
inputs:
  required:
    - path: "input/brs.md"
      mode: full                  # default — full content loaded
    - path: "business-intake/business-intake-summary.md"
      mode: digest                # loads -digest.md instead of full artifact
  optional:
    - path: "business-intake/business-rules.md"
      mode: digest
```

`mode: full` is the default when omitted — no change to existing behaviour.

At runtime the dispatcher resolves `mode: digest` to `<stem>-digest.md` before reading. If the digest file does not exist and `mode: digest` is declared, the dispatcher falls back to the full artifact and logs a warning in the result file: `"digest not found for <path> — loaded full artifact (higher token cost)."`

---

## 5. Digest path convention

| Full artifact path | Digest path |
|---|---|
| `business-intake/business-intake-summary.md` | `business-intake/business-intake-summary-digest.md` |
| `business-analysis/actors-and-personas.md` | `business-analysis/actors-and-personas-digest.md` |
| `business-analysis/process-flows.md` | `business-analysis/process-flows-digest.md` |
| `business-analysis/use-case-spec.md` | `business-analysis/use-case-spec-digest.md` |
| `planning/delivery-structure.md` | `planning/delivery-structure-digest.md` |

Rule: `<directory>/<stem>-digest.md` — always in the same folder as the full artifact.

---

## 6. Digest status in workflow-state.json

Digests are tracked as sub-entries under the full artifact, not as independent artifacts:

```json
"business-intake/business-intake-summary.md": {
  "status": "accepted",
  "produced_by": "EVT-00002",
  "accepted_at": "2026-06-14T16:10:00Z",
  "last_updated": "2026-06-14T16:10:00Z",
  "digest": {
    "path": "business-intake/business-intake-summary-digest.md",
    "status": "ai_validated",
    "produced_by": "EVT-00002"
  }
}
```

`blocked_by` checks use the parent artifact status only — never the digest status. Digests are not blockable artifacts.

---

## 7. Which events benefit most

Ranked by frequency of downstream re-reads:

| Artifact | Re-read by events | Current token cost | With digest |
|---|---|---|---|
| `business-intake-summary.md` | EVT-003..010 (~8 events) | ~3,000 × 8 = 24,000 | ~300 × 6 + 3,000 × 2 = 7,800 |
| `actors-and-personas.md` | EVT-007..010 (~4 events) | ~1,500 × 4 = 6,000 | ~300 × 3 + 1,500 × 1 = 2,400 |
| `business-rules.md` | EVT-007..012 (~6 events) | ~2,000 × 6 = 12,000 | ~300 × 5 + 2,000 × 1 = 3,500 |
| `delivery-structure.md` | EVT-010..015 (~5 events) | ~2,500 × 5 = 12,500 | ~300 × 4 + 2,500 × 1 = 3,700 |

Estimated total reduction across a full OpenSpec run: **~40,000–55,000 tokens** (~40–50% of artifact re-read cost).

The BRS itself (`input/brs.md`) is always read in full — it is the source of truth and cannot be safely digested without losing information that skills need.

---

## 8. Digest quality rule

A digest that omits IDs, invents data, or paraphrases incorrectly is worse than re-reading the full artifact — it propagates errors silently downstream. The producing skill must be instructed:

> "Write only facts that appear verbatim in the full artifact. Do not paraphrase, infer, or summarise prose. If a fact cannot be expressed in under 10 words, omit it from the digest and keep it in the full artifact only."

The `must_include` block for digest-producing events should include:
- `"digest file exists at <digest-path>"`
- `"digest contains no prose sentences"`
- `"all FR-NNN IDs listed in the digest match the full artifact exactly"`

---

## 9. Files to create/modify when implementing

| File | Action | Notes |
|---|---|---|
| `.flow-engine/instructions/dispatcher.md` | **MODIFY** | Step 10: resolve `mode: digest` → digest path before reading; fallback rule |
| `.flow-engine/instructions/event-execution-rules.md` | **MODIFY** | Add digest production rule: if `outputs.digest` present, skill must write it |
| `.flow-engine/schemas/event-schema.yaml` | **MODIFY** | Add `mode: full/digest` to input entries; add `outputs.digest` field; add `digest_rules` block |
| `.flow-engine/schemas/event-result-schema.yaml` | **MODIFY** | Add `digest_written: true/false` to result |
| `.flow-engine/instructions/state-update-rules.md` | **MODIFY** | Add `digest` sub-entry format under artifact status |
| `.brs2spec2/workflow/event-templates/EVT-TPL-002-*.yaml` | **MODIFY** | Add `outputs.digest` + `digest_rules` |
| `.brs2spec2/workflow/event-templates/EVT-TPL-003-*.yaml` | **MODIFY** | Add `outputs.digest` + `digest_rules`; switch `business-intake-summary` input to `mode: digest` |
| `.brs2spec2/workflow/event-templates/EVT-TPL-004-*.yaml` | **MODIFY** | Add `outputs.digest`; switch `business-intake-summary` to `mode: digest` |
| `.brs2spec2/workflow/event-templates/EVT-TPL-005-*.yaml` | **MODIFY** | Switch prior artifacts to `mode: digest` |
| `.brs2spec2/workflow/event-templates/EVT-TPL-006-*.yaml` | **MODIFY** | Add `outputs.digest`; switch prior artifacts to `mode: digest` |
| `.brs2spec2/workflow/event-templates/EVT-TPL-007-*.yaml` | **MODIFY** | Switch all prior artifacts to `mode: digest` except BRS |
| *(all subsequent templates)* | **MODIFY** | Switch prior artifacts to `mode: digest` where full content not needed |
| All skill files that produce a primary artifact | **MODIFY** | Add closing section: "Write digest per event's digest_rules" |
| All artifact template files | **MODIFY** | No change needed — digests have no template |

---

## 10. Open questions before implementation

1. **Digest staleness** — if a prior event updates an artifact (UPDATE_ARTIFACT), must it also re-write the digest? Rule proposed: yes, any event that writes to `write_to[0]` must also re-write `write_to[1]` (the digest) if it exists.
2. **Which events need full vs. digest** — needs a per-template audit before modifying all templates. Some events (e.g. VALIDATE_ARTIFACT) need the full artifact; others (e.g. CREATE_TRACEABILITY_MATRIX) only need IDs from prior artifacts.
3. **Digest for BRS** — the BRS is the highest single token cost. A BRS digest (FR list, AC list, scope summary) could save significant tokens. Risk: skills may miss nuance. Proposed: BRS digest is opt-in per event, never the default.
4. **Max token enforcement** — the 300-token limit on digests cannot be machine-enforced by the dispatcher today (no token counter). It is enforced by the `must_include` check (no prose sentences) and by the skill instruction. A future enhancement could add a `validator: max_tokens` machine check.
