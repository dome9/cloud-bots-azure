# What it does: enable Storage account enable secure transfer
# Usage: AUTO: storage_account_enable_https_traffic_only
# Limitations: None
# Permissions: Microsoft.Storage/storageAccounts/read, Microsoft.Storage/storageAccounts/write
# Updated 8/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountUpdateParameters
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']['name']
    storage_account_name = entity['name']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        storage_client = StorageManagementClient(credentials, subscription_id)
        storage_client.storage_accounts.update(group_name,
                                               storage_account_name,
                                               StorageAccountUpdateParameters(enable_https_traffic_only=True))
        id = entity['id']
        msg = f'Secure transfer was enabled successfully in storage account. id: {id}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to enable secure transfer in storage account - {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
