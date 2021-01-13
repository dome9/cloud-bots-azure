# What it does: Restricts Storage account access to internal subnets only
# Usage: storage_account_disable_public_network_access <vnet resource group> <vnet> <subnet>
# Usage: Example storage_account_disable_public_network_access my-resource-group my-vnet my-subnet
# Limitations: VNet must have service endpoints configured for Storage access
# Last checked 13/1/21

import logging
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountUpdateParameters, NetworkRuleSet, VirtualNetworkRule)


def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg


def run_action(credentials, rule, entity, params):
    logging.info(f'Parameters are: {params}')
    vnet_group_name, vnet_name, subnet_name = params
    logging.info(f'{__file__} - ${run_action.__name__} started')
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']['name']
    storage_account_name = entity['name']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')

    subnet_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + vnet_group_name + \
        '/providers/Microsoft.Network/virtualNetworks/' + \
        vnet_name + '/subnets/' + subnet_name

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        storage_client = StorageManagementClient(credentials, subscription_id)
        storage_client.storage_accounts.update(group_name,storage_account_name, StorageAccountUpdateParameters(network_rule_set=NetworkRuleSet(default_action='Deny', virtual_network_rules=[VirtualNetworkRule(virtual_network_resource_id=subnet_path)])))
        msg = f'Private network access was successfully configured for storage account: {storage_account_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        if 'SubnetsHaveNoServiceEndpointsConfigured' in msg:
            logging.info(f'Unable to set private access as the VNet does not have Service Endpoints configured')
        logging.info(f'{__file__} - {msg}')
        return msg
