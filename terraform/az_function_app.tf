resource "azurerm_function_app" "cg-cloudbots" {
  name                       = var.function_name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  app_service_plan_id        = azurerm_app_service_plan.cg-cloudbots.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = azurerm_storage_account.cg-cloudbots.primary_access_key
  os_type                    = "linux"
  app_settings = {
      "CLIENT_ID" : var.client_id
      "SECRET" : var.secret
      "OUTPUT_EMAIL" : var.output_email
      "SEND_GRID_API_CLIENT" : var.sendgrid_api_key
      "SEND_LOGS" : var.send_logs
      "TENANT" : var.tenant
  }
}
