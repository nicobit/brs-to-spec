# API Contract — Async Action Pattern

## Metadata

| Field | Value |
|---|---|
| Initiative | I003-admin-portal |
| Gate | API contract |
| Triggered | Yes |
| Required | Yes |
| Owner | Architecture / Integration |
| Artifact | quality-gates/api-contract.md |
| Status | Accepted |
| Reviewer | Architecture / Integration |
| Review date | 2026-06-09 |

## Purpose
Define the API contract for operational actions exposing both synchronous and asynchronous execution modes. This contract specifies request/response shapes, HTTP semantics, status endpoints, headers, and required security considerations.

## Summary
- Endpoint: `POST /actions/{actionId}/run` supports both immediate (sync) and deferred (async) execution.
- For long-running operations the server MUST return `202 Accepted` with a `Location` header pointing to the job status endpoint and a response body containing `job_id` and `status_url`.
- Status endpoint: `GET /jobs/{jobId}` returns job state, progress, result (when finished), and audit metadata.

## OpenAPI (snippet)

```yaml
openapi: 3.0.3
info:
  title: Admin Portal Actions API (draft)
  version: 0.1.0
paths:
  /actions/{actionId}/run:
    post:
      summary: Run an operational action (sync or async)
      parameters:
        - name: actionId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ActionRequest'
      responses:
        '200':
          description: Action completed synchronously
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ActionResult'
        '202':
          description: Action accepted for async processing
          headers:
            Location:
              description: URL to poll job status
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AcceptedResponse'
        '400': { description: Bad request }
        '401': { description: Unauthorized }
        '403': { description: Forbidden }
        '429': { description: Too many requests }

  /jobs/{jobId}:
    get:
      summary: Get status of an async job
      parameters:
        - name: jobId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Job status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/JobStatus'
        '404': { description: Not found }
        '401': { description: Unauthorized }
        '403': { description: Forbidden }

components:
  schemas:
    ActionRequest:
      type: object
      properties:
        tenantId:
          type: string
        subscriptionId:
          type: string
        resourceId:
          type: string
        parameters:
          type: object
      required: [tenantId, subscriptionId, resourceId]

    ActionResult:
      type: object
      properties:
        status:
          type: string
        result:
          type: object

    AcceptedResponse:
      type: object
      properties:
        job_id:
          type: string
        status_url:
          type: string

    JobStatus:
      type: object
      properties:
        job_id:
          type: string
        status:
          type: string
          enum: [pending, running, succeeded, failed, cancelled]
        progress:
          type: integer
          format: int32
        result:
          type: object
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
        started_at:
          type: string
          format: date-time
        finished_at:
          type: string
          format: date-time
        audit:
          type: object
          properties:
            initiated_by:
              type: string
            initiated_at:
              type: string
              format: date-time
            correlation_id:
              type: string
```

## API Contract Checklist
- Authentication: Azure AD (Bearer tokens). Validate group membership and roles for action invocation.
- Authorization: enforce `AdminPortalActionRunner` least-privilege role and per-tenant scoping.
- Idempotency: support `Idempotency-Key` header for safe retries where applicable.
- Rate limiting: define per-tenant and per-principal limits; return `429` when exceeded.
- Audit: include `initiated_by`, `correlation_id`, and `initiated_at` in job metadata; write audit entry on start/complete/failure.
- Error model: standardize error codes and messages; include actionable remediation where possible.
- Timeouts: short ops should complete within a configured threshold; server must choose sync vs async based on operation cost and queue length.
- Security: require Key Vault for secrets access; do not return sensitive tokens in responses.
- Observability: emit trace/span IDs and metrics for request latency, queue depth, job durations, failure rates.

## Example Usage
- Short op (sync): `POST /actions/start-vm/run` → `200` with result.
- Long op (async): `POST /actions/reprovision/run` → `202` + `Location: /jobs/{jobId}` and body `{ "job_id": "{jobId}", "status_url": "/jobs/{jobId}" }`.
- Polling: `GET /jobs/{jobId}` → `{ job_id, status: running, progress: 42, audit: {...} }`.

## Acceptance Criteria
- OpenAPI draft reviewed and linked to `quality-gates/api-contract.md` evidence.
- Integration tests validate sync and async paths with sample subscription IDs.
- Security checklist items satisfied (auth, roles, secrets, audit).

---

Draft created to satisfy the API contract quality gate. Add OpenAPI file under `quality-gates/evidence/` as needed.

## Evidence

- OpenAPI (draft): [quality-gates/evidence/admin-portal-actions-openapi.yaml](quality-gates/evidence/admin-portal-actions-openapi.yaml)

Note: The OpenAPI draft has been added to `quality-gates/evidence/` for review. Leave `Status` as `Draft` until Architecture/Integration review and Security acceptance complete; then update `Status` to `Accepted` to close the gate.
