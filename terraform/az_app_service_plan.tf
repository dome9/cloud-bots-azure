resource "azurerm_app_service_plan" "cg-cloudbots" {
  name                = var.app_service_plan
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}
