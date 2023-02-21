provider "azurerm" {
  features {}
}


locals {
  resource_group = var.rg_name 
  location       = var.location
}



resource "azurerm_virtual_network" "net" {
  name                = "vnet-${var.postfix}"
  location            = local.location
  resource_group_name = local.resource_group
  address_space       = ["10.0.0.0/16"]
  dns_servers         = [var.dns_ip_01, var.dns_ip_02]
}


resource "azurerm_subnet" "net" {
  name                 = "subnet-${var.postfix}"
  resource_group_name  = local.resource_group
  virtual_network_name = azurerm_virtual_network.net.name
  address_prefixes     = [var.subnet_prefix]
}

resource "azurerm_network_interface" "net01" {
  name                = "nic-private-${var.postfix}"
  location            = local.location
  resource_group_name = local.resource_group

  ip_configuration {
    name                          = "terratestconfiguration1"
    subnet_id                     = azurerm_subnet.net.id
    private_ip_address_allocation = "Static"
    private_ip_address            = var.private_ip
  }
}

resource "azurerm_public_ip" "net" {
  name                    = "pip-${var.postfix}"
  resource_group_name     = local.resource_group
  location                = local.location
  allocation_method       = "Static"
  ip_version              = "IPv4"
  sku                     = "Basic"
  idle_timeout_in_minutes = "4"
  domain_name_label       = var.domain_name_label
}

resource "azurerm_public_ip" "net2" {
  name                    = "pip2-${var.postfix}"
  resource_group_name     = local.resource_group
  location                = local.location
  allocation_method       = "Static"
  ip_version              = "IPv4"
  sku                     = "Basic"
  idle_timeout_in_minutes = "4"
  domain_name_label       = var.domain_name_label
}

resource "azurerm_network_interface" "net01sai" {
  name                = "nic-public-${var.postfix}"
  location            = local.location
  resource_group_name = local.resource_group

  ip_configuration {
    name                          = "terratestconfiguration1"
    subnet_id                     = azurerm_subnet.net.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.net.id
  }
}

resource "azurerm_network_interface" "net02sai" {
  name                = "nic-public-sai-${var.postfix}"
  location            = local.location
  resource_group_name = local.resource_group

  ip_configuration {
    name                          = "terratestconfiguration1"
    subnet_id                     = azurerm_subnet.net.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.net2.id
  }
}

resource   "azurerm_windows_virtual_machine"   "myvm123"   { 
   name                    =   "myvm123"   
   location                =   local.location 
   resource_group_name     =   local.resource_group
   network_interface_ids   =   [ azurerm_network_interface.net01sai.id ] 
   size                    =   "Standard_B1s" 
   admin_username          =   var.admin_username 
   admin_password          =   var.admin_password

   source_image_reference   { 
     publisher   =   "MicrosoftWindowsServer" 
     offer       =   "WindowsServer" 
     sku         =   "2019-Datacenter" 
     version     =   "latest" 
   } 

   os_disk   { 
     caching             =   "ReadWrite" 
     storage_account_type   =   "Standard_LRS" 
   } 
}

resource "azurerm_windows_virtual_machine" "sai-vm" {
  name                = "sai-vm"
  resource_group_name = local.resource_group
  location            = local.location
  size                = "Standard_D2s_v3"
  admin_username      = var.admin_username
  admin_password      = var.admin_password
  network_interface_ids = [
    azurerm_network_interface.net02sai.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }
}



    
