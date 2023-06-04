# What it does: Set Storage account property allow_blob_public_access to false
# Usage: disable_blob_public_access
# Usage: Example AUTO:disable_blob_public_access
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
    logging.info(f'Parameters are: {params}')
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']['name']
    storage_account_name = entity['name']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')

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
        p1 = StorageAccountUpdateParameters(allow_blob_public_access=False) #set the allow_blob_public_access settings here  
        storage_client.storage_accounts.update(group_name, storage_account_name, p1) #then use update method to update this feature
        msg = f'Allow blob public access was successfully configured to disable for storage account: {storage_account_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to disable blob public access for storage account: {storage_account_name} - {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg
 
    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
