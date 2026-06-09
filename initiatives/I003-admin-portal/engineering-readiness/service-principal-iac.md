 # Service Principal & Custom Role — IaC examples

 Purpose: sample IaC / CLI snippets to create a custom least-privilege role `AdminPortalActionRunner`, provision a service principal, and assign the role scoped to a subscription. Use these as a starting point for Ops to review and harden.

 ## Minimal custom role definition (role.json)

 ```json
 {
   "Name": "AdminPortalActionRunner",
   "IsCustom": true,
   "Description": "Least-privilege role for Admin Portal action orchestration (MVP)",
   "Actions": [
     "Microsoft.Compute/virtualMachines/start/action",
     "Microsoft.Compute/virtualMachines/restart/action",
     "Microsoft.Resources/subscriptions/resourceGroups/read",
     "Microsoft.Resources/deployments/*"
   ],
   "NotActions": [],
   "AssignableScopes": ["/subscriptions/{subscriptionId}"]
 }
 ```

 Replace `{subscriptionId}` with the sample subscription ID provided by Product. For quick local testing you can use `11111111-1111-1111-1111-111111111111` (TEST ONLY).

 ## Azure CLI — create role, service principal, and assignment

 Replace variables before running:

 ```powershell
 $SUBSCRIPTION_ID = "11111111-1111-1111-1111-111111111111"
 $ROLE_DEF=role.json
 $SP_NAME="http://admin-portal-action-runner"

 # Create the custom role (requires Owner or User Access Administrator on subscription)
 az role definition create --role-definition $ROLE_DEF

 # Create a service principal
 az ad sp create-for-rbac --name $SP_NAME --skip-assignment --sdk-auth

 # Capture the principalId of the created SP (example output shows appId/clientId and objectId)
 # Example test service principal object id (TEST ONLY)
 $SP_OBJECT_ID = "b2222222-bbbb-4bbb-8bbb-bbbbbbbbbbbb"

 # Assign the custom role at subscription scope
 az role assignment create --assignee-object-id $SP_OBJECT_ID --role "AdminPortalActionRunner" --scope "/subscriptions/$SUBSCRIPTION_ID"
 ```

 Note: `az ad sp create-for-rbac` returns a JSON credential blob (clientId, clientSecret, tenantId). Store secrets in the approved secret store (Key Vault). Use managed identities where possible in hosted environments.

 ## IaC (ARM/Bicep/Terraform) guidance

 - Prefer declaring the custom role and role assignment in IaC for repeatability. Example: Terraform `azurerm_role_definition` + `azurerm_role_assignment` or Bicep ARM resource type `Microsoft.Authorization/roleDefinitions` and `Microsoft.Authorization/roleAssignments`.
 - Include an automated approval/PR process for role changes and require Security review for any addition to `Actions` in the custom role.

 ## Audit & rotation

 - Rotate SP credentials regularly and automate via Key Vault and CI/CD.
 - Record role definition changes in repository history and require Security sign-off.
