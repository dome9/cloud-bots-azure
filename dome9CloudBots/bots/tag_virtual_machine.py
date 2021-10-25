# What it does : Tags a virtual machine with a key:value pair
# AUTO: tag_virtual_machine tag-name tag-value ##
# Permissions: Microsoft.Compute/virtualMachines/write, Microsoft.Compute/virtualMachines/read

from azure.core.exceptions import HttpResponseError
from azure.mgmt.compute import ComputeManagementClient
import logging
import dome9CloudBots.bots_utils


def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup',{}).get('name')
    vm_name =entity.get('name') 
    tag_name, tag_value = params
    location = entity.get('region')
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} vm_name : {vm_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        compute_client = ComputeManagementClient(credentials, subscription_id)
        compute_client.virtual_machines.begin_create_or_update(group_name, vm_name,{'location':location,'tags': {tag_name:tag_value}})
        id = entity.get('id')
        msg = f'Tag name: {tag_name} with value: {tag_value} at location: {location} was added to virtual machine id: {id}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:   
        msg = f'Filed to add to tag to virtual machine: {e.message}'
        logging.info(f'{__file__} - {msg}') 
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
