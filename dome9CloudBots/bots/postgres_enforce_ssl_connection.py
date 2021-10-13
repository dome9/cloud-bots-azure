# What it does: Enables forcing TLS connections to an Azure PostgreSQL server
# Enforcing SSL connections between database server and client applications helps protect against "man in the middle" attacks by encrypting the data stream between the server and application.
# Corresponds with rule D9.AZU.CRY.17
# Usage: AUTO: postgres_enforce_ssl_connection
# Limitations: None
# Updated 8/2/21

import logging
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.core.exceptions import HttpResponseError
from azure.mgmt.rdbms.postgresql.models import ServerUpdateParameters
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    server_name = entity['name']
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    try:
        db_client = PostgreSQLManagementClient(credentials, subscription_id)
        db_client.servers.begin_update(group_name, 
                                       server_name,
                                       ServerUpdateParameters(ssl_enforcement='Enabled'))
        msg = f'Force SSL connection was enabled successfully on PostgreSQL server: {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    
