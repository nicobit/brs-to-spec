# Coding Handoff - E-003 Compliance & Underwriting

## 0 - Component and Repository Map
- Component: Compliance & Underwriting services — repo: platform/compliance

## 1. Implementation Objective

Implement compliance case creation and underwriter routing, attach explainability artifacts and KYC verification evidence so cases surface to underwriters.

## 2. Scope

In Scope:
- Compliance case API (POST /api/compliance/cases)
- KYC verification enrichment step (HMRC connector)

## 3. Acceptance Criteria (selected)

### S-003.0 — Compliance e2e POC
```gherkin
Scenario: Synthetic application triggers AML COMPLIANCE_HOLD
  Given a synthetic application with failing AML indicators
  When the AML connector processes the application
  Then the AML result is `COMPLIANCE_HOLD`

Scenario: Compliance case created and visible in underwriter queue
  Given a COMPLIANCE_HOLD result
  When the system creates a compliance case
  Then the case appears in the underwriter queue and includes explainability artifacts
```

*This file is the self-contained coding handoff for E-003.*
