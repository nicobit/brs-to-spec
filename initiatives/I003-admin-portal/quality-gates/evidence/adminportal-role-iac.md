# AdminPortalActionRunner — IaC snippet (ARM / az)

## Azure CLI (example)

Replace `{subscriptionId}` and `{roleDefinitionFile}` before running.

```bash
az role definition create --role-definition adminportal-role.json
# Or scoped deployment via ARM/Bicep with role assignment steps in pipeline
```

## Bicep (role assignment example)

```bicep
param principalId string
param subscriptionId string

resource roleDef 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(subscriptionId, 'AdminPortalActionRunner')
  properties: {
    roleName: 'AdminPortalActionRunner'
    description: 'Least-privilege role for Admin Portal action runner.'
    permissions: [
      {
        actions: [
          'Microsoft.Resources/subscriptions/resourceGroups/read',
          'Microsoft.Compute/virtualMachines/start/action',
          'Microsoft.Compute/virtualMachines/restart/action'
        ]
        notActions: [
          'Microsoft.Resources/subscriptions/resourceGroups/delete'
        ]
      }
    ]
    assignableScopes: [
      '/subscriptions/${subscriptionId}'
    ]
  }
}

resource roleAssign 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(principalId, roleDef.name)
  properties: {
    principalId: principalId
    roleDefinitionId: roleDef.id
    principalType: 'ServicePrincipal'
  }
}
```
