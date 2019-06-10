from msrestazure.azure_exceptions import CloudError
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
    network_client = NetworkManagementClient(
    credentials,
    subscription_id
    )
    try:                 
        network_client.network_security_groups.get(resource_group_name, nsg_name)     
        network_client.network_security_groups.delete(resource_group_name, nsg_name)     
        id = entity.get('id')
        logging.info(f'{__file__} - Virtual machine was stopped. id: {id}')
        return f'Virtual machine was stopped. id: {id}'
    except CloudError as e:   
        logging.info(f'{__file__} - Unexpected error : {e.message}') 
        return f'Unexpected error : {e.message}'