# Last checked 13/1/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.compute import ComputeManagementClient
import logging

def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    group_name = entity.get('resourceGroup',{}).get('name')
    vm_name =entity.get('name') 
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} vm_name : {vm_name}')
    if not subscription_id or not credentials:
        msg = 'Error! Subscription id or credentials are missing.'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}' 
    compute_client = ComputeManagementClient(credentials, subscription_id) 
    try:
        compute_client.virtual_machines.power_off (group_name, vm_name)
        id = entity.get('id')
        msg = f'Virtual machine was stopped. id: {id}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
    except HttpResponseError as e:   
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        return f'{msg}'
