# Admin Portal — Deployment Diagram

```mermaid
flowchart LR
  User[User Browser]

  subgraph AzureCloud [Azure - Recommended MVP]
    UIApp[Admin Portal UI<br/>Azure Static Web App / App Service]
    APIGW[Backend API<br/>Azure Functions / App Service]
    AD[Azure Active Directory]
    Log[Azure Monitor / Log Analytics]
    Storage[Audit Storage (Blob/Table)]
    SP[Service Principal]
    Subscriptions[Azure Subscriptions / Resource Groups]
  end

  User --> UIApp
  UIApp -->|HTTPS| APIGW
  APIGW -->|auth| AD
  APIGW -->|uses| SP
  APIGW -->|writes telemetry| Log
  APIGW -->|stores audit| Storage
  APIGW -->|reads| Subscriptions

  classDef infra fill:#eef,stroke:#333,stroke-width:1px;
  class AD,Log,Storage,SP,Subscriptions infra;
```

Notes: recommended hosted components for MVP. Adjust per infra constraints and org standards.
