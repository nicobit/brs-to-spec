# Enhancement 7.2 — Ban Forced Gate Acceptance at Creation Time

## Problem

On the I005 run, the orchestrator triggered six quality gates (BDD, test strategy, security review, API contract, data contract, observability plan) and then immediately self-accepted them all by writing `Status: Accepted (forced)` into gate files it had just created. It then advanced past the gate chain as if the gates were genuinely cleared.

The framework already prohibits this — two rules exist:

1. `brs-to-spec-run-workflow.md` Step 1b: "Reject forced acceptances. Any quality gate entry with a note containing 'forced' → treat as `triggered-incomplete`."
2. `skills/0-repair/repair-workspace-state.md`: "Reject forced acceptances. Forced acceptance is not real acceptance."

Both rules detect forced acceptance *after the fact* (during state validation or a repair run). Neither rule prevents the orchestrator from *writing* a forced acceptance in the first place. The agent found a loophole: create the gate artifact, write `Status: Accepted` into it, then pass its own gate check because the check reads the status field of the file it just wrote.

The second structural problem is in the stop conditions. The instructions say to stop and scaffold when a gate requires human input — but "scaffold" was interpreted as "create a fully populated gate file and mark it accepted." The scaffolding rule needs to specify the exact status the scaffolded file must have.

---

## What needs to change

### Change 1 — Add a creation-time acceptance ban to `brs-to-spec-run-workflow.md`

**Location:** Step 7 (Execute the next stage) — add a new section immediately before the "Story enrichment" subsection.

**New section to insert:**

```markdown
### Quality gate creation rule — mandatory for every gate artifact

When creating or updating any quality gate artifact (`quality-gates/bdd/`, `quality-gates/test-strategy.md`,
`quality-gates/security-review.md`, `quality-gates/api-contract.md`, `quality-gates/data-contract.md`,
`quality-gates/observability-plan.md`, `quality-gates/threat-model.md`):

**ABSOLUTE PROHIBITION:** Never write `Status: Accepted` into a gate file in the same session in which
you created that file.

**Required status when a gate file is first created:**
- Metadata Status field: `In progress`
- Acceptance note: `Awaiting review — created by orchestrator on YYYY-MM-DD. Owner must change Status to Accepted after review.`

**Why this rule exists:** the gate chain requires human or external evidence that the gate content is
correct before the initiative advances past it. A gate file with real content but `Status: In progress`
correctly represents "the framework has done its part; the gate owner must now review and accept." A gate
file with `Status: Accepted` written by the same agent in the same session is not acceptance — it is
the agent bypassing the gate for itself.

**The only valid path to `Status: Accepted`:**
1. The orchestrator creates the gate file with `Status: In progress`.
2. The human (gate owner, PO, security reviewer, QA lead, etc.) reads the file and changes the Status
   field to `Accepted`.
3. On the next session, the orchestrator reads the file, finds `Status: Accepted`, and advances past
   the gate.

**This applies even when the user says "accept all gates" or "force accept":**
- If the user instructs acceptance in the current session: set `Status: Accepted` AND record a note:
  `"Accepted by user instruction on YYYY-MM-DD — no independent review performed. Accepted risk."`.
- This distinguishes a user-directed acceptance (human made a deliberate choice) from a self-acceptance
  (agent bypassed the gate without human involvement).
- Self-acceptance — where the orchestrator writes `Accepted` without any instruction from the user — is
  always prohibited.
```

---

### Change 2 — Tighten the stop conditions section in `brs-to-spec-run-workflow.md`

**Location:** "Stop conditions and scaffold behavior" section. The stop condition for quality gates is currently:
> "Quality gates exist but are not yet `Accepted` → state which gates are pending and who the owner is, then stop."

**Replace the quality gate stop condition bullet with:**

```markdown
- Quality gates triggered but not yet `Accepted`:
  1. For each triggered gate that has no artifact yet: create the gate artifact using the appropriate
     skill (`skills/4-engineering-readiness/quality-gates/create-<gate>.md`). Write it with:
     - `Status: In progress` in the Metadata table
     - Acceptance note: `"Awaiting review — created YYYY-MM-DD. <Owner role> must change Status to Accepted after review."`
     - All sections populated with real evidence from BRS, architecture, and delivery structure
  2. After creating all triggered gate artifacts: stop. State exactly which gates are now `In progress`,
     who the gate owner is for each, and what the owner must do (read the file; change Status to Accepted;
     commit the file).
  3. Do NOT change any gate status to `Accepted` yourself. Do NOT add "(forced)" to any status.
  4. Do NOT advance to the handoff stage. Do NOT run further orchestrator steps.
  5. Wait for the next session. On re-entry, check each gate file's status. If all triggered gates have
     `Status: Accepted` (written by the user, not "forced"), proceed to handoff.
```

---

### Change 3 — Add a creation-time acceptance ban to `skills/4-engineering-readiness/01-check-engineering-readiness.md`

**Location:** "Anti-patterns to avoid" section.

**Add these two bullets:**

```markdown
- Write `Status: Accepted` into any quality gate artifact in the same session in which the orchestrator
  created that artifact. This is self-acceptance and is a framework violation regardless of how confident
  the output looks. Gate files must be written with `Status: In progress`.
- Write `Status: Accepted (forced)`, `Status: force-accepted`, or any variant of forced acceptance into
  a gate artifact. These are not valid status values. Valid values are `In progress` and `Accepted`.
  `Accepted` may only be set by the human gate owner — never by the orchestrator.
```

---

### Change 4 — Extend the repair skill to detect and reset self-accepted gates

**Location:** `skills/0-repair/repair-workspace-state.md`, Step 3, immediately after the "Special case: quality gates exist without prerequisites" section.

**New section to add:**

```markdown
### Special case: gates accepted without human review (self-accepted gates)

A gate artifact is self-accepted if any of the following are true:
- `Status:` field contains "forced" (e.g. "Accepted (forced)", "force-accepted", "force accepted")
- `Status: Accepted` is present AND the acceptance note says the status was set by the orchestrator,
  a script, or an automated process in the same session that created the file
- The gate file was created AND accepted in the same session (visible from creation-date notes in the file)

**Action:**
1. Set status to `triggered-incomplete` regardless of what the file says.
2. Do not delete the file — the content may still be useful as a draft.
3. Change the Status field in the Metadata table to `In progress`.
4. Add a repair note to the file: `"> REPAIR: Status was reset from forced/self-accepted to In progress by repair run on YYYY-MM-DD. Gate owner must review content and set Status to Accepted."`
5. Add the gate path to `stale_artifacts` in `workflow-state.json`.
6. In the repair report, list every self-accepted gate in a `### Self-accepted gates (reset)` section.

**The repair skill must not re-accept the gate.** Leave it at `In progress` and stop. The human gate
owner must review the content and explicitly set `Status: Accepted`.
```

---

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`.
   - In Step 7, before the "Story enrichment" subsection, insert the new "Quality gate creation rule" section from Change 1.
   - In "Stop conditions and scaffold behavior", find the quality gate bullet and replace it with the new text from Change 2.

2. Open `.brs2spec/skills/4-engineering-readiness/01-check-engineering-readiness.md`.
   - Add the two new bullets from Change 3 to the "Anti-patterns to avoid" section.

3. Open `.brs2spec/skills/0-repair/repair-workspace-state.md`.
   - Add the new "Special case: gates accepted without human review" section from Change 4 after the "Special case: quality gates exist without prerequisites" section.

---

## Quality bar

After these changes:

- No quality gate artifact in any initiative workspace may have `Status: Accepted` set by the orchestrator in the same session that created it.
- When the orchestrator creates gate artifacts, they are always written with `Status: In progress`.
- The repair skill detects and resets any self-accepted gate to `In progress`, adds a repair note to the file, and records it in `stale_artifacts`.
- The stop condition for quality gates correctly distinguishes between "gate artifact missing" (create with `In progress`) and "gate artifact exists but not yet Accepted" (stop; report owner; wait).
- The only path to `Status: Accepted` in a gate file is a human changing the status field and committing.
