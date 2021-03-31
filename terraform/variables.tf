terraform {
    required_providers {
        azurerm = {
        source  = "hashicorp/azurerm"
        version = "=2.46.0"
        }
    }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
    features {}
}

# Variables

variable "location" {
    description = "Azure region for resources"
    default = "northeurope"
}

variable "resource_group_name" {
    description = "Name of the resource group to contain the CloudBots function"
    default = "rg-cloudbots" 
}

variable "storage_account_name" {
    description = "Name of the storage account for CloudBots code and logs (MUST BE GLOBALLY UNIQUE)"
    default = "sacloudbots"
}

variable "app_service_plan" {
    description = "App service plan name"
    default = "cloudbots_service_plan"
}

variable "function_name" {
    description = "Name of the Azure Function for CloudBots"
    default = "cloudbots-function"
}

variable "azure_client_id" {
    description = "The App Registration client ID"
    default = "xxxxx-xxxxx-xxxxxx-xxxxx"
}

variable "output_email" {
    description = "E-mail address to send auto remediation notifications to"
    default = "a.person@acme.com"
}

variable "azure_client_secret" {
    description = "The App Registration secret key"
    default = "xxxxxxxxx"
}

variable "sendgrid_api_key" {
    description = "API key for SendGrid e-mail"
    default = "xxxxxxxxxx"
}

variable "send_logs" {
    description = "Send logs to Check Point"
    default = "true"
}

variable "basic_auth_enabled" {
    description = "Basic Auth Enabled Flag"
    default = "0"
}

variable "basic_auth_username" {
    description = "Basic Auth Username"
    default = "xxxxxxxxxxxxxxx"
}

variable "basic_auth_password" {
    description = "Basic Auth Password"
    default = "xxxxxxxxxxxxxxx"
}

variable "azure_tenant_id" {
    description = "Azure AD tenant ID"
    default = "xxxxxxxxxxxxxxx"
}
