# Delivery Spec — D1 Create Onboarding Request

## Purpose

Create the first vertical slice for onboarding request creation.

## Requirements Covered

| Requirement ID | Summary |
|---|---|
| REQ-001 | Create onboarding request |
| REQ-002 | Validate mandatory fields |
| REQ-003 | Emit audit event |
| REQ-004 | Restrict status visibility |

## Architecture Constraints

| Constraint ID | Applied how |
|---|---|
| ARC-001 | Use Entra ID |
| ARC-002 | Enforce role-based access |
| ARC-003 | Persist in Azure SQL |
| ARC-004 | Emit audit event |
| ARC-005 | Structured logs without sensitive data |
