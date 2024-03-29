# What it does: Creates a read-only resource lock at resource group level
# Usage: create_readonly_resource_lock_at_resource_group_level <lock-name>
# Example: create_readonly_resource_lock_at_resource_group_level my-lock
# Limitations: None
# Permissions: Microsoft.Authorization/locks/write
# Last checked 8/2/21


import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.resource import ResourceManagementClient, ManagementLockClient
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')

    lock_name = params
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('name')

    if not lock_name:
        msg = 'Error! Lock name is missing.'
        logging.info(f'{__file__} - {msg}')
        return msg

    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        lock_client = ManagementLockClient(credentials, subscription_id)
        lock_client.management_locks.create_or_update_at_resource_group_level(resource_group_name=group_name, lock_name=lock_name, parameters={"level": "ReadOnly"})
        msg = f'Resource lock {lock_name} successfully on : {group_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to lock {lock_name} on : {group_name} - {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
