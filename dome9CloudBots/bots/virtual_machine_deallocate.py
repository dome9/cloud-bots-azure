# Last update 10/2/21
# Permissions: Microsoft.Compute/virtualMachines/deallocate/action

from azure.core.exceptions import HttpResponseError
from azure.mgmt.compute import ComputeManagementClient
import logging
import dome9CloudBots.bots_utils


def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup',{}).get('name')
    vm_name =entity.get('name') 
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} vm_name : {vm_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        compute_client = ComputeManagementClient(credentials, subscription_id)
        compute_client.virtual_machines.begin_deallocate(group_name, vm_name)
        id = entity.get('id')
        msg = f'Virtual machine was deallocated. id: {id}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:   
        msg = f'Failed to deallocate virtual machine : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
