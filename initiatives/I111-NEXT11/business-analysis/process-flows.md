# Process Flows

## Overview

This document captures high-level process flows for key lifecycles: Application Intake, AI Scoring & Screening, Underwriter Review, and Disbursement.

## Application Intake Flow

```mermaid
flowchart LR
  A[Applicant fills form] --> B{Validation OK}
  B -- No --> C[Show inline errors]
  B -- Yes --> D[Create Application (ARN)] --> E[Trigger AI pre-screening]
```

## AI Scoring & Screening Flow

```mermaid
flowchart LR
  E[AI Scoring] --> F{Recommendation}
  F -- AUTO_APPROVE --> G[Generate Offer]
  F -- REFER_TO_UNDERWRITER --> H[Underwriter Queue]
  F -- AUTO_DECLINE --> I[Notify Applicant]
  H --> J[Underwriter Decision]
```

## Disbursement Flow

```mermaid
flowchart LR
  K[Offer Accepted & Cooling-off expired] --> L[Trigger Disbursement to T24]
  L --> M{Confirmation}
  M -- Success --> N[Update status DISBURSED]
  M -- Fail --> O[Retry once then alert Ops]
```

## Source FRs

- FR-001..FR-030 (as relevant per flow)
