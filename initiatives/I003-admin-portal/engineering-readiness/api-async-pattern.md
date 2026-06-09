 # API Async Pattern — Actions and Job Status

 Purpose: example API patterns and OpenAPI fragment for hybrid sync/async operations (use in delivery slices and API contract).

 ## Principles

 - Short-running operations (<= 30s) may be executed synchronously and return `200 OK` with result.
 - Long-running or multi-resource operations MUST be executed asynchronously: the API returns `202 Accepted` with a `job_id` and `Location` header for status polling.
 - Provide idempotency via `Idempotency-Key` header for mutating endpoints.

 ## OpenAPI fragment (example)

 ```yaml
 paths:
   /actions/{actionId}/run:
     post:
       summary: "Execute an operational action"
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
               $ref: "#/components/schemas/ActionRequest"
       responses:
         '200':
           description: Synchronous execution result
           content:
             application/json:
               schema:
                 $ref: '#/components/schemas/ActionResult'
         '202':
           description: Accepted for asynchronous processing
           headers:
             Location:
               description: URL to poll job status
               schema:
                 type: string
           content:
             application/json:
               schema:
                 $ref: '#/components/schemas/JobAccepted'

   /jobs/{jobId}:
     get:
       summary: "Get job status"
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

 components:
   schemas:
     ActionRequest:
       type: object
       properties:
         targetResources:
           type: array
           items:
             type: string
         parameters:
           type: object
     ActionResult:
       type: object
       properties:
         success:
           type: boolean
         details:
           type: object
     JobAccepted:
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
           enum: [queued, running, succeeded, failed]
         result:
           type: object
         errors:
           type: array
           items:
             type: object
 ```

 ## API behavior guidance

 - Use `202 Accepted` for operations expected to exceed the synchronous timeout threshold. Include `Location` header for `GET /jobs/{jobId}`.
 - Provide `Idempotency-Key` header support for retry-safe operations.
 - Job lifecycle: `queued` → `running` → `succeeded|failed`. Provide error codes and retry guidance in `JobStatus.result` and `errors` fields.
 - Consider WebSocket or server-sent-events only for live UIs that need push updates; otherwise polling is sufficient for MVP.

 ## Example client flow

 1. Client POSTs to `/actions/{actionId}/run` with `Idempotency-Key`.
 2. Server returns `202` with `{ job_id, status_url }`.
 3. Client polls `GET status_url` until `succeeded`/`failed`.
