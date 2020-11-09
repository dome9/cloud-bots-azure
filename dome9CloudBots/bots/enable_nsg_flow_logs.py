from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network.v2020_06_01.models import NetworkSecurityGroup, SecurityRule, FlowLog
from azure.mgmt.network.v2020_06_01.models import SecurityRule

import logging

def run_action(credentials ,rule, entity, params):
    storage_account_name = params
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    resource_group_name = entity.get('resourceGroup',{}).get('name')
    region = entity.get('region')
    nsg_name = entity.get('name')
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {resource_group_name} nsg_name : {nsg_name}')
    if not subscription_id or not credentials:
        msg = 'Error! Subscription id or Resource group name are missing.'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}' 
    network_client = NetworkManagementClient(credentials, subscription_id)

    storage_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group_name + \
        '/providers/Microsoft.Storage/storageAccounts' + storage_account_name
    try:
        flow_log_parameters = {
        flow_logs: [
        'location': region,
        'storage_id': '/subscriptions/e584d070-3c5a-4a7c-8cf9-c063c5c67ee3/resourceGroups/rg-webservers/providers/Microsoft.Storage/storageAccounts/beckettdiags',
        'enabled':True, 
        'format': {version = 2}
        ] 
        },
        network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg_name, parameters=flow_log_parameters)
                      
        id = entity.get('id')
        msg = f'Network Security group was deleted. id: {id}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
    except CloudError as e:   
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        return f'{msg}'