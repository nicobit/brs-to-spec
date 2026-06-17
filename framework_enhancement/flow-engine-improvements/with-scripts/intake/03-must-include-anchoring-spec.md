# Must_Include Count Anchoring — Specification

## Purpose

Replace vague must_include assertions with count-anchored assertions that name
the source of truth. Forces the orchestrator to enumerate IDs explicitly rather
than claim "rows present" without counting.

---

## The current problem

Current must_include item in EVT-TPL-002 (create_business_intake_summary):

```yaml
must_include:
  - "## Requirements section has one row per atomic requirement from the BRS"
```

This is evaluated by the orchestrator as: "does the requirements section have rows?"
If yes → pass. The orchestrator does not count rows or compare to the BRS.

Result: a validation_notes entry is written claiming pass, and the count-gate
accepts it because the entry exists. The artifact can have 9 rows when the BRS
has 30 FRs and still pass.

---

## The fix — count-anchored must_include items

Replace vague assertions with assertions that name the source and require
explicit enumeration:

**Before:**
```yaml
must_include:
  - "## Requirements section has one row per atomic requirement from the BRS"
```

**After:**
```yaml
must_include:
  - "## Requirements section: list every FR-NNN ID found in the artifact, count
    them, then list every FR-NNN ID found in input/brs.md (already read at Step 10),
    count them, and confirm the counts match. If counts differ, name the missing IDs."
  - "## Requirements section: list every NFR-NNN ID found in the artifact, count
    them, then list every NFR-NNN ID found in input/brs.md, count them, and confirm
    the counts match. If counts differ, name the missing IDs."
```

The orchestrator evaluating this must_include item is forced to:
1. Enumerate the IDs in the artifact (not just say "rows present")
2. Enumerate the IDs in the BRS (already in context from Step 10)
3. Compare the two lists explicitly
4. Write the counts and any missing IDs in the `detail` field

A passing validation_notes entry for this item must look like:

```yaml
- rule: "## Requirements section: list every FR-NNN ID found in the artifact..."
  result: pass
  detail: |
    Artifact FR IDs: FR-001, FR-002, FR-003, FR-006, FR-007, FR-009, FR-012,
                     FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021,
                     FR-022, FR-023, FR-024, FR-025, FR-026, FR-027 (20 IDs)
    BRS FR IDs: FR-001 through FR-030 (30 IDs)
    Missing: FR-004, FR-005, FR-008, FR-010, FR-011, FR-013, FR-014, FR-028,
             FR-029, FR-030
    Count mismatch: artifact 20 ≠ BRS 30
```

This entry would trigger a `result: fail` — the counts do not match.
The orchestrator cannot write a passing entry without producing the ID lists,
and the ID lists cannot be fabricated without being verifiably wrong when a
script or human checks the artifact.

---

## Templates to update

### EVT-TPL-002 — create_business_intake_summary

Current vague items to replace:
```yaml
- "## Requirements section has one row per atomic requirement from the BRS"
- "## Requirements section covers non-functional requirements from the BRS"
- "Every requirement row has Business value and Source reference populated"
```

Replacement:
```yaml
- "## Requirements section — FR count: enumerate all FR-NNN IDs present in the
  artifact, enumerate all FR-NNN IDs present in input/brs.md (read at Step 10),
  state both counts, confirm they match, and list any IDs present in BRS but
  absent from artifact"
- "## Requirements section — NFR count: enumerate all NFR-NNN IDs present in
  the artifact, enumerate all NFR-NNN IDs present in input/brs.md, state both
  counts, confirm they match, and list any missing IDs"
- "Every requirement row has Business value and Source reference: spot-check 3
  random rows and quote the Business value and Source cell for each"
```

### EVT-TPL-003 — create_requirements_catalog

Current vague items to replace:
```yaml
- "every FR-NNN has a unique identifier"
- "no placeholder text (TBD / TODO) in output"
```

Replacement:
```yaml
- "FR count: enumerate all FR-NNN IDs in the artifact, enumerate all FR-NNN IDs
  in business-intake/business-intake-summary.md (read at Step 10), state both
  counts, confirm they match, list any missing IDs"
- "NFR count: same as FR count check but for NFR-NNN IDs"
- "No placeholder text: quote any line containing TBD, TODO, [fill in], or
  PLACEHOLDER — if none found, state 'no placeholders found' explicitly"
```

---

## What this does not fix

Count-anchored must_include items require the orchestrator to produce explicit
ID lists in the validation_notes detail field. This is harder to fabricate than
a vague "rows present" claim — but it is still possible for an LLM to write
a plausible-looking ID list that doesn't match the actual file content.

The validation script (`validate-artifact-counts.py`) in
`01-validation-scripts-spec.md` is the mechanical enforcement layer that makes
fabrication detectable. Count-anchored must_include items and the script are
complementary:

- Count-anchored must_include: forces the LLM to engage with the check explicitly
  rather than claim it implicitly
- validate-artifact-counts.py: verifies the claim mechanically regardless of
  what the LLM wrote in validation_notes

Both should be implemented together. Either alone is insufficient.

---

## Impact on must_include count-gate

Count-anchored must_include items are longer and more specific. They do not
change the count-gate logic (N_NOTES must equal N_MUST). The number of
must_include items in the template determines N_MUST — the content of those
items determines what the orchestrator must prove in each entry.

The count-gate remains valid and necessary. Count-anchoring improves what
happens inside each entry, not the count of entries.
