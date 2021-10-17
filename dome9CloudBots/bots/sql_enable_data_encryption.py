# What it does: Enables Transparent Data Encryption (TDE) on an Azure SQL server
# transparent data encryption helps protect against the threat of malicious activity by performing real-time encryption and 
#  decryption of the database, associated backups, and transaction log files at rest without requiring changes to the application.
# Corresponds with rule D9.AZU.CRY.11
# Usage: AUTO: sql_enable_data_encryption
# Limitations: None
# Last updated 10/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import TransparentDataEncryptionStatus, TransparentDataEncryption
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    entity_id = entity.get('id')
    split_id = entity_id.split('/')
    subscription_id = split_id[2]
    group_name = split_id[4]
    server_name = split_id[8]
    print(group_name)
    database_name = split_id[10]
    tde_name='current'
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name} - database_name : {database_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.transparent_data_encryptions.create_or_update(group_name, server_name, database_name, tde_name,
            parameters=TransparentDataEncryption(status=TransparentDataEncryptionStatus.enabled))  
        msg = f'Transparent data encryption enabled successfully on database : {database_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to enable Transparent data encryption on database : {database_name} - {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg

