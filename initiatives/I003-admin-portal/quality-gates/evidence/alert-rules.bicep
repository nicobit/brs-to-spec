// Alert rule: jobs.queue_depth > 100 for 5 minutes
param workspaceId string

resource actionGroup 'Microsoft.Insights/actionGroups@2019-06-01' = {
  name: 'ap-actiongroup'
  location: 'global'
  properties: {
    groupShortName: 'AP'
    enabled: true
    emailReceivers: [
      {
        name: 'OnCall'
        emailAddress: 'oncall@example.com'
        useCommonAlertSchema: true
      }
    ]
  }
}

resource alertRule 'Microsoft.Insights/scheduledQueryRules@2018-04-16' = {
  name: 'jobs-queue-depth-high'
  location: 'global'
  properties: {
    description: 'Alert when jobs.queue_depth > 100 for 5m'
    enabled: true
    source: {
      query: 'metrics | where Name == "jobs.queue_depth" and TimeGenerated > ago(5m) | summarize avg(Value) by bin(TimeGenerated, 1m) | where avg_Value > 100'
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
