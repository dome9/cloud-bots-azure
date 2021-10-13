# What it does: Sets a firewall rule on Azure SQL Server based on EXISTING subnets in EXISTING VNets
# Usage: sql_add_firewall_rule_by_existing_subnet - <firewall rule name> <vnet-resource-group> <existing-vnet-name> <existing-subnet-name>
# Example: sql_add_firewall_rule_by_existing_subnet my_vnet_rule my-resource-group vnet-example subnet-example
# Limitations: A valid VNet SQL Service Endpoint MUST already exist, or the bot will fail
# Last updated 9/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server, VirtualNetworkRule
import dome9CloudBots.bots_utils


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

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    subnet_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + firewall_rule_vnet_rg_name + \
        '/providers/Microsoft.Network/virtualNetworks/' + \
        firewall_rule_vnet_name + '/subnets/' + firewall_rule_subnet_name

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.virtual_network_rules.begin_create_or_update(server_group_name, server_name, firewall_rule_name, parameters=VirtualNetworkRule(
            virtual_network_subnet_id=subnet_path, ignore_missing_vnet_service_endpoint=False))
        msg = f'Azure SQL firewall rule {firewall_rule_name} successfully on : {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    