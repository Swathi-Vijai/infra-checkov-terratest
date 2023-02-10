resource "azurerm_resource_group" "vm_rg" {
  name     = "terratest-vm-rg-${var.postfix}"
  location = var.location
}