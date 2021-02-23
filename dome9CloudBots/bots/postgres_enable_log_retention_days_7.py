# What it does: Enables log retention on an Azure PostgreSQL server to the maximum value of 7 days
# Enabling log_retention_days helps PostgreSQL Database to Sets number of days a log file is retained which in turn generates query and error logs
# Corresponds with rule D9.AZU.LOG.06
# Usage: AUTO: postgres_enable_log_retention_days_7
# Limitations: None
# Updated 8/2/21

import logging
import os
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.core.exceptions import HttpResponseError
from azure.mgmt.rdbms.postgresql.models import Configuration

def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    server_name = entity['name']
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']
    param_name = 'log_retention_days'
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        db_client = PostgreSQLManagementClient(credentials, subscription_id)
        db_client.configurations.begin_create_or_update(group_name,server_name, param_name, parameters=Configuration(value='7'))    
        msg = f'Log retention was set to 7 days successfully on PostgreSQL server: {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    
