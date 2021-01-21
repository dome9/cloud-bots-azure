# What it does: Sets a firewall rule on Azure SQL Server based on EXISTING subnets in EXISTING VNets
# Usage: sql_add_firewall_rule_by_existing_subnet - <firewall rule name> <vnet-resource-group> <existing-vnet-name> <existing-subnet-name>
# Example: sql_add_firewall_rule_by_existing_subnet my_vnet_rule my-resource-group vnet-example subnet-example
# Limitations: A valid VNet SQL Service Endpoint MUST already exist, or the bot will fail
# Last checked 20/1/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server


def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    firewall_rule_name, firewall_rule_vnet_rg_name, firewall_rule_vnet_name, firewall_rule_subnet_name = params
    if not firewall_rule_name:
        msg = 'Error! Firewall rule name is missing.'
        logging.info(f'{__file__} - {msg}')
    elif not firewall_rule_vnet_rg_name:
        msg = 'Error! Firewall rule VNet resource group is missing.'
        logging.info(f'{__file__} - {msg}')
    elif not firewall_rule_vnet_name:
        msg = 'Error! Firewall rule VNet name is missing.'
        logging.info(f'{__file__} - {msg}')    
    elif not firewall_rule_subnet_name:
        msg = 'Error! Firewall rule Subnet name is missing.'
        logging.info(f'{__file__} - {msg}')

    logging.info(f'{__file__} - ${run_action.__name__} started')
    group_name = entity.get('resourceGroup', {}).get('name')
    subscription_id = entity.get('accountNumber')
    server_name = entity.get('name')
    server_location = entity.get('region')
    server_group_name = entity.get('resourceGroup', {}).get('name')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    subnet_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + firewall_rule_vnet_rg_name + \
        '/providers/Microsoft.Network/virtualNetworks/' + \
        firewall_rule_vnet_name + '/subnets/' + firewall_rule_subnet_name

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.virtual_network_rules.create_or_update(server_group_name, server_name, firewall_rule_name, subnet_path, ignore_missing_vnet_service_endpoint=False)
        msg = f'Azure SQL firewall rule {firewall_rule_name} successfully on : {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    