# What it does: Enables Transparent Data Encryption (TDE) on an Azure SQL server
# transparent data encryption helps protect against the threat of malicious activity by performing real-time encryption and 
#  decryption of the database, associated backups, and transaction log files at rest without requiring changes to the application.
# Corresponds with rule D9.AZU.CRY.11
# Usage: AUTO: sql_enable_data_encryption
# Limitations: None
# Last checked 13/1/21

#from azure.common.credentials import ServicePrincipalCredentials
import logging
import os
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import TransparentDataEncryptionStatus
import re

# # Set Azure AD credentials from the environment variables
# credentials = ServicePrincipalCredentials(
#     client_id=os.environ['CLIENT_ID'],
#     secret=os.environ['SECRET'],
#     tenant=os.environ['TENANT']
# )

def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    entity_id = entity.get('id')
    split_id = entity_id.split('/')
    subscription_id = split_id[2]
    group_name = split_id[4]
    server_name = split_id[8]
    print(group_name)
    database_name = split_id[10]
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name} - database_name : {database_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.transparent_data_encryptions.create_or_update(group_name, server_name, database_name, status=TransparentDataEncryptionStatus.enabled)  
        msg = f'Transparent data encryption enabled successfully on database : {database_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    
