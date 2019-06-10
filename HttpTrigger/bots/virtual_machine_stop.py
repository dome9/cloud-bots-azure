from msrestazure.azure_exceptions import CloudError
from azure.mgmt.compute import ComputeManagementClient
import logging

def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup',{}).get('name')
    vm_name =entity.get('name') 
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} vm_name : {vm_name}')
    compute_client = ComputeManagementClient(credentials, subscription_id) 
    try:
        compute_client.virtual_machines.power_off(group_name, vm_name)
        id = entity.get('id')
        logging.info(f'{__file__} - Virtual machine was stopped. id: {id}')
        return f'Virtual machine was stopped. id: {id}'
    except CloudError as e:   
        logging.info(f'{__file__} - Unexpected error : {e.message}') 
        return f'Unexpected error : {e.message}'