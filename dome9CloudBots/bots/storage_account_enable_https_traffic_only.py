# What it does: enable Storage account Secure transfer required field
# Usage: AUTO: storage_account_enable_https_traffic_only
# Limitations: None

import logging
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountUpdateParameters


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup', {}).get('name')
    storage_account_name = entity.get('name')
    logging.info( f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')

    if not subscription_id or not credentials:
        msg = 'Error! Subscription id or credentials are missing.'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    try:
        storage_client = StorageManagementClient(credentials, subscription_id)
        storage_client.storage_accounts.update(group_name, storage_account_name,StorageAccountUpdateParameters(enable_https_traffic_only=True))
        id = entity.get('id')
        msg = f'Secure transfer was enabled successfully in storage account. id: {id}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
