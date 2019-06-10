## AUTO: tag_virtual_machine tag-name tag-value ##

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.compute import ComputeManagementClient
import logging

def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup',{}).get('name')
    vm_name =entity.get('name') 
    tag_name = params[0]
    tag_value = params[1]
    location = entity.get('region')
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} vm_name : {vm_name}')
    compute_client = ComputeManagementClient(credentials, subscription_id) 
    try:
        compute_client.virtual_machines.create_or_update(group_name, vm_name,{'location':location,'tags': {tag_name:tag_value}})
        id = entity.get('id')
        logging.info(f'{__file__} - Tag name: {tag_name} with value: {tag_value} at location: {location} was added to virtual machine id: {id}')
        return f'Tag name: {tag_name} with value: {tag_value} was added to virtual machine id: {id}'
    except CloudError as e:   
        logging.info(f'{__file__} - Unexpected error : {e.message}') 
        return f'Unexpected error : {e.message}'