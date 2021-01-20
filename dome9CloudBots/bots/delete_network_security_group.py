from azure.core.exceptions import HttpResponseError
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.v2019_02_01.models import NetworkSecurityGroup
from azure.mgmt.network.v2019_02_01.models import SecurityRule

import logging

def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    resource_group_name = entity.get('resourceGroup',{}).get('name')
    nsg_name = entity.get('name')
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {resource_group_name} nsg_name : {nsg_name}')
    
    if not subscription_id or not credentials:
        msg = 'Error! Subscription id or Resource group name are missing.'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}' 
    network_client = NetworkManagementClient(credentials, subscription_id)
    
    try:                 
        network_client.network_security_groups.get(resource_group_name, nsg_name)     
        network_client.network_security_groups.delete(resource_group_name, nsg_name)     
        id = entity.get('id')
        msg = f'Network Security group was deleted. id: {id}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
    except HttpResponseError as e:   
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        return f'{msg}'