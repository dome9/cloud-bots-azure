# What it does: Enables disconnection logging on an Azure PostgreSQL server to log end of a session, including duration,
# which in turn generates query and error logs.
# Query and error logs can be used to identify, troubleshoot,
# and repair configuration errors and sub-optimal performance.
# Corresponds with rule D9.AZU.LOG.03 
# Usage: AUTO: postgres_enable_log_disconnections
# Limitations: None
# Permissions: Microsoft.DBforPostgreSQL/servers/configurations/write
# Updated 8/2/21

import logging
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.core.exceptions import HttpResponseError
from azure.mgmt.rdbms.postgresql.models import Configuration
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    server_name = entity['name']
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']
    param_name = 'log_disconnections'
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        db_client = PostgreSQLManagementClient(credentials, subscription_id)
        db_client.configurations.begin_create_or_update(group_name,server_name, param_name, parameters=Configuration(value='ON'))   
        msg = f'Log disconnections was enabled successfully on PostgreSQL server: {server_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed enabling log disconnections on PostgreSQL server: {server_name} - \n{e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
