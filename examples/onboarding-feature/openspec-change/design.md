# Design — Onboarding Approval

## Overview

Reuse existing frontend, API, database, and audit patterns.

## Component Changes

- Frontend adds onboarding creation form.
- Backend adds create endpoint and approval/rejection endpoint.
- Database adds onboarding request table if not already present.
- Audit service records creation and status changes.

## Security and Authorization

- Require Relationship Manager role for creation.
- Require Compliance role for approval/rejection.

## Test Approach

- Unit tests for domain validation.
- API tests for authorization.
- Integration tests for audit events.
