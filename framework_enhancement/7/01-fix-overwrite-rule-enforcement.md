# Enhancement 7.1 — Enforce the Overwrite Rule with a Pre-Write Check

## Problem

The orchestrator ran the delivery structure skill four times. Each run appended a new version to `planning/delivery-structure.md` instead of replacing it. The same corruption happened to `engineering-readiness/readiness-check.md`. The resulting files had 3–4 concatenated versions, which the orchestrator then misread on subsequent passes — finding both "NOT READY" and "Ready" in the same file and treating the file as complete.

The overwrite rule exists in `brs-to-spec-run-workflow.md` Step 4b:
> "Always overwrite — never append. A file with two or more versions concatenated is a corrupt artifact."

It is stated once as prose but there is no enforcement mechanism — no pre-write check, no corrupt-file detection before writing, and no visible consequence described that would stop the agent from appending. The rule fires too late because by the time the agent checks done criteria, the damage is already done.

The repair skill `skills/0-repair/repair-workspace-state.md` has a "special case: multiple versions concatenated" rule that marks the file as `stub`, but this only applies during a repair run — it does not prevent the corruption from happening.

---

## What needs to change

### Change 1 — Add a pre-write corrupt-file check to `brs-to-spec-run-workflow.md`

**Location:** replace Step 4b in `brs-to-spec-run-workflow.md`.

**Current Step 4b text:**
```
## Step 4b — Universal output rule (applies to every artifact written by every skill)

**Always overwrite — never append.**

When a skill produces an artifact at a path that already exists, replace the entire file content
with the new output. Never append new output below existing content. A file with two or more
versions concatenated is a corrupt artifact — the orchestrator cannot assess its stage status
and will misread it on every subsequent run.

This rule applies to every artifact: …

The only exception is state/workflow-state.json …
```

**Replace with:**

```markdown
## Step 4b — Universal output rule (applies to every artifact written by every skill)

**Always overwrite — never append.**

When a skill produces an artifact at a path that already exists, replace the entire file content
with the new output. Never append new output below existing content.

### Pre-write corrupt-file check — mandatory before writing any artifact

Before writing any artifact to a path that already exists, run this check:

1. Read the first 50 lines of the existing file.
2. Count how many times the top-level heading of this artifact type appears (e.g. `# Delivery Structure`, `# Engineering Readiness Check`, `# Architecture Review`).
3. If the heading appears more than once → the file is corrupt (multiple versions concatenated).
   - Do NOT append to it.
   - Do NOT read it for stage assessment — its content cannot be trusted.
   - Mark it as `corrupt` in the internal assessment.
   - Replace the entire file with a clean new version produced by the skill.
   - After writing, record this in `state/workflow-state.json` `stale_artifacts`: add the path with note "corrupt — multiple versions detected; replaced with clean output on YYYY-MM-DD".
4. If the heading appears exactly once → the file is not corrupt. Replace entirely with the new output (still overwrite, never append).
5. If the file does not exist → create it normally.

**This check is not optional.** Run it even when the framework state says the artifact is `complete`. A file marked complete in the state may still be corrupt if the state was written without reading the file content.

### What a corrupt artifact means for stage assessment

A corrupt artifact (multiple versions in one file) has an unknown effective status:
- Do NOT read it to determine stage status.
- Do NOT treat the most recent version as authoritative — you cannot reliably identify which version is most recent.
- Treat the stage as `incomplete` and regenerate the artifact from inputs before advancing.

### The only exception

`state/workflow-state.json` — update it in place using the `maintain-workflow-state.md` skill. It is JSON, not markdown, and has its own update rules.
```

---

### Change 2 — Strengthen the corrupt-file rule in `skills/0-repair/repair-workspace-state.md`

**Location:** Step 3, "Special case: multiple versions concatenated in one file" section.

**Current text:**
```
### Special case: multiple versions concatenated in one file

If any artifact file contains two or more document versions concatenated (e.g. two `# Delivery Structure`
headings, two `# Metadata` tables, two sets of epics), that file is corrupt. Set its status to `stub`
regardless of what version has real content — the orchestrator cannot safely read it. Add it to
`stale_artifacts`. The repair report must call this out explicitly so the user knows the file needs
to be regenerated cleanly.
```

**Replace with:**

```markdown
### Special case: multiple versions concatenated in one file

If any artifact file contains two or more top-level `#` headings for the same artifact type (e.g. two
`# Delivery Structure` headings, two `# Engineering Readiness Check` headings, two Metadata tables),
that file is corrupt.

**Action:**
1. Set its status to `corrupt` (not `stub` — `corrupt` is a distinct condition: the file has content
   but it cannot be trusted because versions are interleaved).
2. Add it to `stale_artifacts` with note: `"corrupt — N versions concatenated; must be regenerated"`.
3. Set `next_action` to the skill that produces this artifact — the corrupt file must be replaced,
   not just flagged.
4. In the repair report, list every corrupt file in a dedicated `### Corrupt artifacts` section.
   For each one, state: artifact path, how many versions were detected, which skill must regenerate it.

**Do NOT:**
- Attempt to parse the "most recent" version from a corrupt file.
- Set the stage to `complete` based on content found in a corrupt file.
- Advance `next_action` past a corrupt file.

**Status value to use:** add `corrupt` to the valid status list alongside `missing`, `stub`,
`incomplete`, `stale`, `complete`, `not-triggered`, `triggered-incomplete`, `triggered-complete`.

A `corrupt` artifact is treated the same as `missing` for gate-chain progression — the stage must
be re-executed to produce a clean file.
```

---

### Change 3 — Add `corrupt` as a valid status value to `skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md`

**Location:** the "Step 2b — Check each artifact and set its status" table.

**Add a new row to the status table:**

| Status | When to use |
|---|---|
| `corrupt` | File exists but contains multiple concatenated versions of the same artifact (two or more top-level `#` headings of the same type). Content cannot be trusted. Treat the same as `missing` for gate-chain progression. |

**Also add to the Anti-patterns section:**

> - Do not read a corrupt file to determine stage status. A file with two `# Delivery Structure` headings cannot be assessed — its effective content is unknown.

---

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`. Locate Step 4b. Replace the entire Step 4b section with the new text from Change 1 above.
2. Open `.brs2spec/skills/0-repair/repair-workspace-state.md`. Locate "Special case: multiple versions concatenated in one file" in Step 3. Replace with the new text from Change 2.
3. Open `.brs2spec/skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md`. Add the `corrupt` row to the status table (Step 2b) and the anti-pattern note. Also add `corrupt` to the valid status values list in the same file.

---

## Quality bar

After these changes:

- Any time the orchestrator is about to write an artifact that already exists, it reads the first 50 lines first and counts heading occurrences.
- A file that gets flagged corrupt is immediately replaced with a clean new version — never appended to.
- The repair skill's scan catches corrupt files and reports them with the specific skill needed to regenerate them.
- The `maintain-workflow-state.md` skill recognizes `corrupt` as a valid status and treats it identically to `missing` for gate-chain purposes.
- It is impossible for the orchestrator to mark a stage `complete` if its artifact is corrupt.
