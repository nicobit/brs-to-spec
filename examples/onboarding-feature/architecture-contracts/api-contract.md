# API Contract

## 1. Summary

The onboarding feature requires backend endpoints to create onboarding requests and support approval decisions.

## 3. Endpoints

### POST /onboarding-requests

Purpose:
Create a new onboarding request.

Related requirements:
- FR-001

Status codes:
- 201 Created
- 400 Validation error
- 403 Unauthorized

Authorization:
Only authorized relationship manager roles may create requests.

Audit/logging:
Creation must produce an audit event.

### POST /onboarding-requests/{requestId}/decision

Purpose:
Approve or reject an onboarding request.

Related requirements:
- FR-002
- SEC-002
- AUD-001
