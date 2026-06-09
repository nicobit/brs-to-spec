# Observability — F-004.1 Actions API

- Emit `jobs.created`, `jobs.duration`, `jobs.failures` with `tenant_id`, `action_id`, `job_id` tags
- Trace job lifecycle across API → worker with `trace_id`
