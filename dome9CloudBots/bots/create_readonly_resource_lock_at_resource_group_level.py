# What it does: Creates a read-only resource lock at resource group level
# Usage: create_readonly_resource_lock_at_resource_group_level <lock-name>
# Example: create_readonly_resource_lock_at_resource_group_level my-lock
# Limitations: None

import logging
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.resource import ResourceManagementClient, ManagementLockClient

def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    lock_name = params
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('name')

    if not lock_name:
        msg = 'Error! Lock name is missing.'
        logging.info(f'{__file__} - {msg}') 
   
    logging.info(f'{__file__} - ${run_action.__name__} started')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()
    
    try:
        lock_client = ManagementLockClient(credentials, subscription_id)
        lock_client.management_locks.create_or_update_at_resource_group_level(resource_group_name=group_name, lock_name=lock_name, parameters={"level": "ReadOnly"})
        msg = f'Resource lock {lock_name} successfully on : {group_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    