# Coding Handoff - E-004 Offer, Acceptance & Disbursement

## 0 - Component and Repository Map
- Component: Offer service, Acceptance webhook, Disbursement orchestrator

## 1. Implementation Objective

Generate offers, record acceptances (DocuSign), and orchestrate disbursement instructions while preserving audit evidence.

## 2. Scope

In Scope:
- Offer generation API
- Acceptance callback handling and idempotent recording
- Disbursement instruction emission

## 3. Acceptance Criteria (selected)

### S-004.1 — Digital acceptance via DocuSign
```gherkin
Scenario: Acceptance recorded - happy path
  Given an offer exists with id "O1"
  When DocuSign posts an acceptance callback
  Then AcceptanceRecord is created with signed_at and signer recorded
```

*This file is the self-contained coding handoff for E-004.*
