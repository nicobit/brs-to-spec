// Extended alert rules for Admin Portal observability
param workspaceId string
param actionGroupName string = 'ap-actiongroup'

resource actionGroup 'Microsoft.Insights/actionGroups@2019-06-01' existing = {
  name: actionGroupName
}

// 1) Job failure rate: if failed jobs > 2% over 15m
resource jobFailureRate 'Microsoft.Insights/scheduledQueryRules@2018-04-16' = {
  name: 'jobs-failure-rate-high'
  location: 'global'
  properties: {
    description: 'Alert when job failure rate > 2% over 15 minutes'
    enabled: true
    source: {
      query: '''
        // Job failure rate over 15m
        Jobs
        | where TimeGenerated > ago(15m)
        | summarize failures = countif(status == 'failed'), total = count()
        | extend failure_rate = todouble(failures) / todouble(total) * 100
        | where failure_rate > 2
      '''
      dataSourceId: workspaceId
      queryType: 'ResultCount'
    }
    schedule: {
      frequencyInMinutes: 5
      timeWindowInMinutes: 15
    }
    action: {
      odata.type: 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction'
      customEmails: [ 'oncall@example.com' ]
    }
  }
}

// 2) Action invocation latency (P95) > threshold
resource actionLatency 'Microsoft.Insights/scheduledQueryRules@2018-04-16' = {
  name: 'action-invocation-latency-p95'
  location: 'global'
  properties: {
    description: 'Alert when P95 latency of POST /actions/* > 2000ms'
    enabled: true
    source: {
      query: '''
        // P95 latency for action endpoints
        requests
        | where Url startswith "/actions/" and Timestamp > ago(5m)
        | summarize p95 = percentiles(duration, 95)
        | where p95 > 2000
      '''
      dataSourceId: workspaceId
      queryType: 'ResultCount'
    }
    schedule: {
      frequencyInMinutes: 5
      timeWindowInMinutes: 5
    }
    action: {
      odata.type: 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction'
      customEmails: [ 'oncall@example.com' ]
    }
  }
}

// 3) Auth failure spike (401/403) > threshold
resource authFailure 'Microsoft.Insights/scheduledQueryRules@2018-04-16' = {
  name: 'auth-failure-spike'
  location: 'global'
  properties: {
    description: 'Alert on spike of 401/403 responses for action endpoints'
    enabled: true
    source: {
      query: '''
        requests
        | where Url startswith "/actions/" and Timestamp > ago(10m)
        | where ResultCode == "401" or ResultCode == "403"
        | summarize count() by bin(Timestamp, 5m)
        | where count_ > 50
      '''
      dataSourceId: workspaceId
      queryType: 'ResultCount'
    }
    schedule: {
      frequencyInMinutes: 5
      timeWindowInMinutes: 10
    }
    action: {
      odata.type: 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction'
      customEmails: [ 'oncall@example.com' ]
    }
  }
}

// 4) Long job duration alert
resource longJob 'Microsoft.Insights/scheduledQueryRules@2018-04-16' = {
  name: 'long-job-duration'
  location: 'global'
  properties: {
    description: 'Alert when jobs have duration > 30m'
    enabled: true
    source: {
      query: '''
        Jobs
        | where TimeGenerated > ago(30m)
        | where status == 'running' and datetime_diff('minute', now(), started_at) > 30
      '''
      dataSourceId: workspaceId
      queryType: 'ResultCount'
    }
    schedule: {
      frequencyInMinutes: 5
      timeWindowInMinutes: 30
    }
    action: {
      odata.type: 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction'
      customEmails: [ 'oncall@example.com' ]
    }
  }
}
