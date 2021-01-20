## AUTO: tag_virtual_machine tag-name tag-value ##
# Last checked 13/1/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.compute import ComputeManagementClient
import logging

def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup',{}).get('name')
    vm_name =entity.get('name') 
    tag_name, tag_value = params
    location = entity.get('region')
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} vm_name : {vm_name}')
    if not subscription_id or not credentials:
        msg = 'Error! Subscription id or credentials are missing.'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}' 
    compute_client = ComputeManagementClient(credentials, subscription_id) 
    try:
        compute_client.virtual_machines.create_or_update(group_name, vm_name,{'location':location,'tags': {tag_name:tag_value}})
        id = entity.get('id')
        msg = f'Tag name: {tag_name} with value: {tag_value} at location: {location} was added to virtual machine id: {id}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
    except HttpResponseError as e:   
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        return f'{msg}'
