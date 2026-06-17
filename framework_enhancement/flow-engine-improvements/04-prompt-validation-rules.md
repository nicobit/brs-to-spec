# Prompt 04 — Add Section 6 to validation-rules.md

## Target file

`.flow-engine/instructions/validation-rules.md`

## What to do

Read the file first. Then append a new Section 6 at the end of the file.
Do not change any existing section.

## New section to append

---

## 6. Suspicious failure detection (read_evidence cross-check)

This section defines how the orchestrator uses `read_evidence` to detect fabricated
or lazy failure reasons before accepting a `status: fail` result.

**When this rule applies:**
- The event result has `status: fail`
- The `failure_reason` makes a claim about input content quality (not about a missing
  file, schema error, or must_include failure)
- The `read_evidence` block is present in the result file

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
   - The failure is automatically unverifiable regardless of the reason text.
   - Reject with:
     `failure_reason: "unverifiable failure: read_evidence is absent. Cannot confirm
     inputs were read before the failure was declared. Re-run Step 10 properly."`

**Critical distinction:** this rule rejects **generic emptiness claims** on non-empty
files. It does NOT prevent genuine semantic failures. A file with 100 lines can still
be a stub, placeholder content, or domain-irrelevant. In that case, the `failure_reason`
must quote the specific content found and explain precisely why it is insufficient.
Line count rules out "empty file" — it does not rule out "wrong content".

---

## Verification

After making the change, confirm:
1. Section 6 is appended after Section 5 (Validation failure handling)
2. The trigger phrases list is present
3. The three-branch check (exists:false / lines<=20 / lines>20) is present
4. The fallback rule for absent read_evidence is present
5. No existing section was modified
