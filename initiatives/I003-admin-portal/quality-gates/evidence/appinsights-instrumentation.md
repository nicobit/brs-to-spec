# Application Insights / OpenTelemetry Instrumentation Samples

## .NET (ASP.NET Core) example

Install package:

```bash
dotnet add package Microsoft.ApplicationInsights.AspNetCore
```

Startup snippet:

```csharp
services.AddApplicationInsightsTelemetry();

// Correlation headers
services.AddOpenTelemetryTracing(builder =>
{
    builder
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddSource("AdminPortal.Actions")
        .AddAzureMonitorTraceExporter(options => { /* configure */ });
});
```

When creating job spans, include `correlation_id` and `job_id` as attributes.

## Node (Express) example with OpenTelemetry

```bash
npm install @opentelemetry/api @opentelemetry/node @opentelemetry/instrumentation-http @opentelemetry/exporter-azure-monitor
```

Snippet:

```javascript
const { NodeTracerProvider } = require('@opentelemetry/node');
const { AzureMonitorTraceExporter } = require('@opentelemetry/exporter-azure-monitor');

const provider = new NodeTracerProvider();
provider.register();

const exporter = new AzureMonitorTraceExporter({ connectionString: process.env.APPINSIGHTS_CONNECTION_STRING });
provider.addSpanProcessor(new BatchSpanProcessor(exporter));

// In action handler
const tracer = provider.getTracer('AdminPortal.Actions');
const span = tracer.startSpan('action.invoke', { attributes: { job_id, correlation_id } });
// ... process
span.end();
```

## Best practices
- Propagate `trace_id` / `correlation_id` through headers to job processors and across retries.
- Record `initiated_by`, `tenantId`, `subscriptionId`, and `resourceId` as span attributes for rich filtering.
- Sample traces for low-priority actions to reduce storage; keep full fidelity for failures.
