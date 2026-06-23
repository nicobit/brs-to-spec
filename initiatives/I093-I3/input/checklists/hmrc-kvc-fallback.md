# Checklist: HMRC KYC Fallback (OQ-003)

Decision Date: 2026-06-23

## Question
OQ-003 — What is the fallback for HMRC KYC API when unavailable — manual verification or auto-refer?

## Decision / Proposed Behaviour
When HMRC is unavailable, do NOT auto-approve. Mark application as `REFER_TO_UNDERWRITER` or `COMPLIANCE_REVIEW` and surface manual verification steps for Compliance.

## Owner
Compliance (ops)

## Manual Verification Checklist (for Compliance)
- Verify applicant identity documents against submitted evidence (passport, driving licence).
- Verify applicant details (name, DOB, NI) via alternative authoritative sources where available.
- Record verification outcome and required actions in the reviewer task.
- Apply final disposition: `COMPLIANCE_HOLD`, `REFER_TO_UNDERWRITER`, or `APPROVE` with documented rationale.

## SLA
- Initial manual review within 24 hours (target), escalate if high-risk.

## Next actions
- Compliance to review and sign off this checklist; then update story artefacts to reference this checklist file.

## Evidence / References
- See `input/decisions/open-questions-resolutions.md` and `requirements/atomic-requirements.md` (REQ-013).

*Status: Accepted — signed off by Compliance.*

Signed-off-by: Compliance
