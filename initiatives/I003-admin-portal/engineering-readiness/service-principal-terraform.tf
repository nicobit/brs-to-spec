// Terraform example: create Azure AD app, service principal, password, custom role, and role assignment
// Providers required: azurerm, azuread
provider "azurerm" {
  features {}
}

provider "azuread" {}

variable "subscription_id" {
  type    = string
  default = "11111111-1111-1111-1111-111111111111" # TEST ONLY
}

resource "azuread_application" "admin_portal_app" {
  display_name = "admin-portal-action-runner-app"
}

resource "azuread_service_principal" "admin_portal_sp" {
  application_id = azuread_application.admin_portal_app.application_id
}

resource "azuread_service_principal_password" "sp_password" {
  service_principal_id = azuread_service_principal.admin_portal_sp.id
  value                = random_password.sp_pass.result
  end_date_relative    = "8760h" // 1 year
}

resource "random_password" "sp_pass" {
  length  = 32
  special = true
}

resource "azurerm_role_definition" "admin_portal_role" {
  name        = "AdminPortalActionRunner"
  scope       = "/subscriptions/${var.subscription_id}"
  permissions {
    actions = [
      "Microsoft.Compute/virtualMachines/start/action",
      "Microsoft.Compute/virtualMachines/restart/action",
      "Microsoft.Resources/subscriptions/resourceGroups/read",
      "Microsoft.Resources/deployments/*"
    ]
    not_actions = []
  }
  assignable_scopes = ["/subscriptions/${var.subscription_id}"]
}

resource "azurerm_role_assignment" "sp_role_assignment" {
  scope                = "/subscriptions/${var.subscription_id}"
  role_definition_id   = azurerm_role_definition.admin_portal_role.role_definition_resource_id
  principal_id         = azuread_service_principal.admin_portal_sp.object_id
}

output "service_principal_app_id" {
  value = azuread_application.admin_portal_app.application_id
}

output "service_principal_client_secret" {
  value     = azuread_service_principal_password.sp_password.value
  sensitive = true
}
