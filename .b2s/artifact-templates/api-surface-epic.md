# API Surface — E-NNN {{Epic Title}}

## Exposed Endpoints

| EP | Method | Path | Purpose | Auth | Story |
|---|---|---|---|---|---|
| EP-001 | GET / POST / PUT / DELETE | /api/v1/{{resource}} | {{purpose}} | JWT / API key / None | F-NNN.N |

---

## OpenAPI Specification

The OpenAPI definition below is the **primary API contract** for this epic. It MUST be complete enough for a coding agent to generate server stubs. Do NOT abbreviate — include every field, type, constraint, and error response.

```yaml
openapi: "3.0.3"
info:
  title: "{{Epic Title}} API"
  version: "1.0.0"
paths:
  /api/v1/{{resource}}:
    post:
      summary: "{{purpose}}"
      operationId: "{{operationId}}"
      tags:
        - "{{epic-slug}}"
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - {{field_1}}
                - {{field_2}}
              properties:
                {{field_1}}:
                  type: string
                  description: "{{description}}"
                  minLength: {{N}}
                  maxLength: {{N}}
                {{field_2}}:
                  type: string
                  format: date
                  description: "{{description}}"
      responses:
        "201":
          description: "Created"
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  status:
                    type: string
                    enum: [{{status_values}}]
                  created_at:
                    type: string
                    format: date-time
        "400":
          description: "Validation error"
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    enum: ["VALIDATION_ERROR"]
                  fields:
                    type: array
                    items:
                      type: object
                      properties:
                        field:
                          type: string
                        message:
                          type: string
        "422":
          description: "Business rule violation"
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                  message:
                    type: string
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

## Endpoint Details

### EP-001 — {{Method}} {{Path}}

**Idempotency:** Yes / No — {{behaviour on retry}}
**Rate Limit:** {{N req/min or None}}
**SLA:** {{response time target from requirements}}

---

## Consumed APIs (External)

| API | Provider | Purpose | Story | Timeout | Fallback |
|---|---|---|---|---|---|
| {{api name}} | {{provider}} | {{why this epic calls it}} | F-NNN.N | {{ms}} | {{what happens on failure}} |

### {{API Name}} — Contract Summary

**Endpoint:** {{method}} {{url}}
**Auth:** {{mechanism}}
**Expected Response Time:** {{ms}}
**Circuit Breaker:** {{threshold, recovery time}}
**Fallback Behaviour:** {{what the system does when this API is unavailable}}

---
*The OpenAPI YAML is the primary contract. A coding agent uses it to generate stubs. Do NOT abbreviate — include every field with type, format, and constraints.*
