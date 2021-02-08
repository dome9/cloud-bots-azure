# What it does: Set Storage account property allow_blob_public_access to false
# Usage: disable_blob_public_access
# Usage: Example AUTO:disable_blob_public_access
# Limitations: None
# Updated 8/2/21
 
import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountUpdateParameters
 
def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg
 
def run_action(credentials, rule, entity, params):
    logging.info(f'Parameters are: {params}')
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
        p1 = StorageAccountUpdateParameters(allow_blob_public_access=False) #set the allow_blob_public_access settings here  
        storage_client.storage_accounts.update(group_name, storage_account_name, p1) #then use update method to update this feature
        msg = f'Allow blob public access was successfully configured to disable for storage account: {storage_account_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
 
    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'Unable to set Allow blob public access property to false')
        logging.info(f'{__file__} - {msg}')
        return msg
