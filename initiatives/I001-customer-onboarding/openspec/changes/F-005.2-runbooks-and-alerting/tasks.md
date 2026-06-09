# Tasks — F-005.2: Runbooks and Alerting

> Wave 5 — parallel with F-004.2, F-002.2, F-003.2. Starts after F-005.1 deployed.

## Implementation tasks

- [ ] OS-F005.2-001: Tune alert thresholds against staging traffic baseline
  - Requirement: NFR-005
  - Acceptance: AC-002 — thresholds documented; minimal false positives in staging
  - Data: none
  - API: none
  - Events to emit: none — reads existing signals from F-005.1
  - Evidence expected: updated alert rule expressions; staging alert firing log reviewed

- [ ] OS-F005.2-002: Execute pager drill — P1 alert rules
  - Requirement: NFR-005
  - Acceptance: AC-003 — on-call receives pager notification
  - Data: none
  - API: none
  - Events to emit: none
  - Evidence expected: pager drill result documented; on-call contact list confirmed correct

- [ ] OS-F005.2-003: Review runbooks with SRE and Engineering; attach dashboard links
  - Requirement: NFR-005
  - Acceptance: AC-001, AC-004 — runbooks reviewed; dashboard links in observability-plan.md
  - Data: none — updates `quality-gates/observability-plan.md` (dashboard links section)
  - API: none
  - Events to emit: none
  - Evidence expected: runbook review sign-off; dashboard links filled in observability-plan.md

## Done criteria

- [ ] Alert thresholds tuned and documented
- [ ] Pager drill completed and result attached
- [ ] All P1 runbooks reviewed by SRE
- [ ] Dashboard links filled in `quality-gates/observability-plan.md`
