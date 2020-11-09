# What it does: Sets "Deny public network access" Azure SQL flag to "Yes" and optionally, "Minimal TLS Version"
# Usage: sql_disable_public_access <optional-min-tls-version> - supported values are tls_10, tls_11, tls_12
# Example: sql_disable_public_access tls_12
# Example: sql_disable_public_access
# Limitations: An Azure Private Endpoint MUST be pre-configured to allow traffic, see https://docs.microsoft.com/en-gb/azure/azure-sql/database/connectivity-settings#deny-public-network-access

import logging
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server

def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    min_tls_version = params
    if 'tls_12' in min_tls_version:
        min_tls = '1.2'
    elif 'tls_11' in min_tls_version:
        min_tls = '1.1'
    elif 'tls_10' in min_tls_version:
        min_tls = '1.0'

    logging.info(f'{__file__} - ${run_action.__name__} started')
    group_name = entity.get('resourceGroup', {}).get('name')
    subscription_id = entity.get('accountNumber')
    server_name = entity.get('name')
    server_location = entity.get('region')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.servers.create_or_update(group_name, server_name, Server(location=server_location, public_network_access='Disabled', minimal_tls_version=min_tls))        
        msg = f'Azure SQL public network access disabled successfully on : {server_name}, TLS version set to {min_tls}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    