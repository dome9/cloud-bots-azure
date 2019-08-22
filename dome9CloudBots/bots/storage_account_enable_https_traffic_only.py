# What it does: enable Storage account enable secure transfer
# Usage: AUTO: storage_account_enable_https_traffic_only
# Limitations: None

import logging
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountUpdateParameters


def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']['name']
    storage_account_name = entity['name']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        storage_client = StorageManagementClient(credentials, subscription_id)
        storage_client.storage_accounts.update(group_name,
                                               storage_account_name,
                                               StorageAccountUpdateParameters(enable_https_traffic_only=True))
        id = entity['id']
        msg = f'Secure transfer was enabled successfully in storage account. id: {id}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
