# What it does: Sets "Deny public network access" Azure SQL flag to "Yes" and optionally, "Minimal TLS Version"
# Usage: sql_disable_public_access <optional-min-tls-version> - supported values are tls_10, tls_11, tls_12
# Example: sql_disable_public_access tls_12
# Example: sql_disable_public_access
# Limitations: Requires a Private Endpoint Connection to be created to enable the "Deny public access" feature
# Permissions: Microsoft.Sql/servers/write
# Updated 8/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    min_tls_version = params
    global min_tls
    if 'tls_12' in min_tls_version:
        min_tls = '1.2'
    elif 'tls_11' in min_tls_version:
        min_tls = '1.1'
    elif 'tls_10' in min_tls_version:
        min_tls = '1.0'
    else:
        msg = 'TLS version not defined correctly - should be tls_10, tls_11 or tls_12'
        logging.info(f'{__file__} - {msg}')
        return msg

    group_name = entity.get('resourceGroup', {}).get('name')
    subscription_id = entity.get('accountNumber')
    server_name = entity.get('name')
    server_location = entity.get('region')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.servers.begin_create_or_update(group_name, server_name, Server(location=server_location, public_network_access='Disabled', minimal_tls_version=min_tls))
        msg = f'Azure SQL public network access disabled successfully on : {server_name}, TLS version set to {min_tls}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to disable public network access on: {server_name} - {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
