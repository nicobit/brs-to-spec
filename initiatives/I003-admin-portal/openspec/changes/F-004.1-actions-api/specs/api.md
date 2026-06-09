# API Specs — F-004.1 Actions API

See `quality-gates/api-contract.md` for full contract. Summary:

POST /actions/{actionId}/run
- 200: synchronous result
- 202: accepted with `job_id` and `status_url`

GET /jobs/{jobId}
- 200: job status and audit metadata
