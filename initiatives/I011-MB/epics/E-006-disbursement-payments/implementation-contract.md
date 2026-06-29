# Implementation Contract — E-006 Disbursement & Payments

## Data Entities

### ER Diagram

```mermaid
erDiagram
    PAYMENT_SCHEDULE {
        uuid id PK
        uuid application_arn FK
        number amount_due
        timestamp due_date
        string status
    }
    PAYMENT {
        uuid id PK
        uuid schedule_id FK
        number amount
        timestamp paid_at
    }
    APPLICATION {
        uuid arn PK
    }
    PAYMENT }|..|{ PAYMENT_SCHEDULE : "for"
    PAYMENT_SCHEDULE }|..|{ APPLICATION : "on"
```

## API Surface

```yaml
openapi: "3.0.3"
info:
  title: "Servicing API"
  version: "1.0.0"
paths:
  /api/v1/servicing/schedules/{applicationArn}:
    get:
      summary: "Get payment schedules for an application"
      parameters:
        - name: applicationArn
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: "Schedules returned"
```

## Events

| Event | Type | Producer | Consumers | Trigger |
|---|---|---|---|---|
| servicing.payment_missed | domain | servicing-worker | notifications, collections | payment missed |

*End of contract.*
