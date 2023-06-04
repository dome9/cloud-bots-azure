# What it does: Restricts Storage account access to internal subnets only
# Usage: storage_account_disable_public_network_access <vnet resource group> <vnet> <subnet>
# Usage: Example storage_account_disable_public_network_access my-resource-group my-vnet my-subnet
# Limitations: VNet must have service endpoints configured for Storage access
# Permissions: Microsoft.Storage/storageAccounts/read, Microsoft.Storage/storageAccounts/write
# Updated 8/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountUpdateParameters, NetworkRuleSet, VirtualNetworkRule)
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    logging.info(f'Parameters are: {params}')
    vnet_group_name, vnet_name, subnet_name = params
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']['name']
    storage_account_name = entity['name']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')

    subnet_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + vnet_group_name + \
        '/providers/Microsoft.Network/virtualNetworks/' + \
        vnet_name + '/subnets/' + subnet_name

    entity_type = entity.get('type')
    if not dome9CloudBots.bots_utils.is_correct_type(dome9CloudBots.bots_utils.EntitiesTypes.STORAGE_ACCOUNT,
                                                     entity_type):
        error_msg = f'Error! entity type is not Storage Account'
        logging.error(f'{__file__} - {error_msg}')
        raise TypeError(error_msg)

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        storage_client = StorageManagementClient(credentials, subscription_id)
        storage_client.storage_accounts.update(group_name,storage_account_name, StorageAccountUpdateParameters(network_rule_set=NetworkRuleSet(default_action='Deny', virtual_network_rules=[VirtualNetworkRule(virtual_network_resource_id=subnet_path)])))
        msg = f'Private network access was successfully configured for storage account: {storage_account_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to configure Private network access for storage account: {storage_account_name} - {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
