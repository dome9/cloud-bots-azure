resource "azurerm_resource_group" "cg-cloudbots" {
  name     = var.resource_group_name
  location = var.location
}
